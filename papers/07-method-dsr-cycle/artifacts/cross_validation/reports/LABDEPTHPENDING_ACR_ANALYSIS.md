# LabDepthPending ACR Analysis — v7 Substrate (Iteration 3 AI/ML expansion)

**Substrate:** `data/p7_olir_audit/p7_v2_corrected/v7/SUPPLIER_v7_0.json`
**Iteration:** Cycle A Iteration 3 (DSR Robustness Validation under AI/ML Expanded Source Pressure)
**Date:** 2026-05-08
**Author:** Cartographer (READ-ONLY analysis)
**Substrate baseline:** `substrate-v6-acr004-incorporated` (= ff28860; v6, 26 sources)
**v5 LDP analysis baseline:** `data/p7_olir_audit/p7_v2_corrected/v5/reports/LABDEPTHPENDING_ACR_ANALYSIS.md` (canonical pre-Iteration-3 cluster baseline)

> **Discipline note.** Cartographer presents clusters with cross-source convergence and adjacency diagnostics. **No ACR decisions are made here.** Decisions remain joint review by programme-lead + Orchestrator + Archon (per ACR review discipline; `feedback_acr_joint_review.md`). Items are flagged `adjacent_candidate` only at the cluster level for downstream review.

> **Joint-review HALT resolution 2026-05-08.** GROUNDED rate 74.41% < 75.38% v6 baseline accepted as corpus-expansion statistical artifact (NOT methodology regression); 26 baseline reproduces bit-identically; 5 iter-3 sources at domain-appropriate rates 58.5%–90%. Substrate v7 ratified for Iteration 3 evidence base. This Stage 6 LDP analysis is the formal post-substrate-v7 cluster-analysis deliverable.

---

## 1. Population

| Metric | Value |
|---|---:|
| Total v7 items | 3861 |
| GROUNDED | 2873 |
| **LabDepthPending (LDP) — analysed here** | **988** |
| OOS_AppSec | 0 |
| LDP fraction | 25.59% |

## 2. Per-source LDP profile

Top contributors to LDP population (sorted by count):

| Source | LDP count | mean top-1 | median top-1 | iter-3? |
|---|---:|---:|---:|:---:|
| cwe_software_development_view_v4_19_1 | 247 | 0.321 | 0.335 |   |
| capec_v3_9 | 204 | 0.355 | 0.360 |   |
| nist_sp800_53_rev5 | 204 | 0.356 | 0.361 |   |
| mitre_atlas | 98 | 0.374 | 0.378 | ✓ |
| asvs_v5_0_0 | 95 | 0.352 | 0.361 |   |
| owasp_dsomm | 23 | 0.367 | 0.366 |   |
| nist_ai_rmf_1_0 | 22 | 0.368 | 0.381 | ✓ |
| cis_controls_v8_1_2 | 18 | 0.378 | 0.385 |   |
| pci_dss_v4_0_1 | 16 | 0.337 | 0.334 |   |
| nist_ai_100_2_e2025 | 15 | 0.363 | 0.365 | ✓ |
| eu_dora | 13 | 0.388 | 0.371 |   |
| eu_cra | 5 | 0.404 | 0.406 |   |
| mcp_official_security_foundations_2025 | 5 | 0.395 | 0.386 |   |
| ssdf_sp800_218_v1_1 | 5 | 0.374 | 0.393 |   |
| eu_rgpd | 3 | 0.393 | 0.402 |   |
| hipaa_security_rule | 3 | 0.410 | 0.381 |   |
| safecode_agile_2012 | 3 | 0.360 | 0.370 |   |
| owasp_mcp_third_party_servers_v1_0 | 2 | 0.416 | 0.416 |   |
| owasp_mcp_top_10_v0_1_2025_beta | 2 | 0.396 | 0.396 |   |
| enisa_multilayer_ai_cybersecurity_practices_2023 | 1 | 0.413 | 0.413 |   |
| owasp_llm_top_10 | 1 | 0.575 | 0.575 | ✓ |
| owasp_ml_top_10 | 1 | 0.393 | 0.393 | ✓ |
| owasp_top_10_2021 | 1 | 0.441 | 0.441 |   |
| slsa_spec_v1_0_build_track | 1 | 0.361 | 0.361 |   |

## 3. Clustering

Items embedded with SBERT all-MiniLM-L6-v2 @ revision `c9745ed1` (augmentation symmetry §F preserved against ontology embeddings v1.1). Three granularities of agglomerative clustering on cosine distance (mirrors v5 LDP method):

| Granularity | distance threshold | n_clusters |
|---|---:|---:|
| Tight | 0.55 | 382 |
| Broad | 0.65 | 201 |
| Coarse | 0.75 | 77 ← used below |

## 4. ACR-candidacy framing — Iteration 3 burden of proof

Per dispatcher §4 (Outcome A/B/C asymmetric burden of proof) + `feedback_acr_appsec_core_engineering_only.md`:

- **Outcome A (DEFAULT, prose only):** sustained without positive evidence
- **Outcome B (Practice/Mechanism expansion):** ≥3 INDEPENDENT source families STRONG
- **Outcome C (CO/Slice expansion forced, H1 refuted):** ≥4 INDEPENDENT families + structural inadequacy + extraordinary joint-review consensus

Sources within the same family count as ONE for INDEPENDENT family calculation. Source family map per `SOURCE_FAMILY` in script.

## 5. Categorisation summary

Coarse-clustering yielded **77 clusters** of 988 LDP items.

| Category | n_clusters | n_items |
|---|---:|---:|
| **STRONG (≥3 INDEPENDENT families)** | **27** | 713 |
| MODERATE (2 families) | 22 | 123 |
| WEAK (1 family, size ≥ 2) | 18 | 142 |
| Singletons (1 item) | 10 | 10 |
| **AI/ML-inflected (≥1 iter-3 source)** | **14** | 314 |

## 6. STRONG ACR candidates (≥3 INDEPENDENT source families)

### CID7-011

**Size:** 118 items · **Sources:** 3 (3 INDEPENDENT families) · **avg/med top-1:** 0.3224/0.3399

