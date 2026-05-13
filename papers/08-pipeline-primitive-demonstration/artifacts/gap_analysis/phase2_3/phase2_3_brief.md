# P8 Gap Analysis Phase 2/3 — Claim Gap + Cross-Reference Gap Detection

**Date:** 2026-05-11
**Phase:** 2/3 augment to Phase 1 delivery (commit `b6133a1`)
**Method:** Deterministic keyword-based semantic match; LLM-free; reproducible.
**Discipline:** Cartographer FLAGS candidates via keyword evidence; human inspection finalises per P2 v0 Pass 3.

## Refined classification of 38 Phase-1 content_gap entries

| Refined classification | Count | % of 38 |
|---|---:|---:|
| `candidate_claim_gap` | 31 | 81.6% |
| `candidate_cross_reference_gap` | 6 | 15.8% |
| `confirmed_content_gap` | 1 | 2.6% |

## Distribution by match strength

| Match strength | Count | Interpretation |
|---|---:|---|
| strong_expected | 31 | ≥3 keywords + ≥5 occurrences in expected chapter |
| strong_other | 6 | ≥3 keywords + ≥5 occurrences only in non-expected chapter(s) |
| weak | 1 | Matches below strong threshold |

## Refined V1 gap taxonomy (V1 entity total = 259)

| Classification | Count |
|---|---:|
| `candidate_claim_gap` (Manual prose covers; rastreabilidade exposure pending; needs verification) | 31 |
| `candidate_cross_reference_gap` (Manual covers in non-expected chapter; needs verification) | 6 |
| `confirmed_content_gap` (genuine authoring deficit; weak or no keyword matches) | 1 |
| `scope_exclusion` (Artifact entities; substrate v7 architectural design) | 57 |

**Total V1 gaps:** 95 (unchanged from Phase 1).
**Refined V1 coverage status:** 164 covered + 95 gaps = 259; the 38 content_gap entries now have refined classification within the 95 gap subset.

## P2 v0 comparison (historical context only — NOT scaling proxy)

Per dispatcher §Phase 2/3 background, P2 v0 found:
- 22/36 apparent gaps = claim gaps (61%)
- 7/36 cross-reference gaps (19%)
- 4/36 content gaps (11%)
- 3/36 scope exclusions (8%)

At V1 scale (38 apparent gaps post-Phase-1; excluding 57 Artifact scope_exclusions):
- candidate_claim_gap: 31/38 (81.6%)
- candidate_cross_reference_gap: 6/38 (15.8%)
- confirmed_content_gap: 1/38 (2.6%)

Comparison with P2 v0 reserved for Curator §discussion (programme-lead 2026-05-11 reminder: distribution similarity expected IF Manual consistently authored; substantive divergence is finding).

## Candidate claim_gap entities (top by match strength)

| entity_id | type | slice | expected chapter | strong-match in expected | keywords matched |
|---|---|---|---|---|---|
| `ACP-SCBI-005` | Practice | SCBI | `05-dependencias-sbom-sca` | 7kw × 89 | approval, enforce, gates, generation, policy |
| `ACP-SCBI-007` | Practice | SCBI | `05-dependencias-sbom-sca` | 4kw × 164 | build, container, policy, supply |
| `ACM-SCBI-006` | Mechanism | SCBI | `05-dependencias-sbom-sca` | 5kw × 29 | enforcement, proxy, registries, registry, source |
| `ACM-IAT-005` | Mechanism | IAT | `04-arquitetura-segura` | 4kw × 35 | boundaries, gateway, identity, service |
| `ACP-ATB-006` | Practice | ATB | `04-arquitetura-segura` | 5kw × 76 | architecture, governance, review, thresholds, trigger |
| `ACP-TSV-007` | Practice | TSV | `10-testes-seguranca` | 4kw × 100 | final, release, review, test |
| `ACP-TMR-006` | Practice | TMR | `03-threat-modeling` | 5kw × 381 | go-live, model, models, review, threat |
| `ACP-TMR-007` | Practice | TMR | `03-threat-modeling` | 7kw × 391 | access, artifacts, lifecycle, model, review |
| `ACP-TMR-008` | Practice | TMR | `03-threat-modeling` | 5kw × 305 | models, policies, requirements, risk, threat |
| `ACP-TMR-009` | Practice | TMR | `03-threat-modeling` | 3kw × 13 | compliance, development, requirements |
| `ACP-IVF-002` | Practice | IVF | `06-desenvolvimento-seguro` | 4kw × 13 | accepted, allowlist, enforcement, validation |
| `ACP-IVF-007` | Practice | IVF | `06-desenvolvimento-seguro` | 4kw × 14 | encoding, escaping, html, output |
| `ACM-IVF-005` | Mechanism | IVF | `06-desenvolvimento-seguro` | 3kw × 19 | html, json, output |
| `ACP-ITS-005` | Practice | ITS | `04-arquitetura-segura` | 4kw × 49 | integration, interface, review, trust |
| `ACP-ITS-006` | Practice | ITS | `04-arquitetura-segura` | 5kw × 33 | calls, context, logging, record, review |
| `ACM-ITS-005` | Mechanism | ITS | `04-arquitetura-segura` | 5kw × 33 | calls, context, logging, record, review |
| `ACP-RPR-002` | Practice | RPR | `11-deploy-seguro` | 5kw × 108 | artifact, identity, promotion, provenance, release |
| `ACP-RPR-003` | Practice | RPR | `11-deploy-seguro` | 5kw × 117 | gate, gates, policy, promotion, staging |
| `ACP-RPR-005` | Practice | RPR | `11-deploy-seguro` | 4kw × 198 | production, rollback, rollout, runtime |
| `ACP-RPR-006` | Practice | RPR | `11-deploy-seguro` | 3kw × 29 | change, progressive, rollout |
| _... and 11 more_ | | | | | |

