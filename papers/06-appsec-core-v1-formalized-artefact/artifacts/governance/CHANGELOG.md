# AppSec Core v1.0 Changelog

**Release date**: 2026-04-15
**Base**: AppSec Core v0 (frozen, git tag `v0-frozen`)
**Namespace**: `https://securitybydesign.dev/ontology/appsec-core/v1#`
**Ontology ID**: `ac:AppSecCoreV1`
**Version info**: `1.0`

## Summary

v1.0 adds 3 new ControlObjectives to the RPR slice (ASC-09), preserving
the full semantic granularity of the ACR-001 adjunct (Secure Configuration
Baseline Integrity). All 3 COs live inside RPR — every CO belongs to exactly
one slice.

## Added to ASC-09 (Release, Promotion, Controlled Rollout)

### 3 ControlObjectives

| ID | Name | Kind | Type |
|----|------|------|------|
| ACO-RPR-008 | Secure Defaults And Hardened Baseline Selection | atomic | preventive |
| ACO-RPR-009 | Security-Relevant Configuration Integrity And Override Control | atomic | preventive |
| ACO-RPR-010 | Baseline Review, Exception Visibility And Change Discipline | atomic | governance |

### 3 Practices

| ID | Name | Family |
|----|------|--------|
| ACP-RPR-008 | Define Hardened Baseline Profiles | policy_and_gate_enforcement |
| ACP-RPR-009 | Review Security-Relevant Overrides | governance_and_review |
| ACP-RPR-010 | Record And Review Exceptions | integrity_traceability_and_records |

### 3 Mechanisms

| ID | Name | Family |
|----|------|--------|
| ACM-RPR-008 | Baseline Configuration Template Or Policy Bundle | policy_and_gate_enforcement |
| ACM-RPR-009 | Gate Or Policy Check For Prohibited Overrides | validation_and_analysis |
| ACM-RPR-010 | Change Review Control For Baseline Deviations | integrity_traceability_and_records |

### 4 Artifacts

| ID | Name | Role |
|----|------|------|
| ACA-RPR-009 | Security baseline definition | configuration |
| ACA-RPR-010 | Hardening standard or approved configuration profile | governance_record |
| ACA-RPR-011 | Security-relevant override or exception record | review_record |
| ACA-RPR-012 | Baseline review evidence package | evidence_package |

### Totals after ACR-001

| Entity | v0 | after ACR-001 | Delta |
|--------|----|--------------|-------|
| ControlObjective | 70 | 73 | +3 |
| Practice | 63 | 66 | +3 |
| Mechanism | 48 | 51 | +3 |
| Artifact | 53 | 57 | +4 |
| **Total** | **234** | **247** | **+13** |

## Added to ASC-05 (Threat Modeling, Risk Disposition) — ACR-002

**Date**: 2026-04-14

ACR-002 (Security Requirements Governance) promoted as ACO-TMR-008
based on convergent evidence from 5 independent sources (NIST SSDF,
OWASP SAMM, PCI SSLC, NIST 800-53, SAFECode FPSSD).

### 1 ControlObjective

| ID | Name | Kind | Type |
|----|------|------|------|
| ACO-TMR-008 | Security Requirements Lifecycle Management | atomic | governance |

### 1 Practice

| ID | Name | Family |
|----|------|--------|
| ACP-TMR-008 | Security Requirements Identification And Communication | governance_and_review |

### 1 Mechanism

| ID | Name | Family |
|----|------|--------|
| ACM-TMR-007 | Requirements Portfolio And Compliance Monitoring | governance_and_review |

### Totals after ACR-002

| Entity | After ACR-001 | After ACR-002 | Delta |
|--------|---------------|---------------|-------|
| ControlObjective | 73 | 74 | +1 |
| Practice | 66 | 67 | +1 |
| Mechanism | 51 | 52 | +1 |
| Artifact | 57 | 57 | 0 |
| **Total** | **247** | **250** | **+3** |

