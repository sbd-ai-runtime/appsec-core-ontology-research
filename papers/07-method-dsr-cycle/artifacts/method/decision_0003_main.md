# Decision 0003 — Normalization Against an Imposed Model (2026-05-03)

**The thesis of this decision, in one line:** the product is a single substrate that normalizes the 26 ESI against AppSec Core; conformance is demonstrated by SHACL validation that imposes the model. The algorithm is an attempt to produce that substrate; we iterate the algorithm until SHACL declares conformance. Whatever algorithm we adopt, the test of acceptance is the same — the imposed model.

There is one product. There are no phases of work toward it; there are iterations. SHACL is the authority.



**Status:** Ratified by programme-lead Pedro Farinha 2026-05-03.
**Supersedes:** the Stage-6.bis overlay system (`A_NIST_relax`, `B4_alpha_split_promote`, `preserved_grounded_from_v40_v2`, `B1_TMR_boundary`, `preserved_oos_amendment`) and the v3.2 / v4.x scoring scripts that emit slice-incoherent anchors.
**Authority docs:**
- Halt: `agentic/em-curso/2026-05-03-slice-coherence-halt.md`
- Cartographer slice-violation audit: `data/p7_olir_audit/p7_v2_corrected/SLICE-VIOLATION-AUDIT-2026-05-03.md`
- Archon SHACL completeness diagnosis: `data/p7_olir_audit/p7_v2_corrected/SHACL-SLICE-COMPLETENESS-DIAGNOSIS-2026-05-03.md`

This decision is the **single source of truth** for the redesigned normalization algorithm and the SHACL guard that enforces it. Cartographer (substrate construction) and Archon (SHACL + validator) consume this document as the binding spec; their briefs are wrappers pointing here.

---

## 1. Why this redesign

The current normalization process produces incoherent output — verified empirically by Cartographer's audit. The substrate violates three structural invariants (anchored CO outside slice; GROUNDED items without anchor; primary slice with cardinality > 1). The SHACL guard that should have caught these is incomplete and unreachable in four layers (no shape, no `belongsToSlice` triple emission, validator runs with `ont_graph=None`, IRI scheme misalignment between substrate and ontology).

Programme-lead direction: **coherence-first reset, not patch hunt.** Fix the algorithm at construction time; build SHACL as guard against future regression. Do not enumerate violations and patch items.

This redesign also incorporates a structural insight raised by programme-lead 2026-05-03: ESI items live at **different abstraction levels** (CO / Practice / Mechanism). Some sources are CO-level, some are Mechanism-level, many mix levels. A normalization that flattens everything to CO loses information and inflates apparent coverage. The ontology must be preserved regardless of source; the algorithm must respect each item's natural level. Sources with extractable internal hierarchy (`area → control → practice → mechanism`) emit a **chain** of anchors, not a single point.

---

## 2. Invariants — model vs process (ratified, amended 2026-05-03)

The redesign distinguishes **model invariants** (statements about AppSec Core itself — true regardless of consumer) from **process invariants** (statements about how the normalization pipeline is built — true regardless of dataset). The two have different homes, different tools, different owners.

### 2.1 Model invariants (SHACL, in `sbd-toe-ontology`)

These derive directly from the relations the AppSec Core V1 ontology declares. Any consumer (this normalization, the Manual KG, an MCP plugin, anything else) is bound by them. SHACL is the right tool because the rules are declarative, graph-shaped, and consumer-agnostic.

For every normalized item *I* in any consumer's output:

- **M1. CO ∈ Slice** — every CO anchor belongs to the slice declared by `belongsToSlice` in the ontology.
- **M2. Practice ∈ CO** — every Practice anchor belongs to a CO via `objective_realized_by_practice` in the ontology.
- **M3. Mechanism ∈ Practice** — every Mechanism anchor belongs to a Practice via `objective_implemented_by_mechanism` in the ontology.
- **M4. Cardinalities the ontology declares** — e.g., every CO has exactly one Slice. (Inventory at SHACL build time; record any cardinalities the ontology itself asserts.)

These are enforced by SHACL shapes living alongside `appsec-core-v0-shapes.ttl` (the apparatus tag is immutable; new shapes are WRITE-NEW in a parallel file). Owner: Archon. Repo: `sbd-toe-ontology`.

### 2.2 Process invariants (NOT SHACL — schema + assertions + unit tests, in ESI)

