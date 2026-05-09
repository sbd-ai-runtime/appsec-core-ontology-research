# OLIR Conversion Methodology — substrate v7 → IR 8477 + IR 8278A r1 STRM

**Author:** Cartographer (Claude Opus 4.7)
**Authority:** programme-lead Pedro Farinha 2026-05-09 (Step 2 generation RATIFIED)
**Mini-dispatcher:** `2026-05-09-orchestrator-cartographer-olir-vocabulary-verification-and-generation.md`
**Substrate v7 SUPPLIER SHA-256:** `596783ed984d9c0e8c8ef6439a0eaee8fbaf2d863af37138cde8fad55d62be04`

## TL;DR

Substrate v7 claim-centric output (custom AppSec-Core-internal vocabulary) converted to **NIST IR 8477 relationship vocabulary + NIST IR 8278A r1 STRM resource model** via deterministic Python script. Outputs:

| Artefact | Formats | Count |
|---|---|---:|
| AppSec Core V1 OLIR Reference Document | XML + JSON | 1 (×2) |
| Per-source OLIR Concept Crosswalks | XML + JSON | 31 (×2) |
| OLIR validator report | Markdown + JSON | 1 (×2) |
| **Total** | | **66 files** |

**16,490 OLIR pairs emitted** across 31 sources (2,277 primary + 14,213 secondary). Self-structural validator passes 32/32 artefacts. External NIST OLIR validator pass deferred to future-work §13 (programme-lead authorization for external submission required).

## Source state vs target state

### Source: substrate v7 claim-centric schema (Decision 0003 Amendment 1)

- 22,534 typed entity instances in `v7-substrate-claims.ttl` (3,861 Items + 18,673 Claims; 202,178 RDF triples)
- Custom `ac:` namespace (`https://securitybydesign.dev/ontology/appsec-core/v1#`)
- Predicates: `ac:claim_id`, `ac:disambiguation_margin`, `ac:item_ref`, `ac:level`, `ac:lifted_row_ref`, `ac:similarity_score`, `ac:slice`, `ac:source`, `ac:source_object_id`, `ac:target_core_entity`
- Continuous similarity score per claim; multi-claim per source-item (1:N source-item → multiple targets at multiple ontology levels)

### Target: NIST IR 8477 + IR 8278A r1 STRM (OLIR-conformant)

- IR 8477 relationship vocabulary: 6 categorical relationship types (`subset-of` / `intersects-with` / `equal` / `not-related` / `superset-of` / `unspecified`)
- IR 8278A r1 STRM resource model: 4 resource types (`Concept` / `ConcreteImpl` / `ConceptualImpl` / `DocumentaryImpl`)
- Pair-relational: each (Source Document Element, Reference Document Element) row carries one categorical relationship type
- 1:1 or 1:few cardinality typical (NOT 1:N continuous-score multi-claim)

### Compatibility model

The two information models are **compatible but structurally different**: same conceptual mappings can be expressed in either format. Mechanical translation requires:

1. **Continuous → categorical translation:** map similarity scores to discrete relationship types via threshold
2. **Multi-claim → primary-pair-per-target:** select highest-similarity claim per (item, target) pair
3. **Resource type assignment:** map AppSec Core entity levels to STRM resource types
4. **Identifier convention:** map `ac:source` + `ac:source_object_id` → STRM `Document Identifier` + `Source Document Element ID`

## Schema decisions (RATIFIED VERBATIM by programme-lead 2026-05-09)

### Decision 1 — Continuous → categorical threshold

| Cosine similarity range | IR 8477 relationship-type |
|---|---|
| `sim ≥ 0.6` | `equal` |
| `0.4 ≤ sim < 0.6` | `intersects-with` |
| `sim < 0.4` | `unspecified` |

**Rationale:** The substrate's E2 admissibility threshold (calibrated empirically on cohort SSDF + CIS + SAMM + CWE; per-level percentile ~0.41) is the floor below which claims are considered too weak to ground. Mapping this floor to `unspecified` aligns with IR 8477 semantics ("relationship not determined"). The 0.6 threshold for `equal` is a methodologically conservative choice — high-confidence semantic equivalence at the scale where claim and target are unambiguously aligned.

