# Amendment 1 to Decision 0003 — Claim-Centric Normalization (2026-05-03)

**Status:** RATIFIED by programme-lead Pedro Farinha 2026-05-03.
**Supersedes:** sections of `agentic/decisions/0003-normalization-algorithm-redesign-2026-05-03.md` as listed in §A. Decision 0003 itself is preserved per Append-Only History (Programme Preservation Protocol Principle 2); the amendment supersedes specific sections without modifying the original.

**Source documents:**
- Cartographer rev-3 proposal: `agentic/briefs/2026-05-03-cartographer-to-orchestrator-decision-0003-amendment-claims-not-chains-rev3.md`
- Cartographer rev-2 proposal (preserved): `agentic/briefs/2026-05-03-cartographer-to-orchestrator-decision-0003-amendment-claims-not-chains-rev2.md`
- Cartographer rev-1 proposal (preserved): `agentic/briefs/2026-05-03-cartographer-to-orchestrator-decision-0003-amendment-claims-not-chains.md`
- Theoretical foundations appendix: `agentic/briefs/2026-05-03-cartographer-amendment-1-theoretical-foundations-appendix.md`
- Archon SBERT viability inspection: `sbd-toe-ontology/agentic/em-curso/2026-05-03-sbert-embedding-inspection.md`

---

## 1. Why this amendment

Decision 0003's algorithm assumed item-level slice classification with chain-aware multi-anchor. Programme-lead's "peixe-aquacultura" structural objection (2026-05-03) showed that slice-coherence (M1 in the original) is necessary but not sufficient — an item can map to the right slice and still anchor wrongly within it. The amendment adds semantic warrant (M5), reframes around claims rather than item-anchors, and splits the algorithm into two pipelines: structural lifting per source, then source-agnostic ontology grounding.

The amendment also formalises augmentation symmetry: source-side seeds and ontology-side entity representations must share composition rule and embedding model so that similarity scores are interpretable.

---

## 2. Ratified decisions

- **A.1 — Multiplicity detection method**: deterministic heuristic per flattener. A.2 (Lab review) retained as optional ad-hoc checkpoint, not mandatory.
- **B.2 — E3 disambiguation margin**: gap within same `(slice, level)` tuple, not gap against global next-best.
- **C.1 — Phase 1a/1b sequencing**: sequential without mandatory Lab review checkpoint between them.
- **§G already-resolved**: the cross-persona dependency surfaced in Cartographer rev-3 §G — whether the ontology-side matching surface is Archon-side artefact (Path G.A) or Cartographer-side ad-hoc (Path G.B) — was decided in parallel before rev-3 landed. Path G.A ratified 2026-05-03 after the SBERT viability inspection; Archon Part A brief (`agentic/briefs/2026-05-03-archon-embeddings-release-artefact.md`) is in execution. Cartographer rev-3 §G analysis (literature review of three traditions; trade-off matrix V1–V8 / D1–D8; appendix §4-bis) remains valuable as paper §3 prose foundation regardless. §G.5 implementation decisions (α–ε) closed in the Archon Part A brief.

---

## §A — What this amendment supersedes in Decision 0003

- **Decision 0003 §2 invariants** — All seven invariants (M1, M2, M3, M4, P1, P2, P3, P4, P5, P6 mapped per the original document). Replaced by:
  - **M1' — Slice coherence on claim**: every claim's `slice(target)` belongs to the slice classifier+context for the seed.
  - **M5 — Semantic warrant on claim**: `claim.similarity_score ≥ E2(level)` AND `disambiguation_margin ≥ E3(level)`.
  - **P1' — GROUNDED implies claims**: `final_classification = GROUNDED ⇒ |claims[]| ≥ 1`.
  - **Revoked**: P2 (`|primary_slice|=1`), P3 (`|secondary_slice|≤1`), P4 (single principal), P5 (chain anchors in primary), P6 (bottom-up in secondary). All artefacts of the item-anchor framing, made trivial or meaningless under claims.
  - **Retained on the model side (M2–M4)**: CO ∈ Slice, Practice ∈ CO, Mechanism ∈ Practice, plus declared cardinalities. Live in `sbd-toe-ontology` SHACL apparatus, target node `claim`. Archon Part B owns these.

- **Decision 0003 §3 algorithm** — Single algorithm replaced by two pipelines. See §B and §C below.

