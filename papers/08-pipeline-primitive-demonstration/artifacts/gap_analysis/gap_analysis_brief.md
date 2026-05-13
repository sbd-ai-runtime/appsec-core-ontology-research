# P8 Gap Analysis Brief — V1 Scale (Manual Validation)

**Date:** 2026-05-11
**Author:** Cartographer (under programme-lead Pedro Farinha)

**Anchors (fresh compute; NO delta archaeology):**
- V1 ontology: tag `ontology-v1.1-fair-baseline` @ `84fe8bf` (259 entities via belongsToSlice OWL triples)
- Substrate v7: tag `cycle-a-frozen-2026-05-08` (SUPPLIER sha256 `596783ed984d9c0e8c8ef6439a0eaee8fbaf2d863af37138cde8fad55d62be04`)
- Manual: commit `b1d129f0` (Iter 2 base; includes Iter 1 rastreabilidade-regen + Iter 2 AI/ML extension)
- Codex KG linkage: `manual_rastreabilidade_iter2.jsonl` (2,835 records; anchor at ``)

## Overall V1 → Manual coverage

- **V1 entities total:** **259**
- **Covered (specific OR via slice):** **164** (63.32%)
- Covered (specific anchor): 89
- Covered (via slice anchor; CO entities only): 75
- **Gap:** 95

### Gap taxonomy breakdown

| Classification | Count |
|---|---:|
| `content_gap` | 38 |
| `scope_exclusion` | 57 |

## Per-slice coverage (10 slices)

| Slice | Total | Covered (specific) | Covered (via slice) | Gap | Coverage % |
|---|---:|---:|---:|---:|---:|
| `ASC-01` | 30 | 10 | 7 | 13 | 56.7% |
| `ASC-02` | 25 | 10 | 7 | 8 | 68.0% |
| `ASC-03` | 23 | 10 | 7 | 6 | 73.9% |
| `ASC-04` | 25 | 11 | 7 | 7 | 72.0% |
| `ASC-05` | 29 | 13 | 8 | 8 | 72.4% |
| `ASC-06` | 19 | 8 | 7 | 4 | 78.9% |
| `ASC-07` | 26 | 7 | 8 | 11 | 57.7% |
| `ASC-08` | 23 | 7 | 7 | 9 | 60.9% |
| `ASC-09` | 39 | 6 | 10 | 23 | 41.0% |
| `ASC-10` | 20 | 7 | 7 | 6 | 70.0% |

## Per-substrate-source linkage support

| Substrate source | Linkage records | Manual chapters | V1 anchors |
|---|---:|---:|---:|
| `nist_sp_800_53` | 989 | 7 | 55 |
| `mitre_capec` | 355 | 7 | 24 |
| `owasp_asvs` | 250 | 6 | 23 |
| `mitre_atlas` | 180 | 7 | 10 |
| `owasp_dsomm` | 170 | 7 | 31 |
| `pci_dss` | 165 | 7 | 31 |
| `mitre_cwe` | 152 | 7 | 23 |
| `cis_controls` | 148 | 7 | 36 |
| `owasp_samm` | 90 | 7 | 22 |
| `nist_ssdf` | 55 | 7 | 18 |
| `safecode` | 55 | 7 | 23 |
| `nist_ai_100_2` | 38 | 6 | 8 |
| `nist_ai_rmf` | 31 | 6 | 7 |
| `pci_secure_slc` | 28 | 7 | 13 |
| `owasp_mcp` | 23 | 5 | 16 |
| `hipaa` | 19 | 5 | 12 |
| `slsa` | 13 | 4 | 3 |
| `eu_dora` | 11 | 5 | 7 |
| `owasp_proactive_controls` | 10 | 4 | 5 |
| `owasp_llm_top_10` | 9 | 4 | 5 |
| _... and 7 more_ | | | |

## Manual section routing (empirical delta)

- Total Manual sections (with linkage entries): **322**
- core_mapped (≥1 V1 anchor): **7**
- manual_only (in AppSec; outside V1 bounds): 315
- out_of_appsec: 0

**manual_only examples (first 10):**

- `03-threat-modeling/addon/00-catalogo-requisitos.md`
- `04-arquitetura-segura/addon/01-catalogo-requisitos.md`
- `05-dependencias-sbom-sca/addon/00-catalogo-requisitos.md`
- `06-desenvolvimento-seguro/recomendacoes-avancadas.md`
- `12-monitorizacao-operacoes/addon/00-catalogo-requisitos.md`
- `00-fundamentos/baseline.md`
- `00-fundamentos/canon/25-rastreabilidade.md`
- `00-fundamentos/canon/26-metodologia-validacao-claims.md`
- `00-fundamentos/intro.md`
- `00-fundamentos/roles-responsabilidades/appsec-engineer.md`

## Methodology notes (verbatim)

**Coverage status semantics:**
- `covered_specific`: V1 entity has ≥1 direct Codex linkage anchor (`v1_anchor_id == entity_id`); applies to specific Practice/Mechanism entities.
- `covered_via_slice`: V1 entity (typically CO) covered via slice-level anchor (`v1_anchor_id == ACO-<slice_abbrev>`); weaker than specific anchor but valid V1 → Manual evidence.
- `gap`: no anchors → classified per gap taxonomy.

**Gap taxonomy (P2 v0 §4.5 preserved at V1 scale):**
- `claim_gap`: Manual prose covers area BUT rastreabilidade has no entry (Codex linkage absence + Manual content presence; not detected here — requires Manual prose semantic analysis).
- `content_gap`: NO Manual content covers V1 entity (default classification for non-Artifact gap entities here; refinable via deeper Manual content analysis).
- `cross_reference_gap`: covered in unexpected chapter (not detected here — requires expected-chapter mapping per slice).
- `scope_exclusion`: V1 entity intentionally NOT covered (default for Artifact entities since substrate v7 doesn't ground at Artifact level — architectural design, not authoring deficit).

**Three-way routing (P6/P7 §10):**
- `core_mapped`: Manual section maps to ≥1 V1 entity (per linkage).
- `manual_only`: Manual section has linkage records BUT no V1 anchors (or anchors NULL); content in AppSec scope but outside V1 ontology bounds.
- `out_of_appsec`: Manual section NOT in AppSec scope at all (not detected via current linkage; would need explicit signal).

## Out of scope (per dispatcher)

- Cycle B frozen ceremony tag creation (Orchestrator; post-analysis)
- Curator P8 manuscript drafting (Curator territory)
- Manual ontology formal (Stream 2; separate paper)
- Substrate v8 re-grounding (deferred)

## Cross-references

- Dispatcher: `sbd-ai-runtime/handover/em-curso/2026-05-11-orchestrator-cartographer-p8-gap-analysis-dispatch.md`
- V1 entity index: `sbd-toe-ontology/ontology/appsec-core-v0-instance-index.yaml`
- OWL formal: `sbd-toe-ontology/formal/appsec_core/02-owl/exports/appsec-core-v0-bounded-v1.ttl`
- Substrate v7 SUPPLIER: `data/p7_olir_audit/p7_v2_corrected/v7/SUPPLIER_v7_0.json`
- Codex KG linkage: `sbd-toe-knowledge-graph/data/publish/runtime/v1/manual_rastreabilidade_iter2.jsonl` (2,835 records)
- Cartographer per-entity source map: `data/p8_inputs/per_entity_source_map.json` (commit `aa3c13c`)
- P2 v0 methodology reference: `papers/02-coverage-preserving-knowledge-compilation/source/manuscript.md` (gap taxonomy + routing semantics; historical context only)