**Independent families:** MITRE_CWE, MITRE_CAPEC, OWASP_DSOMM
**AI/ML inflected:** NO

**Top-3 closest Core entities (by top-1 vote count):**

| Rank | Target | Votes |
|---|---|---:|
| 1 | `ACO-IVF-005` | 29 |
| 2 | `ACO-IVF-003` | 17 |
| 3 | `ACO-IVF-002` | 4 |

**Sample items:**

- `[capec_v3_9/CAPEC-228]` top-1 `ACO-IVF-003` (0.439) — DTD Injection. DTD Injection. An attacker injects malicious content into an application's DTD in an attempt to produce a…
- `[cwe_software_development_view_v4_19_1/CWE-1024]` top-1 `ACO-IVF-003` (0.316) — Comparison of Incompatible Types. The product performs a comparison between two entities, but the entities are of differ…
- `[cwe_software_development_view_v4_19_1/CWE-1025]` top-1 `ACM-IVF-001` (0.337) — Comparison Using Wrong Factors. The code performs a comparison between two entities, but the comparison examines the wro…

### CID7-027

**Size:** 102 items · **Sources:** 9 (8 INDEPENDENT families) · **avg/med top-1:** 0.3731/0.3761

**Independent families:** MITRE_ATLAS, NIST_AI_TAXONOMY, MITRE_CAPEC, OWASP_MCP, CIS, MITRE_CWE, NIST_800_53, OWASP_TOP10
**AI/ML inflected:** YES

**Top-3 closest Core entities (by top-1 vote count):**

| Rank | Target | Votes |
|---|---|---:|
| 1 | `ACO-TMR-005` | 9 |
| 2 | `ACM-SCBI-002` | 7 |
| 3 | `ACO-TSV-006` | 7 |

**Sample items:**

- `[capec_v3_9/CAPEC-167]` top-1 `ACM-TSV-001` (0.375) — White Box Reverse Engineering. White Box Reverse Engineering. An attacker discovers the structure, function, and composi…
- `[capec_v3_9/CAPEC-185]` top-1 `ACO-TMR-004` (0.361) — Malicious Software Download. Malicious Software Download. An attacker uses deceptive methods to cause a user or an autom…
- `[capec_v3_9/CAPEC-189]` top-1 `ACM-TSV-001` (0.404) — Black Box Reverse Engineering. Black Box Reverse Engineering. An adversary discovers the structure, function, and compos…

### CID7-033

**Size:** 57 items · **Sources:** 5 (5 INDEPENDENT families) · **avg/med top-1:** 0.3532/0.3609

**Independent families:** MITRE_CAPEC, CIS, MITRE_CWE, ASVS, MCP_OFFICIAL
**AI/ML inflected:** NO

**Top-3 closest Core entities (by top-1 vote count):**

| Rank | Target | Votes |
|---|---|---:|
| 1 | `ACO-IVF-008` | 10 |
| 2 | `ACO-IVF-005` | 9 |
| 3 | `ACP-IAT-005` | 7 |

**Sample items:**

- `[asvs_v5_0_0/ASVS-REQ-V17.3.1]` top-1 `ACP-ITS-004` (0.407) — Verify that the signaling server is able to continue processing legitimate incoming signaling messages during a flood at…
- `[capec_v3_9/CAPEC-33]` top-1 `ACP-IAT-005` (0.390) — HTTP Request Smuggling. HTTP Request Smuggling. An adversary abuses the flexibility and discrepancies in the parsing and…
- `[capec_v3_9/CAPEC-34]` top-1 `ACO-IVF-008` (0.391) — HTTP Response Splitting. HTTP Response Splitting. An adversary manipulates and injects malicious content, in the form of…

### CID7-030

**Size:** 47 items · **Sources:** 3 (3 INDEPENDENT families) · **avg/med top-1:** 0.3497/0.3526

**Independent families:** MITRE_CAPEC, NIST_800_53, MITRE_ATLAS
**AI/ML inflected:** YES

**Top-3 closest Core entities (by top-1 vote count):**

| Rank | Target | Votes |
|---|---|---:|
| 1 | `ACO-IAT-006` | 13 |
| 2 | `ACO-ITS-003` | 8 |
| 3 | `ACP-IAT-001` | 4 |

**Sample items:**

- `[capec_v3_9/CAPEC-158]` top-1 `ACO-ITS-003` (0.384) — Sniffing Network Traffic. Sniffing Network Traffic. In this attack pattern, the adversary monitors network traffic betwe…
- `[capec_v3_9/CAPEC-173]` top-1 `ACP-IAT-001` (0.407) — Action Spoofing. Action Spoofing. An adversary is able to disguise one action for another and therefore trick a user int…
- `[capec_v3_9/CAPEC-313]` top-1 `ACP-SPC-005` (0.411) — Passive OS Fingerprinting. Passive OS Fingerprinting. An adversary engages in activity to detect the version or type of …

### CID7-022

**Size:** 42 items · **Sources:** 5 (5 INDEPENDENT families) · **avg/med top-1:** 0.3582/0.371

**Independent families:** MITRE_CAPEC, ASVS, MITRE_CWE, MITRE_ATLAS, SAFECODE
**AI/ML inflected:** YES

**Top-3 closest Core entities (by top-1 vote count):**

| Rank | Target | Votes |
|---|---|---:|
| 1 | `ACM-TMR-005` | 6 |
| 2 | `ACP-SPC-001` | 6 |
| 3 | `ACO-RPR-009` | 5 |

**Sample items:**

- `[asvs_v5_0_0/ASVS-REQ-V5.1.1]` top-1 `ACP-IVF-002` (0.338) — Verify that the documentation defines the permitted file types, expected file extensions…
- `[asvs_v5_0_0/ASVS-REQ-V5.2.1]` top-1 `ACO-IVF-005` (0.390) — Verify that the application will only accept files of a size which it can process without causing a loss of performance …
- `[asvs_v5_0_0/ASVS-REQ-V5.2.2]` top-1 `ACP-SCBI-002` (0.374) — Verify that when the application accepts a file, either on its own or within an archive such as a zip file, it checks if…

