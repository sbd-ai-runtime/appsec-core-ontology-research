---
date: 2026-05-08
author: Archon (under programme-lead Pedro Farinha)
type: brief
status: delivery (sealed)
responds_to: sbd-ai-runtime/handover/em-curso/2026-05-08-orchestrator-archon-p7-pass-6-ontology-audit-mini-dispatch.md
authority: programme-lead Pedro Farinha 2026-05-08 (mini-dispatch); Orchestrator coordinated
output_destination: Curator P7 Pass 6 — §6 schema preservation prose + §2.2 / §6.1 EvidencePattern disposition
---

# P7 Pass 6 — V0→V1 attribution audit + EvidencePattern V1 disposition

## TL;DR

Item 1: V0→V1 net delta (+25) decomposes into ACR-001 (13) + ACR-002 (5) + ACR-004 (3) + within-slice "4 missing Mechanisms" patch (4). Per-entity attribution sealed via `git log -S` between `ontology-v0-frozen` and `ontology-v1-final`. Item 2: `EvidencePatternShape` declarative class retained at V1 with `target_node_count = 0` (zero populated instances); v0 supporting index of 213 patterns canonical preservation at `sbd-toe-knowledge-graph/data/publish/runtime/evidence_patterns.json` (SHA-256 `89305ffc…`).

## Verifiable totals

| Snapshot | Tag | Commit | CO | P | M | A | Total |
|----------|-----|--------|---:|---:|---:|---:|------:|
| V0 | `ontology-v0-frozen` | `bd78a93ec5c904af30ee1e077bdc88aaaca555ac` | 70 | 63 | 48 | 53 | **234** |
| V1 | `ontology-v1-final` | `b267cf32b6dd5f528ba29cd265a0886878bcf2a5` | 75 | 69 | 58 | 57 | **259** |
| Net delta | — | — | +5 | +6 | +10 | +4 | **+25** |

Source: `git show <tag>:ontology/appsec-core-v0-instance-index.yaml`. Both tags read directly. Summary block matches per-slice list aggregation.

## Item 1 — V0→V1 per-instance attribution table (sealed)

| Source of addition | +CO | +P | +M | +A | Per-entity list (introducing commit) |
|---|---:|---:|---:|---:|---|
| **ACR-001** Repository coverage / Secure Configuration Baseline (RPR slice ASC-09) | **3** | **3** | **3** | **4** | ACO-RPR-008 (`7de4a3a`); ACO-RPR-009/010 (`46792f6`); ACP-RPR-008 (`7de4a3a`); ACP-RPR-009/010 (`46792f6`); ACM-RPR-008 (`7de4a3a`); ACM-RPR-009/010 (`46792f6`); ACA-RPR-009/010/011/012 (`46792f6`) |
| **ACR-002** Security Requirements Lifecycle (TMR slice ASC-05) | **1** | **2** | **2** | **0** | ACO-TMR-008 (`f633c8e`); ACP-TMR-008 (`f633c8e`); ACP-TMR-009 (`e782bb0`); ACM-TMR-007 (`f633c8e`); ACM-TMR-008 (`e782bb0`) |
| **ACR-004** Output Rendering Safety / Context-Aware Encoding (IVF slice ASC-07) | **1** | **1** | **1** | **0** | ACO-IVF-008, ACP-IVF-007, ACM-IVF-005 — all in `e6c88ea` |
| **Within-slice refinements** (4 missing Mechanisms patch) | 0 | 0 | **4** | 0 | ACM-RPR-005, ACM-SCBI-006, ACM-SLG-005, ACM-SLG-006 — all in `e782bb0` |
| **Total V0→V1 net delta** | **+5** | **+6** | **+10** | **+4** | 25 entities introduced; V0 234 → V1 259 |

### Method

`git log --oneline -S "<entity_id>" --reverse ontology-v0-frozen..ontology-v1-final -- ontology/` per entity ID. The first matching commit is the introducing commit. Result table above is the verbatim mapping. All 25 entities resolve to one of 5 commits: `7de4a3a`, `46792f6`, `f633c8e`, `e782bb0`, `e6c88ea`.

