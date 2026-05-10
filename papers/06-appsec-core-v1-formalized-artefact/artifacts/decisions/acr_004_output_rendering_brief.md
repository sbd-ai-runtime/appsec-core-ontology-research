---
date: 2026-05-05
author: Archon (under programme-lead Pedro Farinha)
type: brief
status: proposal — pending Orchestrator ratification dispatcher
responds_to: sbd-ai-runtime/handover/em-curso/2026-05-05-orchestrator-archon-acr004-output-rendering-promotion.md
authority_chain: programme-lead 2026-05-05 (promotion-in-principle) → Orchestrator dispatcher 2026-05-05 → Archon proposal (this brief) → Orchestrator review → programme-lead ratification → Orchestrator dispatcher #2 (execution) → Archon execution
---

# ACR-004 — Slice-boundary proposal: Output Rendering Safety / Context-Aware Encoding

## TL;DR

Promote ACR-004 as **Practice + Mechanism under a new ControlObjective `ACO-IVF-008`** ("Context-Aware Output Encoding And Rendering Safety") inside an **expanded ASC-07 slice**. Preserve `ACO-IVF` prefix with reinterpreted meaning ("Input/Output Validation & Filtering"). Update composite `ACO-IVF-007` to include 008. Remap manual requirement VAL-005 from current mis-anchoring to new 008. No new slice. No identifier renaming.

## Verification of current state (§0.6)

| Item | State at 2026-05-05 | Evidence |
|------|---------------------|----------|
| Slice ASC-07 scope | `input_validation_safe_parsing_and_controlled_failure` | `ontology/appsec-core-input-validation-safe-failure-slice-contract.yaml:5` |
| ACO-IVF COs in use | 001-007 (007 composite); **008 free** | slice contract `objective_set` |
| ACP-IVF in use | 001-006; **007 free** | slice contract `component_subset.normalized_practices` |
| ACM-IVF in use | 001-004; **005 free** | slice contract `component_subset.normalized_mechanisms` |
| ACO-IVF-003 current label | "Injection-Resistant Input Handling And Dangerous Pattern Exclusion" | `ontology/appsec-core-input-validation-safe-failure-draft.yaml:172` |
| ACO-IVF-003 current anchors | VAL-004, VAL-007 | same file |
| VAL-005 current anchor | **Mis-anchored to ACO-IVF-004** (Validation Before Internal Use And Trust Crossing) — VAL-005 in manual is XSS / output sanitization, not trust-crossing | `ontology/appsec-core-input-validation-safe-failure-draft.yaml:204`; manual `010-sbd-manual/02-requisitos-seguranca/addon/07-validacao-requisitos.md:167` |
| Cumulative v1.0 totals | 74 CO / 68 P / 57 M / 57 A = 256 | `ontology/v1.0/CHANGELOG.md:147` |
| Embeddings tag | `appsec-core-embeddings-v1.0` ratified 2026-05-03 (programme-lead) — corpus 209 entities | `formal/appsec_core/08-embeddings/embeddings-manifest.json` |
| Apparatus anchor | `apparatus-shacl-pyshacl-v2` at `ee73c19` | FREEZE-REGISTRY |
| LDP cluster CID-26 | 69 items, 5 sources STRONG (asvs_v5_0_0, capec_v3_9, cwe_software_development_view_v4_19_1, mcp_official_security_foundations_2025, owasp_dsomm); top-1 votes split ACP_IAT_005=18, ACP_IVF_003=10, ACO_IVF_003=9; adjacency ceiling ~0.40 | `ExternalSourcesInventory/data/p7_olir_audit/p7_v2_corrected/v5/reports/LABDEPTHPENDING_ACR_ANALYSIS.md:127-151` (currently in `.claude/worktrees/v5-normalization-phase-1a/` — flag path drift) |

## Decision (Archon judgment per AGENTS §3.3 slice authority)

### 1. Slice scope — EXPAND (Option B)

Rename slice scope label from `input_validation_safe_parsing_and_controlled_failure` to `input_output_data_safety_and_controlled_failure`.

**Rationale.** Slice contract integrity preserved: input-side validation/filtering and output-side context-aware encoding are two faces of the same trust-boundary concept ("untrusted-data hygiene"). The 10-slice structure stays intact. Cluster CID-26 evidence shows top-1 votes already concentrating in IVF Practice/CO entries — adjacency points to within-slice expansion, not new-slice carve-out.

### 2. Identifier prefix — PRESERVE `ACO-IVF`