### CID7-064

**Size:** 37 items · **Sources:** 3 (3 INDEPENDENT families) · **avg/med top-1:** 0.3515/0.3611

**Independent families:** ASVS, MITRE_CWE, MCP_OFFICIAL
**AI/ML inflected:** NO

**Top-3 closest Core entities (by top-1 vote count):**

| Rank | Target | Votes |
|---|---|---:|
| 1 | `ACO-IAT-004` | 9 |
| 2 | `ACP-IAT-005` | 6 |
| 3 | `ACO-IAT-002` | 5 |

**Sample items:**

- `[asvs_v5_0_0/ASVS-REQ-V3.3.1]` top-1 `ACO-IAT-004` (0.252) — Verify that cookies have the 'Secure' attribute set, and if the '\__Host-' prefix is not used for the cookie name, the '…
- `[asvs_v5_0_0/ASVS-REQ-V3.3.2]` top-1 `ACO-IAT-004` (0.384) — Verify that each cookie's 'SameSite' attribute value is set according to the purpose of the cookie, to limit exposure to…
- `[asvs_v5_0_0/ASVS-REQ-V3.3.3]` top-1 `ACO-IAT-004` (0.228) — Verify that cookies have the '__Host-' prefix for the cookie name unless they are explicitly designed to be shared with …

### CID7-044

**Size:** 35 items · **Sources:** 5 (3 INDEPENDENT families) · **avg/med top-1:** 0.3745/0.3722

**Independent families:** EU, NIST_800_53, ASVS
**AI/ML inflected:** NO

**Top-3 closest Core entities (by top-1 vote count):**

| Rank | Target | Votes |
|---|---|---:|
| 1 | `ACO-TMR-008` | 3 |
| 2 | `ACO-RPR-001` | 2 |
| 3 | `ACM-TMR-002` | 2 |

**Sample items:**

- `[asvs_v5_0_0/ASVS-REQ-V14.2.6]` top-1 `ACO-IVF-005` (0.372) — Verify that the application only returns the minimum required sensitive data for the application's functionality. For ex…
- `[eu_cra/CRA-ART-15]` top-1 `ACO-RPR-001` (0.406) — CRA Article 15. Article 15 (Voluntary reporting) provides that manufacturers, importers and distributors may, on a volun…
- `[eu_cra/CRA-ART-16]` top-1 `ACP-ITS-003` (0.412) — CRA Article 16. Article 16 (Other provisions related to reporting) sets out modalities and confidentiality safeguards fo…

### CID7-026

**Size:** 34 items · **Sources:** 4 (4 INDEPENDENT families) · **avg/med top-1:** 0.3803/0.3897

**Independent families:** NIST_AI_RMF, MITRE_ATLAS, ENISA, NIST_800_53
**AI/ML inflected:** YES

**Top-3 closest Core entities (by top-1 vote count):**

| Rank | Target | Votes |
|---|---|---:|
| 1 | `ACO-TMR-002` | 8 |
| 2 | `ACO-TMR-005` | 6 |
| 3 | `ACM-SCBI-002` | 2 |

**Sample items:**

- `[enisa_multilayer_ai_cybersecurity_practices_2023/ENISA-AI-FAICP-LAYER-I]` top-1 `ACO-TMR-002` (0.413) — Layer I - Cybersecurity foundations for AI-hosting ICT environments. A multilayer framework for good cybersecurity pract…
- `[mitre_atlas/AML.TA0015]` top-1 `ACO-TMR-002` (0.390) — Lateral Movement. The adversary is trying to move through your AI environment.

Lateral Movement consists of techniques …
- `[mitre_atlas/AML.T0000]` top-1 `ACM-TMR-005` (0.393) — Search Open Technical Databases. Adversaries may search for publicly available research and technical documentation to l…

### CID7-009

**Size:** 26 items · **Sources:** 3 (3 INDEPENDENT families) · **avg/med top-1:** 0.3011/0.3141

**Independent families:** MITRE_CWE, MITRE_CAPEC, ASVS
**AI/ML inflected:** NO

**Top-3 closest Core entities (by top-1 vote count):**

| Rank | Target | Votes |
|---|---|---:|
| 1 | `ACO-IVF-005` | 7 |
| 2 | `ACP-IVF-005` | 3 |
| 3 | `ACO-IVF-003` | 2 |

**Sample items:**

- `[asvs_v5_0_0/ASVS-REQ-V1.4.2]` top-1 `ACP-IVF-001` (0.404) — Verify that sign, range, and input validation techniques are used to prevent integer overflows.…
- `[capec_v3_9/CAPEC-47]` top-1 `ACO-IVF-003` (0.318) — Buffer Overflow via Parameter Expansion. Buffer Overflow via Parameter Expansion. In this attack, the target software is…
- `[capec_v3_9/CAPEC-92]` top-1 `ACP-IAT-005` (0.332) — Forced Integer Overflow. Forced Integer Overflow. This attack forces an integer variable to go out of range. The integer…

### CID7-052

**Size:** 23 items · **Sources:** 5 (5 INDEPENDENT families) · **avg/med top-1:** 0.3824/0.3814

**Independent families:** NIST_800_53, CIS, MITRE_ATLAS, OWASP_DSOMM, PCI
**AI/ML inflected:** YES

**Top-3 closest Core entities (by top-1 vote count):**

| Rank | Target | Votes |
|---|---|---:|
| 1 | `ACM-TSV-004` | 4 |
| 2 | `ACP-TSV-006` | 3 |
| 3 | `ACP-TMR-001` | 3 |

**Sample items:**

- `[cis_controls_v8_1_2/CIS-14.5]` top-1 `ACO-ATB-003` (0.405) — Train Workforce Members on Causes of Unintentional Data Exposure. Train workforce members to be aware of causes for unin…
- `[mitre_atlas/AML.T0005.002]` top-1 `ACO-TMR-001` (0.465) — Use Pre-Trained Model. Adversaries may use an off-the-shelf pre-trained model as a proxy for the victim model to aid in …
- `[nist_sp800_53_rev5/SP800-53-AT-2.1]` top-1 `ACP-TSV-006` (0.291) — Practical Exercises. Provide practical exercises in literacy training that simulate events and incidents.…

