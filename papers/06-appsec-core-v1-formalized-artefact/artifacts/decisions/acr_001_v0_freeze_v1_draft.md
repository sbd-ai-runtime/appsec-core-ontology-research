# AppSec Core v0 Freeze and v1-draft Creation

Date: `2026-04-13`
Status: `active_handover`
Scope: `v0 freeze, ACR-001 promotion as 3 COs in RPR, v1-draft creation`

## What happened

AppSec Core v0 was frozen and v1-draft was created by adding 3 new COs
from the ACR-001 adjunct (Secure Configuration Baseline Integrity) into
the RPR slice (ASC-09).

### v0 freeze

- Git tag `v0-frozen` on commit `bd78a93`
- Physical frozen copy at `ontology/v0/` (63 files)
- Frozen package at `packages/ontology/appsec-core/v0/`

### v1-draft: 3 COs in RPR slice

The 3 semantically distinct COs from the ACR-001 adjunct were promoted
into the RPR slice with full granularity preserved:

| ID | Name | Type |
|----|------|------|
| ACO-RPR-008 | Secure Defaults And Hardened Baseline Selection | preventive |
| ACO-RPR-009 | Security-Relevant Configuration Integrity And Override Control | preventive |
| ACO-RPR-010 | Baseline Review, Exception Visibility And Change Discipline | governance |

Plus 3 Practices (ACP-RPR-008/009/010), 3 Mechanisms (ACM-RPR-008/009/010),
4 Artifacts (ACA-RPR-009/010/011/012).

### Instance delta

| Entity | v0 | v1 | Delta |
|--------|----|----|-------|
| ControlObjective | 70 | 73 | +3 |
| Practice | 63 | 66 | +3 |
| Mechanism | 48 | 51 | +3 |
| Artifact | 53 | 57 | +4 |
| **Total** | **234** | **247** | **+13** |

### Placement rationale

- SPC "Protected Configuration" = configuration containing secrets (secret-first)
- Config baselines = secure defaults, hardening posture, config integrity (deployment-time)
- RPR-004 already covers deployment configuration traceability
- P1 §3.3: "cardinality 7 is methodological, not ontological"
- RPR goes from 7→10 COs — consistent with the method allowing variable counts

### Formalization

- OWL regenerated with all 13 new instances (all with belongsToSlice ASC-09)
- SHACL validation: **conforms** (0 violations)
- No script changes needed
- 18 tests passing

## What was NOT done

- ACR-002 (Security Requirements Governance) — deferred
- EvidencePattern as first-class global index — deferred to v2
- Threat/Signal global indexing — deferred to v2
- TMR-007 decomposition — mapping correction, not ontology change

## Next steps

1. Notify ExternalSourcesInventory to re-run instance mapping (25 core_gap items)
2. Notify authoring agent to proceed with P1-v2 manuscript
3. The 3 CIS IR items (TMR-007 -> SLG-007) are a MAPPING correction

## Commands

```bash
python3 -B scripts/formalize_appsec_core.py all
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -B -m unittest discover -s tests
```