- **Decision 0003 §4 D-rules and E-rules**:
  - **D1 revoked**: problem-space sources no longer pre-step their `primary_slice`; PIPELINE 2 handles them uniformly via the source-agnostic search.
  - **F1 revoked**: chain-aware multi-anchor framing.
  - **E1, E4, E5 reformulated** around claim and lifted-row.
  - **E3 redefined precisely**: per-(slice, level) gap, not global gap.
  - **E2 calibration cohort**: SSDF + CIS + SAMM + CWE (covers the four shape classes from Phase 0 audit).
  - **D2, D3, D4 retained**.

- **Decision 0003 §5 paper metrics** — Reformulated. New metrics:
  - claims-per-source
  - atomicity ratio (lifted rows / source items)
  - claim emission ratio (claims / lifted rows)
  - distinct Core entities reached per source, with level distribution (CO/Practice/Mechanism)
  - disambiguation margin distribution per source
  - multiplicity-in-supposed-atomic rate
  - classifier ablation (with vs without chain context)

- **Decision 0003 §7 sequencing** — Phase 1 splits into Phase 1a (PIPELINE 1) and Phase 1b (PIPELINE 2). Optional Lab review ad-hoc between them. Phase 2 retained: re-audit against M1' / M5 / P1'.

- **Decision 0003 §8 schema** — Replaced by lifted-row schema (PIPELINE 1 output) + item+claim schema (PIPELINE 2 output). See §C and §D.

---

## §B — Algorithm: two pipelines

**PIPELINE 1 — Structural lifting (per source; runs once; deterministic; emits one intermediate file per source)**

Input: source raw artefacts + `source_object_inventory.json` per source + per-source flattener config.

Per-source steps:
1.1 Read source items + their hierarchy.
1.2 Apply per-source decomposer (per `decomposition_policy`, deterministic heuristic from A.1).
1.3 Build `contextualised_text` per lifted row, composing seed text with source-internal hierarchy titles.
1.4 Preserve `source_chain` (titles + structural levels).
1.5 Preserve `source_facets` (maturity, stream, etc.).
1.6 Emit `<source>_lifted.jsonl`.

Output: 26 `.jsonl` files, one per active source.

**PIPELINE 2 — Ontology grounding (source-agnostic; uniform; consumes lifted files as canonical input)**

Input: the 26 `<source>_lifted.jsonl` files + AppSec Core ontology matching surface (Archon Part A release artefact: `augmented-text-corpus.json` + `embeddings-{model}-{commit}.npz` + `augmentation-rule.yaml`).

Per-lifted-row steps:
2.1 Embed `contextualised_text` with the same SBERT model + commit that Archon used. Score similarity (cosine) against ontology entity embeddings across all 10 slices and 3 levels (CO / Practice / Mechanism).
2.2 Apply E2 admissibility threshold per level.
2.3 Apply E3 disambiguation margin against next-best in same `(slice, level)` tuple.
2.4 Emit zero or more claims: for each candidate passing E2 ∧ E3, `claim(lifted_row_ref, target_core_entity, level, slice, similarity_score, disambiguation_margin)`.
2.5 If no claim emitted → record as `lab_depth_pending` row.

Post-pass:
2.6 Aggregate claims per `source_item_id`.
2.7 Build ontology-side index (paper §5/§6 view).

Output: substrate (item + claims) per the schema in §D.

---

## §C — Schema: PIPELINE 1 output (`<source>_lifted.jsonl`)

```yaml
lifted_row:
  lifted_id: "<source>-LIFTED-<seq>"
  source_pilot: "<source_key>"
  source_object_id: "<source-internal-id>"
  source_text_span: "<exact text excerpt>"
  contextualised_text: "<source-chain-titles> / <seed text>"
  structural_provenance:
    chain: ["<title at level 0>", ...]
    levels: ["<level name 0>", ...]
    facets: {maturity_tier, stream, ...}
  decomposition:
    method: "passthrough" | "heuristic_split" | "multiplicity_triggered"
    seed_index: <int>
    seed_total: <int>
  flattener_version: "<source>_flattener_v0.1"
  emitted_at: <iso8601>
```

---

## §D — Schema: PIPELINE 2 output (substrate)

```yaml
item:
  item_id, source, source_object_id
  source_text
  source_lifted_rows: [lifted_id, ...]
  final_classification: GROUNDED | LabDepthPending | OOS_AppSec
  claims: [...]
  lab_depth_seeds: [lifted_id, ...]
  decomposition_diagnostic:
    n_lifted_rows
    multiplicity_in_supposed_atomic: bool

claim:
  claim_id
  lifted_row_ref: lifted_id
  item_ref: item_id
  target_core_entity
  level: CO | Practice | Mechanism
  slice: ACO-XXX
  similarity_score
  disambiguation_margin
  rationale_snippet
  ablation_baseline_score:
    score_without_chain_context: float | null
    differs_from_with_context: bool | null
```