These are **how the normalization pipeline interprets and treats the 26 ESI** to produce an output coherent with AppSec Core. They are not statements about AppSec Core; they are statements about the algorithm and the schema of its output. They live with the pipeline.

For every record the algorithm emits:

- **P1.** `GROUNDED ⇒ anchors[]` non-empty. (Step 5/6 of the algorithm guarantees this by construction.)
- **P2.** `|primary_slice| = 1`. (Step 2 emits cardinality 1 by construction.)
- **P3.** `|secondary_slice| ∈ {0, 1}`. (Step 4 by construction.)
- **P4.** Exactly one `is_principal: true` per GROUNDED item. (Step 3 designates by construction.)
- **P5.** Anchors with `provenance = "source-chain"` are all in `primary_slice`. (Step 3 cases A/B by construction; case C escalates to LabDepthPending.)
- **P6.** Anchors with `provenance = "bottom-up"` have `slice(anchor) = secondary_slice`. (Step 4 sets secondary by construction.)

Tools (none of them SHACL):

- **Schema validation** at output time — Pydantic / JSON Schema over `SUPPLIER_v5_0.json`. Catches malformed records the moment they are emitted.
- **Inline assertions** inside the algorithm code — `assert len(primary_slice) == 1` after Step 2, etc. Catches algorithm bugs at the line they happen.
- **Unit tests** of the algorithm — verify across input fixtures that emitted records satisfy P1–P6 by construction.

Owner: Cartographer. Repo: ExternalSourcesInventory.

A non-zero count of P1–P6 violations in the substrate is a **bug in the algorithm code**, not a substrate-quality problem. The fix is in the code, not in the data. This is the lesson of the Stage-6.bis overlay system: process invariants were treated as data-quality knobs and "patched" via overlay rules; the result was incoherent normalization. Process invariants must hold by construction.

### 2.3 Why this distinction matters

- The model invariants (M1–M4) exist whether this pipeline exists or not. They are properties of AppSec Core. SHACL is the correct enforcement tool because the rules are declarative and serve every future consumer.
- The process invariants (P1–P6) exist only because we chose this algorithm and this output schema. Different algorithm → different process invariants. SHACL is the wrong tool for them — they are not graph statements about a model; they are construction-time guarantees about an algorithm.
- Conflating the two leads to dívida técnica: process invariants leak into ontology shapes (where they outlive their algorithm), and model invariants are enforced only on the consumer (where they are not enforced for other consumers). The 8-stage caveat that produced this halt was exactly this conflation, in reverse: a model invariant (M1) was registered as "future work for the pipeline's SHACL" instead of being where it belonged — in the ontology's SHACL.

---

## 3. The algorithm (chain-aware, level-aware, top-down + bottom-up)

