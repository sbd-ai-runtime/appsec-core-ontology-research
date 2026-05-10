# AppSec Core V1 — SBERT Embeddings Release Artefact

**Owner:** Archon (sbd-toe-ontology)
**Rule version:** 1.0 (ratified by programme-lead Pedro Farinha, 2026-05-03)
**Authority:** Decision 0003 Amendment 1 §F (augmentation symmetry principle), Embeddings Part A brief.

---

## What this is

Pre-computed SBERT embeddings for AppSec Core V1 ontology entities, plus the augmentation rule + corpus they were built from. Any consumer that needs to perform similarity-based matching against AppSec Core entities — the current normalization pipeline, a future Manual KG, an MCP plugin, anything else — uses these artefacts as the canonical matching surface.

The embeddings are deterministic, reproducible, and pinned to a specific model revision. Any consumer running the same model + same library versions on the same architecture gets bit-identical embeddings.

## Files in this folder

| File | Purpose |
|---|---|
| `augmentation-rule.yaml` | Deterministic specification of how each ontology entity is converted into augmented text (rule v1.0). Cited by every other artefact here. |
| `format-conventions-snippet.md` | Five format conventions shared with Cartographer's source-side flattener for §F symmetry. Final convergence at most-specific-first ordering 2026-05-03. |
| `augmented-text-corpus.json` | Output of the rule applied to canonical YAML. 209 records (Slice 10 + CO 74 + Practice 68 + Mechanism 57). Source of truth for the embeddings file. |
| `embeddings-all-MiniLM-L6-v2-c9745ed1.npz` | Pre-computed embeddings: 209 × 384 float32 + entity IRIs + entity levels + entity ids + slice families. |
| `embeddings-manifest.json` | Manifest: model name + HF revision SHA + library versions + platform + corpus sha256 + npz sha256 + counts per level. |
| `build-script.py` | Deterministic regenerator: canonical YAML + this rule + pinned model → corpus + .npz + manifest. Reproducible bit-for-bit. |

## What is excluded (and why)

Two entity levels are excluded from this release per the SBERT viability inspection (`sbd-toe-ontology/agentic/em-curso/2026-05-03-sbert-embedding-inspection.md`):

- **EvidencePattern** — zero normalized instances exist in V1. Schema is first-class; instances are not yet authored. Will be added when consumer authoring lands.
- **Artifact** — median 2 augmented-words per entity (no `description` field; only `name + role + local`). Structurally text-poor and not in the algorithm's anchor loop per Decision 0003 §3 + Amendment 1 §A. Will be added when a future consumer needs Artifact-level discrimination.

Both are tracked as future-work gaps; neither blocks any current consumer.

## How a consumer uses this

Three-line load + cosine similarity example (Python):

```python
import numpy as np

# Load
data = np.load("embeddings-all-MiniLM-L6-v2-c9745ed1.npz", allow_pickle=True)
embeddings = data["embeddings"]            # shape (209, 384), float32, L2-normalized
entity_iris = data["entity_iris"]          # array of 209 IRIs (objects), e.g. "ac:ACO_IVF_002"
entity_levels = data["entity_levels"]      # array of 209 levels, e.g. "ControlObjective"
entity_ids = data["entity_ids"]            # array of 209 short ids, e.g. "ACO-IVF-002"
families = data["families"]                # array of 209 family codes, e.g. "ACO-IVF"

# Score a query (must use the SAME model + revision + library versions; see manifest)
# Below: pseudocode for the query-side encode, then cosine similarity.
query_text = "validate JSON schema at the API boundary"
query_vec  = encode([query_text])[0]       # 384-dim L2-normalized vector
scores     = embeddings @ query_vec        # cosine similarity (both already L2-normalized)
top_k_idx  = np.argsort(-scores)[:5]
for i in top_k_idx:
    print(f"{scores[i]:.3f}  {entity_levels[i]:>16s}  {entity_iris[i]}")
```

Filter at retrieval time using `entity_levels` (e.g., select only `ControlObjective` candidates) — the level is **not** an in-text token in the embedded text, so similarity is comparable across levels.

## Pinning — what consumers must mirror