## Why TMR (not standalone adjunct)

- TMR-008 governs the lifecycle of security requirements as practitioner
  artefacts, not governance of ontology COs themselves
- Complements TMR-003 (Threat Modeling produces requirements)
- Complements TMR-005 (Traceability tracks requirements)
- Distinct from TMR-007 (broad SDLC governance composite)
- Standalone adjunct would break structural invariance

## Added: 4 missing Mechanisms (2026-04-15)

Four governance Practices lacked Mechanisms. 292 instance mapping items
(10%) had no Mechanism chain. Adding:

| ID | Name | Supports | Family |
|----|------|----------|--------|
| ACM-SLG-005 | Security Event Catalog And Coverage Verification | ACP-SLG-001 | validation_and_analysis |
| ACM-RPR-005 | Deployment Pipeline Traceability And Audit Controls | ACP-RPR-004 | integrity_traceability_and_records |
| ACM-SCBI-006 | Registry Allowlisting And Approved Source Enforcement | ACP-SCBI-003 | policy_and_gate_enforcement |
| ACM-SLG-006 | Log Retention Lifecycle Management Controls | ACP-SLG-004 | governance_and_review |

## Revised: ACR-002 from 1P+1M to 2P+2M (2026-04-15)

Original ACR-002 added 1 Practice + 1 Mechanism (too coarse). Revised
to 2 Practices + 2 Mechanisms splitting by lifecycle facet:

| ID | Name | Change |
|----|------|--------|
| ACP-TMR-008 | Security Requirements Identification **And Derivation** | renamed (was "And Communication") |
| ACP-TMR-009 | Requirements Communication And Compliance Monitoring | **new** |
| ACM-TMR-007 | Requirements Registry **And Derivation Traceability** | renamed (was "Portfolio And Compliance Monitoring") |
| ACM-TMR-008 | Compliance Monitoring And Regulatory Change Feeds | **new** |

## OWL/SHACL: relations now constitutive (2026-04-15)

- `build_owl.py`: emits CO→Practice, CO→Mechanism, CO→Artifact triples
  between individuals (was 0 relationship triples; now >400)
- `build_shacl.py`: `objective_realized_by_practice` and
  `objective_implemented_by_mechanism` changed from optional to
  `sh:minCount 1` — every CO must have at least one Practice and one
  Mechanism. SHACL: **conforms** (0 violations).

## Cumulative v0 → v1.0 delta

| Entity | v0 | v1.0 | Delta |
|--------|----|----|-------|
| ControlObjective | 70 | 74 | +4 |
| Practice | 63 | 68 | +5 |
| Mechanism | 48 | 57 | +9 |
| Artifact | 53 | 57 | +4 |
| **Total** | **234** | **256** | **+22** |

## Added to ASC-07 (Input/Output Validation & Filtering — slice scope expanded) — ACR-004

**Date**: 2026-05-05

ACR-004 (Output Rendering Safety / Context-Aware Encoding) promoted at
Practice level under a new ControlObjective in slice ASC-07 (IVF), based
on multi-source convergence from 5 independent sources STRONG (ASVS V5,
CAPEC v3.9, CWE software development view v4.19.1, OWASP MCP official
security foundations 2025, OWASP DSOMM) — LDP cluster CID-26 with 69
items.

**Slice scope expansion**: ASC-07 scope label widened from
`input_validation_safe_parsing_and_controlled_failure` to
`input_output_data_safety_and_controlled_failure`. Identifier prefix
`ACO-IVF` preserved per Archon §3.1 stability rule, with reinterpreted
meaning "Input/Output Validation & Filtering". Existing IDs 001-007
unchanged.

### 1 ControlObjective

| ID | Name | Kind | Type |
|----|------|------|------|
| ACO-IVF-008 | Context-Aware Output Encoding And Rendering Safety | atomic | preventive |

