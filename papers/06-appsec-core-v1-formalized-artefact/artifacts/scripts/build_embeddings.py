#!/usr/bin/env python3
"""
build-script.py — AppSec Core V1 SBERT embeddings release artefact builder.

Deterministic regenerator. Given:
  - Canonical YAML at sbd-toe-ontology/ontology/
  - augmentation-rule.yaml (this folder, version 1.0, ratified 2026-05-03)
  - The pinned SBERT model snapshot (SHA recorded in the manifest)

Emits:
  - augmented-text-corpus.json
  - embeddings-{model}-{commit}.npz
  - embeddings-manifest.json

Reproducibility contract:
  - Same inputs → bit-identical augmented-text-corpus.json (architecture-agnostic).
  - Same inputs + same architecture → bit-identical embeddings .npz (architecture-
    dependent due to floating-point determinism; cross-architecture identity is
    not guaranteed; the manifest records arch + lib versions to diagnose).

Usage (project-local venv setup once):
    python3 -m venv --system-site-packages .venv
    .venv/bin/pip install --upgrade "Pillow>=9.1.0"
    .venv/bin/python3 build-script.py [--out-dir <path>]

The venv inherits system torch/transformers/numpy/pyyaml; only Pillow is
upgraded inside the venv (the system Pillow 9.0.1 lacks PIL.Image.Resampling
which transformers' image_utils requires; isolating the Pillow upgrade in the
venv keeps system Python untouched).

Per Decision 0003 Amendment 1 §F: the augmentation rule + format conventions
are coordinated with Cartographer's source-side flattener; both sides MUST
share the same model + commit + library versions for similarity scores in
PIPELINE 2 §2.1 to be interpretable. The manifest emitted here is the
contract Cartographer mirrors.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import torch
import transformers
import yaml
from transformers import AutoModel, AutoTokenizer

# ============================================================
# Paths
# ============================================================

REPO_ROOT = Path(__file__).resolve().parents[3]  # sbd-toe-ontology/
ONTOLOGY_DIR = REPO_ROOT / "ontology"
THIS_DIR = Path(__file__).resolve().parent
RULE_FILE = THIS_DIR / "augmentation-rule.yaml"

# ============================================================
# Pinned model
# ============================================================

MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2"
# Pinned HF snapshot SHA. Fixed at the time of build; recorded in manifest.
# To upgrade: change here, re-run build, ship new artefact with new manifest.
MODEL_REVISION = "c9745ed1d9f207416be6d2e6f8de32d1f16199bf"
ENCODER_MAX_TOKENS = 256  # matches SBERT default for this model

# ============================================================
# Slice → file map (mirrors augmentation-rule.yaml source_files.slice_drafts)
# ============================================================

SLICE_DRAFTS = [
    ("ACO-SCBI", "ASC-01", "appsec-core-supply-chain-build-integrity-draft.yaml"),
    ("ACO-IAT",  "ASC-02", "appsec-core-identity-access-session-trust-draft.yaml"),
    ("ACO-ATB",  "ASC-03", "appsec-core-architecture-trust-boundaries-draft.yaml"),
    ("ACO-TSV",  "ASC-04", "appsec-core-testing-security-validation-draft.yaml"),
    ("ACO-TMR",  "ASC-05", "appsec-core-threat-modeling-risk-disposition-draft.yaml"),
    ("ACO-SPC",  "ASC-06", "appsec-core-secrets-protected-config-draft.yaml"),
    ("ACO-IVF",  "ASC-07", "appsec-core-input-validation-safe-failure-draft.yaml"),
    ("ACO-ITS",  "ASC-08", "appsec-core-integration-trust-service-security-draft.yaml"),
    ("ACO-RPR",  "ASC-09", "appsec-core-release-promotion-controlled-rollout-draft.yaml"),
    ("ACO-SLG",  "ASC-10", "appsec-core-security-event-logging-audit-trail-draft.yaml"),
]

SEPARATOR = ". "

# ============================================================
# Augmentation rule (encoded directly in code; mirrors augmentation-rule.yaml v1.0)
# ============================================================

def snake_to_words(s: str) -> str:
    """Replace `_` with space; preserve original casing (per clarification 1).
    The ontology's snake_case enums are already lowercase, so this is a no-op
    on casing for the ontology side; Cartographer's source side may preserve
    proper nouns (e.g., "RESTful Web Services") that this rule must not
    damage."""
    if not s:
        return ""
    return s.replace("_", " ")


def _strip_trailing_period(s: str) -> str:
    """Strip trailing period(s) and surrounding whitespace, per clarification 2."""
    return re.sub(r"[.\s]+$", "", s)


def join_fields(fields: list[str]) -> str:
    """Join non-empty fragments with SEPARATOR; each fragment is period-
    stripped (trailing) before joining, to avoid duplicated `.. ` at fragment
    boundaries (per clarification 2 ratified 2026-05-03)."""
    parts = [_strip_trailing_period(f.strip()) for f in fields if f and f.strip()]
    parts = [p for p in parts if p]  # drop fragments that became empty after strip
    out = SEPARATOR.join(parts)
    out = re.sub(r"\s+", " ", out).strip()
    return out


def slice_iri(asc_id: str) -> str:
    n = asc_id.replace("ASC-", "")
    return f"ac:SliceASC{n}"


def co_iri(co_id: str) -> str:
    return f"ac:{co_id.replace('-', '_')}"


def practice_iri(p_id: str) -> str:
    return f"ac:{p_id.replace('-', '_')}"


def mech_iri(m_id: str) -> str:
    return f"ac:{m_id.replace('-', '_')}"


# ============================================================
# Phase A — augmented-text-corpus.json (deterministic; no model needed)
# ============================================================

def build_corpus() -> list[dict]:
    """Read canonical YAML + apply rule → list of corpus records."""
    records: list[dict] = []

    # Load all slice drafts + components + contracts up front so Mechanism
    # aggregation can index Practice descriptions across the slice.
    slice_data: dict[str, dict] = {}
    components_data: dict[str, dict] = {}
    contract_data: dict[str, dict] = {}
    for fam, asc, draft_fn in SLICE_DRAFTS:
        slice_data[fam] = yaml.safe_load((ONTOLOGY_DIR / draft_fn).read_text())
        comp_fn = draft_fn.replace("-draft.yaml", "-components-draft.yaml")
        components_data[fam] = yaml.safe_load((ONTOLOGY_DIR / comp_fn).read_text())
        ctr_fn = draft_fn.replace("-draft.yaml", "-slice-contract.yaml")
        contract_data[fam] = yaml.safe_load((ONTOLOGY_DIR / ctr_fn).read_text())

    # ---- Slice ----
    # Order (most-specific → least-specific per rule v1.0 — Cartographer
    # Phase 1a final convergence 2026-05-03):
    #   meta.name . meta.scope . meta.description . purpose.current_goal
    for fam, asc, _ in SLICE_DRAFTS:
        ctr = contract_data[fam] or {}
        meta = ctr.get("meta", {}) or {}
        purpose = ctr.get("purpose", {}) or {}
        text = join_fields([
            meta.get("name", ""),
            snake_to_words(meta.get("scope", "")),
            meta.get("description", ""),
            purpose.get("current_goal", ""),
        ])
        records.append({
            "entity_iri": slice_iri(asc),
            "entity_level": "Slice",
            "entity_id": asc,
            "family": fam,
            "augmented_text": text,
            "source_fields": ["meta.name", "meta.scope", "meta.description", "purpose.current_goal"],
            "rule_version": "1.0",
        })

    # ---- ControlObjective ----
    # Order (most-specific → least-specific per rule v1.0):
    #   name . statement . expected_outcome . verification_posture
    for fam, asc, _ in SLICE_DRAFTS:
        d = slice_data[fam] or {}
        for cid, obj in (d.get("normalized_objectives", {}) or {}).items():
            text = join_fields([
                obj.get("name", ""),
                obj.get("statement", ""),
                obj.get("expected_outcome", ""),
                snake_to_words(obj.get("verification_posture", "")),
            ])
            records.append({
                "entity_iri": co_iri(cid),
                "entity_level": "ControlObjective",
                "entity_id": cid,
                "family": fam,
                "augmented_text": text,
                "source_fields": ["name", "statement", "expected_outcome", "verification_posture"],
                "rule_version": "1.0",
            })

    # ---- Practice ----
    # Order (most-specific → least-specific per rule v1.0):
    #   name . description . practice_family . local_practice_type
    for fam, asc, _ in SLICE_DRAFTS:
        cd = components_data[fam] or {}
        for pid, pr in (cd.get("normalized_practices", {}) or {}).items():
            text = join_fields([
                pr.get("name", ""),
                pr.get("description", ""),
                snake_to_words(pr.get("practice_family", "")),
                snake_to_words(pr.get("local_practice_type", "")),
            ])
            records.append({
                "entity_iri": practice_iri(pid),
                "entity_level": "Practice",
                "entity_id": pid,
                "family": fam,
                "augmented_text": text,
                "source_fields": ["name", "description", "practice_family", "local_practice_type"],
                "rule_version": "1.0",
            })

    # ---- Mechanism (with supports_practices aggregation) ----
    # Order (most-specific → least-specific per rule v1.0):
    #   name . aggregated_supports_practices . note . mechanism_family . local_mechanism_type
    for fam, asc, _ in SLICE_DRAFTS:
        cd = components_data[fam] or {}
        practices_in_slice = cd.get("normalized_practices", {}) or {}
        for mid, me in (cd.get("normalized_mechanisms", {}) or {}).items():
            sup = me.get("supports_practices", []) or []
            derived = SEPARATOR.join(
                _strip_trailing_period(practices_in_slice[p].get("description", ""))
                for p in sup
                if p in practices_in_slice and practices_in_slice[p].get("description")
            )
            text = join_fields([
                me.get("name", ""),
                derived,
                me.get("note", ""),
                snake_to_words(me.get("mechanism_family", "")),
                snake_to_words(me.get("local_mechanism_type", "")),
            ])
            records.append({
                "entity_iri": mech_iri(mid),
                "entity_level": "Mechanism",
                "entity_id": mid,
                "family": fam,
                "augmented_text": text,
                "source_fields": [
                    "name",
                    "supports_practices->Practice.description (aggregated)",
                    "note",
                    "mechanism_family",
                    "local_mechanism_type",
                ],
                "rule_version": "1.0",
            })

    return records


def write_corpus(records: list[dict], out_path: Path) -> str:
    """Write records to JSON; return sha256."""
    payload = {
        "schema": "appsec-core-v1-augmented-text-corpus/1.0",
        "rule_version": "1.0",
        "n_records": len(records),
        "records": records,
    }
    s = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=False)
    out_path.write_text(s, encoding="utf-8")
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


# ============================================================
# Phase B — embeddings .npz + manifest (model required; deterministic)
# ============================================================

def encode_corpus(records: list[dict], device: str = "cpu") -> tuple[np.ndarray, list[str]]:
    """Mean-pool + L2-normalize. Mirrors sentence-transformers' default pooling
    for `all-MiniLM-L6-v2` (CLS-pooling NOT used; mean-pool over attention mask)."""
    torch.manual_seed(0)
    np.random.seed(0)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=MODEL_REVISION)
    model = AutoModel.from_pretrained(MODEL_ID, revision=MODEL_REVISION)
    model.eval()
    model.to(device)

    texts = [r["augmented_text"] for r in records]
    iris = [r["entity_iri"] for r in records]

    # Encode in fixed batch order for reproducibility
    batch_size = 32
    chunks: list[np.ndarray] = []
    with torch.no_grad():
        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            enc = tokenizer(
                batch,
                padding=True,
                truncation=True,
                max_length=ENCODER_MAX_TOKENS,
                return_tensors="pt",
            ).to(device)
            out = model(**enc)
            mask = enc["attention_mask"].unsqueeze(-1).expand(out.last_hidden_state.size()).float()
            pooled = (out.last_hidden_state * mask).sum(1) / mask.sum(1).clamp(min=1e-9)
            normed = torch.nn.functional.normalize(pooled, p=2, dim=1)
            chunks.append(normed.cpu().numpy().astype(np.float32))

    embeddings = np.concatenate(chunks, axis=0)
    assert embeddings.shape[0] == len(records)
    return embeddings, iris


def write_npz(embeddings: np.ndarray, iris: list[str], records: list[dict], out_path: Path) -> str:
    """Write .npz with embeddings + iris + entity_levels for consumer convenience."""
    np.savez(
        out_path,
        embeddings=embeddings,
        entity_iris=np.array(iris, dtype=object),
        entity_levels=np.array([r["entity_level"] for r in records], dtype=object),
        entity_ids=np.array([r["entity_id"] for r in records], dtype=object),
        families=np.array([r["family"] for r in records], dtype=object),
    )
    return hashlib.sha256(out_path.read_bytes()).hexdigest()


def write_manifest(
    out_path: Path,
    n_entities: int,
    embedding_dim: int,
    corpus_sha256: str,
    npz_sha256: str,
    npz_filename: str,
    counts_per_level: dict[str, int],
) -> None:
    manifest = {
        "schema": "appsec-core-v1-embeddings-manifest/1.0",
        "release_artefact": "AppSec Core V1 — SBERT embeddings",
        "rule_version": "1.0",
        "ratification": {
            "date": "2026-05-03",
            "authority": "programme-lead Pedro Farinha",
            "decision_amendment": "ExternalSourcesInventory/agentic/decisions/0003-normalization-algorithm-redesign-2026-05-03-amendment-1-claims-not-chains.md",
            "augmentation_symmetry_section": "§F",
        },
        "model": {
            "name": MODEL_ID,
            "hf_revision_sha": MODEL_REVISION,
            "encoder_max_tokens": ENCODER_MAX_TOKENS,
            "pooling": "mean (attention-mask-weighted)",
            "normalize": "L2 (p=2, dim=1)",
        },
        "library_versions": {
            "transformers": transformers.__version__,
            "torch": torch.__version__,
            "numpy": np.__version__,
        },
        "platform": {
            "system": platform.system(),
            "machine": platform.machine(),
            "python": sys.version.split()[0],
        },
        "corpus": {
            "filename": "augmented-text-corpus.json",
            "sha256": corpus_sha256,
            "n_records": n_entities,
            "counts_per_level": counts_per_level,
        },
        "embeddings": {
            "filename": npz_filename,
            "sha256": npz_sha256,
            "n_entities": n_entities,
            "embedding_dim": embedding_dim,
            "dtype": "float32",
        },
        "build": {
            # Timestamps OUT of the bit-identical artefacts; recorded in manifest only
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        },
        "notes": [
            "Embedding determinism: same inputs + same arch + same lib versions → bit-identical .npz; cross-arch identity not guaranteed.",
            "Excluded entities: EvidencePattern (0 normalized instances in v1) + Artifact (median 2 words; not in algorithm anchor loop). Both registered as future-work gaps.",
            "Cartographer's PIPELINE 2 §2.1 must use the same model + revision + library versions to mirror the encoding side per Decision 0003 Amendment 1 §F.",
        ],
    }
    out_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")


# ============================================================
# Main
# ============================================================

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default=str(THIS_DIR), help="Output directory (default: this folder)")
    ap.add_argument("--corpus-only", action="store_true", help="Build only augmented-text-corpus.json (skip embeddings)")
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[1/3] Building augmented-text-corpus.json from {ONTOLOGY_DIR} ...")
    records = build_corpus()
    counts = {}
    for r in records:
        counts[r["entity_level"]] = counts.get(r["entity_level"], 0) + 1
    print(f"      records: {len(records)} | counts: {counts}")
    corpus_path = out_dir / "augmented-text-corpus.json"
    corpus_sha = write_corpus(records, corpus_path)
    print(f"      sha256: {corpus_sha[:16]}...  -> {corpus_path}")

    if args.corpus_only:
        print("[2/3] Skipped (--corpus-only).")
        print("[3/3] Skipped (--corpus-only).")
        return

    print(f"[2/3] Encoding via {MODEL_ID}@{MODEL_REVISION[:8]} ...")
    os.environ.setdefault("HF_HUB_OFFLINE", "1")  # use cached snapshot only; never silent download
    embeddings, iris = encode_corpus(records)
    npz_filename = f"embeddings-all-MiniLM-L6-v2-{MODEL_REVISION[:8]}.npz"
    npz_path = out_dir / npz_filename
    npz_sha = write_npz(embeddings, iris, records, npz_path)
    print(f"      shape: {embeddings.shape}  sha256: {npz_sha[:16]}...  -> {npz_path}")

    print("[3/3] Writing embeddings-manifest.json ...")
    write_manifest(
        out_dir / "embeddings-manifest.json",
        n_entities=len(records),
        embedding_dim=embeddings.shape[1],
        corpus_sha256=corpus_sha,
        npz_sha256=npz_sha,
        npz_filename=npz_filename,
        counts_per_level=counts,
    )
    print(f"      done.")


if __name__ == "__main__":
    main()
