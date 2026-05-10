---
date: 2026-05-10
owner: Archon
type: closing-note (Phase C completion)
status: closed — awaiting programme-lead tag execution (ontology-v1.1-fair-baseline)
predecessor: agentic/em-curso/2026-05-10-p6-ontology-validation-phase-a.md (Phase A)
brief: agentic/briefs/2026-05-10-p6-ontology-validation-phase-a.md
authority: programme-lead Pedro Farinha 2026-05-10 (direct authorisation — "sim, confirmo" for Phase C scope + tag name `ontology-v1.1-fair-baseline`)
---

# P6 ontology validation — Phase C close

## Outcome

Phase C batched fix applied. **OOPS! 0/1/5 → 0/0/3.** **FOOPS!-equivalent 5/15 → 13/15 (87%).** SHACL conformance preserved on both validators. Cartographer normalization unaffected.

## Edits applied to `build_owl.py`

| Section | Fix | Result |
|---------|------|--------|
| Header (`@prefix` + `ac:AppSecCoreV1` block) | Added cc/foaf/vann prefixes + dcterms:title/description/license/rights/creator/publisher/created/issued/modified/bibliographicCitation, owl:versionIRI, vann:preferredNamespacePrefix/Uri | FOOPS! OM1+OM2+OM4.1+OM4.2+OM5.1+OM5.2+VER1 (7 checks) lifted |
| `_entity_comments()` function | Added `ENTITY_COMMENT_OVERRIDES` for natural-language descriptions of 5 first-class entity classes (ControlObjective/Practice/Mechanism/Artifact/EvidencePattern); fallback humanizes snake_case `role` | OOPS! P20 closed (2 elements) |
| Schema-derived datatype properties loop | Pre-compute `field_to_entities` map; emit `rdfs:domain` per property (single owner → specific entity; shared field → `ac:AppSecCoreEntity`); add `rdfs:comment` from `field_descriptions` table | OOPS! P11 Important closed (14 elements); P08 Minor partial; FOOPS! VOC4 lifted |
| Controlled-vocab subclasses (ObjectiveKind/Type/ArtifactRole/PracticeFamily/MechanismFamily/DetectableSurface) | Added `rdfs:comment` per subclass | OOPS! P08 Minor partial; FOOPS! VOC4 contribution |
| Controlled-vocab object properties (hasObjectiveKind/Type/PracticeFamily/MechanismFamily/CanonicalArtifactRole/CanonicalEvidenceKind/detectableInSurface) | Added `rdfs:comment` per property | OOPS! P08 Minor partial |
| `belongsToSlice` | Added `rdfs:comment` + `owl:inverseOf ac:hasMember` + emitted `ac:hasMember` inverse property | OOPS! P13 partial; P08 partial |
| Stable cross-entity relations (5: objective_realized_by_practice / implemented_by_mechanism / expects_artifact / verified_by_evidence_pattern + artifact_supports_evidence_pattern) | Added `rdfs:comment` + `owl:inverseOf` + emitted 5 inverse property declarations (practice_realizes_objective / mechanism_implements_objective / artifact_supports_objective / evidence_pattern_verifies_objective / evidence_pattern_supported_by_artifact) | OOPS! P13 reduced 13→7; P08 closed |
| Slice datatype properties (slice_id/scope_key/objective_family_code/current_control_mode/contract_path) | Added `rdfs:comment` per property | OOPS! P08 closed (final batch) |

## Validation outcomes post-fix

| Validator | Pre-Phase-C | Post-Phase-C |
|-----------|-------------|--------------|
| OOPS! | 0 Critical / 1 Important / 5 Minor | **0 Critical / 0 Important / 3 Minor** |
| FOOPS!-equivalent | 5/15 (33%) | **13/15 (87%)** |
| Bounded SHACL validator | conforms=True / 0 violations | **conforms=True / 0 violations** (unchanged) |
| pyshacl 0.31.0 (composed apparatus-v3) | conforms=True / 0 violations (data 1808 / shapes 396) | **conforms=True / 0 violations (data 1925 / shapes 396)** |

### Remaining pitfalls/gaps (documented as intentional or deferred to Cycle B)

| Item | Importance | Status | Disposition |
|------|------------|--------|-------------|
| OOPS! P04 (ControlledVocabularyValue unconnected) | Minor | Intentional design | Grouping superclass for 6 controlled-vocab subclasses; documented |
| OOPS! P13 partial (7 controlled-vocab object properties without inverses) | Minor | Deferred | Optional Cycle B; 5 stable relations already covered |
| OOPS! P22 (mixed naming convention) | Minor | Documented | snake_case ∩ camelCase is deliberate convention split (schema-derived vs OWL-generated) |
| FOOPS! PURL1 (persistent URL) | — | Deferred | Cycle B: w3id.org/sbd-toe/appsec-core redirect registration |
| FOOPS! OM3 (doi/logo/status) | — | Post-publication | DOI assigned at figshare deposit; logo + status not ontology-side |

## Impact assessment (answer to Pedro's two questions)

### Q: SHACL impact?

**Zero violations added.** Both validators continue `conforms=True / 0 violations`. CO→P/M minCount 1 invariant preserved.