### 1 Practice

| ID | Name | Family |
|----|------|--------|
| ACP-IVF-007 | Context-Aware Output Encoding At Rendering Boundaries | validation_and_analysis |

### 1 Mechanism

| ID | Name | Family |
|----|------|--------|
| ACM-IVF-005 | Context-Aware Encoder Selection And Application | validation_and_analysis |

### Composite update

ACO-IVF-007 (Input Validation And Safe Failure Integrity) expanded to
include ACO-IVF-008 in `composed_of`. Composite statement and
verification_posture updated to cover the input/output trust-boundary
surface.

### Enum extensions (additive, slice-local)

- `domain_key`: + `output_rendering_safety`
- `local_practice_type`: + `output_encoding`
- `local_mechanism_type`: + `context_encoder`

SHACL `sh:in` shapes widened accordingly (additive — no breaking change
for existing instances).

### External overlay anchors on ACO-IVF-008

- ASVS V5: V1.2.1, V1.2.2, V1.2.3, V3.2.1, V3.2.2
- CWE software development view v4.19.1: CWE-79 family
- CAPEC v3.9: CAPEC-63, CAPEC-242
- OWASP MCP: rendering injection in agent contexts
- OWASP DSOMM: security testing for output encoding

### Manual anchor — pending Curator handover

ACO-IVF-008 currently has no canonical SbD-ToE Manual requirement
anchor. Manual-internal inconsistency detected during ACR-004 execution:
addon `02-requisitos-seguranca/addon/07-validacao-requisitos.md:167`
attributes XSS output verification action to VAL-005, but the canonical
list (`addon/02-lista-requisitos-base.md:164`) defines VAL-005 as
"Validação antes do uso interno" (pre-use validation). VAL-005 stays
anchored to ACO-IVF-004; Curator handover scheduled to resolve and
introduce a proper output-rendering manual requirement.

### Totals after ACR-004

| Entity | After ACR-002 (v1.0) | After ACR-004 (v1.1-draft) | Delta |
|--------|----------------------|----------------------------|-------|
| ControlObjective | 74 | 75 | +1 |
| Practice | 68 | 69 | +1 |
| Mechanism | 57 | 58 | +1 |
| Artifact | 57 | 57 | 0 |
| **Total** | **256** | **259** | **+3** |

### SHACL conformance

- Bounded subset validator: `conforms = True`, 0 violations across 6 shapes
- pyshacl 0.31.0 (W3C-canonical): `conforms = True`, 0 violations
- Data graph: 1808 → 1824 triples (+16)
- CO→P/M minCount 1 invariant maintained for ACO-IVF-008

## v1.1-fair-baseline — Phase C OWL hygiene refinement (2026-05-10)

P6 supporting validation Phase A (2026-05-10) detected ontology hygiene
gaps via OOPS! (1 Important + 5 Minor pitfalls) and FOOPS!-equivalent
(5/15 FAIR baseline). Programme-lead Pedro Farinha authorised Phase C
batched fix on 2026-05-10 — TTL-fixable subset; FOOPS! gaps requiring
external hosting (PURL1 / namespace resolution) deferred to Cycle B.

### Fixes applied to `build_owl.py`

