# Source Provenance — Consolidated (31-source corpus, substrate v7)

**Date:** 2026-05-09
**Author:** Cartographer (under programme-lead Pedro Farinha)
**Substrate:** v7 (`SUPPLIER_v7_0.json` SHA `596783ed984d9c0e8c8ef6439a0eaee8fbaf2d863af37138cde8fad55d62be04`)
**Generator:** `scripts/build_source_provenance_consolidated.py` (deterministic Python)

This document consolidates per-source provenance across both repo conventions:
- **26 baseline sources:** `pilots/<source>/source_manifest.yaml` (multi-schema; canonical_url + doi_url + checksum + retrieved_at)
- **5 iter-3 sources** (mitre_atlas, nist_ai_100_2_e2025, nist_ai_rmf_1_0, owasp_llm_top_10, owasp_ml_top_10): `data/<source>/stubs/source_retrieval_receipt.json` (uniform schema; origin_url + sha256 + retrieved_at + version)

Both conventions provide URL + version + access date + checksum + local snapshot path. This single artefact is reviewer-citable as the unified provenance source-of-truth for the substrate v7 corpus.

## Per-source provenance table

| # | Source | Title | Publisher | Version | Publication date | URL (canonical / origin) | DOI | sha256 (primary) | Retrieved | Artefacts |
|---:|---|---|---|---|---|---|---|---|---|---:|
| 1 | `asvs_v5_0_0` | OWASP Application Security Verification Standard — Version 5… | OWASP Foundation | 5.0.0 | 2025-05-30 | https://github.com/OWASP/ASVS/releases/tag/v5.0.0_release | — | `2d780ff96782…` | 2025-05-30 | 1 |
| 2 | `capec_v3_9` | CAPEC Attack Pattern Catalog v3.9 | MITRE_CAPEC | 3.9 |  | https://capec.mitre.org/data/xml/capec_latest.xml | — | `70279a2dff0c…` | 2026-04-13 | 1 |
| 3 | `cis_controls_v8_1_2` | CIS Controls Version 8.1.2 (March 2025) | CIS_CONTROLS | 8.1.2 |  | https://learn.cisecurity.org/cis-controls-download | — | `56ee1b73be5d…` | 2026-04-13 | 2 |
| 4 | `cwe_software_development_view_v4_19_1` | CWE View 699 - Software Development | MITRE | 4.19.1 | 2026-01-21 | https://cwe.mitre.org/data/definitions/699.html | — | `ac28f1ddf07b…` | 2026-04-03 | 1 |
| 5 | `enisa_multilayer_ai_cybersecurity_practices_2023` | Multilayer Framework for Good Cybersecurity Practices for AI… | ENISA | 2023-06-07 | 2023-06-07 | https://www.enisa.europa.eu/publications/multilayer-framework-for-good-cybersecurity-practices-for-ai | — | `808955a45673…` | 2026-04-04 | 1 |
| 6 | `eu_cra` | Cyber Resilience Act (CRA) | European Union |  |  | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R2847 | — | `e3ecaabddf6e…` | 2026-05-09 | 1 |
| 7 | `eu_dora` | Digital Operational Resilience Act (DORA) | European Union |  |  | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022R2554 | — | `85307f9e2a04…` | 2026-05-09 | 1 |
| 8 | `eu_nis2` | Network and Information Security Directive (NIS2) | European Union |  |  | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022L2555 | — | `20d29e9c5300…` | 2026-05-09 | 1 |
| 9 | `eu_rgpd` | General Data Protection Regulation (GDPR) | European Union |  |  | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679 | — | `bd84e63f5b62…` | 2026-05-09 | 1 |
| 10 | `hipaa_security_rule` | HIPAA Security Rule (45 CFR Part 164, Subpart C) | U.S. Department of Health and Human Services (HHS) | CFR 2023 | 2003-02-20 | https://www.hhs.gov/hipaa/for-professionals/security/laws-regulations/index.html | — | `84622f565b19…` | 2026-04-13 | 1 |
| 11 | `mcp_official_security_foundations_2025` | MCP Authorization | mcp_official_security_docs |  | 2025-11-25 | https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization | — | `f24df721f884…` | — | 2 |
| 12 | `mitre_atlas` | SRC-ATLAS-V5_6_0 | MITRE_ATLAS | 5.6.0 |  | https://raw.githubusercontent.com/mitre-atlas/atlas-data/main/dist/ATLAS.yaml | — | `8a5693df5113…` | 2026-05-07 | 1 |
| 13 | `nist_ai_100_2_e2025` | Adversarial Machine Learning: A Taxonomy and Terminology of … | NIST_AI | AI 100-2 E2025 | 2025-03-24 | https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-2e2025.pdf | — | `4811fb6ad73f…` | 2026-05-07 | 1 |
| 14 | `nist_ai_rmf_1_0` | Artificial Intelligence Risk Management Framework (AI RMF 1.… | NIST_AI | AI RMF 1.0 / NIST AI 100-1 | 2023-01 | https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf | — | `7576edb531d9…` | 2026-05-07 | 1 |
| 15 | `nist_sp800_53_rev5` | Security and Privacy Controls for Information Systems and Or… | NIST | Rev 5 | 2020-09-23 | https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final | https://doi.org/10.6028/NIST.SP.800-53r5 | `cc4ad0c9e759…` | 2026-04-12 | 1 |
| 16 | `owasp_dsomm` | OWASP DevSecOps Maturity Model — Generated model snapshot 4.… | OWASP Foundation / OWASP DevSecOps Project | 4.2.0 | 2026-04-05 | https://dsomm.owasp.org | — | `e365b0f08af8…` | 2026-04-05 | 1 |
| 17 | `owasp_llm_top_10` | SRC-OWASP-LLM-HUB-2025 | OWASP_GenAI | 2025 |  | https://genai.owasp.org/llm-top-10/ | — | `3bfa21c53bd9…` | 2026-05-07 | 11 |
| 18 | `owasp_mcp_secure_server_development_v1_0` | A Practical Guide for Secure MCP Server Development | OWASP Gen AI Security Project | 1.0 | 2026-02-16 | https://genai.owasp.org/resource/a-practical-guide-for-secure-mcp-server-development/ | — | `e0681dc7f640…` | 2026-04-03 | 1 |
| 19 | `owasp_mcp_third_party_servers_v1_0` | A Practical Guide for Securely Using Third-Party MCP Servers | OWASP GenAI Security Project | 1.0 | 2025-11-04 | https://genai.owasp.org/resource/cheatsheet-a-practical-guide-for-securely-using-third-party-mcp-servers-1-0/ | — | `694452661fcc…` | 2026-04-04 | 1 |
| 20 | `owasp_mcp_top_10_v0_1_2025_beta` | OWASP MCP Top 10 | OWASP Foundation | v0.1 |  | https://owasp.org/www-project-mcp-top-10/ | — | `41ec2354bdba…` | 2026-04-04 | 1 |
| 21 | `owasp_ml_top_10` | SRC-OWASP-ML-HUB-2023 | OWASP_ML | 0.3 Draft (2023) |  | https://owasp.org/www-project-machine-learning-security-top-10/ | — | `23114d044ed5…` | 2026-05-07 | 11 |
| 22 | `owasp_proactive_controls_2018` | OWASP Proactive Controls 2018 | OWASP | 3.0 | 2018-01-01 | https://owasp.org/www-project-proactive-controls/ | — | `c11d050724b6…` | 2026-04-12 | 1 |
| 23 | `owasp_samm_v2_1` | OWASP Software Assurance Maturity Model — Version 2 model li… | OWASP Foundation / OWASP SAMM Project | 2 | 2020-01-31 | https://owaspsamm.org/model/ | — | `0069f5ce10f7…` | 2026-04-05 | 1 |
| 24 | `owasp_top_10_2021` | OWASP Top 10:2021 | OWASP | 2021 | 2021-09-24 | https://owasp.org/Top10/ | — | `1dd91b2e1bfd…` | 2026-04-12 | 1 |
| 25 | `pci_dss_v4_0_1` | Payment Card Industry Data Security Standard v4.0.1 | PCI Security Standards Council | 4.0.1 | 2024-06-01 | https://www.pcisecuritystandards.org/document_library/ | — | `5e6b9093b840…` | 2026-04-13 | 1 |
| 26 | `pci_sslc_v1_1` | PCI Software Security Framework: Secure Software Lifecycle R… | PCI Security Standards Council | 1.1 | 2021-02 | https://www.pcisecuritystandards.org/document_library?category=sware_sec | — | `a4f959b130e8…` | 2026-04-14 | 1 |
| 27 | `safecode_agile_2012` | Practical Security Stories and Security Tasks for Agile Deve… | SAFECode | 1.0 | 2012-07-17 | https://safecode.org/publication/SAFECode_Agile_Dev_Security0712.pdf | — | `0261982c92b7…` | 2026-04-14 | 1 |
| 28 | `safecode_fpssd_2018` | Fundamental Practices for Secure Software Development: Essen… | SAFECode | 3rd edition | 2018-03 | https://safecode.org/wp-content/uploads/2018/03/SAFECode_Fundamental_Practices_for_Secure_Software_Development_March_2018.pdf | — | `9a9a07b5fab1…` | 2026-04-14 | 1 |
| 29 | `safecode_sic_2010` | Software Integrity Controls: An Assurance-Based Approach to … | SAFECode | 1.0 | 2010-06-14 | https://safecode.org/publication/SAFECode_Software_Integrity_Controls0610.pdf | — | `pending…` | 2026-04-14 | 1 |
| 30 | `slsa_spec_v1_0_build_track` | SLSA v1.0 Build Track and Verification Surface | SLSA project | 1.0 | 2023-05-18 | https://slsa.dev/spec/v1.0/ | — | `bb85b967d27c…` | 2026-04-03 | 5 |
| 31 | `ssdf_sp800_218_v1_1` | Secure Software Development Framework (SSDF) Version 1.1 — R… | NIST | 1.1 | 2022-02-03 | https://csrc.nist.gov/pubs/sp/800/218/final | https://doi.org/10.6028/NIST.SP.800-218 | `617746e553a9…` | 2026-04-03 | 1 |

## Schema source per row

| Source | Schema source path |
|---|---|
| `asvs_v5_0_0` | `pilots/asvs_v5_0_0/source_manifest.yaml` |
| `capec_v3_9` | `pilots/capec_v3_9/source_manifest.yaml` |
| `cis_controls_v8_1_2` | `pilots/cis_controls_v8_1_2/source_manifest.yaml` |
| `cwe_software_development_view_v4_19_1` | `pilots/cwe_software_development_view_v4_19_1/source_manifest.yaml` |
| `enisa_multilayer_ai_cybersecurity_practices_2023` | `pilots/enisa_multilayer_ai_cybersecurity_practices_2023/source_manifest.yaml` |
| `eu_cra` | `pilots/eu_cra/source_manifest.yaml` |
| `eu_dora` | `pilots/eu_dora/source_manifest.yaml` |
| `eu_nis2` | `pilots/eu_nis2/source_manifest.yaml` |
| `eu_rgpd` | `pilots/eu_rgpd/source_manifest.yaml` |
| `hipaa_security_rule` | `pilots/hipaa_security_rule/source_manifest.yaml` |
| `mcp_official_security_foundations_2025` | `pilots/mcp_official_security_foundations_2025/source_manifest.yaml` |
| `mitre_atlas` | `data/mitre_atlas/stubs/source_retrieval_receipt.json` |
| `nist_ai_100_2_e2025` | `data/nist_ai_100_2_e2025/stubs/source_retrieval_receipt.json` |
| `nist_ai_rmf_1_0` | `data/nist_ai_rmf_1_0/stubs/source_retrieval_receipt.json` |
| `nist_sp800_53_rev5` | `pilots/nist_sp800_53_rev5/source_manifest.yaml` |
| `owasp_dsomm` | `pilots/owasp_dsomm/source_manifest.yaml` |
| `owasp_llm_top_10` | `data/owasp_llm_top_10/stubs/source_retrieval_receipt.json` |
| `owasp_mcp_secure_server_development_v1_0` | `pilots/owasp_mcp_secure_server_development_v1_0/source_manifest.yaml` |
| `owasp_mcp_third_party_servers_v1_0` | `pilots/owasp_mcp_third_party_servers_v1_0/source_manifest.yaml` |
| `owasp_mcp_top_10_v0_1_2025_beta` | `pilots/owasp_mcp_top_10_v0_1_2025_beta/source_manifest.yaml` |
| `owasp_ml_top_10` | `data/owasp_ml_top_10/stubs/source_retrieval_receipt.json` |
| `owasp_proactive_controls_2018` | `pilots/owasp_proactive_controls_2018/source_manifest.yaml` |
| `owasp_samm_v2_1` | `pilots/owasp_samm_v2_1/source_manifest.yaml` |
| `owasp_top_10_2021` | `pilots/owasp_top_10_2021/source_manifest.yaml` |
| `pci_dss_v4_0_1` | `pilots/pci_dss_v4_0_1/source_manifest.yaml` |
| `pci_sslc_v1_1` | `pilots/pci_sslc_v1_1/source_manifest.yaml` |
| `safecode_agile_2012` | `pilots/safecode_agile_2012/source_manifest.yaml` |
| `safecode_fpssd_2018` | `pilots/safecode_fpssd_2018/source_manifest.yaml` |
| `safecode_sic_2010` | `pilots/safecode_sic_2010/source_manifest.yaml` |
| `slsa_spec_v1_0_build_track` | `pilots/slsa_spec_v1_0_build_track/source_manifest.yaml` |
| `ssdf_sp800_218_v1_1` | `pilots/ssdf_sp800_218_v1_1/source_manifest.yaml` |

## Notes

### `asvs_v5_0_0`
- cross-confirmation: also present at data/asvs_v5_0_0/stubs/source_retrieval_receipt.json (4 artefacts)

### `cwe_software_development_view_v4_19_1`
- cross-confirmation: also present at data/cwe_software_development_view_v4_19_1/stubs/source_retrieval_receipt.json (4 artefacts)

### `enisa_multilayer_ai_cybersecurity_practices_2023`
- cross-confirmation: also present at data/enisa_multilayer_ai_cybersecurity_practices_2023/stubs/source_retrieval_receipt.json (2 artefacts)

### `eu_cra`
- cross-confirmation: also present at data/eu_cra/stubs/source_retrieval_receipt.json (1 artefacts)

### `eu_dora`
- cross-confirmation: also present at data/eu_dora/stubs/source_retrieval_receipt.json (1 artefacts)

### `eu_nis2`
- cross-confirmation: also present at data/eu_nis2/stubs/source_retrieval_receipt.json (1 artefacts)

### `eu_rgpd`
- cross-confirmation: also present at data/eu_rgpd/stubs/source_retrieval_receipt.json (1 artefacts)

### `mcp_official_security_foundations_2025`
- cross-confirmation: also present at data/mcp_official_security_foundations_2025/stubs/source_retrieval_receipt.json (? artefacts)

### `nist_ai_rmf_1_0`
- governance-heavy; large lifted-concern fraction expected per dispatcher §source-list CAUTION note

### `owasp_dsomm`
- cross-confirmation: also present at data/owasp_dsomm/stubs/source_retrieval_receipt.json (5 artefacts)

### `owasp_mcp_secure_server_development_v1_0`
- cross-confirmation: also present at data/owasp_mcp_secure_server_development_v1_0/stubs/source_retrieval_receipt.json (? artefacts)

### `owasp_mcp_third_party_servers_v1_0`
- cross-confirmation: also present at data/owasp_mcp_third_party_servers_v1_0/stubs/source_retrieval_receipt.json (2 artefacts)

### `owasp_mcp_top_10_v0_1_2025_beta`
- cross-confirmation: also present at data/owasp_mcp_top_10_v0_1_2025_beta/stubs/source_retrieval_receipt.json (1 artefacts)

### `owasp_ml_top_10`
- Draft v0.3 (2023) — OWASP project still in draft; flagged for quality dossier review

### `owasp_samm_v2_1`
- cross-confirmation: also present at data/owasp_samm_v2_1/stubs/source_retrieval_receipt.json (4 artefacts)

### `slsa_spec_v1_0_build_track`
- cross-confirmation: also present at data/slsa_spec_v1_0_build_track/stubs/source_retrieval_receipt.json (5 artefacts)

### `ssdf_sp800_218_v1_1`
- cross-confirmation: also present at data/ssdf_sp800_218_v1_1/stubs/source_retrieval_receipt.json (? artefacts)

## Cross-references

- Substrate v7 SUPPLIER (input): `data/p7_olir_audit/p7_v2_corrected/v7/SUPPLIER_v7_0.json`
- Substrate v7 MANIFEST: `data/p7_olir_audit/p7_v2_corrected/v7/MANIFEST_v7_0.json`
- PIPELINE 1 lifted rows: `data/p7_olir_audit/p7_v2_corrected/v5/lifted/<source>_lifted.jsonl` × 31
- PIPELINE 2 grounded contracts: `data/p7_olir_audit/p7_v2_corrected/v7/<source>/per_item_contract.json` × 31
- OLIR exports: `data/p7_olir_audit/p7_v2_corrected/v7/olir_exports/concept_crosswalk_<source>.{xml,json}` × 31 + Schema 1.1 conformant × 31
- Cycle A frozen tag: `cycle-a-iter-1-frozen-2026-05-04` (substrate v5 anchor); `substrate-v7-iter-3-ai-ml-incorporated` (substrate v7 anchor)