### CID7-025

**Size:** 22 items · **Sources:** 4 (4 INDEPENDENT families) · **avg/med top-1:** 0.377/0.3811

**Independent families:** MITRE_CAPEC, NIST_800_53, CIS, OWASP_DSOMM
**AI/ML inflected:** NO

**Top-3 closest Core entities (by top-1 vote count):**

| Rank | Target | Votes |
|---|---|---:|
| 1 | `ACO-TMR-004` | 3 |
| 2 | `ACO-ITS-003` | 2 |
| 3 | `ACO-IVF-004` | 2 |

**Sample items:**

- `[capec_v3_9/CAPEC-407]` top-1 `ACO-TMR-004` (0.414) — Pretexting. Pretexting. An adversary engages in pretexting behavior to solicit information from target persons, or manip…
- `[capec_v3_9/CAPEC-410]` top-1 `ACO-ITS-003` (0.375) — Information Elicitation. Information Elicitation. An adversary engages an individual using any combination of social eng…
- `[capec_v3_9/CAPEC-412]` top-1 `ACO-IVF-004` (0.417) — Pretexting via Customer Service. Pretexting via Customer Service. An adversary engages in pretexting behavior, assuming …

### CID7-053

**Size:** 22 items · **Sources:** 4 (4 INDEPENDENT families) · **avg/med top-1:** 0.3573/0.3567

**Independent families:** NIST_800_53, HIPAA, NIST_SSDF, NIST_AI_RMF
**AI/ML inflected:** YES

**Top-3 closest Core entities (by top-1 vote count):**

| Rank | Target | Votes |
|---|---|---:|
| 1 | `ACP-TMR-001` | 3 |
| 2 | `ACP-RPR-001` | 3 |
| 3 | `ACP-TMR-009` | 3 |

**Sample items:**

- `[hipaa_security_rule/HIPAA-164-308a7]` top-1 `ACP-TMR-001` (0.374) — Contingency Plan. Contingency Plan — Administrative Safeguard. Establish (and implement as needed) policies and procedur…
- `[hipaa_security_rule/HIPAA-164-314b1]` top-1 `ACO-TMR-008` (0.381) — Requirements for Group Health Plans. Requirements for Group Health Plans — Organizational Requirement. Except when the o…
- `[nist_ai_rmf_1_0/NIST-AI-RMF-MAP-1.2]` top-1 `ACP-ITS-001` (0.286) — Interdisciplinary AI actors, competencies, skills, and. capacities for establishing context reflect demographic diversit…

### CID7-008

**Size:** 20 items · **Sources:** 3 (3 INDEPENDENT families) · **avg/med top-1:** 0.2947/0.2951

**Independent families:** MITRE_CWE, OWASP_DSOMM, SAFECODE
**AI/ML inflected:** NO

**Top-3 closest Core entities (by top-1 vote count):**

| Rank | Target | Votes |
|---|---|---:|
| 1 | `ACM-IVF-001` | 5 |
| 2 | `ACP-SPC-001` | 3 |
| 3 | `ACO-IVF-003` | 2 |

**Sample items:**

- `[cwe_software_development_view_v4_19_1/CWE-1052]` top-1 `ACO-IVF-003` (0.342) — Excessive Use of Hard-Coded Literals in Initialization. The product initializes a data element using a hard-coded litera…
- `[cwe_software_development_view_v4_19_1/CWE-1071]` top-1 `ACO-SPC-001` (0.292) — Empty Code Block. The source code contains a block that does not contain any code, i.e., the block is empty.…
- `[cwe_software_development_view_v4_19_1/CWE-1080]` top-1 `ACP-SPC-001` (0.356) — Source Code File with Excessive Number of Lines of Code. A source code file has too many lines of code.…

### CID7-065

**Size:** 18 items · **Sources:** 4 (4 INDEPENDENT families) · **avg/med top-1:** 0.3351/0.3309

**Independent families:** ASVS, MITRE_CWE, PCI, MITRE_CAPEC
**AI/ML inflected:** NO

**Top-3 closest Core entities (by top-1 vote count):**

| Rank | Target | Votes |
|---|---|---:|
| 1 | `ACO-IAT-001` | 5 |
| 2 | `ACO-IAT-002` | 3 |
| 3 | `ACP-IAT-001` | 2 |

**Sample items:**

- `[asvs_v5_0_0/ASVS-REQ-V6.2.1]` top-1 `ACO-IAT-001` (0.315) — Verify that user set passwords are at least 8 characters in length although a minimum of 15 characters is strongly recom…
- `[asvs_v5_0_0/ASVS-REQ-V6.2.2]` top-1 `ACO-IAT-003` (0.385) — Verify that users can change their password.…
- `[asvs_v5_0_0/ASVS-REQ-V6.2.3]` top-1 `ACP-IAT-001` (0.323) — Verify that password change functionality requires the user's current and new password.…

### CID7-067

**Size:** 16 items · **Sources:** 3 (3 INDEPENDENT families) · **avg/med top-1:** 0.3437/0.3484

**Independent families:** NIST_800_53, ASVS, PCI
**AI/ML inflected:** NO

**Top-3 closest Core entities (by top-1 vote count):**

| Rank | Target | Votes |
|---|---|---:|
| 1 | `ACO-IAT-004` | 4 |
| 2 | `ACP-IAT-001` | 4 |
| 3 | `ACO-IAT-001` | 2 |

**Sample items:**