## Candidate cross_reference_gap entities

| entity_id | type | slice | expected | found in (strong) |
|---|---|---|---|---|
| `ACM-IAT-006` | Mechanism | IAT | `04-arquitetura-segura` | 03-threat-modeling, 12-monitorizacao-operacoes, 14-governanca-contratacao |
| `ACP-ATB-007` | Practice | ATB | `04-arquitetura-segura` | 03-threat-modeling, 08-iac-infraestrutura, 13-formacao-onboarding |
| `ACP-SPC-005` | Practice | SPC | `06-desenvolvimento-seguro` | 07-cicd-seguro, 08-iac-infraestrutura, 11-deploy-seguro |
| `ACP-SPC-006` | Practice | SPC | `06-desenvolvimento-seguro` | 00-fundamentos, 05-dependencias-sbom-sca, 07-cicd-seguro, 13-formacao-onboarding, 14-governanca-contratacao |
| `ACP-IVF-006` | Practice | IVF | `06-desenvolvimento-seguro` | 00-fundamentos, 07-cicd-seguro, 10-testes-seguranca, 12-monitorizacao-operacoes, 13-formacao-onboarding, 14-governanca-contratacao |
| `ACM-ITS-003` | Mechanism | ITS | `04-arquitetura-segura` | 14-governanca-contratacao |

## Methodology notes (verbatim)

**Keyword extraction:** From `augmented-text-corpus.json` per-entity `augmented_text` field; tokenize + filter stopwords (PT+EN) + drop entity-ID parts + drop slice abbreviation + drop tokens shorter than 4 chars; keep top 12 by frequency.

**Matching:** Whole-word, case-insensitive across Manual chapter prose (`canon/*` + `addon/*` + `intro.md` + `recomendacoes-avancadas.md` — `25-rastreabilidade.md` EXCLUDED to avoid trivial via-rastreabilidade-table matches).

**Strong-match threshold:** ≥3 distinct keywords matched AND ≥5 total occurrences in a chapter. Below threshold = weak match.

**Classification logic:**
1. NO matches → `confirmed_content_gap`
2. STRONG match in expected chapter → `candidate_claim_gap`
3. STRONG match ONLY in non-expected chapters → `candidate_cross_reference_gap`
4. ONLY weak matches → `confirmed_content_gap` (with weak-match note)

**Discipline preserved (per dispatcher):** `candidate_*` labels signal that automated heuristic flagged the entity; final classification requires human verification of semantic relevance per P2 v0 Pass 3. Cartographer output is decision-grade EVIDENCE TRAIL, not final verdict.

## Per-entity evidence detail

Full per-entity record with extracted keywords + per-chapter match counts + classification rationale: `data/p8_gap_analysis/phase2_3/phase2_3_per_entity_classification.json` (~166,807 bytes).

## Cross-references

- Phase 1 delivery: `2026-05-11-cartographer-p8-gap-analysis-delivery.md` (commit `b6133a1`)
- Dispatcher Phase 2/3 activation: programme-lead Pedro Farinha 2026-05-11 ratification
- Augmented text corpus: `sbd-toe-ontology/formal/appsec_core/08-embeddings/augmented-text-corpus.json`
- Slice → chapter map: `data/p7_olir_audit/p7_v2_corrected/canon_rewrite/slice_to_chapter_map.yaml`
- Manual base: `SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/` (Iter 2 base `b1d129f0`)