**Empirical observation:** all 16,490 emitted OLIR pairs have similarity ≥ 0.4 (because LDP items with no claim ≥ 0.4 are excluded from OLIR exports — they would map to `unspecified` but produce no row). Distribution: `equal` 667 (4.0%) / `intersects-with` 15,823 (96.0%) / `unspecified` 0.

### Decision 2 — Multi-claim → primary-pair-per-target

For each substrate v7 GROUNDED item:
- **Per unique target Core entity:** emit one OLIR row using the highest-similarity claim for that (item, target) pair.
- **Primary marker (`is-primary="true"`):** the row whose target is the item's overall highest-similarity claim's target. One primary per item.
- **Secondary disclosure (`is-primary="false"`):** rows for other unique targets the item reaches.

**Rationale:** preserves the substrate's multi-claim signal (item reaches multiple targets at varying similarities) without inflating the OLIR row count to N×M (item × all-claims). Each unique (item, target) pair produces at most one OLIR row.

### Decision 3 — Relationship vocabulary subset (3 of 6 used)

| IR 8477 type | Used? | Rationale |
|---|:---:|---|
| `equal` | ✅ | sim ≥ 0.6 threshold |
| `intersects-with` | ✅ | 0.4 ≤ sim < 0.6 threshold |
| `unspecified` | ✅ | sim < 0.4 threshold (empirically unused; reserved for completeness) |
| `subset-of` | ❌ | Cosine similarity is undirected; cannot mechanically infer subset directionality. SME refinement future work (§13). |
| `superset-of` | ❌ | Same reason as `subset-of`. |
| `not-related` | ❌ | Implicit absence: items with no claim ≥ 0.4 to a target produce no row for that target. Not explicitly emitted as `not-related` rows. |

### Decision 4 — STRM resource model (IR 8278A r1)

| Substrate entity | STRM resource type |
|---|---|
| Pilot document (e.g., OWASP ASVS v5.0.0) | `DocumentaryImpl` |
| Source-item (e.g., ASVS-REQ-V1.1.1) | `ConcreteImpl` |
| AppSec Core V1 (the ontology) | Reference Document |
| Core entity (CO/Practice/Mechanism/Slice) | `Concept` |

### Decision 5 — Identifier convention

| STRM field | Source from substrate v7 |
|---|---|
| `Document Identifier` | pilot ID (e.g., `asvs_v5_0_0`) |
| `Source Document Element ID` | `ac:source_object_id` (e.g., `ASVS-REQ-V1.1.1`) |
| `Source Document Element Description` | first 200 chars of `source_text` |
| `Reference Document Element ID` | `ac:target_core_entity` (e.g., `ACP-IVF-001`) |
| `Reference Document Element Description` | first 200 chars of entity's augmented_text from AppSec Core V1 catalog |

## Aggregate stats

| Metric | Value |
|---|---:|
| OLIR pairs emitted (across 31 sources) | 16,490 |
| Primary pairs (one per item) | 2,277 |
| Secondary pairs | 14,213 |
| `equal` (sim ≥ 0.6) | 667 (4.04%) |
| `intersects-with` (0.4 ≤ sim < 0.6) | 15,823 (95.96%) |
| `unspecified` (sim < 0.4) | 0 (0.00%) |
| Reference Document Concepts | 212 (Slice 10 / CO 75 / Practice 69 / Mechanism 58) |
| Self-structural validator pass | 32/32 artefacts |

## Per-source pair counts (top 10 by volume)

| Pilot | items | grounded | OLIR pairs | primary | secondary | `equal` | `intersects-with` |
|---|---:|---:|---:|---:|---:|---:|---:|
| nist_sp800_53_rev5 | 1196 | 992 | 6,581 | 992 | 5,589 | 265 | 6,316 |
| pci_dss_v4_0_1 | 217 | 201 | 1,384 | 201 | 1,183 | 38 | 1,346 |
| capec_v3_9 | 559 | 355 | 1,342 | 355 | 987 | 45 | 1,297 |
| owasp_samm_v2_1 | 90 | 90 | 1,079 | 90 | 989 | 74 | 1,005 |
| asvs_v5_0_0 | 345 | 250 | 1,025 | 250 | 775 | 49 | 976 |
| cis_controls_v8_1_2 | 166 | 148 | 928 | 148 | 780 | 34 | 894 |
| owasp_dsomm | 193 | 170 | 808 | 170 | 638 | 48 | 760 |
| mitre_atlas | 278 | 180 | 592 | 180 | 412 | 4 | 588 |
| cwe_software_development_view_v4_19_1 | 399 | 152 | 582 | 152 | 430 | 20 | 562 |
| ssdf_sp800_218_v1_1 | 61 | 56 | 415 | 56 | 359 | 18 | 397 |