```
INPUT: a single ESI item I with text content and (when extractable) source-internal hierarchy.

OUTPUT: a normalized record {
  primary_slice, secondary_slice,
  anchors: [{ level, concept, provenance, is_principal }],
  final_classification ∈ {GROUNDED, LabDepthPending, OOS_AppSec},
  diagnostics: { ... }
}

──────────────────────────────────────────────────────────────────
STEP 1 — EXTRACT SOURCE-CHAIN (if source has structured hierarchy)
──────────────────────────────────────────────────────────────────
Parse I's source-internal levels (e.g., NIST Family→Control→Enhancement;
SAMM Function→Practice→Activity→Stream; PCI Requirement→Sub→Test).

For each source-level, propose a candidate (slice, ontology_level, concept)
by best similarity match against AppSec Core V1.

Output: source_chain = [(level, concept_candidate, similarity_score), ...]

──────────────────────────────────────────────────────────────────
STEP 2 — CLASSIFY ITEM TOP-DOWN (always)
──────────────────────────────────────────────────────────────────
Read I's text. Emit:
  - top_down_slice (cardinality 1; the dominant domain by semantic analysis)
  - top_down_item_level ∈ {CO, Practice, Mechanism}
        decided by source default + textual cues
        ("ensure capability X" → CO; "use technique Y" → Mechanism;
         "follow approach Z" → Practice)

──────────────────────────────────────────────────────────────────
STEP 3 — RECONCILE source_chain (Step 1) AND top_down (Step 2)
──────────────────────────────────────────────────────────────────
CASE A — Single-slice chain (source-chain extractable, all levels in one slice):
  primary_slice := chain.slice
  anchors := all chain levels above similarity threshold, marked
            provenance="source-chain"
  principal_anchor := deepest level (Mechanism > Practice > CO)
  IF top_down_slice disagrees → set diagnostic_flag.classifier_chain_disagreement = true
  GO TO STEP 5

CASE B — Majority-slice chain (≥ 50% of chain levels in one slice):
  primary_slice := majority.slice
  chain_anchors := levels in primary_slice (above threshold)
  outliers (chain levels in other slices) → recorded in diagnostics.chain_outliers,
           NOT emitted as additional anchors (preserved as data, not asserted as fact)
  principal_anchor := deepest level in primary_slice
  GO TO STEP 5

CASE C — Fragmented chain (no slice owns majority):
  Tiebreaker: top_down_slice. If top_down_slice == any chain.level.slice,
              that becomes primary_slice; chain_anchors in primary_slice only.
  IF still unresolved → final_classification := LabDepthPending
                       diagnostics.chain_full_record := source_chain
                       (preserved for human review)
  GO TO STEP 6

CASE D — No source-chain (flat source):
  primary_slice := top_down_slice
  anchor := search at top_down_item_level in primary_slice (cascade: text similarity
            against AppSec Core entities at that level)
  IF found → emit single anchor with provenance="top-down"
             principal_anchor := this anchor
             GO TO STEP 5
  IF not found → GO TO STEP 4 (bottom-up rescue)

──────────────────────────────────────────────────────────────────
STEP 4 — BOTTOM-UP RESCUE (only when top-down fails to anchor)
──────────────────────────────────────────────────────────────────
Search at top_down_item_level across the other 9 slices.
Take best match above level-specific threshold (see § 4 for thresholds).

IF found:
  secondary_slice := slice(rescued_anchor)
  primary_slice stays as classified top-down
  anchor with provenance="bottom-up", is_principal=true
  GO TO STEP 5

IF not found:
  final_classification := LabDepthPending
  GO TO STEP 6

──────────────────────────────────────────────────────────────────
STEP 5 — EMIT GROUNDED RECORD
──────────────────────────────────────────────────────────────────
final_classification := GROUNDED
emit primary_slice, secondary_slice (if any), anchors[], principal_anchor.

ALWAYS COMPUTE AND STORE (diagnostic, does not influence anchoring):
  - best alternative anchor at same level in different slice (measures
    classifier accuracy)
  - best alternative anchor at adjacent levels in primary_slice (measures
    ontology depth gaps)

──────────────────────────────────────────────────────────────────
STEP 6 — EMIT LabDepthPending OR OOS RECORD
──────────────────────────────────────────────────────────────────
LabDepthPending: classifier and bottom-up both failed; OOS rules did not match.
OOS_AppSec: matches an OOS rule (already-defined: ASVS chapter meta, PCI 9.x
            physical, SAMM context, META-empty, asvs_v4_0_2 amendment).
```

---

## 4. Decisions ratified for the algorithm

- **D1 — Problem-space sources** (CAPEC, CWE, SafeCode, EU regulatory): populate `primary_slice` from `candidate_slice` (the inverted-keyword index output) before applying the algorithm. Invariant 1 then applies universally.
- **D2 — Adjunct `ACR-*` anchors:** out of scope for this redesign; deferred. Items with `ACR-*` anchors are treated as `OOS_AppSec` for normalization purposes; downstream programme decision will define whether to register a 11th category or admit them via a separate path.
- **D3 — GROUNDED-without-anchor:** Invariant 2 applies. The 415 current items with `final_classification = GROUNDED` and `candidate_appsec_core_concept = null` become `LabDepthPending` upon re-run.
- **D4 — IRI alignment:** canonical = the AppSec Core V1 ontology format (`ac:ACO_XXX_NNN` for COs, `ac:SliceASC0X` for slices, etc.). Substrate emission aligns to ontology. Validator loads the ontology graph (`ont_graph` non-null).
- **E1 — Anchor granularity:** single `final_classification = GROUNDED` taxonomy; granularity carried by per-anchor `level ∈ {CO, Practice, Mechanism}` field.
- **E2 — Similarity thresholds:** three thresholds, one per anchor level (CO, Practice, Mechanism), calibrated empirically on the first 4–5 sources processed and then fixed for the remainder. Threshold values to be determined by Cartographer during Phase 1 implementation; recorded in the redesign appendix once chosen.
- **E3 — Existing classifier-secondary:** discard. The 389 items currently carrying classifier-derived `secondary_slice` will have it cleared and re-derived bottom-up only if Step 4 of the algorithm fires.
- **E4 — `item_level` classification:** each source declares a default level (CO, Practice, Mechanism, or "mixed"). Item-level textual analysis overrides default when textual cues are unambiguous. Both default and override recorded per item for audit.
- **E5 — Item-level not in slice:** LabDepthPending without level promotion. Do not promote items to a coarser ontology level when their natural level is absent in the slice — that is the failure mode the overlay system instantiated. The diagnostic value is a paper-citable ontology gap.
- **D-rule-1 (tie-breaker):** when an anchor is found in primary, do not search secondary even if it might also have a match. Prefer top-down classifier authority. **However**, always store the best alternative-slice score in diagnostics for later transparency.
- **F1 — Tier 2 chain-aware multi-anchor:** ratified. Source-chain (when extractable) emits multiple anchors with provenance and a single principal.

