# OLIR validator report — substrate v7 OLIR exports

**Generated:** 2026-05-08
**Validator:** self-structural (IR 8278A r1 documented requirements)
**External NIST OLIR validator:** NOT invoked at generation time (see caveat below)

## Aggregate

- **Reference Document:** `appsec_core_v1_reference_doc.xml` + `.json` (212 Concepts; Slice 10 / CO 75 / Practice 69 / Mechanism 58)
- **Per-source Concept Crosswalks:** 31 pilots × 2 formats (XML + JSON) = 62 files
- **OLIR pairs emitted:** 16490 (2873 primary + 13617 secondary)
- **Relationship type distribution:**
  - `equal` (sim ≥ 0.6): 667
  - `intersects-with` (0.4 ≤ sim < 0.6): 15823
  - `unspecified` (sim < 0.4): 0

## Self-validator results

- Artefacts validated: 32
- Pass: **32** / Fail: 0

### Caveat — external validator not invoked

> External NIST OLIR validators (per https://csrc.nist.gov/projects/olir) not invoked at generation time — programme-lead may commission external OLIR submission review separately as part of OLIR registration future work (§13). Self-validation tests structural conformance against IR 8278A r1 documented requirements: namespaces, metadata blocks, STRM resource types, ratified relationship vocabulary.

## Per-artefact structural conformance

| Artefact | Type | Pass? | Checks |
|---|---|:---:|---|
| `appsec_core_v1_reference_doc.xml` | Reference Document | ✅ | 6/6 |
| `concept_crosswalk_asvs_v5_0_0.xml` | Concept Crosswalk | ✅ | 8/8 |
| `concept_crosswalk_capec_v3_9.xml` | Concept Crosswalk | ✅ | 8/8 |
| `concept_crosswalk_cis_controls_v8_1_2.xml` | Concept Crosswalk | ✅ | 8/8 |
| `concept_crosswalk_cwe_software_development_view_v4_19_1.xml` | Concept Crosswalk | ✅ | 8/8 |
| `concept_crosswalk_enisa_multilayer_ai_cybersecurity_practices_2023.xml` | Concept Crosswalk | ✅ | 8/8 |
| `concept_crosswalk_eu_cra.xml` | Concept Crosswalk | ✅ | 8/8 |
| `concept_crosswalk_eu_dora.xml` | Concept Crosswalk | ✅ | 8/8 |
| `concept_crosswalk_eu_nis2.xml` | Concept Crosswalk | ✅ | 8/8 |
| `concept_crosswalk_eu_rgpd.xml` | Concept Crosswalk | ✅ | 8/8 |
| `concept_crosswalk_hipaa_security_rule.xml` | Concept Crosswalk | ✅ | 8/8 |
| `concept_crosswalk_mcp_official_security_foundations_2025.xml` | Concept Crosswalk | ✅ | 8/8 |
| `concept_crosswalk_mitre_atlas.xml` | Concept Crosswalk | ✅ | 8/8 |
| `concept_crosswalk_nist_ai_100_2_e2025.xml` | Concept Crosswalk | ✅ | 8/8 |
| `concept_crosswalk_nist_ai_rmf_1_0.xml` | Concept Crosswalk | ✅ | 8/8 |
| `concept_crosswalk_nist_sp800_53_rev5.xml` | Concept Crosswalk | ✅ | 8/8 |
| `concept_crosswalk_owasp_dsomm.xml` | Concept Crosswalk | ✅ | 8/8 |
| `concept_crosswalk_owasp_llm_top_10.xml` | Concept Crosswalk | ✅ | 8/8 |
| `concept_crosswalk_owasp_mcp_secure_server_development_v1_0.xml` | Concept Crosswalk | ✅ | 8/8 |
| `concept_crosswalk_owasp_mcp_third_party_servers_v1_0.xml` | Concept Crosswalk | ✅ | 8/8 |
| `concept_crosswalk_owasp_mcp_top_10_v0_1_2025_beta.xml` | Concept Crosswalk | ✅ | 8/8 |
| `concept_crosswalk_owasp_ml_top_10.xml` | Concept Crosswalk | ✅ | 8/8 |
| `concept_crosswalk_owasp_proactive_controls_2018.xml` | Concept Crosswalk | ✅ | 8/8 |
| `concept_crosswalk_owasp_samm_v2_1.xml` | Concept Crosswalk | ✅ | 8/8 |
| `concept_crosswalk_owasp_top_10_2021.xml` | Concept Crosswalk | ✅ | 8/8 |
| `concept_crosswalk_pci_dss_v4_0_1.xml` | Concept Crosswalk | ✅ | 8/8 |
| `concept_crosswalk_pci_sslc_v1_1.xml` | Concept Crosswalk | ✅ | 8/8 |
| `concept_crosswalk_safecode_agile_2012.xml` | Concept Crosswalk | ✅ | 8/8 |
| `concept_crosswalk_safecode_fpssd_2018.xml` | Concept Crosswalk | ✅ | 8/8 |
| `concept_crosswalk_safecode_sic_2010.xml` | Concept Crosswalk | ✅ | 8/8 |
| `concept_crosswalk_slsa_spec_v1_0_build_track.xml` | Concept Crosswalk | ✅ | 8/8 |
| `concept_crosswalk_ssdf_sp800_218_v1_1.xml` | Concept Crosswalk | ✅ | 8/8 |

## Per-pilot stats

| Pilot | items | grounded | OLIR pairs | primary | secondary | equal | intersects-with | unspecified |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `asvs_v5_0_0` | 345 | 250 | 1025 | 250 | 775 | 49 | 976 | 0 |
| `capec_v3_9` | 559 | 355 | 1342 | 355 | 987 | 45 | 1297 | 0 |
| `cis_controls_v8_1_2` | 166 | 148 | 928 | 148 | 780 | 34 | 894 | 0 |
| `cwe_software_development_view_v4_19_1` | 399 | 152 | 582 | 152 | 430 | 20 | 562 | 0 |
| `enisa_multilayer_ai_cybersecurity_practices_2023` | 5 | 4 | 7 | 4 | 3 | 0 | 7 | 0 |
| `eu_cra` | 9 | 4 | 25 | 4 | 21 | 0 | 25 | 0 |
| `eu_dora` | 24 | 11 | 30 | 11 | 19 | 0 | 30 | 0 |
| `eu_nis2` | 4 | 4 | 49 | 4 | 45 | 0 | 49 | 0 |
| `eu_rgpd` | 6 | 3 | 43 | 3 | 40 | 0 | 43 | 0 |
| `hipaa_security_rule` | 22 | 19 | 133 | 19 | 114 | 2 | 131 | 0 |
| `mcp_official_security_foundations_2025` | 13 | 8 | 21 | 8 | 13 | 0 | 21 | 0 |
| `mitre_atlas` | 278 | 180 | 592 | 180 | 412 | 4 | 588 | 0 |
| `nist_ai_100_2_e2025` | 53 | 38 | 180 | 38 | 142 | 0 | 180 | 0 |
| `nist_ai_rmf_1_0` | 53 | 31 | 102 | 31 | 71 | 0 | 102 | 0 |
| `nist_sp800_53_rev5` | 1196 | 992 | 6581 | 992 | 5589 | 265 | 6316 | 0 |
| `owasp_dsomm` | 193 | 170 | 808 | 170 | 638 | 48 | 760 | 0 |
| `owasp_llm_top_10` | 10 | 9 | 130 | 9 | 121 | 7 | 123 | 0 |
| `owasp_mcp_secure_server_development_v1_0` | 10 | 10 | 60 | 10 | 50 | 2 | 58 | 0 |
| `owasp_mcp_third_party_servers_v1_0` | 8 | 6 | 30 | 6 | 24 | 0 | 30 | 0 |
| `owasp_mcp_top_10_v0_1_2025_beta` | 10 | 8 | 48 | 8 | 40 | 3 | 45 | 0 |
| `owasp_ml_top_10` | 10 | 9 | 96 | 9 | 87 | 4 | 92 | 0 |
| `owasp_proactive_controls_2018` | 10 | 10 | 68 | 10 | 58 | 12 | 56 | 0 |
| `owasp_samm_v2_1` | 90 | 90 | 1079 | 90 | 989 | 74 | 1005 | 0 |
| `owasp_top_10_2021` | 10 | 9 | 46 | 9 | 37 | 4 | 42 | 0 |
| `pci_dss_v4_0_1` | 217 | 201 | 1384 | 201 | 1183 | 38 | 1346 | 0 |
| `pci_sslc_v1_1` | 28 | 28 | 253 | 28 | 225 | 12 | 241 | 0 |
| `safecode_agile_2012` | 29 | 26 | 135 | 26 | 109 | 9 | 126 | 0 |
| `safecode_fpssd_2018` | 17 | 17 | 123 | 17 | 106 | 8 | 115 | 0 |
| `safecode_sic_2010` | 12 | 12 | 83 | 12 | 71 | 2 | 81 | 0 |
| `slsa_spec_v1_0_build_track` | 14 | 13 | 92 | 13 | 79 | 7 | 85 | 0 |
| `ssdf_sp800_218_v1_1` | 61 | 56 | 415 | 56 | 359 | 18 | 397 | 0 |

## Methodology — schema decisions ratified by programme-lead 2026-05-09

**Continuous → categorical translation (threshold-based):**
- `sim ≥ 0.6` → relationship-type `equal`
- `0.4 ≤ sim < 0.6` → relationship-type `intersects-with`
- `sim < 0.4` → relationship-type `unspecified`

**Multi-claim per source-item:**
- One OLIR row per (source-item, target-Core-entity) unique pair using highest-similarity claim for that target.
- `is-primary=true` marks item's overall highest-similarity claim's target (one primary per item).
- Lower-similarity claims to other targets become secondary OLIR rows (`is-primary=false`).

**Relationship vocabulary used (subset of IR 8477 6-element catalog):**
- `equal`, `intersects-with`, `unspecified` (3 of 6)

**Relationship vocabulary NOT used (first-cut limitation):**
- `subset-of`, `superset-of`: cosine similarity is undirected; cannot mechanically infer subset/superset directionality. SME refinement future work (§13).
- `not-related`: only emitted as absence (item with no claim ≥ 0.4 to a target produces no row for that target). Not explicitly emitted as `not-related` rows.

**STRM resource model (IR 8278A r1):**
- Pilot document → `DocumentaryImpl`
- Source item → `ConcreteImpl`
- AppSec Core V1 → Reference Document
- Core entity (CO/Practice/Mechanism/Slice) → `Concept`

**Substrate v7 anchor:** SUPPLIER SHA-256 `596783ed984d9c0e8c8ef6439a0eaee8fbaf2d863af37138cde8fad55d62be04`; tag `substrate-v7-iter-3-ai-ml-incorporated`; cycle-a-frozen-2026-05-08.

## Future work (§13 — out of scope for this generation)

- SME review of individual mappings + κ inter-rater reliability
- NIST CRWS peer submission
- OLIR registration via NIST OLIR Submission Tool
- subset-of / superset-of vocabulary extension (requires directional information beyond cosine similarity)
- External NIST OLIR validator pass (requires programme-lead authorization for external submission)