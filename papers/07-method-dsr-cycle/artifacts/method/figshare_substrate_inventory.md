# Figshare bundle — substrate-side inventory (Cartographer)

**Author:** Cartographer (Claude Opus 4.7)
**Authority:** programme-lead Pedro Farinha 2026-05-08
**Mini-dispatcher:** `2026-05-08-orchestrator-cartographer-figshare-inventory-mini-dispatch.md`
**Parent dispatcher:** `2026-05-08-orchestrator-curator-phase-a-figshare-bundle-coordination.md`
**Cycle A frozen tag:** `cycle-a-frozen-2026-05-08`
**Substrate v7 SUPPLIER SHA-256:** `596783ed984d9c0e8c8ef6439a0eaee8fbaf2d863af37138cde8fad55d62be04`

**Total artefacts indexed:** 289 (210 data / 57 script / 14 report / 8 doc)

All paths are relative to the `ExternalSourcesInventory` repo root. SHA-256 computed at the substrate v7 frozen state (worktree `cartographer-iteration-3-ai-ml-expansion` HEAD).

---

## Reproducibility chain

### Environment specification (5-dim baseline per Decision 0003 Amendment 1 §F)

```
Platform           : Darwin x86_64
Python             : 3.10.1
transformers       : 4.57.1
torch              : 2.2.2
numpy              : 1.24.4
SBERT model        : sentence-transformers/all-MiniLM-L6-v2
HF model revision  : c9745ed1d9f207416be6d2e6f8de32d1f16199bf
Encoder cap        : 256 tokens; mean-pooled; L2-normalized; float32 (N, 384)
```

Bit-identical reproducibility requires environment match on these 5 dimensions plus the pinned model revision. sentence-transformers wrapper version is irrelevant (encoder uses raw HuggingFace transformers + manual mean pooling).

### Cross-repo input dependencies

| Repo | Tag | Path | SHA-256 | Purpose |
|---|---|---|---|---|
| `sbd-toe-ontology` | `appsec-core-embeddings-v1.1` | `formal/appsec_core/08-embeddings/embeddings-all-MiniLM-L6-v2-c9745ed1.npz` | `17f6aac4...23c8` | Per-AppSec-Core-entity embeddings (212 entities; Slice 10 / CO 75 / Practice 69 / Mechanism 58); consumed by PIPELINE 2 grounding |
| `sbd-toe-ontology` | `appsec-core-embeddings-v1.1` | `formal/appsec_core/08-embeddings/augmented-text-corpus.json` | `5951fd82...96c42` | Augmented text corpus (input to embedder); Archon Part A Decision 0003 Amendment 1 §F augmentation rule v1.0 |
| `sbd-toe-ontology` | `apparatus-shacl-pyshacl-v3` | `formal/appsec_core/03-shacl/shapes/appsec-core-v0-shapes.ttl` + `consumer-conformance-shapes.ttl` | (programme-lead Option C composition) | SHACL apparatus (2-file composition; 11 shapes total — 6 ontology-side + 5 consumer-conformance Claim shapes) |
| `sbd-toe-ontology` | `ontology-v1-next-acr004-promoted` | `formal/appsec_core/02-owl/exports/appsec-core-v0-bounded-v1.ttl` | (V1.next 1824 triples; ACO-IVF-008 + ACP-IVF-007 + ACM-IVF-005 included) | OWL bounded TTL — V1.next ontology (incorporates ACR-001 + ACR-002 + ACR-004) |

### Execution sequence (raw sources → cross-validation outputs)

```
1. Stage 1 (source acquisition):
   For each of 31 active sources:
     curl <origin_url> > sources/<pilot>/<artefact>
     compute SHA-256; record in source_retrieval_receipt.json
     For 5 iter-3 sources, also: python3 -m scripts.extract_iteration_3_ai_ml_sources

2. Stage 2 (PIPELINE 1 — per-source flattening):
   python3 -m scripts.v5_normalization.run_all_flatteners
   → emits 31 lifted_rows.jsonl files at data/.../v5/lifted/

3. Stage 3 (per-source quality gate; iter-3 sources only):
   python3 -m scripts.v5_normalization.run_iteration_3_flatteners
   → emits 5 quality_dossier.json files + aggregate

4. Stage 4-5 (PIPELINE 2 grounding + substrate v7 emission):
   python3 -m scripts.v5_normalization.grounding.run_pipeline_v7
   → emits SUPPLIER_v7_0.json + MANIFEST_v7_0.json + 31 per_item_contract.json + reports/
   Verify: SHA-256 of SUPPLIER_v7_0.json == 596783ed984d9c0e8c8ef6439a0eaee8fbaf2d863af37138cde8fad55d62be04

5. SHACL conformance gate:
   python3 -m scripts.v5_normalization.grounding.emit_substrate_v7_ttl
   python3 sbd-toe-ontology/scripts/consumer_conformance_validator.py \
     --data .../v7-substrate-claims.ttl \
     --shapes <composed apparatus-v3 shapes graph> \
     --ontology .../appsec-core-v0-bounded-v1.ttl \
     --report .../reports/
   Expected: conforms=True / 0 violations

6. Stage 6 (LDP cluster analysis):
   python3 -m scripts.v5_normalization.grounding.ldp_cluster_analysis_v7
   → LABDEPTHPENDING_ACR_ANALYSIS.md + ldp_cluster_analysis.json

7. P7 Pass 6 cross-validation:
   python3 -m scripts.cross_validate_ssdf_references_v7
   python3 -m scripts.cross_validate_ssdf_references_v7_filtered
   python3 -m scripts.cross_validate_scf_strm_v7
   python3 -m scripts.frontier_match_and_audit_v7

8. P7 §8.2 figures:
   python3 -m scripts.figures.generate_p7_section_8_2_figures
```

All Python scripts are deterministic given the same SUPPLIER + environment (no LLM API calls in pipeline execution; methodology authoring layer is provenance-logged at `data/p7_olir_audit/p7_v2_corrected/v7/reports/llm_assist_provenance_v7_addendum.md` with 11 J-points).

### Tag chain references (Cycle A frozen state)

| Tag | Repo | Commit | Anchor purpose |
|---|---|---|---|
| `cycle-a-iter-1-frozen-2026-05-04` | ESI | `e404b56` | Substrate v5 (26-source baseline; AppSec Core V1.draft + apparatus-shacl-pyshacl-v2 + embeddings v1.0) |
| `substrate-v6-acr004-incorporated` | ESI | `ff28860` | Substrate v6 (Iteration 2 evidence; ACR-004 promoted) |
| `substrate-v7-iter-3-ai-ml-incorporated` | ESI | `be6fa9a` | Substrate v7 (Iteration 3 evidence; AI/ML expansion) |
| `cycle-a-frozen-2026-05-08` | ESI + sbd-toe-ontology + DevelopmentGovernance | (cross-repo) | Cycle A terminal frozen state (3 peer cross-repo tags) |
| `ontology-v1-next-acr004-promoted` | sbd-toe-ontology | `b267cf3` | V1.next ontology (incorporates ACR-001 + ACR-002 + ACR-004) |
| `apparatus-shacl-pyshacl-v3` | sbd-toe-ontology | `58b1958` | SHACL apparatus 2-file composition (Option C) |
| `appsec-core-embeddings-v1.1` | sbd-toe-ontology | `b948356` | SBERT embeddings v1.1 (212 entities) |

---

## Data artefacts

Substrate suppliers + manifests, per-source contracts (v5/v6/v7), lifted rows, cross-validation outputs, LDP analysis, H2 decision, process integrity reports, calibration distributions, ontology-side index, claims TTL + SHACL reports, per-source quality dossiers, source retrieval receipts, source object/unit inventories.