Data graph triple count grew **1808 → 1925 triples (+117 triples)**. New triples are:
- Ontology header metadata (~14 dcterms/vann/owl declarations)
- `rdfs:domain` on 14 datatype properties (14 triples)
- `rdfs:comment` on 38 properties (38 triples)
- `owl:inverseOf` on 5 stable relations + `belongsToSlice` (6 triples)
- 5 new inverse property declarations (5 × 5 = 25 triples for each: rdf:type/label/comment/domain/range)
- `hasMember` inverse property (5 triples)
- `rdfs:comment` on 6 controlled-vocab subclasses (6 triples)

Shapes graph unchanged (396 triples).

### Q: Cartographer normalization impact?

**Zero impact on normalization output.** Verified:

| Cartographer component | Depends on OWL header/axioms? | Impact |
|------------------------|:-----------------------------:|--------|
| AppSec Core embeddings .npz | ❌ — `augmentation-rule.yaml` v1.0 driven by YAML | None; SHA `17f6aac4…` still valid |
| Source-side embeddings (ASVS/CWE/CAPEC/MCP/DSOMM) | ❌ | None |
| Grounding similarity (top-1 votes / CID clustering) | ❌ — uses embeddings + IRIs | None |
| IRI scheme (`ac:ACO_IVF_008` etc.) | — | Unchanged |
| Claim emission | ❌ — uses AppSec Core IRIs as `target_core_entity` | Unchanged |
| Apparatus-v3 SHACL validation of substrate v7 claims | Yes — uses OWL TTL as `ont_graph` for `sh:sparql` visibility | New TTL SHA; logic unchanged; outcome still conforms=True / 0 violations |

Substrate v7 grounding evidence stays valid because entity set (5 first-class entities + 75/69/58/57 instance counts + IRIs) is unchanged.

Cartographer optional follow-up: substrate v8 re-grounding for clean lineage. Cycle B.

## Sprint commits (this session)

Currently at HEAD `41cc09f` (Phase A pushed); Phase C edits staged, pending commit:

| Stage | Files |
|-------|-------|
| Phase A (already pushed `41cc09f`) | brief + em-curso |
| Phase C (current commit) | `build_owl.py` + TTL + 3 alt-formats + 2 validation summaries + CHANGELOG + FREEZE-REGISTRY + closing notes (this file + programme mirror) |

## New SHA-256 baselines

| File | Pre-Phase-C | Post-Phase-C |
|------|-------------|--------------|
| `formal/appsec_core/02-owl/exports/appsec-core-v0-bounded-v1.ttl` | `89b4ac1f1eb687ce92bc22526a430f0a5671ef7c1f4bb9c55a4d2f211a5aaf3b` | `29329daf8a632ce0a98ab462c89343f710970489b8636add294de06ab1d90c8c` |
| `formal/appsec_core/02-owl/exports/alt-formats/appsec-core-v1.0.owl` | (prior) | `50c6d773f4424de74f24859e263794a2748a4b3f6d7f75e645be3b67216b72bb` |
| `formal/appsec_core/02-owl/exports/alt-formats/appsec-core-v1.0.jsonld` | (prior) | `1af2fd6407baf3b78d69cb8ada32758184ddd0b8e67e4f2424f815b554609500` |
| `formal/appsec_core/02-owl/exports/alt-formats/appsec-core-v1.0.nt` | (prior) | `86232afeeb55fa13fe470c045b076a223a9906db7014a8b440d04199f2c35f85` |
| `formal/appsec_core/05-validation/reports/appsec-core-v0-shacl-validation-summary.json` | (prior) | `42fdef6272ea77b3e0982cffc7ee2eadb5cdddf7a83f05d5a9e3a5a877fba39f` |
| `formal/appsec_core/05-validation/reports/appsec-core-v1-pyshacl-summary.json` | (prior) | `1b19007f057c5455041e1e2925bd566cbea393a064c414a47fa7067e5595c884` |

## Tag proposal

`ontology-v1.1-fair-baseline` at the Phase C commit. Successor to `ontology-v1-final` (`b267cf3`) for v1 line. Entity set unchanged (75 CO / 69 P / 58 M / 57 A = 259); only metadata + schema annotations changed. ACR-001/002/004 promotion claims unchanged.

Optional: `apparatus-shacl-pyshacl-v3.1` refresh on same commit (shapes graph unchanged; data graph SHA changed). Programme-lead discretion.

## Asks (one line each)

1. Programme-lead: ratify Phase C commit + create `ontology-v1.1-fair-baseline` tag.
2. Curator: re-pin SHA-256 references in P6 §3.1 + §6 + §10.6 + figshare-deposit MANIFEST.md with new baselines (table above).
3. Orchestrator: optionally dispatch Cartographer for substrate v8 re-grounding (clean lineage; not blocking).
4. Orchestrator: confirm Curator polish Bloco 2/3 can now incorporate post-fix validation results (OOPS! 0/0/3 + FOOPS! 13/15).

## References

- Phase A brief: `agentic/briefs/2026-05-10-p6-ontology-validation-phase-a.md`
- Phase A em-curso: `agentic/em-curso/2026-05-10-p6-ontology-validation-phase-a.md`
- Phase A close mirror: `sbd-ai-runtime/handover/em-curso/2026-05-10-archon-p6-ontology-validation-phase-a-delivery.md`
- Phase C programme mirror: `sbd-ai-runtime/handover/em-curso/2026-05-10-archon-p6-ontology-validation-phase-c-close.md`
- Architectural baseline (apparatus-v3 composition): `agentic/decisions/0001-consumer-conformance-shapes-ontology-owned.md`
- Pre-fix commit anchors: `ontology-v1-final` (`b267cf3`) + `cycle-a-frozen-2026-05-08` (`6006e80`)