Reinterpret the prefix as "Input/Output Validation & Filtering". Identifier stability rule (Archon §3.1, AGENTS rule 3) honoured: existing identifiers ACO-IVF-001..007 unchanged; OWL/SHACL bindings unchanged; downstream consumer contract (Codex) unbroken. **No introduction of `ACO-IOF`** — would break stability without semantic gain.

### 3. Host CO — NEW `ACO-IVF-008`, NOT a rename of `ACO-IVF-003`

**Reject simple rename of ACO-IVF-003.**

- ACO-IVF-003 core is input-side rulepack (injection-prevention, dangerous-pattern exclusion). Folding 69 output-encoding items into it dilutes the semantic core and obscures `domain_key` distinctions.
- Substrate evidence: top-1 votes for CID-26 distribute across three distinct entities (ACP_IAT_005=18, ACP_IVF_003=10, ACO_IVF_003=9) with adjacency capped at ~0.40 — signal of missing-entity, not underspecified-entity. Renaming does not create the missing landing zone.
- Composite ACO-IVF-007 already exists as the slice umbrella; adding 008 to its `composed_of` is the natural extension.

**Reject new slice (Option D).**

- 69 items is cluster-shaped, not slice-shaped.
- Concept fit-within-IVF is clear once scope is expanded to include output side.
- Cost of breaking the 10-slice invariance > value gained.

**Accept new ACO-IVF-008 (Practice-level promotion under CO-as-anchor framing).**

- Programme-lead position 2026-05-05 explicitly authorises Practice-level promotion under "a new ACO-IVF-008 dedicated to output encoding (still Practice-level focus per programme-lead, with the CO acting as semantic anchor only)" (dispatcher §item 3 bullet 3).
- VAL-005 ("Sanitização de output / SEC-Lx-VAL-XSS") is currently mis-anchored to ACO-IVF-004 — ACO-IVF-008 creates the correct semantic home and corrects pre-existing manual-mapping debt.

### 4. Practice + Mechanism naming

| ID | Name | Family | Local type | New enum value? |
|----|------|--------|------------|-----------------|
| **ACO-IVF-008** (new CO) | Context-Aware Output Encoding And Rendering Safety | atomic / preventive | `domain_key: output_rendering_safety` | yes (additive to `domain_key` enum) |
| **ACP-IVF-007** (new Practice) | Context-Aware Output Encoding At Rendering Boundaries | `validation_and_analysis` | `local_practice_type: output_encoding` | yes (additive) |
| **ACM-IVF-005** (new Mechanism) | Context-Aware Encoder Selection And Application | `validation_and_analysis` | `local_mechanism_type: context_encoder` | yes (additive) |

Enum extensions are additive — SHACL `sh:in` shapes only widen the accepted set; no breaking change for existing instances.

### 5. Slice contract amendment — diff scope

Files to amend (no edits to v0/ — frozen):

- `ontology/appsec-core-input-validation-safe-failure-slice-contract.yaml`
  - `meta.scope`: new label
  - `purpose.current_goal`: include output-encoding clause
  - `objective_set.atomic_objectives`: + ACO-IVF-008
  - `objective_set.composite_rules.ACO-IVF-007.composed_of`: + ACO-IVF-008
  - `objective_set.composite_rules.ACO-IVF-007.statement`: append output-side clause
  - `component_subset.normalized_practices`: + ACP-IVF-007
  - `component_subset.normalized_mechanisms`: + ACM-IVF-005
  - `scope.domains`: + `output_rendering_safety`
- `ontology/appsec-core-input-validation-safe-failure-draft.yaml`
  - New CO ACO-IVF-008 block (statement, expected_outcome, verification_posture, anchors)
  - ACO-IVF-004: remove `VAL-005` from `current_manual_requirement_anchors`
  - ACO-IVF-008: add `VAL-005` + ASVS V1.2.1, V1.2.2, V1.2.3, V3.2.1, V3.2.2 references; CWE-79 family + CAPEC-63/242 as overlay anchors
- `ontology/appsec-core-input-validation-safe-failure-components-draft.yaml`
  - New ACP-IVF-007 + ACM-IVF-005 entries
- `ontology/appsec-core-input-validation-safe-failure-mapping-draft.yaml`
  - VAL-005 → ACO-IVF-008
- `ontology/appsec-core-v0-instance-index.yaml`
  - +3 instances (ACO-IVF-008, ACP-IVF-007, ACM-IVF-005)
- `ontology/appsec-core-entity-schema-v0-draft.yaml`
  - 3 enum extensions (additive)

### 6. OWL/SHACL regeneration plan

Run `python/build_owl.py` then `python/build_shacl.py`. Pyshacl conformance run via `formal/appsec_core/python/...` consistent with `apparatus-shacl-pyshacl-v2`.

