---
date: 2026-05-10
owner: Archon
type: closing-note (Phase D follow-on)
status: closed — awaiting programme-lead tag execution (ontology-v1.1-fair-baseline at Phase D commit)
predecessor: agentic/done/2026-05-10-p6-ontology-validation-phase-c-close.md
brief: agentic/briefs/2026-05-10-p6-ontology-validation-phase-a.md
authority: programme-lead Pedro Farinha 2026-05-10 ("se não impactar o que já está documentado, segue")
---

# P6 ontology validation — Phase D close (final hygiene quick-wins)

## Outcome

Phase D applied same day as Phase C, leveraging the not-yet-re-pinned Phase C SHAs to avoid double-cascade. **Final OOPS!: 0 Critical / 0 Important / 2 Minor (P04 + P22 documented intentional).** **Final FOOPS!-equivalent: 13/15 binary (PURL1 + OM3 doi remain publication-blocked / Cycle B external).** SHACL conformance preserved on both validators. Cartographer normalization unaffected.

## Why Phase D piggy-backed on Phase C

Phase C just shipped (`22ef625`) but Curator hadn't yet re-pinned downstream P6/P7/figshare with new SHAs. Adding the trivial quick-wins (P13 closure + P04 semantic improvement + logo + status) NOW means Curator does **one** re-pin pass against the FINAL state (Phase D SHAs), not two passes (Phase C then Phase D). Programme-lead authorisation explicit: "se não impactar o que já está documentado, segue" — and "documentado" refers to scientific record (papers cited, claims emitted, downstream consumers), not internal SHA-pins-pending-re-pin.

## Edits applied to `build_owl.py` (Phase D)

| Section | Fix | Result |
|---------|------|--------|
| Header `@prefix` declarations | Added `@prefix adms: <http://www.w3.org/ns/adms#>` | Enables `adms:status` declaration |
| Header `ac:AppSecCoreV1` ontology block | Added `foaf:depiction <https://securitybydesign.dev/assets/appsec-core-v1-logo.svg>` (placeholder URL — will resolve when namespace hosted) + `adms:status <http://purl.org/adms/status/Completed>` | FOOPS! OM3 sub-fields 3/6 → 5/6 (only DOI missing; binary check still all-or-nothing) |
| `ac:ControlledVocabularyValue` class declaration | Added `owl:disjointWith ac:AppSecCoreEntity` axiom | Semantic improvement (the grouping superclass is explicitly distinct from AppSec Core entities); OOPS! P04 still flags because analyzer requires instance-level relations, not class axioms |
| Controlled-vocab object properties (7) | Added `owl:inverseOf` link + emitted inverse property declaration for each: `hasObjectiveKind` ↔ `isObjectiveKindOf`, `hasObjectiveType` ↔ `isObjectiveTypeOf`, `hasPracticeFamily` ↔ `isPracticeFamilyOf`, `hasMechanismFamily` ↔ `isMechanismFamilyOf`, `hasCanonicalArtifactRole` ↔ `isCanonicalArtifactRoleOf`, `hasCanonicalEvidenceKind` ↔ `isCanonicalEvidenceKindOf`, `detectableInSurface` ↔ `surfaceOfDetectableEvidencePattern` | **OOPS! P13 closed 13→0** |

## Validation outcomes (Phase A → C → D progression)

| Validator | Phase A baseline | Post-Phase-C | Post-Phase-D |
|-----------|-----------------|--------------|--------------|
| OOPS! Critical | 0 | 0 | **0** |
| OOPS! Important | 1 (P11) | 0 | **0** |
| OOPS! Minor | 5 (P04+P08+P13+P20+P22) | 3 (P04+P13 partial+P22) | **2** (P04+P22) |
| FOOPS! binary | 5/15 (33%) | 13/15 (87%) | **13/15 (87%)** |
| FOOPS! OM3 sub-fields | 3/6 | 3/6 | **5/6** (publisher/source/issued + logo + status) |
| Bounded SHACL | conforms / 0 | conforms / 0 | **conforms / 0** |
| pyshacl 0.31.0 (composed v3) | conforms / 0 (data 1808) | conforms / 0 (data 1925) | **conforms / 0 (data 1970)** |

## Remaining items (Phase D final state)

| Item | Importance | Status | Path to closure |
|------|-----------|--------|-----------------|
| OOPS! P04 (ControlledVocabularyValue) | Minor | Documented design choice | Grouping superclass for 6 controlled-vocab subclasses; `owl:disjointWith` axiom added as semantic improvement; analyzer flag is conservative (requires instance-level relations); **acceptable as-is** |
| OOPS! P22 (mixed naming) | Minor | Documented design choice | snake_case mirrors YAML keys (schema-derived) ∩ camelCase mirrors RDF convention (OWL-generated); **acceptable as-is** unless programme-lead authorises mass-rename |
| FOOPS! PURL1 (persistent URL) | — | Cycle B external | Requires w3id.org redirect registration (community PR ~1-2 weeks); namespace IRI cascade affects all instance IRIs |
| FOOPS! OM3 binary (DOI) | — | Publication-blocked | DOI assigned at figshare/zenodo deposit; `dcterms:identifier <DOI>` added at publication time |