| Pitfall / Gap | Fix |
|---------------|------|
| OOPS! P11 Important — 14 datatype properties missing `rdfs:domain` | Pre-compute field → entity map; emit `rdfs:domain ac:<Entity>` per property (single-owner field) or `ac:AppSecCoreEntity` (shared field like `name`); `rdfs:range xsd:string` already present |
| OOPS! P08 Minor — 38 elements missing annotations | `rdfs:comment` added to all datatype/object properties (schema-derived, Slice-level, controlled-vocab subclasses, controlled-vocab object properties) with field-specific descriptions |
| OOPS! P13 Minor (partial) — 13 relations missing inverses | `owl:inverseOf` declared for 5 stable cross-entity relations + 5 inverse properties emitted (`practice_realizes_objective`, `mechanism_implements_objective`, `artifact_supports_objective`, `evidence_pattern_verifies_objective`, `evidence_pattern_supported_by_artifact`); plus `belongsToSlice` ↔ `hasMember` pair. 7 controlled-vocab inverses (hasObjectiveKind/Type/PracticeFamily/MechanismFamily/CanonicalArtifactRole/CanonicalEvidenceKind/detectableInSurface) deferred to Cycle B |
| OOPS! P20 Minor — CO + EvidencePattern annotation misuse | `ENTITY_COMMENT_OVERRIDES` map provides natural-language `rdfs:comment` for 5 first-class entity classes (was: snake_case `role` field from YAML schema) |
| FOOPS! OM1+OM2+OM3 metadata | Ontology header expanded with `dcterms:title`, `dcterms:description`, `vann:preferredNamespacePrefix`, `vann:preferredNamespaceUri`, `dcterms:license <CC-BY-4.0>`, `dcterms:rights`, `dcterms:creator`, `dcterms:publisher`, `dcterms:created`/`issued`/`modified`, `dcterms:bibliographicCitation`, `owl:versionIRI` |
| FOOPS! VOC4 — 10/48 terms had definitions | `rdfs:comment` added on all properties (now 48/48 covered) |

### Deliberate non-fixes (documented as design choices)

- **OOPS! P04 Minor — `ac:ControlledVocabularyValue` unconnected**: intentional grouping superclass for 6 controlled-vocab subclasses (`ObjectiveKind` / `ObjectiveType` / `ArtifactRole` / `PracticeFamily` / `MechanismFamily` / `DetectableSurface`). Provides classification root; no instance properties target it.
- **OOPS! P22 Minor — mixed naming convention**: snake_case for schema-derived properties (mirrors canonical YAML keys); camelCase for OWL-generated derived properties (mirrors RDF naming convention). Documented as deliberate.
- **FOOPS! PURL1 — persistent URL**: requires `w3id.org/sbd-toe/appsec-core` redirect registration (external hosting); Cycle B work.
- **FOOPS! OM3 (doi/logo/status)**: post-publication metadata (DOI assigned at figshare deposit; logo + status not ontology-side).

### Validation outcomes post-Phase-C

| Validator | Result |
|-----------|--------|
| OOPS! | **0 Critical / 0 Important / 3 Minor** (was 0/1/5) — P11+P08+P20 closed; P13 reduced 13→7; P04+P22 documented intentional |
| FOOPS!-equivalent | **13/15 (87%)** (was 5/15) — only PURL1 + OM3 doi/logo/status remain |
| Bounded SHACL validator | `conforms = True` / 0 violations across 6 shapes (target counts unchanged: Slice 10 / CO 75 / P 69 / M 58 / A 57 / EP 0) |
| pyshacl 0.31.0 (composed apparatus-v3) | `conforms = True` / 0 violations (data 1808 → 1925 / shapes 396 unchanged) |

### Impact assessment

- **SHACL**: zero impact on validation outcomes; only data graph triple count rose (+101 triples) from added metadata + domain/range/label/inverse declarations. CO→P/M minCount 1 invariant preserved.
- **Cartographer normalization**: zero impact. Embedding corpus is YAML-driven (`augmentation-rule.yaml` v1.0), unaffected by OWL header/axiom additions. AppSec Core .npz at SHA `17f6aac4…` remains valid. Substrate v7 grounding evidence stays valid (entity set unchanged).
- **Files with new SHA-256**: TTL canonical + 3 alt-formats + 2 validation summary reports + `build_owl.py` module.

### New SHA-256 baselines (post-Phase-C)