---

## §E — Acceptance criteria for halt-lift (revised)

There is one product. The halt lifts when, on the same substrate emission:

1. Phase 0 audit landed (done) + extension landed (done).
2. Phase 1a emitted 26 lifted `.jsonl` files.
3. Phase 1b emitted v5 substrate per the schema in §D.
4. Phase 2 re-audit reports zero violations of M1' + M5 + P1' on v5 substrate.
5. Archon SHACL Tier-2 (Part B) reports conformance against v5 substrate, targeting `claim` nodes, with model invariants M2–M4 enforced.
6. Programme-lead + Orchestrator jointly declare the **acceptable attempt**.

Once accepted, Paper 3 first stage proceeds to SSDF/SCF triangulation against the accepted substrate. Paper 3 second stage (Manual + KG iteration to freeze) remains paused until first stage closes.

---

## §F — Augmentation symmetry principle (formalised)

The function used to score `similarity(contextualised_text, target_core_entity_representation)` in PIPELINE 2 step 2.1 must compare two representations that are **structurally analogous**. Specifically:

- **Source side** (PIPELINE 1 output `contextualised_text`): composed by per-source flattener of seed text with source-internal hierarchy titles ascending up the chain.
- **Ontology side** (Archon Part A release artefact): composition per the ratified augmentation rule (Slice/CO/Practice/Mechanism templates from Q2 of the SBERT viability inspection).

Both sides share the same **embedding model + commit + library version** (Archon's choice; Cartographer mirrors). Both sides share the same **format conventions** — separator characters, label prefixes, snake-case handling, ascending order. Format conventions are coordinated through a Cartographer ↔ Archon snippet exchange before either side commits its composition rule.

If the two sides diverge structurally, similarity scores compare incomparable representations and E2/E3 thresholds become uninterpretable.

---

## §G — Cross-persona dependency on ontology-side matching surface (resolved)

Cartographer rev-3 §G surfaced the dependency that PIPELINE 2 requires an ontology-side matching surface that did not exist as a release artefact at the time of writing. Two paths were proposed: G.A (Archon-side release artefact) or G.B (Cartographer-side ad-hoc).

**Resolved 2026-05-03 in parallel with rev-3 drafting**: Path G.A ratified. Archon Part A brief (`agentic/briefs/2026-05-03-archon-embeddings-release-artefact.md`) dispatched. Archon's SBERT viability inspection completed. Mechanism `supports_practices` aggregation rule ratified. Implementation decisions α–ε from §G.5 closed in the Part A brief.

The §G analysis itself — literature review of three converging traditions (ontology embeddings, dense retrieval indexes, ontology lookup services); trade-off matrix V1–V8 / D1–D8; appendix §4-bis — remains valuable as paper §3 prose foundation. Two ontology-side gaps surfaced by the inspection (EvidencePattern: 0 normalized instances; Artifact: structurally text-poor) recorded as future work, not blocking.

---

## §H — Sequencing + executable plan summary

**Now (in flight)**:
- **Archon Part A** — embeddings release artefact in `sbd-toe-ontology/formal/appsec_core/<embeddings-path>/`.

**In parallel after format-convention coordination**:
- **Cartographer Phase 1a** — PIPELINE 1 structural lifting per source. Does not require SBERT model at runtime. Requires Archon's format conventions (separator chars, label prefixes, snake-case handling, ordering) to mirror on the source-side composition.

**After Archon Part A lands and Cartographer Phase 1a lands**:
- **Cartographer Phase 1b** — PIPELINE 2 ontology grounding. Consumes Archon's `.npz` + Cartographer's `.jsonl` files. Embeds source side with the same model.

**After Cartographer amendment-1 ratification (now)**:
- **Archon Part B** — SHACL Tier-2 build. Target node = `claim` (fixed by this amendment). Shapes for M2–M4 model invariants. Parametric validator with `ont_graph` loaded.

**Coordination**:
- **Cartographer ↔ Archon format conventions snippet** — before either commits composition rule, exchange separator/prefix/ordering choices to eliminate format mismatch risk. Orchestrator coordinates if needed.

**After substrate v5 lands**:
- **Orchestrator dispatches**: run Archon validator against v5; produce SHACL conformance report; reconcile with Cartographer Phase 2 process-invariant report; programme-lead + Orchestrator ratify acceptable attempt; halt lifts.