### Commit roles

- **`7de4a3a`** — "feat: freeze AppSec Core v0 and create v1-draft with ACO-RPR-008" — initial v1-draft seed for ACR-001 promotion (ACO-RPR-008 + ACP-RPR-008 + ACM-RPR-008, before the 3-CO expansion).
- **`46792f6`** — "fix: expand RPR-008 to 3 COs preserving full ACR-001 semantic granularity" — ACR-001 expansion (RPR-009/010 + ACP-RPR-009/010 + ACM-RPR-009/010 + ACA-RPR-009/010/011/012). Also tagged `ontology-v1-acr001-promoted` per FREEZE-REGISTRY.
- **`f633c8e`** — "feat: promote ACR-002 as ACO-TMR-008 in TMR slice (v1-draft)" — initial ACR-002 promotion (1P+1M).
- **`e782bb0`** — "feat: execute 3-prompt sequence — 4 mechs + ACR-002 (2P+2M) + OWL/SHACL constitutive relations" — bundles three independent work items: (a) 4 missing Mechanisms patch (ACM-RPR-005, ACM-SCBI-006, ACM-SLG-005, ACM-SLG-006 — within-slice refinement filling Practices that lacked Mechanisms per CHANGELOG `ontology/v1.0/CHANGELOG.md:106-117`); (b) ACR-002 revision from 1P+1M to 2P+2M (ACP-TMR-009 + ACM-TMR-008); (c) OWL/SHACL constitutive relations.
- **`e6c88ea`** — "feat(ontology): promote ACR-004 as ACO-IVF-008 + ACP-IVF-007 + ACM-IVF-005 (v1.1-draft)" — single ACR-004 promotion commit on branch `acr004-output-rendering`.

### Disambiguations requested by Orchestrator

| Entity | Orchestrator preliminary inference | Sealed attribution | Evidence |
|--------|-----------------------------------|--------------------|----------|
| **ACM-RPR-005** | "ACR-001 OR within-slice refinement" | **Within-slice refinement** | Introduced in `e782bb0` 4-mechs patch; supports ACP-RPR-004 per CHANGELOG; sits between V0 sequential numbering (ACM-RPR-001..004) and ACR-001 jump (008/009/010) — explicitly the gap-fill, not part of the ACR-001 promotion bundle |
| **ACM-SCBI-006** | "presumably within-slice" | ✅ **Within-slice refinement** | Introduced in `e782bb0` 4-mechs patch; supports ACP-SCBI-003 per CHANGELOG |
| **ACM-SLG-005, ACM-SLG-006** | "presumably within-slice" | ✅ **Within-slice refinement** | Introduced in `e782bb0` 4-mechs patch; support ACP-SLG-001 and ACP-SLG-004 respectively per CHANGELOG |
| **ACA-RPR-009/010/011/012** | "likely ACR-001" | ✅ **ACR-001** | Introduced in `46792f6` (ACR-001 expansion-to-3-COs commit). Per CHANGELOG: 4 artifacts added at the same commit as RPR-009/010 expansion: `ACA-RPR-009 Security baseline definition`, `ACA-RPR-010 Hardening standard`, `ACA-RPR-011 Security-relevant override or exception record`, `ACA-RPR-012 Baseline review evidence package` |

### Caveats / commit-bundle observations

1. **Commit `e782bb0` is bundled.** It carries within-slice refinement (4 mechs) + ACR-002 expansion (TMR-009/008) + OWL/SHACL relations in one commit. The CHANGELOG (`ontology/v1.0/CHANGELOG.md`) maintains the conceptual separation: §"Added: 4 missing Mechanisms (2026-04-15)" attributes the 4 mechs to within-slice refinement; §"Revised: ACR-002 from 1P+1M to 2P+2M (2026-04-15)" attributes TMR-009/008 to ACR-002. Per-entity attribution above respects the conceptual separation declared in the CHANGELOG; the commit is shared by both.

2. **No within-slice CO additions in V0→V1.** All +5 COs are ACR-driven (3 ACR-001 + 1 ACR-002 + 1 ACR-004). The V1 expansion of CO surface is governed by the bidirectional CO promotion protocol; within-slice expansion is mechanism-level only.

