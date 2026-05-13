# Cycle B Frozen State — Consolidated Reference

**Status:** RATIFIED 2026-05-12 (programme-lead Pedro Farinha; "1, 2c, 3 e 4 sim")
**Authority:** programme-lead Pedro Farinha
**Author:** Orchestrator
**Date:** 2026-05-12
**Purpose:** consolidated single-document reference for Cycle B frozen state. Input for P8 paper authoring (Curator dispatcher follows). Sequenced after Cycle A frozen (`cycle-a-frozen-2026-05-08`).

---

## 1. Cycle B scope and closure

Cycle B is the **Manual + KG integration phase** of the SbD-ToE programme. It applied AppSec Core V1 (Cycle A output) + substrate v7 to refine the practitioner Manual + regenerate the Manual KG, demonstrating the **operational Manual ingest pipeline as programme primitive** (per P8 paper reframing 2026-05-11).

Six iterations across Cycle B Manual content work:

| Iteration | Closed | Substantive output | Commit |
|---|---|---|---|
| Iteration 1 | 2026-05-11 | Rastreabilidade-regen + Manual-internal items resolved (VAL-005 §6.6 → VAL-008 split; chapter 04 ASVS; ACO-IVF-008 anchor) | `96fd9cea` / `c3bacd4d` / `94a757b0` |
| Iteration 2 | 2026-05-11 | AI/ML prose extension (5 chapters scope B; 4 new requirements THR-008/ARC-014/OPS-011/DEP-011; 17 substrate v7 IDs) | `b1d129f0` |
| Iteration 3 | 2026-05-11 | Stage 5 Editorial Feedback applied (Path D entity-first regenerate; 38/38 Phase 2/3 entries resolved) | `71b9c029` |
| Iteration 4 | 2026-05-11 | Rastreabilidade richness extension (4-section tabular: Core-mapped + Manual-only + Out-of-AppSec + Future-work) | `16dfa5ae` |
| Run 1 | 2026-05-11 | §26 methodology refresh + Manual ontology V2 vocab integration nos 25-rastreabilidade (5-section) | `a9e70c98` |
| Run 2 | 2026-05-11 | achievable-maturity × 14 + 50-ameacas-mitigadas × 14 enrichment com same methodology | `455124a1` |

Cycle B frozen ceremony 2026-05-12 — four peer cross-repo tags at:
- `SbD-ToE-Manual` `phase-c-methodology-revision` `455124a1` → `cycle-b-frozen-2026-05-12` (tag obj TBD)
- `sbd-toe-knowledge-graph` master `dacfaca` (post FREEZE-REGISTRY backfill; tag chain anchor `kg-v1-cycle-b-run-2-aligned-2026-05-12` @ `727d4c3d`) → `cycle-b-frozen-2026-05-12` (tag obj TBD)
- `ExternalSourcesInventory` main `d5da1a0` (post-Cartographer-merge) → `cycle-b-frozen-2026-05-12` (tag obj TBD)
- `DevelopmentGovernance` (commit landing this consolidated brief) → `cycle-b-frozen-2026-05-12` (tag obj TBD)

---

## 2. Manual ontology V2 — finding and alignment

### 2.1 Manual ontology V2 canonical state

Manual ontology V2 canonical YAML em `sbd-toe-knowledge-graph/ontology/sbdtoe-ontology.yaml`:

| Field | Value |
|---|---|
| Name | SbD-ToE Manual Ontology |
| Version | 2.0 |
| Status | current |
| Scope | Manual ontology (distinct from AppSec Core) |
| Format | Semi-formal YAML (NÃO OWL+SHACL ainda; Stream 2 future) |

### 2.2 Structure (Knowledge Bundle aware)

| Layer | Entities |
|---|---|
| core (15) | Requirement, Control, Practice, PracticeAssignment, Artifact, Threat, Role, SDLCPhase, UserStory, EvidencePattern, Concept, Mechanism, Pattern, AntiPattern, Signal |
| supporting (9) | KnowledgeBundle, BundleDocument, DocumentUnit, PolicyReference, MaturityMapping, ExternalFramework, ExternalObligation, OverlayPlaybook, OverlayMapping |
| runtime (2) | ApplicationContext, ArtifactRequirement |
| stub (1) | ImplementationRule |