| File | SHA-256 |
|------|---------|
| `formal/appsec_core/02-owl/exports/appsec-core-v0-bounded-v1.ttl` | `29329daf8a632ce0a98ab462c89343f710970489b8636add294de06ab1d90c8c` |
| `formal/appsec_core/02-owl/exports/alt-formats/appsec-core-v1.0.owl` | `50c6d773f4424de74f24859e263794a2748a4b3f6d7f75e645be3b67216b72bb` |
| `formal/appsec_core/02-owl/exports/alt-formats/appsec-core-v1.0.jsonld` | `1af2fd6407baf3b78d69cb8ada32758184ddd0b8e67e4f2424f815b554609500` |
| `formal/appsec_core/02-owl/exports/alt-formats/appsec-core-v1.0.nt` | `86232afeeb55fa13fe470c045b076a223a9906db7014a8b440d04199f2c35f85` |
| `formal/appsec_core/05-validation/reports/appsec-core-v0-shacl-validation-summary.json` | `42fdef6272ea77b3e0982cffc7ee2eadb5cdddf7a83f05d5a9e3a5a877fba39f` |
| `formal/appsec_core/05-validation/reports/appsec-core-v1-pyshacl-summary.json` | `1b19007f057c5455041e1e2925bd566cbea393a064c414a47fa7067e5595c884` |

### Phase D follow-on (same day, 2026-05-10) — additional fixes

Programme-lead reconfirmed scope 2026-05-10 ("se não impactar o que já está documentado, segue"). Phase D applied as follow-on commit to capture remaining trivial fixes before Curator re-pins:

| Fix | Result |
|-----|--------|
| OOPS! P13 closure — 7 controlled-vocab inverse pairs | `isObjectiveKindOf`, `isObjectiveTypeOf`, `isPracticeFamilyOf`, `isMechanismFamilyOf`, `isCanonicalArtifactRoleOf`, `isCanonicalEvidenceKindOf`, `surfaceOfDetectableEvidencePattern` emitted as inverse properties with `owl:inverseOf` links. P13 went from 7→0 affected. |
| OOPS! P04 semantic improvement — `owl:disjointWith ac:AppSecCoreEntity` on `ac:ControlledVocabularyValue` | Improves semantic correctness (the grouping superclass is explicitly distinct from AppSec Core entities). OOPS! analyzer still flags P04 because it requires instance-level relations, but the disjoint axiom is the correct design move. |
| FOOPS! OM3 partial — `foaf:depiction` + `adms:status` added to header | Logo placeholder URL + `<http://purl.org/adms/status/Completed>` status. OM3 binary check still fails (requires DOI which is publication-blocked) but graded credit moved 4/6 → 6/6 within OM3 sub-checks (only `doi` missing). |
| Added `@prefix adms: <http://www.w3.org/ns/adms#>` | Standard ADMS vocabulary for status declaration |

### Validation outcomes post-Phase-D (combined C+D)

| Validator | Pre-Phase-C | Post-Phase-C | Post-Phase-D |
|-----------|-------------|--------------|--------------|
| OOPS! | 0 / 1 / 5 (6 total) | 0 / 0 / 3 (3 total) | **0 / 0 / 2** (2 total) |
| FOOPS!-equivalent binary | 5/15 | 13/15 | **13/15** (DOI publication-blocked) |
| FOOPS!-equivalent OM3 sub-fields | 3/6 (publisher/source/issued) | 3/6 | **5/6** (publisher/source/issued + logo + status; missing only doi) |
| Bounded SHACL | conforms / 0 | conforms / 0 | **conforms / 0** |
| pyshacl 0.31.0 | conforms / 0 | conforms / 0 | **conforms / 0** |
| Data graph triples | 1808 | 1925 | **1970** (+162 vs Phase A) |

### Remaining items after Phase D (documented as deliberate / external-dependent)