Full per-pilot table at `data/p7_olir_audit/p7_v2_corrected/v7/olir_exports/olir_validator_report.md`.

## External validator caveat

External NIST OLIR validators (per https://csrc.nist.gov/projects/olir) **NOT invoked at generation time**. Reasons:
- External submission validators may not be publicly accessible without programme-lead authorization
- NIST CRWS peer submission + OLIR registration are explicitly programme-lead-authority + scoped as future work (§13)

**Self-structural validator** runs at generation: tests namespace declarations, metadata blocks, STRM resource type usage, ratified relationship vocabulary subset. 32/32 artefacts pass.

Programme-lead may commission external OLIR submission review separately as part of OLIR registration future work.

## Generator script

- **Path:** `scripts/olir/generate_olir_exports.py`
- **Determinism:** byte-identical re-emission against same SUPPLIER + AppSec Core entity catalog. No model API calls; no LLM invocations during generation.
- **Run:** `python3 -m scripts.olir.generate_olir_exports`
- **Inputs:** substrate v7 SUPPLIER + ontology v1.1 augmented-text-corpus
- **Outputs:** 66 files in `data/p7_olir_audit/p7_v2_corrected/v7/olir_exports/`

## Future work (§13)

Out of scope for this generation per dispatcher §"Out of scope":

1. **SME review of individual mappings + κ inter-rater reliability** — would refine the `equal` / `intersects-with` boundary case-by-case beyond threshold heuristic.
2. **NIST CRWS peer submission** — formal external review of OLIR submission package.
3. **OLIR registration via NIST OLIR Submission Tool** — official programme submission, requires programme-lead authorization.
4. **subset-of / superset-of vocabulary extension** — requires directional information beyond cosine similarity (e.g., per-claim explicit hierarchy markers).
5. **External NIST OLIR validator pass** — when programme-lead authorizes external submission.
6. **Per-pilot SME refinement of source descriptions** — current source descriptions are first 200 chars of source_text; SME-curated abstracts would improve OLIR submission quality.

## Programme integration

- **P7 §Contribution 4:** wording stays verbatim per dispatcher §"Pedro continues P7 review in parallel". The factual claim is now backed by deliverable artefacts.
- **Phase A figshare bundle:** absorbs OLIR exports as substantial deliverable (66 files). Curator integrates into MANIFEST.md.
- **LLM-assist provenance:** generator script authored by Cartographer (Claude Opus 4.7); generation step is 100% deterministic Python. Provenance documented per existing `llm_assist_provenance_v7_addendum.md` discipline (Phase 7.3 already covers script-authoring).

## Cross-references

- Mini-dispatcher (Step 2 RATIFIED): `sbd-ai-runtime/handover/em-curso/2026-05-09-orchestrator-cartographer-olir-vocabulary-verification-and-generation.md`
- Step 1 verification (Cartographer's NOT-compliant verdict): `agentic/em-curso/2026-05-09-olir-vocabulary-verification.md`
- OLIR exports artefacts: `data/p7_olir_audit/p7_v2_corrected/v7/olir_exports/`
  - `appsec_core_v1_reference_doc.{xml,json}` (Reference Document)
  - `concept_crosswalk_<pilot>.{xml,json}` × 31 (per-source crosswalks)
  - `olir_validator_report.{md,json}` (self-validation results)
- Generator: `scripts/olir/generate_olir_exports.py`
- Substrate v7 SUPPLIER (input): `data/p7_olir_audit/p7_v2_corrected/v7/SUPPLIER_v7_0.json` (SHA `596783ed...62be04`)
- AppSec Core V1 entity catalog (input): `sbd-toe-ontology/formal/appsec_core/08-embeddings/augmented-text-corpus.json`
- NIST OLIR program: https://csrc.nist.gov/projects/olir
- IR 8477: "Mapping Relationships Between Documentary Standards, Regulations, Frameworks, and Reference Materials"
- IR 8278A r1: "National Online Informative References (OLIR) Program: Submission Guidance for OLIR Developers"