---

## 5. Three diagnostic metrics for paper

The redesigned algorithm emits per source and per slice:

1. **Top-down classifier accuracy.** Items rescued bottom-up / total items. Measures slice-classifier precision per source.
2. **Source ontological depth.** Distribution of items by `principal_anchor.level` (CO / Practice / Mechanism). Shows where each ESI naturally lives.
3. **Ontology coverage gap.** LabDepthPending / total per slice and per level. Identifies AppSec Core's depth gaps as future work.

These three replace `% GROUNDED` as the Paper 3 evidence headline.

---

## 6. Anchor-distinct counting (Manual + paper level)

Per programme-lead 2026-05-03: when *N* items from a source anchor to the same ontology point, that is *one* contribution to the ontology with *N* supporting evidences, not *N* contributions. Post-processing collapses items by principal anchor for paper-prose counting:

> *"CIS contributed 171 items mapped to 87 distinct ontology points (54 COs, 25 Practices, 8 Mechanisms). 23 items converged on capability X, reflecting the source's redundant articulation of that domain."*

Per-item granularity is preserved in the substrate; collapsed counting is a derived view.

---

## 7. Who does what (amended 2026-05-03 — no phases, only iterations toward one product)

The redesign separates **model enforcement** (Archon, in `sbd-toe-ontology`) from **process enforcement** (Cartographer, in ESI). Different repos, different tools, different owners. There is one final product: the conforming substrate.

### 7.1 Archon — owns the imposition of the model

- **Inventory the ontology's declared relations** (`belongsToSlice`, `objective_realized_by_practice`, `objective_implemented_by_mechanism`, plus cardinalities). If a relation is implied by the model but not asserted formally in the ontology files, flag for programme-lead — do not invent.
- **Write SHACL shapes** in a new file in `sbd-toe-ontology` alongside (not modifying) the immutable apparatus shapes. Shapes target the consumer's normalized-item nodes; use `ont_graph` to access ontology relations.
- **Write a validator** that loads `ont_graph` (non-null), the substrate's data graph, and the new shapes. Run pyshacl. Emit a conformance report.
- **Each iteration:** validator runs against whatever Cartographer most recently emits; produces a pass/fail report. When SHACL is satisfied, the model declares the substrate conformant.
- **Reconciliation note** after the final iteration: tie SHACL findings to Cartographer's process-invariant report.

### 7.2 Cartographer — owns the algorithm + substrate + process invariants

Sequence of work, but not phases — these are activities within a single iterative effort toward the conforming substrate:

- **Read the 26 sources to understand their hierarchy.** Output: `SOURCE-HIERARCHY-AUDIT-2026-05-03.md` (informs the algorithm; not a delivery gate).
- **Build the algorithm** per § 3 as a deterministic Python pipeline at `scripts/v5_normalization/`. Inline assertions enforce P1–P6 at construction time; Pydantic schema enforces structural invariants on emission; unit tests cover P1–P6 explicitly.
- **Calibrate E2 thresholds** on first 4–5 sources; fix; document.
- **Eliminate Stage-6.bis overlay rules entirely** from the new pipeline.
- **Run on the 26-ESI corpus.** Emit `v5/SUPPLIER_v5_0.json`.
- **Each iteration:** if Archon's SHACL declares non-conformance, fix the algorithm, re-emit. The substrate is not "patched"; the algorithm is corrected and the substrate is regenerated. Iterate until SHACL passes.
- **Final report** when SHACL declares conformance: process-invariant pass (Pydantic + tests) + SHACL pass.