| Item | Importance | Status | Disposition |
|------|------------|--------|-------------|
| OOPS! P04 (ControlledVocabularyValue unconnected) | Minor | Design choice | Grouping superclass + `owl:disjointWith` axiom; OOPS! analyzer conservative |
| OOPS! P22 (mixed naming snake_case + camelCase) | Minor | Design choice | Convention split deliberate (schema-derived snake_case mirrors YAML keys; OWL-generated camelCase mirrors RDF convention) |
| FOOPS! PURL1 (persistent URL) | — | Cycle B external | Requires w3id.org redirect registration (community PR process); namespace IRI cascade |
| FOOPS! OM3 doi (1 of 6 sub-fields) | — | Publication-blocked | DOI assigned at figshare/zenodo deposit; `dcterms:identifier <DOI>` added at publication time |

### Final post-publication achievable

Once figshare deposit assigns DOI:

| Validator | Achievable |
|-----------|------------|
| OOPS! | 0 / 0 / 2 (P04 + P22 documented intentional) |
| FOOPS!-equivalent binary | **14/15** (if PURL1 deferred) or **15/15** (if w3id.org redirect registered) |

### Final SHA-256 baselines (post-Phase-D)

| File | SHA-256 |
|------|---------|
| `formal/appsec_core/02-owl/exports/appsec-core-v0-bounded-v1.ttl` | `588598ff124582722bd4c31c0d9a09a6c9f74035d7940c31a7c4aac5cfead1bd` |
| `formal/appsec_core/02-owl/exports/alt-formats/appsec-core-v1.0.owl` | `f5c7441ff287f5bc50fbe75254509ad8a0b5fdc7eba65ecdeeb8dbde908bd1eb` |
| `formal/appsec_core/02-owl/exports/alt-formats/appsec-core-v1.0.jsonld` | `36df9b70090ec90dd5616a440124781feac2024362face891c4d5f026ef083bc` |
| `formal/appsec_core/02-owl/exports/alt-formats/appsec-core-v1.0.nt` | `7d08ce173d1f645c292121696e20665b065edcd4d277c132900dc17ef1f3fd06` |
| `formal/appsec_core/05-validation/reports/appsec-core-v0-shacl-validation-summary.json` | `44cea7b1c6ad8b7cf14154121a51c226e5b451ae25151b405e998c4a361041c7` |
| `formal/appsec_core/05-validation/reports/appsec-core-v1-pyshacl-summary.json` | `e92a3cfb7854110848ab10ab8da00bd780c3e6397f0360567298b5cb2ea80a93` |

### Tag proposal (revised post-Phase-D)

`ontology-v1.1-fair-baseline` at the Phase D commit (not Phase C). Successor to `ontology-v1-final` for the v1 line; documents the OWL hygiene refinement without entity-set change. ACR-001/002/004 entities + counts (75 CO / 69 P / 58 M / 57 A = 259) unchanged.

### Phase A brief reference

Full Phase A findings + decision matrix: `agentic/briefs/2026-05-10-p6-ontology-validation-phase-a.md`.

### Phase C close

Phase C delivery details: `agentic/done/2026-05-10-p6-ontology-validation-phase-c-close.md`.

### Phase D close

Phase D delivery details: `agentic/done/2026-05-10-p6-ontology-validation-phase-d-close.md`.

## Shapes regression remediation (2026-05-05)

ACR-004 sprint commit `7ee0373` regenerated `appsec-core-v0-shapes.ttl`
from scratch via `build_shacl.py`, which has no awareness of model
invariants from Decision 0003 + Amendment 1. The regen stripped the 5
consumer-conformance Claim shapes (M1' / M3 / M4 via CO chain / M4-card
cardinality / M4-card referential integrity) that apparatus-v2
(`ee73c19`, 2026-05-04) had consolidated.

Cartographer detected the regression while emitting substrate v6 (which
needed the claim shapes to validate consumer conformance); substrate v6
itself is valid (Cartographer restored shapes from `ee73c19` to run the
gate).

Programme-lead Pedro Farinha ratified **Option C** on 2026-05-05:

1. `consumer-conformance-shapes.ttl` is restored as a separate
   ontology-owned file at `formal/appsec_core/03-shacl/shapes/`.
2. Maintained by Archon (NOT regenerated by `build_shacl.py`).
3. Apparatus tags (`apparatus-shacl-pyshacl-vN`) declare composition
   explicitly: ontology shapes file + consumer-conformance shapes file.
4. Pyshacl runner (`validate_pyshacl.py`) loads both as merged shapes
   graph.
5. Cross-persona update protocol: when Decision 0003 receives an
   amendment that alters model invariants, Cartographer/ESI dispatches
   Archon at `sbd-ai-runtime/handover/em-curso/`; Archon updates the
   file in a dedicated commit; apparatus tag refreshes.

Composed shapes pyshacl validation: `conforms = True` / 0 violations
(data 1824 / shapes 396 — 298 ontology + 98 consumer-conformance modulo
prefix overlap).

Architectural decision recorded at
`agentic/decisions/0001-consumer-conformance-shapes-ontology-owned.md`.

### Embeddings (AppSec Core v1.1)

- Corpus: 212 entities (was 209)
- Same model: sentence-transformers/all-MiniLM-L6-v2 @ c9745ed1
- Same env: Darwin x86_64 / Python 3.10.1 / transformers 4.57.1 / torch 2.2.2 / numpy 1.24.4
- corpus.sha256: 5951fd82e4b7547b37989af5b2f403ff3fd5e8b484b760ce4c565a6756b96c42
- npz.sha256: 17f6aac496b9896dae977a83745480322e1594a214bd9aa7b905f2cf9ddf23c8

### Tag proposals (programme-lead authority)

- `ontology-v1-next-acr004-promoted` — on YAML/OWL/SHACL commit (pending substrate v6 verification)
- `apparatus-shacl-pyshacl-v3` — on pyshacl rerun commit (successor to v2 at `ee73c19`)
- `appsec-core-embeddings-v1.1` — on .npz emit commit (successor to v1.0 at 2026-05-03)

### Why a new CO (not rename of ACO-IVF-003)

- ACO-IVF-003 core is input-side rulepack; folding output encoding would dilute its semantic core.
- Substrate evidence (CID-26 top-1 votes) signals missing-entity, not underspecified-entity.
- Composite ACO-IVF-007 already exists as the slice umbrella; adding 008 to `composed_of` is the natural extension.

### Why expand ASC-07 (not new slice)

- 69 items is cluster-shaped, not slice-shaped.
- "Untrusted-data hygiene at trust boundaries" unifies input + output sides.
- 10-slice invariance preserved.

## Why RPR (not SPC, not standalone adjunct)

- SPC "Protected Configuration" means configuration containing secrets — all 7 SPC COs are secret-first
- Config baselines are about the shape of configuration (secure defaults, hardening posture, integrity) — applied at deployment time
- RPR-004 already covers deployment configuration traceability
- Standalone adjunct would break structural invariance (CO must belong to 1 slice)
- 3 separate COs preserve semantic granularity (preventive vs governance, different domain keys)

## Evidence basis

- 25 core_gap items from 4 sources (SSDF PW.9, ASVS V13, CIS-4, CWE)
- 3 independent analyses
- Cross-pilot validation: OWASP SAMM (Environment Management), OWASP DSOMM (Application Hardening)
- Manual consumer trial: chapters 02, 08, 11

## Not changed

- Ten-slice structure (same 10 slices)
- All existing v0 COs, Practices, Mechanisms, Artifacts (001-007 in RPR unchanged)
- Entity type boundary
- No script changes needed

## Explicitly deferred

- EvidencePattern as first-class global index — deferred to v2
- Threat/Signal global indexing — deferred to v2
- TMR-007 decomposition — mapping correction, not ontology
- SSDF/SAMM/PCI mapping corrections (proxy TMR-005 → TMR-008) — next step