| Change | Volume |
|--------|--------|
| New `rdf:type` triples (CO, P, M) | 3 |
| New `objective_realized_by_practice` (008→ACP-007) | 1 |
| New `objective_implemented_by_mechanism` (008→ACM-005) | 1 |
| New `composed_of` (007→008) | 1 |
| Manual mapping: `manual_requirement_maps_to_objective` add (VAL-005→008) | 1 |
| Manual mapping: remove (VAL-005→004) | 1 |
| `sh:in` enum widening (`domain_key`, `local_practice_type`, `local_mechanism_type`) | 3 shapes |

**Conformance target:** `conforms = True`, **0 violations**. CO→P/M minCount 1 satisfied (ACO-IVF-008 has ≥1 Practice + ≥1 Mechanism).

### 7. Embeddings regeneration plan

Embeddings are within Archon scope (verified — `formal/appsec_core/08-embeddings/build-script.py` is the producer; manifest §notes:3 confirms Cartographer mirrors this encoding side).

| Action | Output |
|--------|--------|
| Update `formal/appsec_core/08-embeddings/augmented-text-corpus.json` | + 3 entries (ACO-IVF-008, ACP-IVF-007, ACM-IVF-005) → 212 records (10 Slice + 75 CO + 69 P + 58 M) |
| Confirm `augmentation-rule.yaml` v1.0 covers the 3 new entries without rule change | rule unchanged |
| Re-run `formal/appsec_core/08-embeddings/build-script.py` | new `embeddings-all-MiniLM-L6-v2-c9745ed1.npz` (212 × 384, float32, L2-normalized) |
| Update `embeddings-manifest.json` | new SHA256 (corpus + npz), updated counts, updated `build.timestamp_utc`; same model + revision + library versions per Decision 0003 Amendment 1 §F |

**Determinism dependency:** build environment must match Darwin x86_64 + Python 3.10.1 + transformers 4.57.1 + torch 2.2.2 + numpy 1.24.4. Pre-execution checklist required.

### 8. Manual backing — confirmed, no retrofit (§3.4 promotion threshold)

| Chapter | Anchor | Content |
|---------|--------|---------|
| 02 (Requisitos) | VAL-005 | "Testar output em campos renderizados no browser. Confirmar escaping correcto." (`010-sbd-manual/02-requisitos-seguranca/addon/07-validacao-requisitos.md:167`) — direct backing for context-aware output encoding |
| 06 (Desenvolvimento Seguro) | SAST `high` severity for XSS | `aplicacao-lifecycle.md:574,590,603` — XSS detection at L2+ |
| 04 (Arquitetura Segura) | ASVS V3.5.6 / V3.5.7 (XSSI), V4.2.3 / V4.2.4 (header injection) | `canon/25-rastreabilidade.md:409-410, 424-425` — currently anchored to ACM-ATB-003 / ACM-IVF-003; review recommended in Curator handover |

**Cross-persona handover to Curator (§0.5)** required for:
- Confirming VAL-005 anchor remap to ACO-IVF-008
- Reviewing whether chapter 04 ASVS V3.5.x / V4.2.x anchors should re-target ACO-IVF-008 or remain in ATB/IVF as currently mapped

### 9. Tag convention acknowledged

- `ontology-v1-next-acr004-promoted` — on the commit incorporating YAML + slice contract + OWL/SHACL regeneration. Programme-lead authority required.
- `apparatus-shacl-pyshacl-v3` — on the commit re-running pyshacl conformance. Successor to `apparatus-shacl-pyshacl-v2` at `ee73c19`. Programme-lead authority required.
- `appsec-core-embeddings-v1.1` (or `-v1-next`) — on the commit emitting the new `.npz` + manifest. Programme-lead authority required (Decision 0003 Amendment 1 §F).

## Boundary integrity (§3.3)

This proposal preserves:

1. **10-slice structure** — no slice added or removed; ASC-07 scope label expanded only.
2. **Identifier stability** — all existing IDs unchanged; only +3 new IDs in next-free positions.
3. **CO→P/M minCount 1 SHACL invariant** — ACO-IVF-008 has 1 P + 1 M; conformance maintained.
4. **v0 immutability** — no edits to `ontology/v0/`; v0-frozen tag intact.
5. **Manual prose neutrality** — no manual retrofit; existing VAL-005 + chapter 06 SAST content already supports the Practice.
6. **Composite umbrella** — ACO-IVF-007 remains the slice composite; expanded `composed_of` includes 008.

## Divergences detected during verification

These are flagged transparently per §0.6:

1. **`AGENTS.md` lines 156, 167** describe ACR-002 as "deferred". Outdated: ACR-002 was promoted as ACO-TMR-008 on 2026-04-14 (commit `f633c8e`). Recommend correction in next AGENTS.md amendment.
2. **`PROMPT-ontology-acr002-requirements-lifecycle.md` line 195** cites `74 CO, 68 P, 53 M`. Actual cumulative state per `ontology/v1.0/CHANGELOG.md:147` is 74/68/57/57. The 53 M figure was an intermediate count before 4-missing-mechanisms patch + ACR-002 expansion to 2P+2M.
3. **Dispatcher §Manual content backing** cites "capítulo 04 (Validação e Saneamento)". Actual chapter 04 is "Arquitetura Segura". Manual backing for output encoding is in chapter 02 (VAL-005) + chapter 06 (SAST XSS). Backing exists; chapter reference in dispatcher is mistaken but does not affect promotion decision.
4. **VAL-005 mis-anchoring to ACO-IVF-004** is a pre-existing mapping debt that ACR-004 corrects. Flagged for Curator awareness.
5. **LDP report path drift.** Dispatcher cites `ExternalSourcesInventory/data/p7_olir_audit/p7_v2_corrected/v5/reports/LABDEPTHPENDING_ACR_ANALYSIS.md`; that path exists only in `.claude/worktrees/v5-normalization-phase-1a/`. Recommend Cartographer confirms which path is canonical for V5 substrate.

## Decision matrix returned to Orchestrator (Asks 1-7 per dispatcher)

| Ask | Decision |
|-----|----------|
| 1. Slice-boundary proposal (4-option analysis) | **Option B** (expand scope) **+ new ACO-IVF-008** (rejected: simple rename, new slice) |
| 2. Identifier-prefix decision | **Preserve `ACO-IVF`** with reinterpreted meaning ("Input/Output Validation & Filtering") |
| 3. Host CO + Practice + Mechanism naming | **ACO-IVF-008** + **ACP-IVF-007** + **ACM-IVF-005** with names per §4 above |
| 4. Slice contract amendment diff scope | Per §5 above (6 files, all in `ontology/` excluding v0/) |
| 5. OWL/SHACL regeneration plan + conformance maintenance | Per §6 above; target conforms=True / 0 violations |
| 6. Manual backing confirmation | Per §8 above; cross-persona handover to Curator required for VAL-005 remap + chapter 04 ASVS V3.5.x review |
| 7. V1.next tag-convention proposal | Acknowledged. Three tags: `ontology-v1-next-acr004-promoted`, `apparatus-shacl-pyshacl-v3`, `appsec-core-embeddings-v1.1` (all programme-lead authority) |

## Execution contingent on Orchestrator dispatcher #2

Per §6.5 (No unilateral promotions or freezes), Archon awaits a follow-on dispatcher carrying programme-lead ratification of:

1. The slice-boundary decisions in §1-§4
2. Authorisation envelope for the three tags in §9
3. Cross-persona dispatchers to Cartographer (substrate v6 source-side embeddings + grounding pipeline re-run against new AppSec Core embeddings) and Curator (VAL-005 remap + chapter 04 review)

On receipt of dispatcher #2, Archon executes within ASC-07 / `ontology/` / `formal/appsec_core/` scope and returns a closing note + brief documenting commits, SHA-256 manifests, and SHACL conformance evidence.

## References

- Inbound dispatcher: `sbd-ai-runtime/handover/em-curso/2026-05-05-orchestrator-archon-acr004-output-rendering-promotion.md`
- LDP analysis cluster CID-26: `ExternalSourcesInventory/.claude/worktrees/v5-normalization-phase-1a/data/p7_olir_audit/p7_v2_corrected/v5/reports/LABDEPTHPENDING_ACR_ANALYSIS.md` §7.1
- Slice contract: `ontology/appsec-core-input-validation-safe-failure-slice-contract.yaml`
- v1.0 cumulative state: `ontology/v1.0/CHANGELOG.md`
- Embeddings ratification: `formal/appsec_core/08-embeddings/embeddings-manifest.json`; Decision 0003 Amendment 1 §F
- Apparatus anchor: `apparatus-shacl-pyshacl-v2` at `ee73c19`
- Iteration 1 frozen state: `cycle-a-iter-1-frozen-2026-05-04`
- Manual chapter 02 VAL-005: `SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/02-requisitos-seguranca/addon/07-validacao-requisitos.md:167`
- Archon authority: `AGENTS.md` §3.3 (slice authority), §3.4 (promotion threshold), §6.5 (no unilateral)