3. **No within-slice Practice additions.** All +6 Practices are ACR-driven (3 ACR-001 + 2 ACR-002 + 1 ACR-004).

4. **No within-slice Artifact additions.** All +4 Artifacts are ACR-001 (RPR-009/010/011/012). No within-slice artifact expansion in this cycle.

5. **Mechanism additions are mixed.** +10 Mechanisms = 6 ACR-driven (3 ACR-001 + 2 ACR-002 + 1 ACR-004) + 4 within-slice refinement. The 4 within-slice are the only non-ACR additions in the entire V0→V1 cycle.

## Item 2 — EvidencePattern V1 disposition

### Declarative class retention (sealed via `ontology-v1-final` SHACL summary)

Read from `git show ontology-v1-final:formal/appsec_core/05-validation/reports/appsec-core-v0-shacl-validation-summary.json`:

| Shape | target_node_count | violation_count |
|-------|------------------:|----------------:|
| SliceShape | 10 | 0 |
| ControlObjectiveShape | 75 | 0 |
| PracticeShape | 69 | 0 |
| MechanismShape | 58 | 0 |
| ArtifactShape | 57 | 0 |
| **EvidencePatternShape** | **0** | **0** |

Overall status: `conforms`. Total violations: 0.

`EvidencePatternShape` is defined in `formal/appsec_core/03-shacl/shapes/appsec-core-v0-shapes.ttl` at V1-final with:

- `sh:targetClass ac:EvidencePattern`
- `sh:name "EvidencePatternShape"`
- `sh:description "expected_evidence_shape_used_for_deterministic_review_support"`
- Property shapes (visible from grep) — referenced by ControlObjective `objective_verified_by_evidence_pattern` (sh:class ac:EvidencePattern) and Artifact `artifact_supports_evidence_pattern` (sh:class ac:EvidencePattern). Both relations marked optional cross-entity in the bounded model.

### Populated graph V1 = 0 EvidencePattern instances

`target_node_count = 0` directly attests zero populated instances at V1. Substrate v7 confirmation per Orchestrator (SHA-256 `596783ed984d9c0e8c8ef6439a0eaee8fbaf2d863af37138cde8fad55d62be04`) corroborates: zero EvidencePattern claims at v7 cycle close.

### v0 supporting index of 213 patterns — canonical preservation location

The ontology repo's `ontology/appsec-core-evidence-pattern-index-v0.yaml` (read at V1-final) declares:

```yaml
source_alignment:
  source_file: data/publish/runtime/evidence_patterns.json
  source_status: runtime_aligned
  source_count: 213
```

Filesystem verification across the programme:

| Repository | Path | SHA-256 | n_records |
|------------|------|---------|----------:|
| **`sbd-toe-knowledge-graph`** (Codex publish surface — canonical) | `data/publish/runtime/evidence_patterns.json` | `89305ffcd279bdeb071bad48566cb96d11d524eeafdddd157ce6078bab95e394` | **213** |
| `sbd-toe-mcp-poc` | `data/publish/runtime/evidence_patterns.json` | `89305ffcd279bdeb071bad48566cb96d11d524eeafdddd157ce6078bab95e394` (bit-identical) | 213 |
| `securitybydesign-oss-mcp` | `data/publish/runtime/evidence_patterns.json` | `89305ffcd279bdeb071bad48566cb96d11d524eeafdddd157ce6078bab95e394` (bit-identical) | 213 |
| `sbd-toe-knowledge-graph` (entities source) | `data/entities/evidence_patterns.json` | `9a82b04b9d2b6b636f034505db80048332ec87448dec6b17f4a99b61674b858b` | 213 |

**Canonical citation surface for P7**: `sbd-toe-knowledge-graph/data/publish/runtime/evidence_patterns.json` — the runtime publish bundle owned by Codex, mirrored bit-identically in MCP runtime repos. Latest commit touching the file: `7f6a340` ("feat(publish): refresh backend from manual v0.2.8") on `master`. P3 anchor tags for the same publish surface: `paper-p3-kg-input` (`eaa92dcc7e7848d76e9a4c067c5ae4a3cbe83611`) and `paper-p3-published` (`b567c886662f34fc310bb0c48b4d9eeb25c8c8b2`).