### 2.3 Apparatus

| Apparatus | Definition |
|---|---|
| Classification policy | Concept / Mechanism / Pattern / AntiPattern / Signal (com tests) |
| Authority classes | normative / editorial / semantic / operational / external |
| Source modes | explicit / derived / scored / heuristic / runtime |
| Confidence model | deterministic / bounded / probabilistic |
| Review findings model | missing_expected_artifact / missing_expected_signal / unmapped_requirement / unsupported_control / observed_antipattern / weak_evidence |
| Resolution profiles | consult / guide / review / threats |

### 2.4 AppSec Core ↔ Manual ontology V2 boundary

Manual ontology V2 deliberately exclui `AppSecCoreControlObjective` (per V2 §`not_in_scope_yet`). Rationale: AppSec Core V1 + Manual ontology V2 são **ontologias separadas** com alignment via overlay (Stream 1 future work: OAEI/SKOS/EDOAL formal alignment).

Cycle B operacionalizou alignment via:
- AppSec Core V1 entities mapping para Manual sections via Cartographer per_entity_source_map.json (overlay records)
- Manual ontology V2 entities surfaced per chapter from KG canonical files (data/entities/*.json + data/publish/semantic/*.jsonl)
- Three-way routing per chapter rastreabilidade: § Core-mapped (V1 overlay) + § Manual-only (Manual V2 entities sem V1 anchor) + § Out-of-AppSec (pure editorial)

---

## 3. Cycle B Manual content work — final state

### 3.1 25-rastreabilidade × 15 chapters

Format final: **5-section per chapter** (post Run 1 enrichment over Iter 4 baseline):

1. § Manual ontology V2 — entities canónicas deste capítulo (per chapter index from KG canonical files)
2. § Core-mapped coverage (V1 entity × Manual ontology V2 anchor × Manual section × Authority/Source/§26 label × ES grounding)
3. § Manual-only coverage (out-of-Core-scope; Manual V2 anchor + Authority + ES direct refs)
4. § Out-of-AppSec coverage (pure editorial; Manual V2 anchor if any)
5. § Future-work register (P8 §10 candidates)

V1 coverage state per Phase 2/3 closure:

| §26 methodology label | Phase classification | Count | Closure mechanism |
|---|---|---|---|
| Explícito | Phase 1 covered | 164 | Already exposed pre-Iter-3 |
| Semântico | Phase 2/3 claim_gap | 31 | Path D entity-first exposure (Iter 3); zero new prose |
| Parcial | Phase 2/3 cross_reference_gap | 6 | Cross-chapter pointers added (Iter 3) |
| Gap | Phase 2/3 confirmed_content_gap | 1 | ACM-IVF-004 registered future-work P8 §10 |
| Scope boundary | Cartographer scope_exclusion | 57 | Artifacts OWL-only; not Manual scope |

V1 ontology Manual scope universe = 259 - 57 = 202 substantive entities. Manual-scope coverage post-Iter-3: 201/202 = 99.5%.

### 3.2 achievable-maturity × 14 chapters

Format final: **5-section per chapter** (Run 2):

1. § Manual ontology V2 — entities relevant para maturity (MaturityMapping + Practice + Control)
2. § SAMM v2 / DSOMM maturity progression (primárias per §26 §4) — 168 MaturityMapping items surfaced
3. § SLSA build/integrity progression (conditional; 3 chapters qualify: 05/07/09)
4. § Out-of-Maturity scope (regulatory alignment NÃO maturity per §26 §4)
5. § Future-work register (maturity gaps)

Discipline per §26 canon §4:
- SAMM v2 + DSOMM primary
- SLSA conditional (build/integrity progression only)
- Regulatory alignment ≠ maturity score
- §26 methodology labels per row deterministic

### 3.3 50-ameacas-mitigadas × 14 chapters

Format final: **6-section per chapter** (Run 2):

1. § Manual ontology V2 — entities canónicas (233 Threats + 26 AntiPatterns + 23 Signals)
2. § Threat surfaces (Manual + CAPEC primary)
3. § AntiPattern exposure mapping (5 antipattern_threat_links)
4. § CWE references (supporting only per §26 §4; NÃO substituto)
5. § V1 overlay mitigation pathway (onde Core-mapped)
6. § Future-work register (threat gaps)

Discipline per §26 canon §4:
- Manual + CAPEC primary para threat taxonomy
- CWE supporting limited (complement only)
- Mitigation strength explicitly labelled (forte / parcial / dependente_de_outros_capitulos)
- V1 overlay mantém three-way routing visible

### 3.4 §26 metodologia document refresh

`manuals_src/docs/sbd-toe/010-sbd-manual/00-fundamentos/canon/26-metodologia-validacao-claims.md` refreshed em Run 1 (`a9e70c98`):

- §2: Manual ontology V2 location explicit (`sbd-toe-knowledge-graph/ontology/sbdtoe-ontology.yaml`); previous "knowledge-graph V2" reference confirmed correct (NÃO typo)
- §3: artifact references refreshed → current canonical paths (`coverage_v1_to_manual.json` + `coverage_manual_to_v1.json` + `per_entity_source_map.json` + AppSec Core V1 + KG runtime V1)
- NEW §9: P8 pipeline primitive reframing reference + Stream 2 (OWL+SHACL formalisation) future-work flag
- §1, §4-§8 preserved intact

### 3.5 Generator chain (reprodutibilidade)

| Iter | Generator script | Commit |
|---|---|---|
| 3 | `scripts/iter3_recreate_rastreabilidade.py` | `71b9c029` |
| 4 | `scripts/iter4_inject_es_references.py` | `16dfa5ae` |
| Run 1 | `scripts/run1_inject_manual_ontology_v2_vocab.py` | `a9e70c98` |
| Run 2 | `scripts/run2_apply_methodology_to_maturity_threats.py` | `455124a1` |

---

## 4. Knowledge Graph state — Cycle B closure

### 4.1 Consumer contract progression

| Version | Tag | Date | Substantive change |
|---|---|---|---|
| v1.0 | `kg-v1-cycle-b-iter-2-aligned-2026-05-11` | 2026-05-11 | Initial V1-aligned KG (PR #19) — 245 V1 entities + 529 OWL relations + 2,835 linkage records |
| v1.1 | `kg-v1-cycle-b-iter-3-aligned-2026-05-11` | 2026-05-11 | Iter 3 Path D delta (PR #20) — 2,240 linkage records (entity-first format) + 1 future-work entry |
| v1.2 | `kg-v1-cycle-b-run-2-aligned-2026-05-12` | 2026-05-12 | Run 1 + Run 2 delta (PR #21 @ `727d4c3d`) — Manual V2 vocab integration + maturity_progression_record + threat_mitigation_record linkage classes |

### 4.2 KG runtime structure (post Codex Run 1+Run 2 delta @ `727d4c3d`)

| Surface | State |
|---|---|
| V1 entity index | 245 (unchanged; ontology canonical 259 with 14-entity slice contract back-fill gap deferred) |
| OWL relations | 529 (unchanged) |
| Manual rastreabilidade linkage records (5-section refresh) | **1,105** (`manual_rastreabilidade.jsonl`) |
| Maturity progression linkage records (NEW) | **336** (`manual_maturity_progression.jsonl`) |
| Threat mitigation linkage records (NEW) | **523** (`manual_threat_mitigation.jsonl`) |
| Total Manual ↔ ontology linkage | **1,964 records** |
| evidence_patterns.json | refreshed com V2 entity cross-references + maturity_progression_pattern + threat_mitigation_pattern types |

### 4.3 KG cycle B tag predecessor chain

| Tag | Pointer | Layer |
|---|---|---|
| `corpus-v1-ontology-sync-84fe8bf` | `a9f68e7...` | Pre-Iter-2 ontology sync |
| `kg-v1-cycle-b-iter-2-aligned-2026-05-11` | `4525d47...` | Iter 2 base (PR #19) |
| `kg-v1-cycle-b-iter-3-aligned-2026-05-11` | `482ece91...` | Iter 3 delta (PR #20) |
| `kg-v1-cycle-b-run1-run2-aligned-2026-05-XX` (TBD) | post-Codex-delta HEAD | Run 1+Run 2 delta |

---

## 5. Pipeline primitive demonstration (P8 paper essence)

Cycle B demonstrates the **operational Manual ingest pipeline as programme primitive** (per memory `project_p8_pipeline_primitive_reframing_2026_05_11.md`):

```
New ES identified
   ↓
P7 normalization pipeline (substrate ingest + AppSec Core grounding)
   ↓
V1 ontology binding (per-entity source coverage via per_entity_source_map.json)
   ↓
Manual coverage analysis (V1 ↔ Manual rastreabilidade matrix)
   ↓
Gap classification:
   ├─ claim-gap → automated rastreabilidade refresh (entity-first exposure; zero new prose)
   ├─ cross-reference-gap → automated cross-chapter pointer (no relocation)
   ├─ content-gap → human authoring required OR future-work register
   ↓
Manual updated → KG regenerated (Codex delta single per cycle) → frozen snapshot tagged
```

Cycle B é ONE INSTANTIATION at 31-ES / V1-scale; subsequent cycles re-execute same pipeline with new ES.

### 5.1 Three-way routing demonstrated

Per chapter rastreabilidade exposes three routing layers:

| Routing class | Identification | Anchor |
|---|---|---|
| Core-mapped | Manual section ↔ V1 entity ↔ ES via per_entity_source_map.json | Cartographer canonical |
| Manual-only | Manual section com Manual ontology V2 entity sem V1 anchor; direct ES refs | Manual Agent editorial autoridade (4b ratified) |
| Out-of-AppSec | Manual section sem ES grounding (pure editorial) | Manual Agent editorial autoridade |

### 5.2 Empirical findings vs P2 v0 baseline

| Gap class | P2 v0 (5 frameworks; 36 entries) | V1 (31 sources; 38 entries) | Δ |
|---|---|---|---|
| claim_gap | 61% (22/36) | **82%** (31/38) | +21pp |
| cross_reference_gap | 19% (7/36) | 16% (6/38) | −3pp |
| content_gap | 11% (4/36) | **3%** (1/38) | −8pp |

V1-scale finding: Manual prose at V1 scale is MORE consistently authored than P2 v0 5-framework scale. Higher claim_gap + lower content_gap = gaps são predominantly em rastreabilidade exposure, NÃO em content authoring. Iter 3 Path D empirically confirms hypothesis: 31 claim-gaps closed com zero new prose authoring.

### 5.3 Manual ontology V2 entity surface (canonical extraction post-frozen)

Manual ontology V2 entity surface per chapter (canonical extraction per `cycle-b-frozen-2026-05-12`; Manual Agent + Cartographer cross-validated):

| Chapter | V2 entities surfaced |
|---|---|
| Cap. 02 (Requisitos) | 122 |
| Cap. 08 (IaC) | 87 |
| Cap. 07 (CI/CD) | 81 |
| Cap. 13 (Formação) | 79 |
| Cap. 14 (Governança) | 76 |

**Aggregate metrics (Cycle B canonical):**
- V1-overlay-minimal set (Caps 02/07/08/13/14): **445** V2 entities distintas
- Total V2 entities surfaced (all 15 chapters): **807**
- V1 substantive entities (7 chapters com V1 overlay): **203**
- V1 placeholder chapters: **8** (carry organisational scope; Manual-only at chapter level)

Implication for P8 paper: Manual ontology V2 has substantive intrinsic richness independent de AppSec Core V1 overlay. V1-overlay-minimal set alone has 445 V2 entities (quantitatively substantial Manual editorial autonomy preserved). Reforça pipeline primitive thesis (Manual editorial autonomy preserved; V1 overlay surfaces what's Core-mappable; Manual-only + out-of-AppSec layers preserve Manual richness).

Note: Run 1 placeholder analysis report (139/101/103/88/87) was informal initial count; Manual Agent canonical recount (122/81/87/79/76) supersedes per anti-archaeology discipline (`feedback_no_delta_archaeology_in_analysis.md`).

---

## 6. ACR registry — unchanged from Cycle A

| ACR | Status | Cycle B impact |
|---|---|---|
| ACR-001 | PROMOTED 2026-04-15 (Cycle A) | Cycle B applied — Manual chapter 04 ACO-RPR-008/009/010 references |
| ACR-002 | PROMOTED 2026-04-14 (Cycle A) | Cycle B applied — Manual chapter ACO-TMR-008 references |
| ACR-003 | CLOSED 2026-04-20 (Cycle A) | N/A |
| ACR-004 | PROMOTED 2026-05-05 (Cycle A) | Cycle B applied — Manual chapter ACO-IVF-008 anchor (Iter 1) |

No new ACR promotions during Cycle B. Manual editorial autoridade (per (4b) ratified 2026-05-11) used for Manual-only + Out-of-AppSec section declarations sem ACR scope.

---

## 7. Methodological commitments ratified during Cycle B

Programme-level position formalised through Cycle B iterations:

1. **P8 paper essence reframing (`project_p8_pipeline_primitive_reframing_2026_05_11.md`):** P8 reframed from "DSR Editorial Feedback cycle at V1 scale" to "demonstration of operational Manual ingest pipeline as programme primitive". Cycle B é ONE instantiation; pipeline composes ES → P7 → V1 → Manual coverage analysis → automated closure + flagged authoring.

2. **Manual ontology V2 finding (this Cycle):** Manual ontology V2 canonical YAML exists em `sbd-toe-knowledge-graph/ontology/sbdtoe-ontology.yaml`. `26-metodologia-validacao-claims.md` §2 reference confirmed correct. AppSec Core V1 + Manual ontology V2 são separate ontologies; alignment via overlay (Stream 1 future).

3. **§26 methodology vocabulary canonical (refreshed Cycle B):** Explícito / Semântico / Parcial / Reparação / Gap / Scope boundary — claim quality discipline labels usados per row em rastreabilidade tables.

4. **Three-way routing per chapter:** Core-mapped (V1 overlay) + Manual-only (V2 entities sem V1 anchor) + Out-of-AppSec (pure editorial). Demonstrates Manual editorial autonomy preserved sob V1 grounding pressure.

5. **Manual Agent editorial autoridade ratified (4b):** Manual Agent decisões sobre Manual-only + Out-of-AppSec sections são canonical sem programme-lead per-chapter review.

6. **2-run discipline para multi-document-family iterations (β approach):** When Manual content work involves multiple document families (rastreabilidade + maturity + threats), separate mechanical injection (Run 1) from editorial authoring (Run 2) para verificability + low scope creep.

7. **Single KG delta per cycle:** Codex re-compiles ONCE post Manual content work complete (não per-iteration); preserves consumer contract semver discipline.

---

## 8. Audit trail — joint tag references (pending frozen ceremony)

### 8.1 Cycle B frozen ceremony (4 peer tags)

| Repo | Tag | Pointer commit | Tag obj SHA |
|---|---|---|---|
| SbD-ToE-Manual | `cycle-b-frozen-2026-05-12` | `455124a1` (Run 2 HEAD) | `c838ea20a83073e13d6257a7e92f3f8df6380681` |
| sbd-toe-knowledge-graph | `cycle-b-frozen-2026-05-12` | `dacfaca` (master post FREEZE-REGISTRY backfill; KG v1.2 PR #21 merge `727d4c3d`) | `11369ef6cac79b7cfd86a21a3f75fb8637ad6c9d` |
| ExternalSourcesInventory | `cycle-b-frozen-2026-05-12` | `d5da1a0` (post-Cartographer-merge) | `7bd4404088fcb941b703aa3e321292cd738db3c2` |
| DevelopmentGovernance | `cycle-b-frozen-2026-05-12` | `db60b1b` (commit landing this consolidated brief) | `01f2b3e8c65eaf9b40a150953022d8282d260a08` |

### 8.2 Cycle B iteration anchor preserved

| Tag | Repo | Pointer | Iteration |
|---|---|---|---|
| `kg-v1-cycle-b-iter-2-aligned-2026-05-11` | sbd-toe-knowledge-graph | `4525d47` | Iter 2 base (PR #19) |
| `corpus-v1-ontology-sync-84fe8bf` | sbd-toe-knowledge-graph | `a9f68e7` | Ontology sync |
| `kg-v1-cycle-b-iter-3-aligned-2026-05-11` | sbd-toe-knowledge-graph | `482ece91` | Iter 3 delta (PR #20) |
| `kg-v1-cycle-b-run-2-aligned-2026-05-12` | sbd-toe-knowledge-graph | `727d4c3d` | Run 1+Run 2 delta (PR #21; consumer contract v1.2) |

### 8.3 Predecessor — Cycle A frozen state

| Tag | Repo | Pointer |
|---|---|---|
| `cycle-a-frozen-2026-05-08` | ExternalSourcesInventory | `0a1b897` |
| `cycle-a-frozen-2026-05-08` | sbd-toe-ontology | `6006e807` |
| `cycle-a-frozen-2026-05-08` | DevelopmentGovernance | `d107ddb` |

### 8.4 Key Cycle B records

- Iteration 1 delivery: `sbd-ai-runtime/handover/em-curso/2026-05-11-manual-cycle-b-iteration-1-delivery.md`
- Iteration 2 delivery: `2026-05-11-manual-cycle-b-iteration-2-delivery.md`
- Iteration 3 delivery: `2026-05-11-manual-cycle-b-iteration-3-delivery.md`
- Iteration 4 delivery: `2026-05-11-manual-cycle-b-iteration-4-delivery.md`
- Run 1 delivery: `2026-05-11-manual-cycle-b-run-1-delivery.md`
- Run 2 delivery: `2026-05-11-manual-cycle-b-run-2-delivery.md`
- Codex KG v1.0 delivery: `2026-05-11-codex-kg-recompile-against-v1-delivery.md`
- Codex KG v1.1 delivery: `2026-05-11-codex-kg-delta-iter-3-delivery.md`
- Codex KG v1.2 delivery: `2026-05-12-codex-kg-delta-run-2-delivery.md`
- Cartographer per-entity source map: ESI commit `aa3c13c`
- Cartographer Phase 1 delivery: `2026-05-11-cartographer-p8-gap-analysis-delivery.md`
- Cartographer Phase 2/3 delivery: `2026-05-11-cartographer-p8-gap-analysis-phase2-3-delta-delivery.md`

---

## 9. Paper authoring inputs

### 9.1 P8 paper (Pipeline Primitive Demonstration — Cycle B Manual + KG closure)

**Status:** Cycle B frozen state provides full empirical evidence base for P8 paper authoring.

**Core thesis:** *Operational Manual ingest pipeline composes ES → P7 normalization → V1 grounding → Manual coverage analysis → automated closure (claim + cross-ref) + flagged authoring (content). Pipeline demonstrably scales from P2 v0 5-framework baseline to V1 31-source corpus + Manual integration. Manual editorial autonomy preserved sob V1 grounding pressure via three-way routing (Core-mapped + Manual-only + Out-of-AppSec).*

**Empirical evidence available:**
- Cycle B 6-iteration arc (Iter 1+2+3+4 + Run 1+2)
- Three-way routing demonstrated per chapter (Core-mapped + Manual-only + Out-of-AppSec)
- §26 methodology labels deterministic mapping (Explícito/Semântico/Parcial/Gap/Scope boundary)
- Manual ontology V2 vocab integration (5/6-section structure per document family)
- KG runtime evolution v1.0 → v1.1 → v1.2 (single delta per cycle discipline)
- V1-scale findings vs P2 v0 baseline (claim_gap 61%→82%; content_gap 11%→3%)
- Manual ontology V2 entity surface finding (placeholder chapters reveal substantive intrinsic richness)

**Citation anchor:** `cycle-b-frozen-2026-05-12` (Manual + KG + ESI + DG peer tags) + `kg-v1-cycle-b-run-2-aligned-2026-05-12` + Cycle A predecessor tags (V1 ontology + substrate v7 + apparatus + embeddings).

### 9.2 P6 + P7 papers (Cycle A predecessors)

P6 + P7 final-draft state preserved em `sbd-ai-runtime/appsec-core-ontology-research` repo (tags `v2.0.0-construction-p6-final-draft` + `v2.0.0-construction-p7-final-draft`). Cycle B closure adds P8 to the v2.0.0 publication wave.

---

## 10. Future work register

### 10.1 P8 §10 candidates (registered durante Cycle B)

- **ACM-IVF-004** (Centralized Error Translation And Redaction; IVF slice) — registered Iter 3; pending authoring em subsequent cycle ou Stream 2 work
- Additional content gaps surfacing durante Iter 4 + Run 2 — registered per chapter future-work sections

### 10.2 Stream 1 — formal ontology alignment

AppSec Core V1 ↔ Manual ontology V2 formal alignment (OAEI / SKOS / EDOAL). Currently overlay-based (per_entity_source_map.json + Cartographer Phase 2/3); formalisation deferred to post-P8 work.

### 10.3 Stream 2 — Manual ontology V2 OWL+SHACL formalisation + corpus validation pipeline

- Manual ontology V2 → OWL representation (current YAML é estrutural, não W3C-formal)
- SHACL shapes enforce classification policy + authority/source/confidence constraints
- Automated corpus validation against ontology (operational pipeline)
- Cross-references: memory `project_appsec_core_manual_kg_alignment_2026_04_27.md`

### 10.4 Programme V3 future (verification layer)

Per Manual ontology V2 §`verification_scope.status: deferred_to_v3`: future V3 audit/verification layer modelling verification execution + persistent findings + validation history. Out of scope Cycle B closure.

### 10.5 Slice contracts back-fill

14-entity gap em sbd-toe-ontology slice contracts (245 KG-canonical vs 259 OWL-canonical). Deferred to future Archon cycle.

---

## 11. Sequence ahead

```
2026-05-12 — Cycle B Manual content work COMPLETE ✅
                ↓
        Codex KG delta re-compile (Run 1 + Run 2 single delta) ✅ (PR #21 @ `727d4c3d`; v1.2)
                ↓
        Cycle B FROZEN ✅ (4 peer cross-repo tags created 2026-05-12)
                ↓
        Curator P8 drafting dispatcher emit
                ↓
        P8 paper drafting (~2 weeks Curator)
                ↓
        v2.0.0 publication wave complete (P6 + P7 + P8 frozen final-drafts em public repo)
                ↓
        Stream 1 + Stream 2 + V3 verification layer — post-P8 programme work
```

---

## 12. Programme V1.B milestone

Cycle B frozen state extends programme V1 milestone (Cycle A 2026-05-08) com Manual + KG integration. Programme V1.B operational state:

- AppSec Core V1 (Cycle A; unchanged Cycle B)
- Substrate V1 (substrate v7; unchanged Cycle B)
- Apparatus V1 (apparatus-v3 composition; unchanged Cycle B)
- Embeddings V1.1 (unchanged Cycle B)
- **Manual ontology V2 + Manual content Run 2 baseline** (Cycle B output)
- **Manual KG v1.2** (Cycle B output; Codex PR #21 @ `727d4c3d`)
- Operational ingest pipeline demonstrated end-to-end

P8 paper anchors esta state; pipeline primitive thesis empirically validated.

Programme entered V1.B era 2026-05-12 (Cycle B frozen ceremony executed; 4 peer cross-repo tags created).

---

## 13. Change log

| Date | Change | Author |
|---|---|---|
| 2026-05-12 | Initial DRAFT post Cycle B Manual content work complete (Run 2 @ `455124a1`); pending Codex delivery + frozen ceremony | Orchestrator under Pedro Farinha |
| 2026-05-12 | Codex KG v1.2 delivered (PR #21 @ `727d4c3d`; tag `kg-v1-cycle-b-run-2-aligned-2026-05-12`); status → READY FOR RATIFICATION; pipeline output 1,964 linkage records; frozen tag anchors specified | Orchestrator under Pedro Farinha |
| 2026-05-12 | Programme-lead ratified Cycle B frozen ceremony ("1, 2c, 3 e 4 sim"); 4 peer cross-repo annotated tags `cycle-b-frozen-2026-05-12` created + pushed (DG `01f2b3e8` / Manual `c838ea20` / KG `11369ef6` / ESI `7bd44040`); status → RATIFIED; programme entered V1.B era | Orchestrator under Pedro Farinha |
| 2026-05-13 | P8 Phase 2 consultation packets delivered (Manual Agent + Codex + Archon + Cartographer); §5.3 V2 entity surface refreshed with canonical Manual Agent counts (122/87/81/79/76 + 445 V1-overlay-minimal aggregate + 807 total); Run 1 informal counts superseded per anti-archaeology discipline | Orchestrator under Pedro Farinha |