To produce comparable similarity scores (per Decision 0003 Amendment 1 §F augmentation symmetry), any consumer's query-side encode must use:

| Item | Value |
|---|---|
| Model | `sentence-transformers/all-MiniLM-L6-v2` |
| HF revision SHA | `c9745ed1d9f207416be6d2e6f8de32d1f16199bf` |
| Library: transformers | `4.57.1` |
| Library: torch | `2.2.2` |
| Tokenizer max_length | `256` |
| Padding | `True` |
| Truncation | `True` |
| Pooling | mean (attention-mask-weighted) |
| Normalize | L2 (`p=2`, `dim=1`) |
| Output dtype | `float32` |

The full manifest is at `embeddings-manifest.json`. Consumers should compare their library versions against the manifest at startup; warn or fail loudly if the model revision SHA differs.

## How to regenerate (verify or upgrade)

```bash
# One-time venv setup (system Python's Pillow 9.0.1 lacks PIL.Image.Resampling
# needed by transformers; isolated upgrade inside the venv keeps system Python
# untouched)
python3 -m venv --system-site-packages .venv
.venv/bin/pip install --upgrade "Pillow>=9.1.0"

# Build (regenerates corpus + .npz + manifest into this folder)
.venv/bin/python3 build-script.py

# Or build into a different output dir:
.venv/bin/python3 build-script.py --out-dir /path/to/output

# Or build only the augmented-text-corpus.json (skip embeddings):
.venv/bin/python3 build-script.py --out-dir /path/to/output --corpus-only
```

The build is offline-capable once the model snapshot is cached in `~/.cache/huggingface/hub/models--sentence-transformers--all-MiniLM-L6-v2/`. The script sets `HF_HUB_OFFLINE=1` defensively to prevent silent re-downloads.

## Reproducibility verification

Two independent runs of `build-script.py` against the canonical YAML at this commit produce bit-identical output:

```
augmented-text-corpus.json                     sha256: fc88c38e653d5f3c7dc3f4295193673b46eef3b4b32e4751611ad9f7cc48b17b
embeddings-all-MiniLM-L6-v2-c9745ed1.npz       sha256: a3d3be8cf8b175256ff123ebf9e470b7755f9f5db354fcd880431dcbf41bb66d
```

Cross-architecture bit-identity is **not** guaranteed (floating-point determinism varies across CPU/GPU vendors); the manifest records `platform.system` + `platform.machine` to diagnose any divergence. Same-architecture re-runs are deterministic.

## Provenance + governance

- This release artefact is generated from canonical YAML at `sbd-toe-ontology/ontology/` (per ADR 0010, YAML is canonical; OWL/SHACL/embeddings are derivative skins).
- The augmentation rule is rule_version `1.0`. Any change to the rule that affects augmented text bumps this version and produces a new release artefact alongside this one (append-only history per Programme Preservation Protocol Principle 2).
- The model pinning is by HF revision SHA. Upgrading to a different model OR a different revision is a new release artefact (different filename embeds the model + commit).
- The two excluded entity levels (EvidencePattern, Artifact) remain registered as future-work gaps; they will be added when consumer demand or ontology authoring catches up.
- Coordination with Cartographer's source-side flattener (PIPELINE 2 §2.1 of Decision 0003 Amendment 1) is via the format-conventions snippet in this folder. Both sides converged at the conventions in the snippet during 2026-05-03 sync.

## Cross-references

- Augmentation rule: `augmentation-rule.yaml`
- Format conventions snippet: `format-conventions-snippet.md`
- Build script: `build-script.py`
- Manifest: `embeddings-manifest.json`
- SBERT viability inspection (Q1/Q2/Q3 evidence base): `sbd-toe-ontology/agentic/em-curso/2026-05-03-sbert-embedding-inspection.md`
- Embeddings Part A brief: `ExternalSourcesInventory/agentic/briefs/2026-05-03-archon-embeddings-release-artefact.md`
- Decision 0003 Amendment 1 §F (augmentation symmetry): `ExternalSourcesInventory/agentic/decisions/0003-normalization-algorithm-redesign-2026-05-03-amendment-1-claims-not-chains.md`
