# OLIR JSON Schema 1.1 — official NIST validator report

**Generated:** 2026-05-09
**Validator:** Python `jsonschema` 4.25.1 (Draft 4) against official NIST OLIR JSON Schema 1.1
**Schema source:** `https://www.nist.gov/document/olirschema` (downloaded + archived at `OLIR_Schema.json`)
**Schema id:** `https://csrc.nist.gov/1.1/olir_reference_document_json_1.1.schema`
**Substrate v7 anchor:** SUPPLIER SHA-256 `596783ed...62be04`; tag `substrate-v7-iter-3-ai-ml-incorporated`

## Headline

- **Pass: 31 / 31 pilot submissions**
- **Fail: 0 / 31**
- Total relationships emitted (all pilots): **16490**
- Relationships dropped (Cartographer 'unspecified' — not in OLIR schema enum): **0** (empirically 0 — substrate v7 GROUNDED items have sim ≥ E2 ≈ 0.41)

## Schema mapping summary

Cartographer's custom JSON crosswalk format → OLIR Schema 1.1 (Reference Document submission) translation:

| Cartographer field | OLIR Schema 1.1 field | Notes |
|---|---|---|
| `relationship_type: equal` | `relationship: equal to` | Schema uses spaces, not hyphens |
| `relationship_type: intersects-with` | `relationship: intersects with` | Schema uses spaces |
| `relationship_type: unspecified` | (DROPPED) | Schema enum doesn't include; empirically 0 rows in substrate v7 |
| `source_element.id` | `focalDocumentElement` | Pilot item is the Focal Document Element |
| `source_element.description` | `focalDocumentElementDescription` | |
| `reference_element.id` | `referenceDocumentElement` | AC V1 entity |
| `reference_element.description` | `referenceDocumentElementDescription` | |
| `strength` (cosine sim 0-1) | `strengthOfRelationship` (enum '0'-'10' / 'N/A') | int(round(sim × 10)) clamped 0-10 |
| `is_primary: true/false` | `groupIdentifier: 'primary' or 'secondary'` | |
| (free-text rationale) | `rationale: 'Semantic'` | Schema requires enum: Semantic/Syntactic/Functional. SBERT cosine = semantic alignment. |
| (implicit) | `fulfilledBy: 'Y'` | Asserted alignment per ratified Step 2 discipline. |

## Per-pilot validation

| Pilot | OLIR relationships | Dropped (unspecified) | Valid |
|---|---:|---:|:---:|
| `asvs_v5_0_0` | 1025 | 0 | ✅ |
| `capec_v3_9` | 1342 | 0 | ✅ |
| `cis_controls_v8_1_2` | 928 | 0 | ✅ |
| `cwe_software_development_view_v4_19_1` | 582 | 0 | ✅ |
| `enisa_multilayer_ai_cybersecurity_practices_2023` | 7 | 0 | ✅ |
| `eu_cra` | 25 | 0 | ✅ |
| `eu_dora` | 30 | 0 | ✅ |
| `eu_nis2` | 49 | 0 | ✅ |
| `eu_rgpd` | 43 | 0 | ✅ |
| `hipaa_security_rule` | 133 | 0 | ✅ |
| `mcp_official_security_foundations_2025` | 21 | 0 | ✅ |
| `mitre_atlas` | 592 | 0 | ✅ |
| `nist_ai_100_2_e2025` | 180 | 0 | ✅ |
| `nist_ai_rmf_1_0` | 102 | 0 | ✅ |
| `nist_sp800_53_rev5` | 6581 | 0 | ✅ |
| `owasp_dsomm` | 808 | 0 | ✅ |
| `owasp_llm_top_10` | 130 | 0 | ✅ |
| `owasp_mcp_secure_server_development_v1_0` | 60 | 0 | ✅ |
| `owasp_mcp_third_party_servers_v1_0` | 30 | 0 | ✅ |
| `owasp_mcp_top_10_v0_1_2025_beta` | 48 | 0 | ✅ |
| `owasp_ml_top_10` | 96 | 0 | ✅ |
| `owasp_proactive_controls_2018` | 68 | 0 | ✅ |
| `owasp_samm_v2_1` | 1079 | 0 | ✅ |
| `owasp_top_10_2021` | 46 | 0 | ✅ |
| `pci_dss_v4_0_1` | 1384 | 0 | ✅ |
| `pci_sslc_v1_1` | 253 | 0 | ✅ |
| `safecode_agile_2012` | 135 | 0 | ✅ |
| `safecode_fpssd_2018` | 123 | 0 | ✅ |
| `safecode_sic_2010` | 83 | 0 | ✅ |
| `slsa_spec_v1_0_build_track` | 92 | 0 | ✅ |
| `ssdf_sp800_218_v1_1` | 415 | 0 | ✅ |

## Methodology

All 31 per-pilot crosswalks were translated from Cartographer's custom JSON output (built per substrate v7 + Decision 0003 Amendment 1 §F augmentation symmetry) into OLIR Schema 1.1 conformant Reference Document submissions. Translation is deterministic Python (`scripts/olir/validate_olir_jsonschema.py`); zero LLM invocations during translation or validation step.

Schema-conformant outputs:

```
data/p7_olir_audit/p7_v2_corrected/v7/olir_exports/olir_schema_v1_1/
  OLIR_Schema.json                   ← official NIST schema (archived for reproducibility)
  <pilot>_olir_v1_1.json × 31        ← per-pilot OLIR Schema 1.1 conformant
  olir_schema_v1_1_validator_report.{md,json}  ← this report
```

## Limits / future work

- **NIST OLIR Validation Tool (Java JAR; .xlsx input)**: downloaded JAR (17.4 MB) for completeness; SHA3-256 `5809e7d9...` does NOT match published expected `ccd73e69...` (NIST page may be outdated; JAR file authenticity warrants independent verification before runtime use). JAR expects `.xlsx` Focal Document Template input which is a separate downloadable template (not bundled inside JAR). Full xlsx-roundtrip validation is deferred to programme-lead-authorized external submission (future work §13).
- **`subset of` / `superset of` / `not related to`**: not used in current submission (per ratified discipline; cosine similarity is undirected; SME refinement future work).
- **`comprehensive: 'No'`**: declared per current substrate (computational, not SME-curated). Future SME-curated submissions could declare `Yes`.
- **`securityCategorization` (Low/Moderate/High)**: not declared (optional; would require programme-lead determination).
