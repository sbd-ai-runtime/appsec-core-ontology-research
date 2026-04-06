# CAPEC Bottom-Up Comparison Against Published Manual Threat Surface

Date: `2026-04-03`

Status: `published_manual_threat_surface_compared`

## Summary

- reviewed items: `14`
- `comparison_gap_not_manual_gap`: `6`
- `context_only`: `1`
- `likely_appsec_core_gap_not_manual_gap`: `1`
- `not_manual_gap`: `5`
- `out_of_scope_for_appsec_core`: `1`

## Findings

| External Key | Adjudication | Threat Surface Status | Explicit CAPEC Hits | Read |
|---|---|---|---:|---|
| CAPEC-VIEW-683 | context_only | context_only | 0 | The CAPEC supply-chain view is context for the pilot rather than a discrete threat row to compare against the manual. |
| CAPEC-185 | not_manual_gap | published_surface_semantic_support | 0 | Malicious software download already aligns strongly with malicious-repository, origin-control and dependency-source restrictions in the manual. |
| CAPEC-186 | not_manual_gap | published_surface_semantic_support | 0 | Malicious software update is materially covered by controlled promotion, provenance verification and rollback-ready deploy semantics. |
| CAPEC-206 | not_manual_gap | published_surface_semantic_support | 0 | The manual already publishes signed-artifact, provenance and verified-promotion semantics strongly across CI/CD, containers and deploy. Lack of literal CAPEC-206 does not indicate lack of mitigation coverage. |
| CAPEC-443 | comparison_gap_not_manual_gap | published_surface_semantic_support | 0 | The manual already publishes approved-commit, unauthorized-push and unaudited-code execution threats, but the exact insider-authorized-developer framing is not one explicit threat row today. |
| CAPEC-445 | comparison_gap_not_manual_gap | published_surface_semantic_support | 0 | Pipeline tampering, forged builds, unauthenticated versions and unsafe configuration-management effects are already materially covered, but the exact CAPEC-445 wording is broader than one published row. |
| CAPEC-446 | not_manual_gap | published_surface_semantic_support | 0 | Malicious third-party component inclusion is already strongly present through malicious repository, insecure component and transitive dependency threat coverage. |
| CAPEC-511 | comparison_gap_not_manual_gap | published_surface_semantic_support | 0 | The manual already publishes build-environment compromise, runner isolation and CI/CD threat-modeling semantics, but does not currently package them as one development-environment infiltration row. |
| CAPEC-523 | comparison_gap_not_manual_gap | published_surface_semantic_support | 0 | Forged builds, malicious tooling and shadow execution semantics already exist in the manual, but the generic implanted-malware framing still spans multiple published rows. |
| CAPEC-536 | likely_appsec_core_gap_not_manual_gap | published_surface_semantic_support | 0 | The manual already has unsafe-configuration and validation semantics in IaC and deploy, but AppSec Core v0 still lacks a cleaner reusable landing zone for configuration-data integrity as a bottom-up threat abstraction. |
| CAPEC-669 | not_manual_gap | published_surface_semantic_support | 0 | Software-update alteration is already materially covered through signed provenance, verified promotion and controlled deploy semantics. |
| CAPEC-691 | comparison_gap_not_manual_gap | published_surface_semantic_support | 0 | Metadata spoofing is close to malicious repository, dependency confusion and origin-validation semantics already published in the manual, but the exact metadata-deception wording is not one current threat row. |
| CAPEC-692 | comparison_gap_not_manual_gap | published_surface_semantic_support | 0 | The manual already publishes commit-to-build traceability, approved-commit execution and source-control integrity semantics, but not yet as one explicit commit-metadata spoofing row. |
| CAPEC-693 | out_of_scope_for_appsec_core | out_of_scope_for_appsec_core | 0 | StarJacking is primarily software-selection deception via reputation metadata. It should not be forced into the current manual/AppSec Core threat surfaces. |