- `[asvs_v5_0_0/ASVS-REQ-V7.1.2]` top-1 `ACP-IAT-004` (0.399) — Verify that the documentation defines how many concurrent (parallel) sessions are allowed for one account as well as the…
- `[asvs_v5_0_0/ASVS-REQ-V7.4.2]` top-1 `ACO-IAT-004` (0.410) — Verify that the application terminates all active sessions when a user account is disabled or deleted (such as an employ…
- `[asvs_v5_0_0/ASVS-REQ-V7.4.3]` top-1 `ACP-IAT-001` (0.390) — Verify that the application gives the option to terminate all other active sessions after a successful change or removal…

### CID7-021

**Size:** 15 items · **Sources:** 5 (5 INDEPENDENT families) · **avg/med top-1:** 0.427/0.4111

**Independent families:** OWASP_DSOMM, NIST_800_53, PCI, CIS, EU
**AI/ML inflected:** NO

**Top-3 closest Core entities (by top-1 vote count):**

| Rank | Target | Votes |
|---|---|---:|
| 1 | `ACP-TSV-001` | 3 |
| 2 | `ACP-TSV-005` | 2 |
| 3 | `ACM-TSV-001` | 2 |

**Sample items:**

- `[cis_controls_v8_1_2/CIS-18]` top-1 `ACP-TSV-001` (0.561) — Penetration Testing. Test the effectiveness and resiliency of enterprise assets through identifying and exploiting weakn…
- `[eu_dora/DORA-ART-26]` top-1 `ACP-TSV-005` (0.511) — DORA Article 26. Article 26 (Advanced testing of ICT tools, systems and processes based on TLPT) requires financial enti…
- `[nist_sp800_53_rev5/SP800-53-CA-8.1]` top-1 `ACM-TSV-002` (0.411) — Independent Penetration Testing Agent or Team. Employ an independent penetration testing agent or team to perform penetr…

### CID7-024

**Size:** 14 items · **Sources:** 5 (5 INDEPENDENT families) · **avg/med top-1:** 0.4114/0.3999

**Independent families:** MITRE_CAPEC, ASVS, MITRE_ATLAS, CIS, OWASP_TOP10
**AI/ML inflected:** YES

**Top-3 closest Core entities (by top-1 vote count):**

| Rank | Target | Votes |
|---|---|---:|
| 1 | `ACO-IVF-003` | 3 |
| 2 | `ACM-IVF-001` | 2 |
| 3 | `ACO-IVF-008` | 2 |

**Sample items:**

- `[asvs_v5_0_0/ASVS-REQ-V1.3.3]` top-1 `ACM-IVF-001` (0.476) — Verify that data being passed to a potentially dangerous context is sanitized beforehand to enforce safety measures, suc…
- `[asvs_v5_0_0/ASVS-REQ-V1.3.8]` top-1 `ACM-IVF-001` (0.439) — Verify that the application appropriately sanitizes untrusted input before use in Java Naming and Directory Interface (J…
- `[asvs_v5_0_0/ASVS-REQ-V1.3.9]` top-1 `ACO-IVF-005` (0.329) — Verify that the application sanitizes content before it is sent to memcache to prevent injection attacks.…

### CID7-063

**Size:** 14 items · **Sources:** 4 (4 INDEPENDENT families) · **avg/med top-1:** 0.3819/0.3945

**Independent families:** ASVS, MITRE_CAPEC, MITRE_CWE, SAFECODE
**AI/ML inflected:** NO

**Top-3 closest Core entities (by top-1 vote count):**

| Rank | Target | Votes |
|---|---|---:|
| 1 | `ACP-ITS-003` | 4 |
| 2 | `ACP-ITS-004` | 3 |
| 3 | `ACO-IVF-005` | 2 |

**Sample items:**

- `[asvs_v5_0_0/ASVS-REQ-V4.4.1]` top-1 `ACO-ITS-003` (0.274) — Verify that WebSocket over TLS (WSS) is used for all WebSocket connections.…
- `[asvs_v5_0_0/ASVS-REQ-V4.4.2]` top-1 `ACP-IAT-005` (0.215) — Verify that, during the initial HTTP WebSocket handshake, the Origin header field is checked against a list of origins a…
- `[asvs_v5_0_0/ASVS-REQ-V12.1.1]` top-1 `ACP-ITS-004` (0.304) — Verify that only the latest recommended versions of the TLS protocol are enabled, such as TLS 1.2 and TLS 1.3. The lates…

### CID7-028

**Size:** 10 items · **Sources:** 4 (4 INDEPENDENT families) · **avg/med top-1:** 0.3686/0.3732

**Independent families:** MITRE_CAPEC, MITRE_ATLAS, MITRE_CWE, NIST_800_53
**AI/ML inflected:** YES

**Top-3 closest Core entities (by top-1 vote count):**

| Rank | Target | Votes |
|---|---|---:|
| 1 | `ACP-SPC-002` | 2 |
| 2 | `ACP-TMR-005` | 1 |
| 3 | `ACO-SLG-005` | 1 |

**Sample items:**

- `[capec_v3_9/CAPEC-116]` top-1 `ACP-TMR-005` (0.333) — Excavation. Excavation. An adversary actively probes the target in a manner that is designed to solicit information that…
- `[capec_v3_9/CAPEC-406]` top-1 `ACP-SPC-002` (0.375) — Dumpster Diving. Dumpster Diving. An adversary cases an establishment and searches through trash bins, dumpsters, or are…
- `[capec_v3_9/CAPEC-545]` top-1 `ACO-SLG-005` (0.373) — Pull Data from System Resources. Pull Data from System Resources. An adversary who is authorized or has the ability to s…

### CID7-043

**Size:** 8 items · **Sources:** 4 (4 INDEPENDENT families) · **avg/med top-1:** 0.3845/0.3872

**Independent families:** NIST_800_53, ASVS, CIS, HIPAA
**AI/ML inflected:** NO

**Top-3 closest Core entities (by top-1 vote count):**

| Rank | Target | Votes |
|---|---|---:|
| 1 | `ACM-RPR-001` | 2 |
| 2 | `ACO-IAT-007` | 1 |
| 3 | `ACO-IAT-006` | 1 |

**Sample items:**

- `[asvs_v5_0_0/ASVS-REQ-V8.4.1]` top-1 `ACO-IAT-007` (0.390) — Verify that multi-tenant applications use cross-tenant controls to ensure consumer operations will never affect tenants …
- `[cis_controls_v8_1_2/CIS-1.2]` top-1 `ACO-IAT-006` (0.402) — Address Unauthorized Assets. Ensure that a process exists to address unauthorized assets on a weekly basis. The enterpri…
- `[hipaa_security_rule/HIPAA-164-310d1]` top-1 `ACM-RPR-001` (0.474) — Device and Media Controls. Device and Media Controls — Physical Safeguard. Implement policies and procedures that govern…

### CID7-038

**Size:** 8 items · **Sources:** 3 (3 INDEPENDENT families) · **avg/med top-1:** 0.2995/0.3123

**Independent families:** NIST_800_53, PCI, MITRE_CWE
**AI/ML inflected:** NO

**Top-3 closest Core entities (by top-1 vote count):**

| Rank | Target | Votes |
|---|---|---:|
| 1 | `ACO-RPR-009` | 2 |
| 2 | `ACO-TSV-002` | 1 |
| 3 | `ACM-IVF-004` | 1 |

**Sample items:**

- `[cwe_software_development_view_v4_19_1/CWE-208]` top-1 `ACO-TSV-002` (0.208) — Observable Timing Discrepancy. Two separate operations in a product require different amounts of time to complete, in a …
- `[nist_sp800_53_rev5/SP800-53-SC-36.2]` top-1 `ACM-IVF-004` (0.347) — Synchronization. Synchronize the following duplicate systems or system components: [duplicate systems or system componen…
- `[nist_sp800_53_rev5/SP800-53-SC-45]` top-1 `ACP-ATB-002` (0.301) — System Time Synchronization. Synchronize system clocks within and between systems and system components.…

### CID7-069

**Size:** 7 items · **Sources:** 3 (3 INDEPENDENT families) · **avg/med top-1:** 0.4191/0.4049

**Independent families:** NIST_800_53, MITRE_CAPEC, CIS
**AI/ML inflected:** NO

**Top-3 closest Core entities (by top-1 vote count):**

| Rank | Target | Votes |
|---|---|---:|
| 1 | `ACM-SPC-003` | 2 |
| 2 | `ACP-IAT-002` | 1 |
| 3 | `ACP-IAT-005` | 1 |

**Sample items:**

- `[capec_v3_9/CAPEC-561]` top-1 `ACP-IAT-002` (0.428) — Windows Admin Shares with Stolen Credentials. Windows Admin Shares with Stolen Credentials. An adversary guesses or obta…
- `[capec_v3_9/CAPEC-645]` top-1 `ACP-IAT-005` (0.428) — Use of Captured Tickets (Pass The Ticket). Use of Captured Tickets (Pass The Ticket). An adversary uses stolen Kerberos …
- `[cis_controls_v8_1_2/CIS-5.6]` top-1 `ACM-SPC-003` (0.405) — Centralize Account Management. Centralize account management through a directory or identity service.…

### CID7-029

**Size:** 6 items · **Sources:** 4 (3 INDEPENDENT families) · **avg/med top-1:** 0.3959/0.3924

**Independent families:** MCP_OFFICIAL, OWASP_MCP, MITRE_ATLAS
**AI/ML inflected:** YES

**Top-3 closest Core entities (by top-1 vote count):**

| Rank | Target | Votes |
|---|---|---:|
| 1 | `ACO-IVF-005` | 3 |
| 2 | `ACP-SPC-004` | 1 |
| 3 | `ACP-IAT-005` | 1 |

**Sample items:**

- `[mcp_official_security_foundations_2025/MCP-AUTH-CLIENT-REGISTRATION]` top-1 `ACP-SPC-004` (0.412) — Client registration and client metadata trust. MCP supports three client registration mechanisms. Choose based on your s…
- `[mcp_official_security_foundations_2025/MCP-AUTH-REDIRECT-CLIENT-METADATA-SECURITY]` top-1 `ACP-IAT-005` (0.492) — Authorization code, redirect and client metadata document security. An attacker who has gained access to an authorizatio…
- `[mcp_official_security_foundations_2025/MCP-LOCAL-SERVER-COMPROMISE]` top-1 `ACO-ITS-001` (0.322) — Local MCP server compromise and sandboxing. Local MCP servers are MCP Servers running on a user’s local machine, either …

### CID7-072

**Size:** 3 items · **Sources:** 3 (3 INDEPENDENT families) · **avg/med top-1:** 0.3523/0.3118

**Independent families:** ASVS, MITRE_CWE, OWASP_DSOMM
**AI/ML inflected:** NO

**Top-3 closest Core entities (by top-1 vote count):**

| Rank | Target | Votes |
|---|---|---:|
| 1 | `ACO-RPR-004` | 1 |
| 2 | `ACO-RPR-009` | 1 |
| 3 | `ACP-RPR-006` | 1 |

**Sample items:**

- `[asvs_v5_0_0/ASVS-REQ-V13.4.1]` top-1 `ACO-RPR-004` (0.312) — Verify that the application is deployed either without any source control metadata, including the .git or .svn folders, …
- `[cwe_software_development_view_v4_19_1/CWE-276]` top-1 `ACO-RPR-009` (0.300) — Incorrect Default Permissions. During installation, installed file permissions are set to allow anyone to modify those f…
- `[owasp_dsomm/DSOMM-ACTIVITY-85D52588F5424225A33820DC22A5508D]` top-1 `ACP-RPR-006` (0.445) — Rolling update on deployment. Rolling update on deployment While a deployment is performed, the application can not be r…

### CID7-050

**Size:** 3 items · **Sources:** 3 (3 INDEPENDENT families) · **avg/med top-1:** 0.3076/0.317

**Independent families:** MITRE_CAPEC, NIST_800_53, OWASP_DSOMM
**AI/ML inflected:** NO

**Top-3 closest Core entities (by top-1 vote count):**

| Rank | Target | Votes |
|---|---|---:|
| 1 | `ACP-TMR-001` | 2 |
| 2 | `ACP-IAT-005` | 1 |

**Sample items:**

- `[capec_v3_9/CAPEC-295]` top-1 `ACP-IAT-005` (0.287) — Timestamp Request. Timestamp Request. This pattern of attack leverages standard requests to learn the exact time associa…
- `[nist_sp800_53_rev5/SP800-53-SI-21]` top-1 `ACP-TMR-001` (0.319) — Information Refresh. Refresh [information] at [frequencies] or generate the information on demand and delete the informa…
- `[owasp_dsomm/DSOMM-ACTIVITY-C922981B65ED40F3A94796FEE9A0125F]` top-1 `ACP-TMR-001` (0.317) — Generation of response statistics. Generation of response statistics No or delayed reaction to findings leads to potenti…

### CID7-049

**Size:** 3 items · **Sources:** 3 (3 INDEPENDENT families) · **avg/med top-1:** 0.3657/0.3662

**Independent families:** MITRE_CWE, NIST_800_53, OWASP_DSOMM
**AI/ML inflected:** NO

**Top-3 closest Core entities (by top-1 vote count):**

| Rank | Target | Votes |
|---|---|---:|
| 1 | `ACM-TMR-003` | 1 |
| 2 | `ACP-TMR-009` | 1 |
| 3 | `ACP-ATB-006` | 1 |

**Sample items:**

- `[cwe_software_development_view_v4_19_1/CWE-439]` top-1 `ACM-TMR-003` (0.363) — Behavioral Change in New Version or Environment. A's behavior or functionality changes with a new version of A, or a new…
- `[nist_sp800_53_rev5/SP800-53-PM-26]` top-1 `ACP-TMR-009` (0.368) — Complaint Management. Implement a process for receiving and responding to complaints, concerns, or questions from indivi…
- `[owasp_dsomm/DSOMM-ACTIVITY-B4193D32394847E2A3263748C48019A1]` top-1 `ACP-ATB-006` (0.366) — Definition of a change management process. Definition of a change management process The impact of a change is not contr…

### CID7-051

**Size:** 3 items · **Sources:** 3 (3 INDEPENDENT families) · **avg/med top-1:** 0.3955/0.3992

**Independent families:** NIST_800_53, OWASP_DSOMM, PCI
**AI/ML inflected:** NO

**Top-3 closest Core entities (by top-1 vote count):**

| Rank | Target | Votes |
|---|---|---:|
| 1 | `ACP-TSV-007` | 1 |
| 2 | `ACO-IAT-006` | 1 |
| 3 | `ACM-TSV-004` | 1 |

**Sample items:**

- `[nist_sp800_53_rev5/SP800-53-PS-3]` top-1 `ACP-TSV-007` (0.368) — Personnel Screening. Screen individuals prior to authorizing access to the system; and Rescreen individuals in accordanc…
- `[owasp_dsomm/DSOMM-ACTIVITY-185D5A7419DC4422BE0744EA35226783]` top-1 `ACO-IAT-006` (0.419) — Office Hours. Office Hours Developers and Operations are not in contact with the security team and therefore do not ask …
- `[pci_dss_v4_0_1/PCI-6.2.2]` top-1 `ACM-TSV-004` (0.399) — Software development personnel working on          6.2.2.a Examine software development procedures. Software development…

## 7. AI/ML-inflected clusters (≥1 iter-3 source)

**14 clusters** include ≥1 item from the 5 iter-3 AI/ML sources. Of these:

- **STRONG (≥3 families):** 9
- **MODERATE (2 families):** 4
- **iter-3-only (no baseline-corpus convergence):** 1

### Top 10 AI/ML-inflected clusters by size:

| Cluster | Size | Families | iter-3 % | Top-1 avg | Top-1 target | Sample concept |
|---|---:|---:|---:|---:|---|---|
| CID7-027 | 102 | 8 | 83% | 0.373 | `ACO-TMR-005` | White Box Reverse Engineering. White Box Reverse Engineering. An attacker discov… |
| CID7-030 | 47 | 3 | 2% | 0.350 | `ACO-IAT-006` | Sniffing Network Traffic. Sniffing Network Traffic. In this attack pattern, the … |
| CID7-022 | 42 | 5 | 2% | 0.358 | `ACM-TMR-005` | Verify that the documentation defines the permitted file types, expected file ex… |
| CID7-026 | 34 | 4 | 94% | 0.380 | `ACO-TMR-002` | Layer I - Cybersecurity foundations for AI-hosting ICT environments. A multilaye… |
| CID7-052 | 23 | 5 | 4% | 0.382 | `ACM-TSV-004` | Train Workforce Members on Causes of Unintentional Data Exposure. Train workforc… |
| CID7-053 | 22 | 4 | 4% | 0.357 | `ACP-TMR-001` | Contingency Plan. Contingency Plan — Administrative Safeguard. Establish (and im… |
| CID7-024 | 14 | 5 | 21% | 0.411 | `ACO-IVF-003` | Verify that data being passed to a potentially dangerous context is sanitized be… |
| CID7-028 | 10 | 4 | 30% | 0.369 | `ACP-SPC-002` | Excavation. Excavation. An adversary actively probes the target in a manner that… |
| CID7-029 | 6 | 3 | 17% | 0.396 | `ACO-IVF-005` | Client registration and client metadata trust. MCP supports three client registr… |
| CID7-012 | 5 | 2 | 60% | 0.348 | `ACO-TMR-004` | Financial Harm. Financial harm involves the loss of wealth, property, or other m… |

## 8. H2 sub-hypothesis — preliminary cluster-level signal

H2: *Inverted-mapping methodology generalises from CWE/CAPEC to MITRE ATLAS without refinement.*

### Per-source LDP top-1 adjacency (H2 evidence)

| Source | LDP count | mean top-1 | median top-1 | direction |
|---|---:|---:|---:|---|
| ATLAS (H2 primary) | 98 | 0.374 | 0.378 | problem-space-inverted |
| CAPEC (precedent) | 204 | 0.355 | 0.360 | problem-space-inverted |
| CWE (precedent) | 247 | 0.321 | 0.335 | problem-space-inverted |
| OWASP ML Top 10 (H2 secondary) | 1 | 0.393 | 0.393 | problem-space-inverted |

Compare with v5 baseline (CWE 0.317, CAPEC ~0.32 — from v5 LDP analysis §2). ATLAS LDP top-1 adjacency BEHAVIOR vs CAPEC precedent informs Stage 7 H2 decision (separate document).

**Cluster-level signal:** ATLAS items contribute to 10 clusters (v7); CAPEC items contribute to 24. ATLAS-CAPEC cluster co-membership: 5 (cross-corpus inverted-mapping convergence).

## 9. Comparison vs v5 LDP baseline

| Metric | v5 (substrate v5, 26 sources) | v7 (substrate v7, 31 sources) | Δ |
|---|---:|---:|---:|
| LDP total | 877 | 988 | +111 |
| LDP fraction | 25.4% | 25.6% | +0.2pp |
| Coarse clusters | 57 | 77 | +20 |
| STRONG candidates | 4 (v5 used ≥5 sources; CID-26/25/55/8) | 27 (Iter-3 uses ≥3 INDEPENDENT families) | n/a (criterion changed) |

**Note on STRONG criterion change.** Substrate v5 LDP analysis used **≥5 sources** (raw count) as STRONG threshold. Iteration 3 pre-registration (per dispatcher §4 Outcome B + `feedback_acr_appsec_core_engineering_only.md`) specifies **≥3 INDEPENDENT source families** (sources within same publisher family count as ONE). Different criterion — direct count comparison is not meaningful.

**v5 STRONG candidates check against v7:**
- **CID-26 (output rendering)** — v6 absorbed via ACR-004 (ACO-IVF-008/ACP-IVF-007/ACM-IVF-005). 30 items collapsed to GROUNDED in substrate v6 measurement. Empirically resolved.
- **CID-25 (regulatory incident reporting), CID-55 (workforce training), CID-8 (AI/MCP)** — v5 baseline assigned no joint-review action; tracked as residual STRONG-but-not-promoted. Iteration 3 substrate v7 LDP cluster analysis reassesses under expanded corpus.

## 10. AI/ML cluster suggested response (per Outcome A/B/C alignment)

Per dispatcher §4 + Cartographer's role (flag-only, never decide):

STRONG clusters identified — Stage 8 joint review weighs Outcome B/C against asymmetric burden:
- **CID7-011** (118 items, 3 families): top-1 avg 0.322; top entity `ACO-IVF-005`
- **CID7-027** (102 items, 8 families; AI/ML inflected): top-1 avg 0.373; top entity `ACO-TMR-005`
- **CID7-033** (57 items, 5 families): top-1 avg 0.353; top entity `ACO-IVF-008`
- **CID7-030** (47 items, 3 families; AI/ML inflected): top-1 avg 0.350; top entity `ACO-IAT-006`
- **CID7-022** (42 items, 5 families; AI/ML inflected): top-1 avg 0.358; top entity `ACM-TMR-005`
- **CID7-064** (37 items, 3 families): top-1 avg 0.351; top entity `ACO-IAT-004`
- **CID7-044** (35 items, 3 families): top-1 avg 0.374; top entity `ACO-TMR-008`
- **CID7-026** (34 items, 4 families; AI/ML inflected): top-1 avg 0.380; top entity `ACO-TMR-002`
- **CID7-009** (26 items, 3 families): top-1 avg 0.301; top entity `ACO-IVF-005`
- **CID7-052** (23 items, 5 families; AI/ML inflected): top-1 avg 0.382; top entity `ACM-TSV-004`
- **CID7-025** (22 items, 4 families): top-1 avg 0.377; top entity `ACO-TMR-004`
- **CID7-053** (22 items, 4 families; AI/ML inflected): top-1 avg 0.357; top entity `ACP-TMR-001`
- **CID7-008** (20 items, 3 families): top-1 avg 0.295; top entity `ACM-IVF-001`
- **CID7-065** (18 items, 4 families): top-1 avg 0.335; top entity `ACO-IAT-001`
- **CID7-067** (16 items, 3 families): top-1 avg 0.344; top entity `ACO-IAT-004`
- **CID7-021** (15 items, 5 families): top-1 avg 0.427; top entity `ACP-TSV-001`
- **CID7-024** (14 items, 5 families; AI/ML inflected): top-1 avg 0.411; top entity `ACO-IVF-003`
- **CID7-063** (14 items, 4 families): top-1 avg 0.382; top entity `ACP-ITS-003`
- **CID7-028** (10 items, 4 families; AI/ML inflected): top-1 avg 0.369; top entity `ACP-SPC-002`
- **CID7-043** (8 items, 4 families): top-1 avg 0.385; top entity `ACM-RPR-001`
- **CID7-038** (8 items, 3 families): top-1 avg 0.299; top entity `ACO-RPR-009`
- **CID7-069** (7 items, 3 families): top-1 avg 0.419; top entity `ACM-SPC-003`
- **CID7-029** (6 items, 3 families; AI/ML inflected): top-1 avg 0.396; top entity `ACO-IVF-005`
- **CID7-072** (3 items, 3 families): top-1 avg 0.352; top entity `ACO-RPR-004`
- **CID7-050** (3 items, 3 families): top-1 avg 0.308; top entity `ACP-TMR-001`
- **CID7-049** (3 items, 3 families): top-1 avg 0.366; top entity `ACM-TMR-003`
- **CID7-051** (3 items, 3 families): top-1 avg 0.396; top entity `ACP-TSV-007`

Cartographer presents; programme-lead + Orchestrator + Archon decide A/B/C.

## 11. Reproducibility

```
# Re-run from worktree branch cartographer-iteration-3-ai-ml-expansion
python3 -m scripts.v5_normalization.grounding.ldp_cluster_analysis_v7
```

Encoder: same SBERT all-MiniLM-L6-v2 @ HF revision c9745ed1 as substrate v6+v7 grounding pipelines (Decision 0003 Amendment 1 §F).