### 7.3 Iteration discipline (no phases, no waterfall)

- Cartographer's source-reading and Archon's ontology-inventory + shape design happen concurrently; neither is a gate on the other.
- The first algorithm run produces a substrate; Archon's SHACL evaluates it; if non-conforming, Cartographer iterates.
- Each iteration changes the **algorithm** (and possibly the schema if a model invariant exposes a structural gap), never the substrate-as-data. The substrate is a function of the algorithm.
- The work ends when SHACL declares conformance and process invariants pass. That is the **one final product**.

---

## 8. New substrate schema (per item)

```yaml
item_id: "<source>/<id>"
source: "<source_key>"
final_classification: "GROUNDED" | "LabDepthPending" | "OOS_AppSec"

primary_slice: "ACO-XXX"           # cardinality = 1; absent if OOS or LabDepthPending-no-slice
secondary_slice: "ACO-YYY" | null  # cardinality ≤ 1; bottom-up rescue only

anchors:                            # empty if not GROUNDED
  - level: "CO" | "Practice" | "Mechanism"
    concept: "<canonical IRI>"
    provenance: "source-chain" | "top-down" | "bottom-up"
    is_principal: bool              # exactly one true if GROUNDED
    similarity_score: float

source_chain:                       # only when extractable
  - source_level_label: "<source's own term>"
    mapped_ontology_level: "CO" | "Practice" | "Mechanism"
    candidate_concept: "<IRI>"
    similarity_score: float
    in_primary_slice: bool

diagnostics:
  top_down_slice: "ACO-XXX"
  top_down_item_level: "CO" | "Practice" | "Mechanism"
  source_default_level: "CO" | "Practice" | "Mechanism" | "mixed"
  classifier_chain_disagreement: bool
  chain_outliers: ["<IRI>", ...]
  best_alt_other_slice_anchor: "<IRI>" | null
  best_alt_other_slice_score: float | null
  best_alt_adjacent_level_anchor: "<IRI>" | null
  best_alt_adjacent_level_score: float | null
  oos_reason: "<rule>" | null
  lab_depth_reason: "<reason>" | null
```

---

## 9. Vocabulary

In all artefacts produced under this decision (briefs, audit outputs, paper prose), refer to:
- **"the normalization process"** / **"the algorithm"** — not "v5 / pipeline X / overlay system".
- **"the redesigned algorithm"** when distinguishing from prior attempts is necessary.
- **"chain-aware"**, **"level-aware"** as paper-prose technical descriptors.
- File paths and immutable tag names retain version codenames per Preservation Protocol; user-facing prose does not.

The three-paper baseline framing:
- Paper 1 — AppSec Core V0 (published).
- Paper 2 — proof of AppSec Core V0 on 5 ESI (published).
- Paper 3 — demonstration that the 26-ESI corpus normalizes via AppSec Core (this redesign delivers Paper 3 Phase 1 substrate).

---

## 10. Acceptance — one product, one gate (amended 2026-05-03)

There is one final product: the substrate that AppSec Core's SHACL declares conformant. The slice-coherence halt lifts when **all** of the following hold simultaneously on the same substrate:

1. **Model conformance (the imposed authority):** Archon's SHACL run reports zero violations of M1–M4 on the substrate. Non-zero indicates an algorithm error (anchor outside ontology-declared relations) or an ontology gap (a relation that should be asserted but isn't). Both are findable; both block conformance.
2. **Process integrity:** Cartographer's Pydantic schema validation passes; unit tests pass; inline assertions did not fire during the run. Non-zero indicates an algorithm bug, fixed in the algorithm code (not patched in the substrate).
3. Programme-lead + Orchestrator jointly declare the **acceptable attempt** based on (1) and (2).

The work toward this gate is iterative: each algorithm iteration produces a substrate; Archon validates; if SHACL declares non-conformance, Cartographer fixes the algorithm and emits a new substrate; iterate until conformance.

Once accepted, Paper 3's first stage (extend normalization to 26 ESI + cross-validate via SSDF/SCF triangulation) proceeds against the accepted substrate. Paper 3's second stage (Manual + KG iteration to Manual-frozen + KG-frozen) remains paused until the first stage closes.