### 3-4 sentence prose for §2.2 / §6.1

> EvidencePattern is a first-class declarative class in the AppSec Core V1 ontology — `EvidencePatternShape` is defined in the apparatus SHACL skin (`appsec-core-v0-shapes.ttl`) at `ontology-v1-final` with `sh:targetClass ac:EvidencePattern`, plus optional property shapes referencing it from ControlObjective (`objective_verified_by_evidence_pattern`) and Artifact (`artifact_supports_evidence_pattern`). The class is intentionally unpopulated at V1: the SHACL conformance report records `target_node_count = 0` for `EvidencePatternShape`, and substrate v7 carries zero EvidencePattern claims (SHA-256 `596783ed984d9c0e8c8ef6439a0eaee8fbaf2d863af37138cde8fad55d62be04`). The v0 supporting index of 213 evidence patterns — used by the P3 retrieval runtime — remains preserved at `sbd-toe-knowledge-graph/data/publish/runtime/evidence_patterns.json` (SHA-256 `89305ffcd279bdeb071bad48566cb96d11d524eeafdddd157ce6078bab95e394`), with bit-identical mirrors in `sbd-toe-mcp-poc` and `securitybydesign-oss-mcp`. The ontology declares the relationship via `appsec-core-evidence-pattern-index-v0.yaml`'s `source_alignment` block, which acts as the canonical pointer between the V1 declarative class and the v0 populated supporting surface.

## Verification SHA-256 / commit references for reproducibility

| Anchor | Value | Used for |
|--------|-------|----------|
| V0 frozen tag | `ontology-v0-frozen` → `bd78a93ec5c904af30ee1e077bdc88aaaca555ac` | V0 baseline read |
| V1 final tag | `ontology-v1-final` → `b267cf32b6dd5f528ba29cd265a0886878bcf2a5` | V1 baseline read |
| ACR-001 expansion commit | `46792f6` (also `ontology-v1-acr001-promoted`) | RPR-009/010 + ACP/ACM/ACA-009..012 |
| ACR-001 seed commit | `7de4a3a` | RPR-008 + ACP/ACM-008 |
| ACR-002 promotion commit | `f633c8e` | TMR-008 + ACP/ACM-TMR-008 + ACM-TMR-007 |
| ACR-002 expansion commit | `e782bb0` | TMR-009 + ACM-TMR-008 + 4 missing mechs |
| ACR-004 promotion commit | `e6c88ea` | IVF-008 + ACP-IVF-007 + ACM-IVF-005 |
| Substrate v7 SUPPLIER | `596783ed984d9c0e8c8ef6439a0eaee8fbaf2d863af37138cde8fad55d62be04` | EvidencePattern V1 = 0 confirmation |
| 213-pattern publish file SHA-256 | `89305ffcd279bdeb071bad48566cb96d11d524eeafdddd157ce6078bab95e394` | Canonical 213-pattern preservation pointer |
| 213-pattern entities source SHA-256 | `9a82b04b9d2b6b636f034505db80048332ec87448dec6b17f4a99b61674b858b` | Source-of-truth inventory in Codex |

## References

- Inbound mini-dispatch: `sbd-ai-runtime/handover/em-curso/2026-05-08-orchestrator-archon-p7-pass-6-ontology-audit-mini-dispatch.md`
- V1.0 CHANGELOG (canonical narrative for ACR-001 expansion + 4 mechs + ACR-002 revision): `ontology/v1.0/CHANGELOG.md`
- ACR-004 sprint close (predecessor): `agentic/done/2026-05-05-acr004-output-rendering-execution-close.md`
- ACR-004 shapes regression remediation (predecessor): `agentic/done/2026-05-05-acr004-shapes-regression-remediation.md`
- Cycle A frozen-state consolidated: `DevelopmentGovernance/docs/cycle-a-frozen-state-consolidated.md`
- FREEZE-REGISTRY (tag history): `FREEZE-REGISTRY.md`