## Achievable post-publication state

| Validator | Achievable |
|-----------|------------|
| OOPS! | 0 Critical / 0 Important / 2 Minor (P04 + P22 documented intentional) |
| FOOPS! binary | **14/15** (if PURL1 deferred indefinitely) or **15/15** (if w3id.org redirect registered) |

For P6 paper §10.6 honest reporting, the defensible statement is:
> "AppSec Core V1 passes OOPS! with zero Critical and zero Important pitfalls; 2 Minor pitfalls remain as documented design choices (ControlledVocabularyValue grouping superclass; snake_case ∩ camelCase convention split mirroring source schema and RDF idioms). FOOPS! FAIR baseline scores 13/15 binary at v1.1-fair-baseline, with the 2 remaining checks (PURL1 persistent URL + OM3 DOI) gated on external prerequisites (w3id.org registration + publication deposit) that are scheduled for post-Cycle-A action."

## Impact reassessment (same as Phase C — zero downstream impact)

| Component | Impact of Phase D |
|-----------|-------------------|
| SHACL conformance | Zero violations added; bounded + pyshacl both conforms=True |
| Cartographer embeddings | Zero impact (.npz SHA `17f6aac4…` valid; YAML-driven corpus) |
| Cartographer grounding | Zero impact (entity set unchanged; IRIs unchanged) |
| Substrate v7 evidence | Zero impact (entity set + IRIs unchanged) |
| Apparatus-v3 composition | Shapes graph unchanged; only data graph SHA evolves |
| Papers P6 + P7 | Curator re-pin against final Phase D SHAs (single pass) |

## Final SHA-256 baselines (Phase D — for Curator re-pin)

| File | SHA-256 |
|------|---------|
| `formal/appsec_core/02-owl/exports/appsec-core-v0-bounded-v1.ttl` | `588598ff124582722bd4c31c0d9a09a6c9f74035d7940c31a7c4aac5cfead1bd` |
| `formal/appsec_core/02-owl/exports/alt-formats/appsec-core-v1.0.owl` | `f5c7441ff287f5bc50fbe75254509ad8a0b5fdc7eba65ecdeeb8dbde908bd1eb` |
| `formal/appsec_core/02-owl/exports/alt-formats/appsec-core-v1.0.jsonld` | `36df9b70090ec90dd5616a440124781feac2024362face891c4d5f026ef083bc` |
| `formal/appsec_core/02-owl/exports/alt-formats/appsec-core-v1.0.nt` | `7d08ce173d1f645c292121696e20665b065edcd4d277c132900dc17ef1f3fd06` |
| `formal/appsec_core/05-validation/reports/appsec-core-v0-shacl-validation-summary.json` | `44cea7b1c6ad8b7cf14154121a51c226e5b451ae25151b405e998c4a361041c7` |
| `formal/appsec_core/05-validation/reports/appsec-core-v1-pyshacl-summary.json` | `e92a3cfb7854110848ab10ab8da00bd780c3e6397f0360567298b5cb2ea80a93` |

## Tag proposal (revised)

`ontology-v1.1-fair-baseline` at the Phase D commit (not Phase C). FREEZE-REGISTRY item 15 updated to reflect Phase D as the final tag-eligible state. Optional `apparatus-shacl-pyshacl-v3.1` refresh on same commit (shapes graph unchanged; data graph SHA evolved).

## Asks (one line each)

1. Programme-lead: ratify Phase D commit + create `ontology-v1.1-fair-baseline` annotated tag at Phase D commit SHA.
2. Programme-lead: optional `apparatus-shacl-pyshacl-v3.1` tag (data graph evolved; shapes unchanged).
3. Curator: re-pin 6 SHA-256 baselines (table above) in P6 §3.1 + §6 + §10.6 + figshare MANIFEST.md — **single pass** against Phase D final state.
4. Curator: update P6 §10.6 with defensible final reporting (OOPS! 0/0/2 + FOOPS! 13/15 with 2 deferred to external/publication).

## References

- Phase A brief: `agentic/briefs/2026-05-10-p6-ontology-validation-phase-a.md`
- Phase C close: `agentic/done/2026-05-10-p6-ontology-validation-phase-c-close.md`
- Phase D close (this file)
- Phase D programme mirror: `sbd-ai-runtime/handover/em-curso/2026-05-10-archon-p6-ontology-validation-phase-d-close.md`
- Apparatus composition decision: `agentic/decisions/0001-consumer-conformance-shapes-ontology-owned.md`