| Path | SHA-256 | Size | Description |
|---|---|---:|---|
| `data/p7_olir_audit/p7_v2_corrected/v5/SUPPLIER_v5_0.json` | `ee61675717c064b7…` | 14.01 MB | (no description) |
| `data/p7_olir_audit/p7_v2_corrected/v5/MANIFEST_v5_0.json` | `455deb78855a5102…` | 12.8 KB | (no description) |
| `data/p7_olir_audit/p7_v2_corrected/v6/SUPPLIER_v6_0.json` | `eda43e57e5f1051a…` | 14.05 MB | Substrate v6 supplier (predecessor; preserved for lineage) — 3457 items / 17507 claims / 75.38% GROUNDED across 26 baseline sources. Iteration 2 termination evidence (post-ACR-004 incorporation). |
| `data/p7_olir_audit/p7_v2_corrected/v6/MANIFEST_v6_0.json` | `727fdc1319981af7…` | 13.3 KB | Substrate v6 manifest (predecessor). |
| `data/p7_olir_audit/p7_v2_corrected/v7/SUPPLIER_v7_0.json` | `596783ed984d9c0e…` | 15.37 MB | Substrate v7 supplier — 3861 items / 18673 claims / GROUNDED 74.41% across 31 sources (26 baseline + 5 AI/ML iter-3). Cycle A Iteration 3 termination evidence; Pydantic-validated. |
| `data/p7_olir_audit/p7_v2_corrected/v7/MANIFEST_v7_0.json` | `35e3f7d65cd1657b…` | 18.1 KB | Substrate v7 manifest — schema, generation parameters, per-source summary, calibration thresholds (e2_pct=40 / e3_pct=60), termination gate verdicts, iter-3 caveats (OWASP LLM atomicity / ENISA AI 2024 dropped / NIST AI RMF governance falsification). |
| `data/p7_olir_audit/p7_v2_corrected/v5/asvs_v5_0_0/per_item_contract.json` | `79c06ae93066f5d2…` | 918.6 KB | Substrate v5 per-source items + claims for pilot `asvs_v5_0_0`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v5-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v5/capec_v3_9/per_item_contract.json` | `e5f2b7fe092e83ca…` | 1.63 MB | Substrate v5 per-source items + claims for pilot `capec_v3_9`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v5-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v5/cis_controls_v8_1_2/per_item_contract.json` | `0088559971b26f20…` | 943.6 KB | Substrate v5 per-source items + claims for pilot `cis_controls_v8_1_2`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v5-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v5/cwe_software_development_view_v4_19_1/per_item_contract.json` | `9bc293625741442f…` | 703.9 KB | Substrate v5 per-source items + claims for pilot `cwe_software_development_view_v4_19_1`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v5-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v5/enisa_multilayer_ai_cybersecurity_practices_2023/per_item_contract.json` | `f63d97f3f369dcfb…` | 10.6 KB | Substrate v5 per-source items + claims for pilot `enisa_multilayer_ai_cybersecurity_practices_2023`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v5-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v5/eu_cra/per_item_contract.json` | `a614847791d11556…` | 27.0 KB | Substrate v5 per-source items + claims for pilot `eu_cra`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v5-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v5/eu_dora/per_item_contract.json` | `7a234680575ff0e6…` | 43.0 KB | Substrate v5 per-source items + claims for pilot `eu_dora`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v5-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v5/eu_nis2/per_item_contract.json` | `a8b170957c8bac64…` | 46.1 KB | Substrate v5 per-source items + claims for pilot `eu_nis2`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v5-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v5/eu_rgpd/per_item_contract.json` | `a2ef5cc639c12ea3…` | 43.6 KB | Substrate v5 per-source items + claims for pilot `eu_rgpd`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v5-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v5/hipaa_security_rule/per_item_contract.json` | `6da5352337ba9ae5…` | 123.8 KB | Substrate v5 per-source items + claims for pilot `hipaa_security_rule`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v5-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v5/mcp_official_security_foundations_2025/per_item_contract.json` | `63c2eb7e7e33e485…` | 28.5 KB | Substrate v5 per-source items + claims for pilot `mcp_official_security_foundations_2025`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v5-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v5/nist_sp800_53_rev5/per_item_contract.json` | `649277e612cc2384…` | 5.53 MB | Substrate v5 per-source items + claims for pilot `nist_sp800_53_rev5`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v5-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v5/owasp_dsomm/per_item_contract.json` | `377030864430d099…` | 773.9 KB | Substrate v5 per-source items + claims for pilot `owasp_dsomm`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v5-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v5/owasp_mcp_secure_server_development_v1_0/per_item_contract.json` | `9a73c44967bcf3ad…` | 52.9 KB | Substrate v5 per-source items + claims for pilot `owasp_mcp_secure_server_development_v1_0`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v5-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v5/owasp_mcp_third_party_servers_v1_0/per_item_contract.json` | `5c1212caee68bc55…` | 31.0 KB | Substrate v5 per-source items + claims for pilot `owasp_mcp_third_party_servers_v1_0`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v5-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v5/owasp_mcp_top_10_v0_1_2025_beta/per_item_contract.json` | `954665f0f7af5a4b…` | 44.3 KB | Substrate v5 per-source items + claims for pilot `owasp_mcp_top_10_v0_1_2025_beta`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v5-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v5/owasp_proactive_controls_2018/per_item_contract.json` | `438040021145187b…` | 56.6 KB | Substrate v5 per-source items + claims for pilot `owasp_proactive_controls_2018`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v5-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v5/owasp_samm_v2_1/per_item_contract.json` | `7610abf3715466bf…` | 1.10 MB | Substrate v5 per-source items + claims for pilot `owasp_samm_v2_1`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v5-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v5/owasp_top_10_2021/per_item_contract.json` | `4dedc54a3297b00f…` | 39.1 KB | Substrate v5 per-source items + claims for pilot `owasp_top_10_2021`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v5-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v5/pci_dss_v4_0_1/per_item_contract.json` | `3e8339476b413977…` | 1.12 MB | Substrate v5 per-source items + claims for pilot `pci_dss_v4_0_1`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v5-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v5/pci_sslc_v1_1/per_item_contract.json` | `6fc628df01eb843a…` | 188.1 KB | Substrate v5 per-source items + claims for pilot `pci_sslc_v1_1`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v5-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v5/safecode_agile_2012/per_item_contract.json` | `b4be7e161275dad1…` | 104.6 KB | Substrate v5 per-source items + claims for pilot `safecode_agile_2012`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v5-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v5/safecode_fpssd_2018/per_item_contract.json` | `accb11b3ad914119…` | 87.9 KB | Substrate v5 per-source items + claims for pilot `safecode_fpssd_2018`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v5-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v5/safecode_sic_2010/per_item_contract.json` | `6bec7dd797630e4a…` | 64.6 KB | Substrate v5 per-source items + claims for pilot `safecode_sic_2010`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v5-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v5/slsa_spec_v1_0_build_track/per_item_contract.json` | `9092c9692beac1b1…` | 79.2 KB | Substrate v5 per-source items + claims for pilot `slsa_spec_v1_0_build_track`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v5-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v5/ssdf_sp800_218_v1_1/per_item_contract.json` | `e34fda0bdfc169ed…` | 332.8 KB | Substrate v5 per-source items + claims for pilot `ssdf_sp800_218_v1_1`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v5-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v6/asvs_v5_0_0/per_item_contract.json` | `f92c82c83a88e311…` | 938.0 KB | Substrate v6 per-source items + claims for pilot `asvs_v5_0_0`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v6-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v6/capec_v3_9/per_item_contract.json` | `38d7eddcf04a123a…` | 1.66 MB | Substrate v6 per-source items + claims for pilot `capec_v3_9`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v6-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v6/cis_controls_v8_1_2/per_item_contract.json` | `f647103711f32019…` | 938.9 KB | Substrate v6 per-source items + claims for pilot `cis_controls_v8_1_2`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v6-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v6/cwe_software_development_view_v4_19_1/per_item_contract.json` | `84b1cfe45b495c99…` | 710.2 KB | Substrate v6 per-source items + claims for pilot `cwe_software_development_view_v4_19_1`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v6-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v6/enisa_multilayer_ai_cybersecurity_practices_2023/per_item_contract.json` | `a9ccaa59383548a9…` | 10.6 KB | Substrate v6 per-source items + claims for pilot `enisa_multilayer_ai_cybersecurity_practices_2023`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v6-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v6/eu_cra/per_item_contract.json` | `c5b5226ed29b5166…` | 27.0 KB | Substrate v6 per-source items + claims for pilot `eu_cra`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v6-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v6/eu_dora/per_item_contract.json` | `95d1027e09a79234…` | 43.0 KB | Substrate v6 per-source items + claims for pilot `eu_dora`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v6-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v6/eu_nis2/per_item_contract.json` | `5d5e18f2ff4e4007…` | 46.1 KB | Substrate v6 per-source items + claims for pilot `eu_nis2`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v6-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v6/eu_rgpd/per_item_contract.json` | `6d81ba87d02f4b9a…` | 42.9 KB | Substrate v6 per-source items + claims for pilot `eu_rgpd`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v6-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v6/hipaa_security_rule/per_item_contract.json` | `5be65be776a4fd5e…` | 123.1 KB | Substrate v6 per-source items + claims for pilot `hipaa_security_rule`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v6-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v6/mcp_official_security_foundations_2025/per_item_contract.json` | `bfb6e66521e7aa1b…` | 28.5 KB | Substrate v6 per-source items + claims for pilot `mcp_official_security_foundations_2025`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v6-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v6/nist_sp800_53_rev5/per_item_contract.json` | `e1b8cc1a01d0d6f5…` | 5.53 MB | Substrate v6 per-source items + claims for pilot `nist_sp800_53_rev5`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v6-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v6/owasp_dsomm/per_item_contract.json` | `db3d073814c13c43…` | 775.4 KB | Substrate v6 per-source items + claims for pilot `owasp_dsomm`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v6-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v6/owasp_mcp_secure_server_development_v1_0/per_item_contract.json` | `b0cfaa4abdb69a85…` | 53.7 KB | Substrate v6 per-source items + claims for pilot `owasp_mcp_secure_server_development_v1_0`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v6-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v6/owasp_mcp_third_party_servers_v1_0/per_item_contract.json` | `6a8de1e74fbd0227…` | 30.2 KB | Substrate v6 per-source items + claims for pilot `owasp_mcp_third_party_servers_v1_0`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v6-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v6/owasp_mcp_top_10_v0_1_2025_beta/per_item_contract.json` | `f69a5280f58bfbc9…` | 43.6 KB | Substrate v6 per-source items + claims for pilot `owasp_mcp_top_10_v0_1_2025_beta`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v6-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v6/owasp_proactive_controls_2018/per_item_contract.json` | `8d2fba1edd6507fb…` | 57.3 KB | Substrate v6 per-source items + claims for pilot `owasp_proactive_controls_2018`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v6-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v6/owasp_samm_v2_1/per_item_contract.json` | `c076685693ba3eb5…` | 1.09 MB | Substrate v6 per-source items + claims for pilot `owasp_samm_v2_1`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v6-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v6/owasp_top_10_2021/per_item_contract.json` | `aed38739c821d8a4…` | 39.8 KB | Substrate v6 per-source items + claims for pilot `owasp_top_10_2021`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v6-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v6/pci_dss_v4_0_1/per_item_contract.json` | `8d3fef1d46ec2ee7…` | 1.13 MB | Substrate v6 per-source items + claims for pilot `pci_dss_v4_0_1`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v6-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v6/pci_sslc_v1_1/per_item_contract.json` | `6e5b1bca0bd4654e…` | 188.1 KB | Substrate v6 per-source items + claims for pilot `pci_sslc_v1_1`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v6-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v6/safecode_agile_2012/per_item_contract.json` | `6c5b4ae33d776cca…` | 104.0 KB | Substrate v6 per-source items + claims for pilot `safecode_agile_2012`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v6-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v6/safecode_fpssd_2018/per_item_contract.json` | `0871c40be9a2d81d…` | 87.9 KB | Substrate v6 per-source items + claims for pilot `safecode_fpssd_2018`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v6-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v6/safecode_sic_2010/per_item_contract.json` | `053eb854daff4ab6…` | 64.6 KB | Substrate v6 per-source items + claims for pilot `safecode_sic_2010`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v6-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v6/slsa_spec_v1_0_build_track/per_item_contract.json` | `5158127a60d18dd6…` | 79.2 KB | Substrate v6 per-source items + claims for pilot `slsa_spec_v1_0_build_track`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v6-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v6/ssdf_sp800_218_v1_1/per_item_contract.json` | `a50ecd9ad43d55f9…` | 331.4 KB | Substrate v6 per-source items + claims for pilot `ssdf_sp800_218_v1_1`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v6-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v7/asvs_v5_0_0/per_item_contract.json` | `85805c4daa3fdd30…` | 938.1 KB | Substrate v7 per-source items + claims for pilot `asvs_v5_0_0`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v7-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v7/capec_v3_9/per_item_contract.json` | `49a6c8f8764b3aa4…` | 1.66 MB | Substrate v7 per-source items + claims for pilot `capec_v3_9`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v7-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v7/cis_controls_v8_1_2/per_item_contract.json` | `b42bb5154274aa2a…` | 939.0 KB | Substrate v7 per-source items + claims for pilot `cis_controls_v8_1_2`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v7-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v7/cwe_software_development_view_v4_19_1/per_item_contract.json` | `f2b1b2174a023db1…` | 710.2 KB | Substrate v7 per-source items + claims for pilot `cwe_software_development_view_v4_19_1`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v7-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v7/enisa_multilayer_ai_cybersecurity_practices_2023/per_item_contract.json` | `9dc5fd5ea62170c1…` | 10.6 KB | Substrate v7 per-source items + claims for pilot `enisa_multilayer_ai_cybersecurity_practices_2023`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v7-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v7/eu_cra/per_item_contract.json` | `ba27902f9943064a…` | 27.1 KB | Substrate v7 per-source items + claims for pilot `eu_cra`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v7-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v7/eu_dora/per_item_contract.json` | `831cb3c651cf43c2…` | 43.1 KB | Substrate v7 per-source items + claims for pilot `eu_dora`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v7-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v7/eu_nis2/per_item_contract.json` | `e906a67f038f0be2…` | 46.2 KB | Substrate v7 per-source items + claims for pilot `eu_nis2`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v7-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v7/eu_rgpd/per_item_contract.json` | `e27de81fa2f998e4…` | 43.0 KB | Substrate v7 per-source items + claims for pilot `eu_rgpd`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v7-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v7/hipaa_security_rule/per_item_contract.json` | `da7fa21296a15b9e…` | 123.2 KB | Substrate v7 per-source items + claims for pilot `hipaa_security_rule`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v7-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v7/mcp_official_security_foundations_2025/per_item_contract.json` | `39d7e5dd3f195c53…` | 28.6 KB | Substrate v7 per-source items + claims for pilot `mcp_official_security_foundations_2025`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v7-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v7/mitre_atlas/per_item_contract.json` | `0a0038c31583507c…` | 716.3 KB | Substrate v7 per-source items + claims for pilot `mitre_atlas`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v7-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v7/nist_ai_100_2_e2025/per_item_contract.json` | `53b53a8db46ad621…` | 302.2 KB | Substrate v7 per-source items + claims for pilot `nist_ai_100_2_e2025`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v7-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v7/nist_ai_rmf_1_0/per_item_contract.json` | `15ebebc03732e45c…` | 135.0 KB | Substrate v7 per-source items + claims for pilot `nist_ai_rmf_1_0`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v7-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v7/nist_sp800_53_rev5/per_item_contract.json` | `27244a69a207d63b…` | 5.53 MB | Substrate v7 per-source items + claims for pilot `nist_sp800_53_rev5`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v7-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v7/owasp_dsomm/per_item_contract.json` | `c09d4c3668fddcde…` | 775.4 KB | Substrate v7 per-source items + claims for pilot `owasp_dsomm`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v7-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v7/owasp_llm_top_10/per_item_contract.json` | `2d7335b57b34764c…` | 118.3 KB | Substrate v7 per-source items + claims for pilot `owasp_llm_top_10`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v7-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v7/owasp_mcp_secure_server_development_v1_0/per_item_contract.json` | `b3822f94e445dffd…` | 53.7 KB | Substrate v7 per-source items + claims for pilot `owasp_mcp_secure_server_development_v1_0`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v7-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v7/owasp_mcp_third_party_servers_v1_0/per_item_contract.json` | `ff87d00e6ebc8b0a…` | 30.3 KB | Substrate v7 per-source items + claims for pilot `owasp_mcp_third_party_servers_v1_0`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v7-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v7/owasp_mcp_top_10_v0_1_2025_beta/per_item_contract.json` | `bc63b25c2c239767…` | 43.6 KB | Substrate v7 per-source items + claims for pilot `owasp_mcp_top_10_v0_1_2025_beta`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v7-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v7/owasp_ml_top_10/per_item_contract.json` | `26b9884f70f51af5…` | 89.1 KB | Substrate v7 per-source items + claims for pilot `owasp_ml_top_10`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v7-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v7/owasp_proactive_controls_2018/per_item_contract.json` | `fec947cbf1f56d71…` | 57.3 KB | Substrate v7 per-source items + claims for pilot `owasp_proactive_controls_2018`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v7-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v7/owasp_samm_v2_1/per_item_contract.json` | `488ca5127a49986e…` | 1.09 MB | Substrate v7 per-source items + claims for pilot `owasp_samm_v2_1`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v7-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v7/owasp_top_10_2021/per_item_contract.json` | `e8044e0ebdc24d29…` | 39.9 KB | Substrate v7 per-source items + claims for pilot `owasp_top_10_2021`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v7-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v7/pci_dss_v4_0_1/per_item_contract.json` | `b30a64f5d360ff54…` | 1.13 MB | Substrate v7 per-source items + claims for pilot `pci_dss_v4_0_1`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v7-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v7/pci_sslc_v1_1/per_item_contract.json` | `86854d67c2cd41cf…` | 188.1 KB | Substrate v7 per-source items + claims for pilot `pci_sslc_v1_1`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v7-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v7/safecode_agile_2012/per_item_contract.json` | `6a4b46363bd9b4a8…` | 104.0 KB | Substrate v7 per-source items + claims for pilot `safecode_agile_2012`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v7-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v7/safecode_fpssd_2018/per_item_contract.json` | `244d212a273357f7…` | 87.9 KB | Substrate v7 per-source items + claims for pilot `safecode_fpssd_2018`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v7-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v7/safecode_sic_2010/per_item_contract.json` | `7027d703743ec2d1…` | 64.6 KB | Substrate v7 per-source items + claims for pilot `safecode_sic_2010`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v7-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v7/slsa_spec_v1_0_build_track/per_item_contract.json` | `80a4e7d0da4a119f…` | 79.2 KB | Substrate v7 per-source items + claims for pilot `slsa_spec_v1_0_build_track`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v7-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v7/ssdf_sp800_218_v1_1/per_item_contract.json` | `c77cfa2286fbbfbc…` | 331.5 KB | Substrate v7 per-source items + claims for pilot `ssdf_sp800_218_v1_1`. Pydantic-validated; Cycle A frozen anchor: tag `substrate-v7-*-incorporated`. |
| `data/p7_olir_audit/p7_v2_corrected/v5/lifted/asvs_v5_0_0_lifted.jsonl` | `f37d5054741b8530…` | 337.7 KB | PIPELINE 1 lifted rows for `asvs_v5_0_0` (per-row contextualised_text + structural_provenance + decomposition; reused unchanged across substrate v5/v6/v7 per Decision 0003 Amendment 1 §F augmentation symmetry). |
| `data/p7_olir_audit/p7_v2_corrected/v5/lifted/capec_v3_9_lifted.jsonl` | `7757e1ad68a0415d…` | 1.33 MB | PIPELINE 1 lifted rows for `capec_v3_9` (per-row contextualised_text + structural_provenance + decomposition; reused unchanged across substrate v5/v6/v7 per Decision 0003 Amendment 1 §F augmentation symmetry). |
| `data/p7_olir_audit/p7_v2_corrected/v5/lifted/cis_controls_v8_1_2_lifted.jsonl` | `2275d9f0bc70f93c…` | 254.2 KB | PIPELINE 1 lifted rows for `cis_controls_v8_1_2` (per-row contextualised_text + structural_provenance + decomposition; reused unchanged across substrate v5/v6/v7 per Decision 0003 Amendment 1 §F augmentation symmetry). |
| `data/p7_olir_audit/p7_v2_corrected/v5/lifted/cwe_software_development_view_v4_19_1_lifted.jsonl` | `0a99fd9319ef8898…` | 362.6 KB | PIPELINE 1 lifted rows for `cwe_software_development_view_v4_19_1` (per-row contextualised_text + structural_provenance + decomposition; reused unchanged across substrate v5/v6/v7 per Decision 0003 Amendment 1 §F augmentation symmetry). |
| `data/p7_olir_audit/p7_v2_corrected/v5/lifted/enisa_multilayer_ai_cybersecurity_practices_2023_lifted.jsonl` | `668c71d3cb81ade3…` | 6.8 KB | PIPELINE 1 lifted rows for `enisa_multilayer_ai_cybersecurity_practices_2023` (per-row contextualised_text + structural_provenance + decomposition; reused unchanged across substrate v5/v6/v7 per Decision 0003 Amendment 1 §F augmentation symmetry). |
| `data/p7_olir_audit/p7_v2_corrected/v5/lifted/eu_cra_lifted.jsonl` | `f3140f8c30c7243e…` | 17.1 KB | PIPELINE 1 lifted rows for `eu_cra` (per-row contextualised_text + structural_provenance + decomposition; reused unchanged across substrate v5/v6/v7 per Decision 0003 Amendment 1 §F augmentation symmetry). |
| `data/p7_olir_audit/p7_v2_corrected/v5/lifted/eu_dora_lifted.jsonl` | `003ba0dd11b9f299…` | 53.6 KB | PIPELINE 1 lifted rows for `eu_dora` (per-row contextualised_text + structural_provenance + decomposition; reused unchanged across substrate v5/v6/v7 per Decision 0003 Amendment 1 §F augmentation symmetry). |
| `data/p7_olir_audit/p7_v2_corrected/v5/lifted/eu_nis2_lifted.jsonl` | `c82d2fc6af2a7826…` | 13.9 KB | PIPELINE 1 lifted rows for `eu_nis2` (per-row contextualised_text + structural_provenance + decomposition; reused unchanged across substrate v5/v6/v7 per Decision 0003 Amendment 1 §F augmentation symmetry). |
| `data/p7_olir_audit/p7_v2_corrected/v5/lifted/eu_rgpd_lifted.jsonl` | `c96d9683ae6e7b61…` | 17.2 KB | PIPELINE 1 lifted rows for `eu_rgpd` (per-row contextualised_text + structural_provenance + decomposition; reused unchanged across substrate v5/v6/v7 per Decision 0003 Amendment 1 §F augmentation symmetry). |
| `data/p7_olir_audit/p7_v2_corrected/v5/lifted/hipaa_security_rule_lifted.jsonl` | `d1a2b04615d66a5a…` | 42.5 KB | PIPELINE 1 lifted rows for `hipaa_security_rule` (per-row contextualised_text + structural_provenance + decomposition; reused unchanged across substrate v5/v6/v7 per Decision 0003 Amendment 1 §F augmentation symmetry). |
| `data/p7_olir_audit/p7_v2_corrected/v5/lifted/mcp_official_security_foundations_2025_lifted.jsonl` | `94a10a6855f6c0e5…` | 16.9 KB | PIPELINE 1 lifted rows for `mcp_official_security_foundations_2025` (per-row contextualised_text + structural_provenance + decomposition; reused unchanged across substrate v5/v6/v7 per Decision 0003 Amendment 1 §F augmentation symmetry). |
| `data/p7_olir_audit/p7_v2_corrected/v5/lifted/mitre_atlas_lifted.jsonl` | `96fc796ef7a23a6e…` | 531.6 KB | PIPELINE 1 lifted rows for `mitre_atlas` (per-row contextualised_text + structural_provenance + decomposition; reused unchanged across substrate v5/v6/v7 per Decision 0003 Amendment 1 §F augmentation symmetry). |
| `data/p7_olir_audit/p7_v2_corrected/v5/lifted/nist_ai_100_2_e2025_lifted.jsonl` | `a48cf791cdfc7513…` | 321.0 KB | PIPELINE 1 lifted rows for `nist_ai_100_2_e2025` (per-row contextualised_text + structural_provenance + decomposition; reused unchanged across substrate v5/v6/v7 per Decision 0003 Amendment 1 §F augmentation symmetry). |
| `data/p7_olir_audit/p7_v2_corrected/v5/lifted/nist_ai_rmf_1_0_lifted.jsonl` | `342117eea3426a5d…` | 215.8 KB | PIPELINE 1 lifted rows for `nist_ai_rmf_1_0` (per-row contextualised_text + structural_provenance + decomposition; reused unchanged across substrate v5/v6/v7 per Decision 0003 Amendment 1 §F augmentation symmetry). |
| `data/p7_olir_audit/p7_v2_corrected/v5/lifted/nist_sp800_53_rev5_lifted.jsonl` | `6a54844473f3384d…` | 1.35 MB | PIPELINE 1 lifted rows for `nist_sp800_53_rev5` (per-row contextualised_text + structural_provenance + decomposition; reused unchanged across substrate v5/v6/v7 per Decision 0003 Amendment 1 §F augmentation symmetry). |
| `data/p7_olir_audit/p7_v2_corrected/v5/lifted/owasp_dsomm_lifted.jsonl` | `f8d7a4973df21d2c…` | 299.8 KB | PIPELINE 1 lifted rows for `owasp_dsomm` (per-row contextualised_text + structural_provenance + decomposition; reused unchanged across substrate v5/v6/v7 per Decision 0003 Amendment 1 §F augmentation symmetry). |
| `data/p7_olir_audit/p7_v2_corrected/v5/lifted/owasp_llm_top_10_lifted.jsonl` | `c849280599bebe35…` | 110.8 KB | PIPELINE 1 lifted rows for `owasp_llm_top_10` (per-row contextualised_text + structural_provenance + decomposition; reused unchanged across substrate v5/v6/v7 per Decision 0003 Amendment 1 §F augmentation symmetry). |
| `data/p7_olir_audit/p7_v2_corrected/v5/lifted/owasp_mcp_secure_server_development_v1_0_lifted.jsonl` | `916e8d328f429b41…` | 10.6 KB | PIPELINE 1 lifted rows for `owasp_mcp_secure_server_development_v1_0` (per-row contextualised_text + structural_provenance + decomposition; reused unchanged across substrate v5/v6/v7 per Decision 0003 Amendment 1 §F augmentation symmetry). |
| `data/p7_olir_audit/p7_v2_corrected/v5/lifted/owasp_mcp_third_party_servers_v1_0_lifted.jsonl` | `a4949f2f60b1a0f5…` | 10.0 KB | PIPELINE 1 lifted rows for `owasp_mcp_third_party_servers_v1_0` (per-row contextualised_text + structural_provenance + decomposition; reused unchanged across substrate v5/v6/v7 per Decision 0003 Amendment 1 §F augmentation symmetry). |
| `data/p7_olir_audit/p7_v2_corrected/v5/lifted/owasp_mcp_top_10_v0_1_2025_beta_lifted.jsonl` | `9ad37c7a1af60024…` | 11.9 KB | PIPELINE 1 lifted rows for `owasp_mcp_top_10_v0_1_2025_beta` (per-row contextualised_text + structural_provenance + decomposition; reused unchanged across substrate v5/v6/v7 per Decision 0003 Amendment 1 §F augmentation symmetry). |
| `data/p7_olir_audit/p7_v2_corrected/v5/lifted/owasp_ml_top_10_lifted.jsonl` | `5c8c88d5760bbdf0…` | 49.0 KB | PIPELINE 1 lifted rows for `owasp_ml_top_10` (per-row contextualised_text + structural_provenance + decomposition; reused unchanged across substrate v5/v6/v7 per Decision 0003 Amendment 1 §F augmentation symmetry). |
| `data/p7_olir_audit/p7_v2_corrected/v5/lifted/owasp_proactive_controls_2018_lifted.jsonl` | `aac24dd9a309b9df…` | 12.2 KB | PIPELINE 1 lifted rows for `owasp_proactive_controls_2018` (per-row contextualised_text + structural_provenance + decomposition; reused unchanged across substrate v5/v6/v7 per Decision 0003 Amendment 1 §F augmentation symmetry). |
| `data/p7_olir_audit/p7_v2_corrected/v5/lifted/owasp_samm_v2_1_lifted.jsonl` | `df01adda47147a34…` | 275.5 KB | PIPELINE 1 lifted rows for `owasp_samm_v2_1` (per-row contextualised_text + structural_provenance + decomposition; reused unchanged across substrate v5/v6/v7 per Decision 0003 Amendment 1 §F augmentation symmetry). |
| `data/p7_olir_audit/p7_v2_corrected/v5/lifted/owasp_top_10_2021_lifted.jsonl` | `7c6aa03556292044…` | 10.3 KB | PIPELINE 1 lifted rows for `owasp_top_10_2021` (per-row contextualised_text + structural_provenance + decomposition; reused unchanged across substrate v5/v6/v7 per Decision 0003 Amendment 1 §F augmentation symmetry). |
| `data/p7_olir_audit/p7_v2_corrected/v5/lifted/pci_dss_v4_0_1_lifted.jsonl` | `6854d35c7f9db698…` | 232.3 KB | PIPELINE 1 lifted rows for `pci_dss_v4_0_1` (per-row contextualised_text + structural_provenance + decomposition; reused unchanged across substrate v5/v6/v7 per Decision 0003 Amendment 1 §F augmentation symmetry). |
| `data/p7_olir_audit/p7_v2_corrected/v5/lifted/pci_sslc_v1_1_lifted.jsonl` | `b1bc4dd9327e793c…` | 26.2 KB | PIPELINE 1 lifted rows for `pci_sslc_v1_1` (per-row contextualised_text + structural_provenance + decomposition; reused unchanged across substrate v5/v6/v7 per Decision 0003 Amendment 1 §F augmentation symmetry). |
| `data/p7_olir_audit/p7_v2_corrected/v5/lifted/safecode_agile_2012_lifted.jsonl` | `f02db50bd1e4992a…` | 20.2 KB | PIPELINE 1 lifted rows for `safecode_agile_2012` (per-row contextualised_text + structural_provenance + decomposition; reused unchanged across substrate v5/v6/v7 per Decision 0003 Amendment 1 §F augmentation symmetry). |
| `data/p7_olir_audit/p7_v2_corrected/v5/lifted/safecode_fpssd_2018_lifted.jsonl` | `a8ef3604bb6705f6…` | 11.5 KB | PIPELINE 1 lifted rows for `safecode_fpssd_2018` (per-row contextualised_text + structural_provenance + decomposition; reused unchanged across substrate v5/v6/v7 per Decision 0003 Amendment 1 §F augmentation symmetry). |
| `data/p7_olir_audit/p7_v2_corrected/v5/lifted/safecode_sic_2010_lifted.jsonl` | `f39dceb70f27990d…` | 9.5 KB | PIPELINE 1 lifted rows for `safecode_sic_2010` (per-row contextualised_text + structural_provenance + decomposition; reused unchanged across substrate v5/v6/v7 per Decision 0003 Amendment 1 §F augmentation symmetry). |
| `data/p7_olir_audit/p7_v2_corrected/v5/lifted/slsa_spec_v1_0_build_track_lifted.jsonl` | `981b624f02498085…` | 16.2 KB | PIPELINE 1 lifted rows for `slsa_spec_v1_0_build_track` (per-row contextualised_text + structural_provenance + decomposition; reused unchanged across substrate v5/v6/v7 per Decision 0003 Amendment 1 §F augmentation symmetry). |
| `data/p7_olir_audit/p7_v2_corrected/v5/lifted/ssdf_sp800_218_v1_1_lifted.jsonl` | `8e6590c07728e4d2…` | 59.6 KB | PIPELINE 1 lifted rows for `ssdf_sp800_218_v1_1` (per-row contextualised_text + structural_provenance + decomposition; reused unchanged across substrate v5/v6/v7 per Decision 0003 Amendment 1 §F augmentation symmetry). |
| `data/p7_olir_audit/p7_v2_corrected/v7/reports/H2_INVERTED_MAPPING_DECISION.md` | `d29432ed3845102b…` | 7.6 KB | Stage 7 H2 sub-hypothesis decision: CONFIRMED. Three independent signals (GROUNDED rate parity ATLAS≈CAPEC; LDP top-1 adjacency parity; cross-corpus cluster co-membership at CID7-027). Inverted-mapping methodology generalises to AI/ML problem-space-inverted sources without refinement. |
| `data/p7_olir_audit/p7_v2_corrected/v7/reports/LABDEPTHPENDING_ACR_ANALYSIS.md` | `5eb5c0a014b06a00…` | 36.6 KB | Stage 6 FULL LDP cluster analysis recomputation (Iter-3 mandatory deliverable). 988 LDP items / 77 coarse clusters (agglomerative average-linkage on cosine distance, 3 granularities) / 27 STRONG (≥3 INDEPENDENT families) / 14 AI/ML-inflected. CID7-027 hotspot characterised. |
| `data/p7_olir_audit/p7_v2_corrected/v7/reports/PROCESS_INTEGRITY_REPORT.md` | `b9bce4af19ea842c…` | 13.3 KB | Substrate v7 process integrity report — termination gate verdicts (SHACL CONFORMS ✅, GROUNDED 74.41% < 75.38% ❌ accepted as corpus-expansion artifact per joint-review 2026-05-08). Regression decomposition: 26 baseline bit-identical; 5 iter-3 sources at structural-peer parity. |
| `data/p7_olir_audit/p7_v2_corrected/v7/reports/calibration_distribution.json` | `a345313061a142b5…` | 3.6 KB | E2/E3 threshold calibration distribution (cohort SSDF + CIS + SAMM + CWE; e2_pct=40 / e3_pct=60). Per-level percentile statistics for top-1 score + within-(slice,level) margin distributions. |
| `data/p7_olir_audit/p7_v2_corrected/v7/reports/cross_validation_per_pair_audit.xlsx` | `92144053a1a01e2f…` | 1.20 MB | Per-pair audit XLSX (4 sheets, 1.3 MB) for manual joint-review inspection. Sheet 1 SSDF same-level (142) / Sheet 2 SSDF cross-level (281, ASVS contamination flag) / Sheet 3 SCF v7 (5652) / Sheet 4 summary + 9-cell interpretation matrix + worked examples (PW.8/SA-11 highlighted purple). |
| `data/p7_olir_audit/p7_v2_corrected/v7/reports/frontier_match_and_per_task_audit_v7.json` | `2e8cea49d49492f9…` | 2.7 KB | 3-tier per-pair metrics (strict / slice_primary / frontier) + per-task hit rate audit across 3 pools (SSDF same-level, SSDF cross-level, SCF v7). Programme-lead's 9-cell matrix verdict: 'Strong alignment confirmed' empirically met (per-task frontier ≥97% across all pools). |
| `data/p7_olir_audit/p7_v2_corrected/v7/reports/ldp_cluster_analysis.json` | `2a52e8b8ff180784…` | 73.1 KB | LDP cluster analysis machine-readable output (per-cluster: members, source families, top-1 adjacency stats, top-3 closest Core entities, ACR-candidacy verdict). |
| `data/p7_olir_audit/p7_v2_corrected/v7/reports/ontology_side_index.json` | `63ba6471270c69a6…` | 767.7 KB | Per-target Core entity claim aggregation (200 targets reached). Each entry: target IRI + level + slice + claim count + source distribution + claim refs. |
| `data/p7_olir_audit/p7_v2_corrected/v7/reports/per_source_metadata_table.json` | `9fe9e6929908ef90…` | 9.6 KB | 31-source metadata table (sub-version + tier + mapping direction + GROUNDED rate). Tier classification per 2026-04-22 SCF audit (T1=3 / T2=5 / T3=1 / T4=1 / T5=21 incl. all 5 iter-3 sources). |
| `data/p7_olir_audit/p7_v2_corrected/v7/reports/scf_crossval_v7.json` | `9f80f1e349cf59e9…` | 12.7 KB | SCF v7 cross-validation (PRIMARY oracle for P7 §8.2). Forward-direction pair matching across SCF 2026.1 STRM published cross-references. Strict 10.01% / Adjusted 16.88% / n=5652 cross-pilot decidable pairs. Per-pilot ID normalizers + per-pair-pool decomposition included. |
| `data/p7_olir_audit/p7_v2_corrected/v7/reports/ssdf_crossval_v7.json` | `8e330750baca9b27…` | 2.1 KB | SSDF v7 cross-validation against substrate v7 (Variant B GROUNDED both sides; CO-level-preferred primary anchor). Strict 19.72% / Adjusted 35.25% / n=142 same-level pairs (after task-to-practice fallback). Methodology disclosure included. |
| `data/p7_olir_audit/p7_v2_corrected/v7/reports/ssdf_crossval_v7_filtered.json` | `c43f99a1c9ca5cc5…` | 1.8 KB | SSDF v7 cross-validation filtered to corpus-resolvable references (excludes OWASPASVS / OWASPMASVS / OWASPSCVS due to v4.0.3 → v5.0.0 major-version mismatch). Same-level results identical to full v7 (ASVS pairs were already in cross-level bucket); refines version-drift hypothesis empirically. |
| `data/p7_olir_audit/p7_v2_corrected/v7/reports/v7-substrate-claims-shacl-report.json` | `34c0470fa53b1aed…` | 2.1 KB | SHACL conformance machine-readable output. |
| `data/p7_olir_audit/p7_v2_corrected/v7/reports/v7-substrate-claims-shacl-report.md` | `19c54330b7be967d…` | 2.0 KB | SHACL conformance report (apparatus-v3 composed shapes graph + V1.next ontology). conforms=True / 0 violations across M1' / M3 / M4 / M4-card / referential integrity. Validator: pyshacl 0.31.0 / rdflib 7.6.0. |
| `data/p7_olir_audit/p7_v2_corrected/v7/reports/v7-substrate-claims.ttl` | `2b12a8d9b6252e99…` | 7.86 MB | Substrate v7 claims serialised as RDF Turtle (181464 triples) for SHACL validation. Anchor for apparatus-shacl-pyshacl-v3 conformance gate. |
| `data/p7_olir_audit/p7_v2_corrected/v6/reports/PROCESS_INTEGRITY_REPORT.md` | `69ababcdf6348afc…` | 10.2 KB | Substrate v6 process integrity report (predecessor; Iteration 2 termination evidence; SHACL CONFORMS ✅, GROUNDED 75.38% ≥74.6% baseline ✅). |
| `data/p7_olir_audit/p7_v2_corrected/v6/reports/calibration_distribution.json` | `a345313061a142b5…` | 3.6 KB | Substrate v6 calibration distribution (predecessor; identical thresholds to v7 — same cohort). |
| `data/p7_olir_audit/p7_v2_corrected/v6/reports/ontology_side_index.json` | `8fbaafe7c079d466…` | 725.4 KB | (no description) |
| `data/p7_olir_audit/p7_v2_corrected/v6/reports/v6-substrate-claims-shacl-report.json` | `3ea60bd10aee5b96…` | 1.9 KB | (no description) |
| `data/p7_olir_audit/p7_v2_corrected/v6/reports/v6-substrate-claims-shacl-report.md` | `aa964d9f4b0c51a4…` | 1.8 KB | (no description) |
| `data/p7_olir_audit/p7_v2_corrected/v6/reports/v6-substrate-claims.ttl` | `71c0fcd2afa40989…` | 7.36 MB | Substrate v6 claims TTL (predecessor). |
| `data/p7_olir_audit/p7_v2_corrected/iteration_3/quality_dossier_aggregate.json` | `2d7ea6ea362fdebd…` | 3.2 KB | (no description) |
| `data/asvs_v4_0_2/stubs/source_object_inventory.json` | `469ae8b8d486d49e…` | 246.1 KB | Source object inventory for `asvs_v4_0_2` (post-extraction; pre-lifting). Items include source_object_id, title, statement, statement_kind, framework_family. |
| `data/asvs_v5_0_0/stubs/source_object_inventory.json` | `1c6935ef6bef94bb…` | 398.0 KB | Source object inventory for `asvs_v5_0_0` (post-extraction; pre-lifting). Items include source_object_id, title, statement, statement_kind, framework_family. |
| `data/asvs_v5_0_0/stubs/source_unit_inventory.json` | `6a6bd23246d49ed8…` | 269.4 KB | Source unit inventory for `asvs_v5_0_0` (per-textual-unit; inputs to source-object extraction). |
| `data/asvs_v5_0_0/stubs/source_retrieval_receipt.json` | `b8e9778d588dddc1…` | 2.0 KB | Source retrieval provenance receipt for `asvs_v5_0_0` (origin URL + checksums + retrieval timestamp; reproducibility anchor). |
| `data/capec_v3_9/stubs/source_object_inventory.json` | `fe5592be1235ae94…` | 837.5 KB | Source object inventory for `capec_v3_9` (post-extraction; pre-lifting). Items include source_object_id, title, statement, statement_kind, framework_family. |
| `data/cis_controls_v8_1/stubs/source_object_inventory.json` | `edc0819895bab1cd…` | 14.0 KB | Source object inventory for `cis_controls_v8_1` (post-extraction; pre-lifting). Items include source_object_id, title, statement, statement_kind, framework_family. |
| `data/cis_controls_v8_1/stubs/source_unit_inventory.json` | `1eb3005883293e3f…` | 11.5 KB | Source unit inventory for `cis_controls_v8_1` (per-textual-unit; inputs to source-object extraction). |
| `data/cis_controls_v8_1/stubs/source_retrieval_receipt.json` | `367d7faa68b746d3…` | 911 B | Source retrieval provenance receipt for `cis_controls_v8_1` (origin URL + checksums + retrieval timestamp; reproducibility anchor). |
| `data/cis_controls_v8_1_2/stubs/source_object_inventory.json` | `e6450c59066d1031…` | 137.9 KB | Source object inventory for `cis_controls_v8_1_2` (post-extraction; pre-lifting). Items include source_object_id, title, statement, statement_kind, framework_family. |
| `data/cwe_software_development_view_v4_19_1/stubs/source_object_inventory.json` | `e19b265ea8849668…` | 1.31 MB | Source object inventory for `cwe_software_development_view_v4_19_1` (post-extraction; pre-lifting). Items include source_object_id, title, statement, statement_kind, framework_family. |
| `data/cwe_software_development_view_v4_19_1/stubs/source_unit_inventory.json` | `af6b90d0da41016d…` | 676.0 KB | Source unit inventory for `cwe_software_development_view_v4_19_1` (per-textual-unit; inputs to source-object extraction). |
| `data/cwe_software_development_view_v4_19_1/stubs/source_retrieval_receipt.json` | `26fecca4dd6b39ee…` | 2.5 KB | Source retrieval provenance receipt for `cwe_software_development_view_v4_19_1` (origin URL + checksums + retrieval timestamp; reproducibility anchor). |
| `data/enisa_multilayer_ai_cybersecurity_practices_2023/stubs/source_object_inventory.json` | `ead12fc489d94ad4…` | 11.6 KB | Source object inventory for `enisa_multilayer_ai_cybersecurity_practices_2023` (post-extraction; pre-lifting). Items include source_object_id, title, statement, statement_kind, framework_family. |
| `data/enisa_multilayer_ai_cybersecurity_practices_2023/stubs/source_unit_inventory.json` | `bdd5f7b612f4008f…` | 159.1 KB | Source unit inventory for `enisa_multilayer_ai_cybersecurity_practices_2023` (per-textual-unit; inputs to source-object extraction). |
| `data/enisa_multilayer_ai_cybersecurity_practices_2023/stubs/source_retrieval_receipt.json` | `347c872f50aebe65…` | 1.0 KB | Source retrieval provenance receipt for `enisa_multilayer_ai_cybersecurity_practices_2023` (origin URL + checksums + retrieval timestamp; reproducibility anchor). |
| `data/eu_cra/stubs/source_object_inventory.json` | `9338730f75021a0c…` | 9.0 KB | Source object inventory for `eu_cra` (post-extraction; pre-lifting). Items include source_object_id, title, statement, statement_kind, framework_family. |
| `data/eu_dora/stubs/source_object_inventory.json` | `b97f22b336242cd6…` | 22.3 KB | Source object inventory for `eu_dora` (post-extraction; pre-lifting). Items include source_object_id, title, statement, statement_kind, framework_family. |
| `data/eu_nis2/stubs/source_object_inventory.json` | `3499eff2be37e467…` | 6.0 KB | Source object inventory for `eu_nis2` (post-extraction; pre-lifting). Items include source_object_id, title, statement, statement_kind, framework_family. |
| `data/eu_rgpd/stubs/source_object_inventory.json` | `bae1ba6b964ff9da…` | 9.0 KB | Source object inventory for `eu_rgpd` (post-extraction; pre-lifting). Items include source_object_id, title, statement, statement_kind, framework_family. |
| `data/hipaa_security_rule/stubs/source_object_inventory.json` | `8543c18761c9625f…` | 24.0 KB | Source object inventory for `hipaa_security_rule` (post-extraction; pre-lifting). Items include source_object_id, title, statement, statement_kind, framework_family. |
| `data/mcp_official_security_foundations_2025/stubs/source_object_inventory.json` | `fc90b5a9a65a6aa0…` | 14.2 KB | Source object inventory for `mcp_official_security_foundations_2025` (post-extraction; pre-lifting). Items include source_object_id, title, statement, statement_kind, framework_family. |
| `data/mcp_official_security_foundations_2025/stubs/source_unit_inventory.json` | `308cac4298c4e79c…` | 85.3 KB | Source unit inventory for `mcp_official_security_foundations_2025` (per-textual-unit; inputs to source-object extraction). |
| `data/mcp_official_security_foundations_2025/stubs/source_retrieval_receipt.json` | `f5b2a72ec009e053…` | 1009 B | Source retrieval provenance receipt for `mcp_official_security_foundations_2025` (origin URL + checksums + retrieval timestamp; reproducibility anchor). |
| `data/mitre_atlas/stubs/source_object_inventory.json` | `a7ae2e377f3c747c…` | 339.3 KB | Source object inventory for `mitre_atlas` (post-extraction; pre-lifting). Items include source_object_id, title, statement, statement_kind, framework_family. |
| `data/mitre_atlas/stubs/source_unit_inventory.json` | `c8a5201e6d578e41…` | 208.6 KB | Source unit inventory for `mitre_atlas` (per-textual-unit; inputs to source-object extraction). |
| `data/mitre_atlas/stubs/source_retrieval_receipt.json` | `18f277c17a0473a3…` | 1.2 KB | Source retrieval provenance receipt for `mitre_atlas` (origin URL + checksums + retrieval timestamp; reproducibility anchor). |
| `data/mitre_atlas/stubs/quality_dossier.json` | `8d1c64f1a07ad08c…` | 527 B | Stage 3 per-source quality dossier for `mitre_atlas` (atomicity ratio, decomposition method distribution, governance fraction, duplicate fraction; FLAG/PROCEED verdict). |
| `data/nist_ai_100_2_e2025/stubs/source_object_inventory.json` | `5b395eff1d9c4dcb…` | 170.8 KB | Source object inventory for `nist_ai_100_2_e2025` (post-extraction; pre-lifting). Items include source_object_id, title, statement, statement_kind, framework_family. |
| `data/nist_ai_100_2_e2025/stubs/source_unit_inventory.json` | `d14d67a7d5d07b8b…` | 153.0 KB | Source unit inventory for `nist_ai_100_2_e2025` (per-textual-unit; inputs to source-object extraction). |
| `data/nist_ai_100_2_e2025/stubs/source_retrieval_receipt.json` | `014290df7dc4d427…` | 1.1 KB | Source retrieval provenance receipt for `nist_ai_100_2_e2025` (origin URL + checksums + retrieval timestamp; reproducibility anchor). |
| `data/nist_ai_100_2_e2025/stubs/quality_dossier.json` | `461ee5e27b634d98…` | 488 B | Stage 3 per-source quality dossier for `nist_ai_100_2_e2025` (atomicity ratio, decomposition method distribution, governance fraction, duplicate fraction; FLAG/PROCEED verdict). |
| `data/nist_ai_rmf_1_0/stubs/source_object_inventory.json` | `dee54adf2a55e057…` | 70.2 KB | Source object inventory for `nist_ai_rmf_1_0` (post-extraction; pre-lifting). Items include source_object_id, title, statement, statement_kind, framework_family. |
| `data/nist_ai_rmf_1_0/stubs/source_unit_inventory.json` | `db212a58888f0b81…` | 32.5 KB | Source unit inventory for `nist_ai_rmf_1_0` (per-textual-unit; inputs to source-object extraction). |
| `data/nist_ai_rmf_1_0/stubs/source_retrieval_receipt.json` | `a6503e19e7555bee…` | 1.2 KB | Source retrieval provenance receipt for `nist_ai_rmf_1_0` (origin URL + checksums + retrieval timestamp; reproducibility anchor). |
| `data/nist_ai_rmf_1_0/stubs/quality_dossier.json` | `aabd067fb85fe5f5…` | 484 B | Stage 3 per-source quality dossier for `nist_ai_rmf_1_0` (atomicity ratio, decomposition method distribution, governance fraction, duplicate fraction; FLAG/PROCEED verdict). |
| `data/nist_sp800_53_rev5/stubs/source_object_inventory.json` | `de55ec22266e334b…` | 1.62 MB | Source object inventory for `nist_sp800_53_rev5` (post-extraction; pre-lifting). Items include source_object_id, title, statement, statement_kind, framework_family. |
| `data/owasp_dsomm/stubs/source_object_inventory.json` | `c45e4dc99ee244cf…` | 439.2 KB | Source object inventory for `owasp_dsomm` (post-extraction; pre-lifting). Items include source_object_id, title, statement, statement_kind, framework_family. |
| `data/owasp_dsomm/stubs/source_unit_inventory.json` | `22388d152321b2ea…` | 218.5 KB | Source unit inventory for `owasp_dsomm` (per-textual-unit; inputs to source-object extraction). |
| `data/owasp_dsomm/stubs/source_retrieval_receipt.json` | `f89ee10f9d5525f3…` | 2.2 KB | Source retrieval provenance receipt for `owasp_dsomm` (origin URL + checksums + retrieval timestamp; reproducibility anchor). |
| `data/owasp_llm_top_10/stubs/source_object_inventory.json` | `6d3ea14dc0afcbee…` | 77.3 KB | Source object inventory for `owasp_llm_top_10` (post-extraction; pre-lifting). Items include source_object_id, title, statement, statement_kind, framework_family. |
| `data/owasp_llm_top_10/stubs/source_unit_inventory.json` | `d46990ec8c4067bc…` | 74.4 KB | Source unit inventory for `owasp_llm_top_10` (per-textual-unit; inputs to source-object extraction). |
| `data/owasp_llm_top_10/stubs/source_retrieval_receipt.json` | `663e65aaadfa0e70…` | 7.3 KB | Source retrieval provenance receipt for `owasp_llm_top_10` (origin URL + checksums + retrieval timestamp; reproducibility anchor). |
| `data/owasp_llm_top_10/stubs/quality_dossier.json` | `6d0525c55ce78f56…` | 544 B | Stage 3 per-source quality dossier for `owasp_llm_top_10` (atomicity ratio, decomposition method distribution, governance fraction, duplicate fraction; FLAG/PROCEED verdict). |
| `data/owasp_mcp_secure_server_development_v1_0/stubs/source_object_inventory.json` | `cee9b3c2cb028afa…` | 8.8 KB | Source object inventory for `owasp_mcp_secure_server_development_v1_0` (post-extraction; pre-lifting). Items include source_object_id, title, statement, statement_kind, framework_family. |
| `data/owasp_mcp_secure_server_development_v1_0/stubs/source_unit_inventory.json` | `36d8f8f92dfbea0f…` | 30.1 KB | Source unit inventory for `owasp_mcp_secure_server_development_v1_0` (per-textual-unit; inputs to source-object extraction). |
| `data/owasp_mcp_secure_server_development_v1_0/stubs/source_retrieval_receipt.json` | `54a30889cc8374d7…` | 654 B | Source retrieval provenance receipt for `owasp_mcp_secure_server_development_v1_0` (origin URL + checksums + retrieval timestamp; reproducibility anchor). |
| `data/owasp_mcp_third_party_servers_v1_0/stubs/source_object_inventory.json` | `23a52d325a624ff8…` | 8.4 KB | Source object inventory for `owasp_mcp_third_party_servers_v1_0` (post-extraction; pre-lifting). Items include source_object_id, title, statement, statement_kind, framework_family. |
| `data/owasp_mcp_third_party_servers_v1_0/stubs/source_unit_inventory.json` | `1d0fb99e699646e7…` | 29.3 KB | Source unit inventory for `owasp_mcp_third_party_servers_v1_0` (per-textual-unit; inputs to source-object extraction). |
| `data/owasp_mcp_third_party_servers_v1_0/stubs/source_retrieval_receipt.json` | `4a4f27639a38a2c4…` | 998 B | Source retrieval provenance receipt for `owasp_mcp_third_party_servers_v1_0` (origin URL + checksums + retrieval timestamp; reproducibility anchor). |
| `data/owasp_mcp_top_10_v0_1_2025_beta/stubs/source_object_inventory.json` | `f533a4e4e064ab6b…` | 9.6 KB | Source object inventory for `owasp_mcp_top_10_v0_1_2025_beta` (post-extraction; pre-lifting). Items include source_object_id, title, statement, statement_kind, framework_family. |
| `data/owasp_mcp_top_10_v0_1_2025_beta/stubs/source_unit_inventory.json` | `0a15b4465c5585ac…` | 31.2 KB | Source unit inventory for `owasp_mcp_top_10_v0_1_2025_beta` (per-textual-unit; inputs to source-object extraction). |
| `data/owasp_mcp_top_10_v0_1_2025_beta/stubs/source_retrieval_receipt.json` | `8ba78666920d4dd5…` | 709 B | Source retrieval provenance receipt for `owasp_mcp_top_10_v0_1_2025_beta` (origin URL + checksums + retrieval timestamp; reproducibility anchor). |
| `data/owasp_ml_top_10/stubs/source_object_inventory.json` | `4badb298f1f325db…` | 30.7 KB | Source object inventory for `owasp_ml_top_10` (post-extraction; pre-lifting). Items include source_object_id, title, statement, statement_kind, framework_family. |
| `data/owasp_ml_top_10/stubs/source_unit_inventory.json` | `b6dca3b47aaddef3…` | 27.9 KB | Source unit inventory for `owasp_ml_top_10` (per-textual-unit; inputs to source-object extraction). |
| `data/owasp_ml_top_10/stubs/source_retrieval_receipt.json` | `1d4d51df47dba73a…` | 7.8 KB | Source retrieval provenance receipt for `owasp_ml_top_10` (origin URL + checksums + retrieval timestamp; reproducibility anchor). |
| `data/owasp_ml_top_10/stubs/quality_dossier.json` | `cd9aaaebf3de41d5…` | 496 B | Stage 3 per-source quality dossier for `owasp_ml_top_10` (atomicity ratio, decomposition method distribution, governance fraction, duplicate fraction; FLAG/PROCEED verdict). |
| `data/owasp_proactive_controls_2018/stubs/source_object_inventory.json` | `d6b0de36dc006f4e…` | 7.9 KB | Source object inventory for `owasp_proactive_controls_2018` (post-extraction; pre-lifting). Items include source_object_id, title, statement, statement_kind, framework_family. |
| `data/owasp_samm_v2_1/stubs/source_object_inventory.json` | `8c8eb18d00a38942…` | 423.2 KB | Source object inventory for `owasp_samm_v2_1` (post-extraction; pre-lifting). Items include source_object_id, title, statement, statement_kind, framework_family. |
| `data/owasp_samm_v2_1/stubs/source_unit_inventory.json` | `0bcc0709ac952cbb…` | 276.7 KB | Source unit inventory for `owasp_samm_v2_1` (per-textual-unit; inputs to source-object extraction). |
| `data/owasp_samm_v2_1/stubs/source_retrieval_receipt.json` | `2626834a1b680f84…` | 1.6 KB | Source retrieval provenance receipt for `owasp_samm_v2_1` (origin URL + checksums + retrieval timestamp; reproducibility anchor). |
| `data/owasp_top_10_2021/stubs/source_object_inventory.json` | `c2eea0b020ca3715…` | 7.3 KB | Source object inventory for `owasp_top_10_2021` (post-extraction; pre-lifting). Items include source_object_id, title, statement, statement_kind, framework_family. |
| `data/pci_dss_v4_0_1/stubs/source_object_inventory.json` | `61860db0f9757a61…` | 169.4 KB | Source object inventory for `pci_dss_v4_0_1` (post-extraction; pre-lifting). Items include source_object_id, title, statement, statement_kind, framework_family. |
| `data/slsa_spec_v1_0_build_track/stubs/source_object_inventory.json` | `88f7473e490bca70…` | 11.0 KB | Source object inventory for `slsa_spec_v1_0_build_track` (post-extraction; pre-lifting). Items include source_object_id, title, statement, statement_kind, framework_family. |
| `data/slsa_spec_v1_0_build_track/stubs/source_unit_inventory.json` | `15bf33b4985a7115…` | 60.4 KB | Source unit inventory for `slsa_spec_v1_0_build_track` (per-textual-unit; inputs to source-object extraction). |
| `data/slsa_spec_v1_0_build_track/stubs/source_retrieval_receipt.json` | `fb188086ebba4b39…` | 2.2 KB | Source retrieval provenance receipt for `slsa_spec_v1_0_build_track` (origin URL + checksums + retrieval timestamp; reproducibility anchor). |
| `data/ssdf_sp800_218_v1_1/stubs/source_object_inventory.json` | `c8fc6b40b71ba9e5…` | 65.7 KB | Source object inventory for `ssdf_sp800_218_v1_1` (post-extraction; pre-lifting). Items include source_object_id, title, statement, statement_kind, framework_family. |
| `data/ssdf_sp800_218_v1_1/stubs/source_unit_inventory.json` | `a2780f058dba441a…` | 17.3 KB | Source unit inventory for `ssdf_sp800_218_v1_1` (per-textual-unit; inputs to source-object extraction). |
| `data/ssdf_sp800_218_v1_1/stubs/source_retrieval_receipt.json` | `eb4ec848939a0067…` | 774 B | Source retrieval provenance receipt for `ssdf_sp800_218_v1_1` (origin URL + checksums + retrieval timestamp; reproducibility anchor). |

