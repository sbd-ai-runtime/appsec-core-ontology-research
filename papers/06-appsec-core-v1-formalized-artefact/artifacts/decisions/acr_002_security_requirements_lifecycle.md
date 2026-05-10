# ACR-002 Promotion: Security Requirements Lifecycle Management

Date: `2026-04-14`
Status: `active_handover`
Scope: `ACR-002 promoted as ACO-TMR-008 in TMR slice (ASC-05)`

## What happened

ACR-002 (Security Requirements Governance) was promoted from adjunct
candidate into the TMR slice as ACO-TMR-008, based on convergent evidence
from 5 independent sources (NIST SSDF, OWASP SAMM, PCI SSLC, NIST 800-53,
SAFECode FPSSD).

### New instances (+3)

| ID | Name | Type |
|----|------|------|
| ACO-TMR-008 | Security Requirements Lifecycle Management | governance |
| ACP-TMR-008 | Security Requirements Identification And Communication | governance_and_review |
| ACM-TMR-007 | Requirements Portfolio And Compliance Monitoring | governance_and_review |

### ID correction from prompt

The prompt specified ACP-TMR-006 and ACM-TMR-005, but those IDs were
already taken. Corrected to ACP-TMR-008 (next sequential practice) and
ACM-TMR-007 (next sequential mechanism).

### Instance delta

| Entity | Before | After | Delta |
|--------|----|----|-------|
| ControlObjective | 73 | 74 | +1 |
| Practice | 66 | 67 | +1 |
| Mechanism | 51 | 52 | +1 |
| Artifact | 57 | 57 | 0 |
| **Total** | **247** | **250** | **+3** |

### Placement rationale

- TMR-008 models the **lifecycle of security requirements as practitioner
  artefacts**, not governance of ontology COs themselves
- Complements TMR-003 (Threat Modeling produces requirements)
- Complements TMR-005 (Traceability tracks requirements)
- Distinct from TMR-007 (broad SDLC governance composite)
- No new slice needed; TMR (ASC-05) is the correct home

### Design tension resolution

The original deferral cited circularity: "COs ARE requirements, so
requirements governance is meta-level."

Resolution: ACO-TMR-008 governs the requirements artefact lifecycle
(identify, communicate, derive criteria, implement, monitor, update),
not the ontology itself.

### Formalization

- OWL regenerated with all 3 new instances (all with belongsToSlice ASC-05)
- SHACL validation: **conforms** (0 violations, 1358 data triples)
- No script changes needed
- 18 tests passing

## Files changed

- `ontology/appsec-core-threat-modeling-risk-disposition-draft.yaml` — +ACO-TMR-008
- `ontology/appsec-core-threat-modeling-risk-disposition-components-draft.yaml` — +ACP-TMR-008, +ACM-TMR-007
- `ontology/appsec-core-threat-modeling-risk-disposition-slice-contract.yaml` — updated lists
- `ontology/appsec-core-v0-instance-index.yaml` — updated counts and ID lists
- `mappings/labels/appsec-core-taxonomy-labels.yaml` — +3 labels
- `formal/appsec_core/02-owl/exports/appsec-core-v0-bounded-v1.ttl` — regenerated
- `formal/appsec_core/05-validation/reports/` — regenerated

## What was NOT done

- Mapping corrections (SSDF PO.1.x → TMR-008, SAMM D-SR → TMR-008) — deferred
- EvidencePattern as first-class global index — deferred to v2
- Threat/Signal global indexing — deferred to v2

## Next steps

1. Re-map SSDF PO.1.1/PO.1.2/PO.1.3/PW.1.2 from TMR-005 proxy to TMR-008
2. Re-map SAMM D-SR activities from TMR-005 proxy to TMR-008
3. Re-map PCI SSLC 2.1 from TMR-005 to TMR-008
4. ExternalSourcesInventory re-run
5. P1-v2 manuscript update

## Commands

```bash
python3 -B scripts/formalize_appsec_core.py all
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -B -m unittest discover -s tests
```
