"""SBERT encoder for source-side lifted rows.

Mirrors Archon Part A `build-script.py` exactly per Decision 0003 Amendment 1
§F (augmentation symmetry). Same model, same revision, same library versions,
same pooling, same normalisation.

  Model     : sentence-transformers/all-MiniLM-L6-v2
  Revision  : c9745ed1d9f207416be6d2e6f8de32d1f16199bf
  Max tokens: 256 (encoder cap)
  Pooling   : mean over attention mask
  Normalize : L2 (p=2, dim=1)
  Output    : float32 numpy array, shape (N, 384)

Determinism: deterministic on the same arch + same library versions per the
manifest's `notes` (cross-arch identity not guaranteed).
"""
from __future__ import annotations
import pathlib
from typing import Sequence

import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer

# ---- Pinned model (mirror Archon manifest) -----------------------------------
MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2"
MODEL_REVISION = "c9745ed1d9f207416be6d2e6f8de32d1f16199bf"
ENCODER_MAX_TOKENS = 256
ENCODER_BATCH_SIZE = 32

_tokenizer = None
_model = None


def _ensure_loaded(device: str = "cpu"):
    global _tokenizer, _model
    if _tokenizer is None:
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=MODEL_REVISION)
    if _model is None:
        _model = AutoModel.from_pretrained(MODEL_ID, revision=MODEL_REVISION)
        _model.eval()
        _model.to(device)


def encode_texts(texts: Sequence[str], device: str = "cpu") -> np.ndarray:
    """Encode strings → (N, 384) float32 L2-normalized embeddings.

    Mirror of Archon's `encode_corpus` to byte-for-byte parity (modulo
    OS/arch determinism caveats per manifest).
    """
    if not texts:
        return np.empty((0, 384), dtype=np.float32)

    torch.manual_seed(0)
    np.random.seed(0)

    _ensure_loaded(device=device)

    chunks: list[np.ndarray] = []
    with torch.no_grad():
        for i in range(0, len(texts), ENCODER_BATCH_SIZE):
            batch = list(texts[i : i + ENCODER_BATCH_SIZE])
            enc = _tokenizer(
                batch,
                padding=True,
                truncation=True,
                max_length=ENCODER_MAX_TOKENS,
                return_tensors="pt",
            ).to(device)
            out = _model(**enc)
            mask = enc["attention_mask"].unsqueeze(-1).expand(out.last_hidden_state.size()).float()
            pooled = (out.last_hidden_state * mask).sum(1) / mask.sum(1).clamp(min=1e-9)
            normed = torch.nn.functional.normalize(pooled, p=2, dim=1)
            chunks.append(normed.cpu().numpy().astype(np.float32))

    embeddings = np.concatenate(chunks, axis=0)
    assert embeddings.shape == (len(texts), 384), embeddings.shape
    return embeddings


# ---- Convenience: load Archon's release artefact -----------------------------
ONTOLOGY_REPO = pathlib.Path(
    "/Volumes/G-DRIVE/Shared/SecurityByDesign-TheoryOfEverything/sbd-toe-ontology/formal/appsec_core/08-embeddings"
)


def load_ontology_embeddings():
    """Load Archon Part A release artefact (.npz + corpus + manifest).

    Returns dict with:
      embeddings: (209, 384) float32
      entity_iris: (209,) str — canonical IRI per Archon
      entity_levels: (209,) str — Slice / ControlObjective / Practice / Mechanism
      entity_ids: (209,) str — readable IDs (ASC-01, ACO-IAT-001, etc.)
      families: (209,) str — slice family (ACO-IAT, etc.)
      manifest: dict
      corpus: list[dict]  (per-record metadata)
    """
    import json
    npz_path = ONTOLOGY_REPO / "embeddings-all-MiniLM-L6-v2-c9745ed1.npz"
    manifest_path = ONTOLOGY_REPO / "embeddings-manifest.json"
    corpus_path = ONTOLOGY_REPO / "augmented-text-corpus.json"

    arr = np.load(npz_path, allow_pickle=True)
    with manifest_path.open() as f:
        manifest = json.load(f)
    with corpus_path.open() as f:
        corpus = json.load(f)
    return {
        "embeddings": arr["embeddings"],
        "entity_iris": arr["entity_iris"],
        "entity_levels": arr["entity_levels"],
        "entity_ids": arr["entity_ids"],
        "families": arr["families"],
        "manifest": manifest,
        "corpus": corpus.get("records", []) if isinstance(corpus, dict) else corpus,
    }