---

## Script artefacts

Pipeline drivers (PIPELINE 1 flatteners, PIPELINE 2 grounding, substrate emission), cross-validation drivers (SSDF / SCF / frontier audit), per-source extractors, common modules (encode, score, calibrate, schemas), figure emitter.

| Path | SHA-256 | Size | Description |
|---|---|---:|---|
| `scripts/v5_normalization/grounding/run_pipeline_v7.py` | `a91c31aa7a9dd7e3…` | 16.3 KB | PIPELINE 2 grounding driver — substrate v7 emission (claim-centric two-pipeline against AppSec Core V1.next + embeddings v1.1; 31 ACTIVE_SOURCES). |
| `scripts/v5_normalization/grounding/run_pipeline_v6.py` | `9d6d608536578090…` | 12.6 KB | PIPELINE 2 grounding driver — substrate v6 (predecessor; 26 sources). |
| `scripts/v5_normalization/grounding/run_pipeline_2.py` | `19b720f6372d8338…` | 18.1 KB | Phase 1b PIPELINE 2 entry point (substrate v5 era; superseded by run_pipeline_v6/v7 for later substrates). |
| `scripts/v5_normalization/grounding/emit_substrate_v7_ttl.py` | `fe0a79d43b1ec2cf…` | 2.5 KB | Emit substrate v7 claims as RDF Turtle for SHACL validation. |
| `scripts/v5_normalization/grounding/emit_substrate_v6_ttl.py` | `1c2a6520edac73ac…` | 2.8 KB | Emit substrate v6 claims as RDF Turtle (predecessor). |
| `scripts/v5_normalization/grounding/ldp_cluster_analysis_v7.py` | `f86b9002d7b8f9ed…` | 29.7 KB | Stage 6 LDP cluster analysis driver (agglomerative clustering on cosine distance; 3 granularities; ACR-candidacy lens). |
| `scripts/v5_normalization/grounding/encode.py` | `56ef17b8fcb4b9b2…` | 4.1 KB | SBERT encoder (sentence-transformers/all-MiniLM-L6-v2 @ HF revision c9745ed1; pinned). Augmentation symmetry §F mirror of Archon Part A build-script.py. |
| `scripts/v5_normalization/grounding/score.py` | `6d85a5350e79760d…` | 4.9 KB | Cosine score + claim emission (E2 admissibility + E3 disambiguation; per-(slice,level) margin). |
| `scripts/v5_normalization/grounding/calibrate_thresholds.py` | `01d01be16918c83c…` | 8.3 KB | Empirical E2/E3 threshold calibration on cohort {SSDF, CIS, SAMM, CWE}. |
| `scripts/v5_normalization/grounding/pydantic_schemas.py` | `538d3a8a8f538377…` | 3.3 KB | Pydantic schemas for SubstrateItem / Claim / SubstrateMeta — runtime invariant enforcement (P1' / M5 / referential integrity). |
| `scripts/v5_normalization/run_iteration_3_flatteners.py` | `3e23c9e3e124fac3…` | 6.4 KB | Iteration 3 5-pilot runner + Stage 3 quality dossier emitter (atomicity, decomposition methods, governance fraction estimates). |
| `scripts/v5_normalization/run_all_flatteners.py` | `d5d6b52de498d223…` | 6.3 KB | Phase 1a entry point — runs all 31 active flatteners (26 baseline + 5 iter-3); emits phase_1a_summary.json. |
| `scripts/v5_normalization/configs/source_configs.py` | `e4dbc269e96a1a0e…` | 15.2 KB | Per-source SourceConfig registry (31 entries; has_extractable_hierarchy / atomic_by_convention / decomposition_policy / hierarchy_levels / facet_fields). |
| `scripts/cross_validate_ssdf_references.py` | `681750b1b005ba7c…` | 27.7 KB | SSDF cross-reference validation (original; v3-era instance_level_mapping). Reused as resolver library by v7 variants. |
| `scripts/cross_validate_ssdf_references_v7.py` | `91d2f0c2babafa86…` | 17.5 KB | SSDF v7 cross-val (Variant B; CO-level-preferred primary anchor; reads v7 SUPPLIER directly). |
| `scripts/cross_validate_ssdf_references_v7_filtered.py` | `d6e35b2c28102cfa…` | 12.6 KB | SSDF v7 filtered (excludes OWASPASVS/MASVS/SCVS for version-drift isolation; tests version-drift hypothesis). |
| `scripts/cross_validate_scf_strm_v7.py` | `5564fa4ad7f3d83c…` | 16.4 KB | SCF v7 cross-val driver (PRIMARY oracle for §8.2). Per-pilot ID normalizers (NIST/CIS/SSDF/PCI/HIPAA/EU/OWASP). |
| `scripts/frontier_match_and_audit_v7.py` | `d12469fa0687dc49…` | 33.1 KB | 3-tier (strict/slice_primary/frontier) per-pair metric + per-task hit rate + XLSX writer. |
| `scripts/extract_iteration_3_ai_ml_sources.py` | `11f0fbe54f86ae27…` | 20.8 KB | 5-pilot batched extractor (MITRE ATLAS YAML / OWASP LLM Top 10 HTML / OWASP ML Top 10 HTML / NIST AI 100-2 + NIST AI RMF PDFs via pdftotext). |
| `scripts/figures/generate_p7_section_8_2_figures.py` | `1099d8276e338e4f…` | 19.1 KB | P7 §8.2 multi-claim alignment SVG figure emitter (3 figures via graphviz `dot`; subprocess invocation; 100% deterministic .dot → SVG/PDF/PNG step). |
| `scripts/v5_normalization/flattening/asvs_v5_0_0_flattener.py` | `cfba97f297d23d15…` | 1.5 KB | Per-source flattener for `asvs_v5_0_0` — extracts source items from inventory + composes contextualised_text per claim-centric two-pipeline. |
| `scripts/v5_normalization/flattening/capec_v3_9_flattener.py` | `bb9ecd0670208465…` | 1.6 KB | Per-source flattener for `capec_v3_9` — extracts source items from inventory + composes contextualised_text per claim-centric two-pipeline. |
| `scripts/v5_normalization/flattening/cis_controls_v8_1_2_flattener.py` | `14810054c9be441a…` | 1.8 KB | Per-source flattener for `cis_controls_v8_1_2` — extracts source items from inventory + composes contextualised_text per claim-centric two-pipeline. |
| `scripts/v5_normalization/flattening/cwe_software_development_view_v4_19_1_flattener.py` | `fbd375441359956d…` | 1.4 KB | Per-source flattener for `cwe_software_development_view_v4_19_1` — extracts source items from inventory + composes contextualised_text per claim-centric two-pipeline. |
| `scripts/v5_normalization/flattening/enisa_multilayer_ai_cybersecurity_practices_2023_flattener.py` | `036d0a4fc989e099…` | 1.2 KB | Per-source flattener for `enisa_multilayer_ai_cybersecurity_practices_2023` — extracts source items from inventory + composes contextualised_text per claim-centric two-pipeline. |
| `scripts/v5_normalization/flattening/eu_cra_flattener.py` | `32d6ecace5de9000…` | 289 B | Per-source flattener for `eu_cra` — extracts source items from inventory + composes contextualised_text per claim-centric two-pipeline. |
| `scripts/v5_normalization/flattening/eu_dora_flattener.py` | `75d03f7b027affa9…` | 293 B | Per-source flattener for `eu_dora` — extracts source items from inventory + composes contextualised_text per claim-centric two-pipeline. |
| `scripts/v5_normalization/flattening/eu_nis2_flattener.py` | `0f9f0d5b8bab6df8…` | 293 B | Per-source flattener for `eu_nis2` — extracts source items from inventory + composes contextualised_text per claim-centric two-pipeline. |
| `scripts/v5_normalization/flattening/eu_rgpd_flattener.py` | `2d4751bdd0779d32…` | 300 B | Per-source flattener for `eu_rgpd` — extracts source items from inventory + composes contextualised_text per claim-centric two-pipeline. |
| `scripts/v5_normalization/flattening/hipaa_security_rule_flattener.py` | `20439d34b138fe76…` | 1.4 KB | Per-source flattener for `hipaa_security_rule` — extracts source items from inventory + composes contextualised_text per claim-centric two-pipeline. |
| `scripts/v5_normalization/flattening/mcp_official_security_foundations_2025_flattener.py` | `4358d1db4a568fe8…` | 1.0 KB | Per-source flattener for `mcp_official_security_foundations_2025` — extracts source items from inventory + composes contextualised_text per claim-centric two-pipeline. |
| `scripts/v5_normalization/flattening/mitre_atlas_flattener.py` | `da8504f7efa3c810…` | 3.1 KB | Per-source flattener for `mitre_atlas` — extracts source items from inventory + composes contextualised_text per claim-centric two-pipeline. |
| `scripts/v5_normalization/flattening/nist_ai_100_2_e2025_flattener.py` | `23f754485334f83a…` | 2.6 KB | Per-source flattener for `nist_ai_100_2_e2025` — extracts source items from inventory + composes contextualised_text per claim-centric two-pipeline. |
| `scripts/v5_normalization/flattening/nist_ai_rmf_1_0_flattener.py` | `9c4ca0b0f77be435…` | 2.5 KB | Per-source flattener for `nist_ai_rmf_1_0` — extracts source items from inventory + composes contextualised_text per claim-centric two-pipeline. |
| `scripts/v5_normalization/flattening/nist_sp800_53_rev5_flattener.py` | `170bfd15f8a145fd…` | 1.8 KB | Per-source flattener for `nist_sp800_53_rev5` — extracts source items from inventory + composes contextualised_text per claim-centric two-pipeline. |
| `scripts/v5_normalization/flattening/owasp_dsomm_flattener.py` | `fc498a847add3b5e…` | 2.9 KB | Per-source flattener for `owasp_dsomm` — extracts source items from inventory + composes contextualised_text per claim-centric two-pipeline. |
| `scripts/v5_normalization/flattening/owasp_llm_top_10_flattener.py` | `200611f1a392f133…` | 1.2 KB | Per-source flattener for `owasp_llm_top_10` — extracts source items from inventory + composes contextualised_text per claim-centric two-pipeline. |
| `scripts/v5_normalization/flattening/owasp_mcp_secure_server_development_v1_0_flattener.py` | `29d4114f98fc1533…` | 1.0 KB | Per-source flattener for `owasp_mcp_secure_server_development_v1_0` — extracts source items from inventory + composes contextualised_text per claim-centric two-pipeline. |
| `scripts/v5_normalization/flattening/owasp_mcp_third_party_servers_v1_0_flattener.py` | `58d7b4d5051fb7de…` | 1023 B | Per-source flattener for `owasp_mcp_third_party_servers_v1_0` — extracts source items from inventory + composes contextualised_text per claim-centric two-pipeline. |
| `scripts/v5_normalization/flattening/owasp_mcp_top_10_v0_1_2025_beta_flattener.py` | `ecff62f1371da712…` | 1015 B | Per-source flattener for `owasp_mcp_top_10_v0_1_2025_beta` — extracts source items from inventory + composes contextualised_text per claim-centric two-pipeline. |
| `scripts/v5_normalization/flattening/owasp_ml_top_10_flattener.py` | `66ccaa961c2d47a2…` | 1.3 KB | Per-source flattener for `owasp_ml_top_10` — extracts source items from inventory + composes contextualised_text per claim-centric two-pipeline. |
| `scripts/v5_normalization/flattening/owasp_proactive_controls_2018_flattener.py` | `298af316a7f20b06…` | 1.0 KB | Per-source flattener for `owasp_proactive_controls_2018` — extracts source items from inventory + composes contextualised_text per claim-centric two-pipeline. |
| `scripts/v5_normalization/flattening/owasp_samm_v2_1_flattener.py` | `8aaf093b2eb0debf…` | 3.2 KB | Per-source flattener for `owasp_samm_v2_1` — extracts source items from inventory + composes contextualised_text per claim-centric two-pipeline. |
| `scripts/v5_normalization/flattening/owasp_top_10_2021_flattener.py` | `af824b440d88c5fe…` | 1.2 KB | Per-source flattener for `owasp_top_10_2021` — extracts source items from inventory + composes contextualised_text per claim-centric two-pipeline. |
| `scripts/v5_normalization/flattening/pci_dss_v4_0_1_flattener.py` | `d796a8e258a8ac11…` | 1.4 KB | Per-source flattener for `pci_dss_v4_0_1` — extracts source items from inventory + composes contextualised_text per claim-centric two-pipeline. |
| `scripts/v5_normalization/flattening/pci_sslc_v1_1_flattener.py` | `97b554b1a6cf4d76…` | 1.6 KB | Per-source flattener for `pci_sslc_v1_1` — extracts source items from inventory + composes contextualised_text per claim-centric two-pipeline. |
| `scripts/v5_normalization/flattening/safecode_agile_2012_flattener.py` | `7c60e39db963a124…` | 375 B | Per-source flattener for `safecode_agile_2012` — extracts source items from inventory + composes contextualised_text per claim-centric two-pipeline. |
| `scripts/v5_normalization/flattening/safecode_fpssd_2018_flattener.py` | `aca5dae61b575016…` | 580 B | Per-source flattener for `safecode_fpssd_2018` — extracts source items from inventory + composes contextualised_text per claim-centric two-pipeline. |
| `scripts/v5_normalization/flattening/safecode_sic_2010_flattener.py` | `834c85c128eaa1e3…` | 373 B | Per-source flattener for `safecode_sic_2010` — extracts source items from inventory + composes contextualised_text per claim-centric two-pipeline. |
| `scripts/v5_normalization/flattening/slsa_spec_v1_0_build_track_flattener.py` | `1de58c3fdd3d7477…` | 1.5 KB | Per-source flattener for `slsa_spec_v1_0_build_track` — extracts source items from inventory + composes contextualised_text per claim-centric two-pipeline. |
| `scripts/v5_normalization/flattening/ssdf_sp800_218_v1_1_flattener.py` | `82dcf49bff8688dc…` | 1.6 KB | Per-source flattener for `ssdf_sp800_218_v1_1` — extracts source items from inventory + composes contextualised_text per claim-centric two-pipeline. |
| `scripts/v5_normalization/flattening/_base.py` | `a7bb72acd2b42a48…` | 9.4 KB | Flattener base class — Base. |
| `scripts/v5_normalization/flattening/_eu_regulatory_base.py` | `ecce3e161e3a9184…` | 1.2 KB | Flattener base class — Eu Regulatory Base. |
| `scripts/v5_normalization/flattening/_safecode_base.py` | `33c81edaaa057a74…` | 1.7 KB | Flattener base class — Safecode Base. |
| `scripts/v5_normalization/common/compose_contextualised_text.py` | `f06a63017359ee52…` | 3.9 KB | Common pipeline module — Compose Contextualised Text. |
| `scripts/v5_normalization/common/lifted_row_schema.py` | `67a04a7e53459996…` | 950 B | Common pipeline module — Lifted Row Schema. |
| `scripts/v5_normalization/common/multiplicity_detector.py` | `373eb0f6cea3fd68…` | 8.9 KB | Common pipeline module — Multiplicity Detector. |

---

## Report artefacts

P7 §8.2 multi-claim alignment figures (3 figures × 4 formats: .dot / .svg / .pdf / -preview.png) + figure prompt specs + LLM-assist provenance log v7 addendum.

| Path | SHA-256 | Size | Description |
|---|---|---:|---|
| `data/p7_olir_audit/p7_v2_corrected/v7/reports/llm_assist_provenance_v7_addendum.md` | `983486671dc98ad4…` | 10.2 KB | v7 addendum to programme LLM-assist provenance log discipline. Phase 7.1 (Iteration 3 substrate emission) + Phase 7.2 (P7 Pass 6 cross-val deliveries) + Phase 7.3 (§8.2 figures). 11 J-points logged for joint-review inspection. Headline: 0 runtime LLM calls in pipeline execution. |
| `data/p7_olir_audit/p7_v2_corrected/v7/reports/figures/figure-1-pw8-sa11-multi-claim-alignment-preview.png` | `072934dbc082e19d…` | 189.5 KB | Programme-lead worked example: frontier match captures alignment that strict misses (PW.8 ↔ SA-11) — raster preview (150 dpi PNG). |
| `data/p7_olir_audit/p7_v2_corrected/v7/reports/figures/figure-1-pw8-sa11-multi-claim-alignment.dot` | `aefb34c367c7f935…` | 8.8 KB | Programme-lead worked example: frontier match captures alignment that strict misses (PW.8 ↔ SA-11) — graphviz DSL source ('the prompt'; declarative deterministic spec). |
| `data/p7_olir_audit/p7_v2_corrected/v7/reports/figures/figure-1-pw8-sa11-multi-claim-alignment.pdf` | `245afa8786ef4b76…` | 67.3 KB | Programme-lead worked example: frontier match captures alignment that strict misses (PW.8 ↔ SA-11) — LaTeX-ready PDF. |
| `data/p7_olir_audit/p7_v2_corrected/v7/reports/figures/figure-1-pw8-sa11-multi-claim-alignment.svg` | `d14900d256a63317…` | 27.0 KB | Programme-lead worked example: frontier match captures alignment that strict misses (PW.8 ↔ SA-11) — vector SVG (paper-quality). |
| `data/p7_olir_audit/p7_v2_corrected/v7/reports/figures/figure-2-po1-sa1-strict-match-baseline-preview.png` | `591f5d45801537ff…` | 200.4 KB | Strict primary-CO match clean baseline (PO.1 ↔ SA-1; both → ACO-TMR-008) — raster preview (150 dpi PNG). |
| `data/p7_olir_audit/p7_v2_corrected/v7/reports/figures/figure-2-po1-sa1-strict-match-baseline.dot` | `9ad732dd3e4e419a…` | 10.4 KB | Strict primary-CO match clean baseline (PO.1 ↔ SA-1; both → ACO-TMR-008) — graphviz DSL source ('the prompt'; declarative deterministic spec). |
| `data/p7_olir_audit/p7_v2_corrected/v7/reports/figures/figure-2-po1-sa1-strict-match-baseline.pdf` | `0d8837b93e89f9c6…` | 67.7 KB | Strict primary-CO match clean baseline (PO.1 ↔ SA-1; both → ACO-TMR-008) — LaTeX-ready PDF. |
| `data/p7_olir_audit/p7_v2_corrected/v7/reports/figures/figure-2-po1-sa1-strict-match-baseline.svg` | `6fe7e534d6e8e944…` | 31.2 KB | Strict primary-CO match clean baseline (PO.1 ↔ SA-1; both → ACO-TMR-008) — vector SVG (paper-quality). |
| `data/p7_olir_audit/p7_v2_corrected/v7/reports/figures/figure-3-po2-ops15-genuine-divergence-preview.png` | `f80362201ed0afd2…` | 172.3 KB | Honest disclosure: frontier=FALSE genuine semantic divergence (PO.2 ↔ SCAGILE-OPS-15) — raster preview (150 dpi PNG). |
| `data/p7_olir_audit/p7_v2_corrected/v7/reports/figures/figure-3-po2-ops15-genuine-divergence.dot` | `dfc39c655bf0be19…` | 6.6 KB | Honest disclosure: frontier=FALSE genuine semantic divergence (PO.2 ↔ SCAGILE-OPS-15) — graphviz DSL source ('the prompt'; declarative deterministic spec). |
| `data/p7_olir_audit/p7_v2_corrected/v7/reports/figures/figure-3-po2-ops15-genuine-divergence.pdf` | `683b544bd1959283…` | 67.5 KB | Honest disclosure: frontier=FALSE genuine semantic divergence (PO.2 ↔ SCAGILE-OPS-15) — LaTeX-ready PDF. |
| `data/p7_olir_audit/p7_v2_corrected/v7/reports/figures/figure-3-po2-ops15-genuine-divergence.svg` | `391f803d7d137ce7…` | 21.9 KB | Honest disclosure: frontier=FALSE genuine semantic divergence (PO.2 ↔ SCAGILE-OPS-15) — vector SVG (paper-quality). |
| `data/p7_olir_audit/p7_v2_corrected/v7/reports/figures/figures-p7-section-8-2-prompt-specs.md` | `41dd511ea33c850d…` | 9.7 KB | (no description) |

---

## Documentation artefacts

DSR-HISTORY round records (Cycle A Iteration 2 + 3) + Cartographer decisions + Iteration 3 evidence package brief + substrate v6 emission brief + P7 Pass 6 data delivery brief.

| Path | SHA-256 | Size | Description |
|---|---|---:|---|
| `docs/DSR-HISTORY/cycle-a-iter-2-substrate-v6-2026-05-05.md` | `ca71a69f0f14d400…` | 5.7 KB | Cycle A Iteration 2 substrate v6 emission DSR record (post-ACR-004 incorporation). |
| `docs/DSR-HISTORY/cycle-a-iter-3-2026-05-08.md` | `238f51cca1938bac…` | 8.7 KB | Cycle A Iteration 3 DSR Robustness Validation under AI/ML Expanded Source Pressure record. Termination evidence + Outcome A (DEFAULT, prose only) recommendation per pre-registered asymmetric burden of proof. |
| `agentic/decisions/0001-model-boundary-taxonomy.md` | `2dd8d551c4767caa…` | 6.3 KB | Decision 0001 — Model boundary gap class (Track 1). |
| `agentic/decisions/0002-pilot-staging-rationale.md` | `c5ad24cffcded1c9…` | 6.7 KB | Decision 0002 — Pilot staging rationale (extraction families + completeness checklist). |
| `agentic/decisions/0003-normalization-algorithm-redesign-2026-05-03-amendment-1-appendix-thresholds.md` | `d99a5b8a40ed2ef2…` | 5.4 KB | Decision 0003 Amendment 1 Appendix — calibration threshold rationale (e2_pct=40 / e3_pct=60). NOTE: main Decision 0003 + Amendment 1 documents are referenced throughout substrate evidence but NOT in canonical agentic/decisions/ — see "Gap flag" in this inventory. |
| `agentic/briefs/2026-05-05-substrate-v6-acr004-incorporated.md` | `8fd51c5d2a59a80d…` | 6.9 KB | Substrate v6 emission brief (Iteration 2; ACR-004 Output Rendering Safety promotion incorporation). |
| `agentic/briefs/2026-05-08-iteration-3-evidence-package.md` | `8a376fb76f38643d…` | 15.8 KB | Iteration 3 joint-review evidence package brief (Stage 8). H2 confirmed; Cartographer-recommended Outcome A; full A/B/C asymmetric-burden analysis. |
| `agentic/briefs/2026-05-08-p7-pass-6-data-delivery.md` | `f7836ed49dd7f5d3…` | 15.0 KB | P7 Pass 6 data delivery (Items 1+2+3): SSDF v7 cross-val + LLM-assist null-result + per-source metadata table. |

---

## Gap flag — Decision 0003 main + Amendment 1 main

Programme-lead visibility / Curator coordination action item:

- Substrate v6/v7 evidence chain consistently cites `agentic/decisions/0003-normalization-algorithm-redesign-2026-05-03.md` (main) + `…-amendment-1-claims-not-chains.md` (Amendment 1 main).
- These reference documents exist as untracked files in the parent ESI checkout (branch `p7-v2-stage-6-v1-lab-overlay`) but **NOT in canonical agentic/decisions/ at HEAD or any tag-reachable commit**.
- Only the `…-amendment-1-appendix-thresholds.md` file is in canonical history (committed via substrate v5 emission commit `11355c9`).
- For figshare deposit reproducibility/auditability, recommend Curator + programme-lead coordinate to bring the main 0003 + Amendment 1 documents into canonical history before bundle finalisation.

This gap does NOT affect substrate v7 reproducibility (the algorithm is fully documented in scripts + appendix-thresholds + DSR-HISTORY records), but it affects the methodology audit trail completeness.

---

## License + citation

Per programme convention (Curator confirms with programme-lead):
- Documentation: CC BY-SA 4.0
- Code: Apache-2.0
- Data: ODbL (Open Database License)

Citation: programme DOI 10.17605/OSF.IO/7T849 + Cycle A frozen tag `cycle-a-frozen-2026-05-08` + figshare DOI when assigned + paper DOIs (P6, P7) when assigned.