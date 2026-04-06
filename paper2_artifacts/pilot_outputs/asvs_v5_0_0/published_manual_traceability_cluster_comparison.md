# ASVS Published Manual Traceability Cluster Comparison

Status: `published_traceability_surface_cluster_compared`

## Summary

- clusters reviewed: `36`
- items considered: `289`

### Counts by Adjudication

- `comparison_gap_not_manual_gap`: `28`
- `likely_appsec_core_gap_or_traceability_gap`: `2`
- `not_manual_gap`: `6`

## Items

### anti_automation_projection_gap

- adjudication: `comparison_gap_not_manual_gap`
- traceability surface status: `published_surface_semantic_support`
- item count: `2`
- section ids: `V2.4`
- reason: Anti-automation controls may exceed the current packaging style, but this is still comparison pressure rather than evidence of manual absence.
- evidence files:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/02-requisitos-seguranca/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/11-deploy-seguro/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/12-monitorizacao-operacoes/canon/25-rastreabilidade.md`

### api_protocol_specific_projection_gap

- adjudication: `comparison_gap_not_manual_gap`
- traceability surface status: `published_surface_semantic_support`
- item count: `6`
- section ids: `V4.3, V4.4`
- reason: Protocol-specific API families such as GraphQL and WebSocket remain more granular than the current published manual packaging, but not proven absent.
- evidence files:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/04-arquitetura-segura/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/11-deploy-seguro/canon/25-rastreabilidade.md`

### architecture_and_dependency_hardening_projection_gap

- adjudication: `comparison_gap_not_manual_gap`
- traceability surface status: `published_surface_semantic_support`
- item count: `5`
- section ids: `V15.2`
- reason: Architecture hardening and dependency discipline are already supported, but the current top-down publication is broader than the ASVS section wording.
- evidence files:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/04-arquitetura-segura/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/05-dependencias-sbom-sca/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/06-desenvolvimento-seguro/canon/25-rastreabilidade.md`

### authentication_lifecycle_and_recovery

- adjudication: `comparison_gap_not_manual_gap`
- traceability surface status: `published_surface_semantic_support`
- item count: `6`
- section ids: `V6.4`
- reason: Lifecycle and recovery semantics for authentication exist in the manual, but the published rows remain broader than the ASVS family articulation.
- evidence files:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/11-deploy-seguro/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/13-formacao-onboarding/canon/25-rastreabilidade.md`

### authentication_strength_and_assurance

- adjudication: `comparison_gap_not_manual_gap`
- traceability surface status: `published_surface_semantic_support`
- item count: `37`
- section ids: `V6.1, V6.2, V6.3, V6.5, V6.6, V6.7`
- reason: Authentication strength and assurance are supported by the published manual, but not yet packaged as one dedicated ASVS-style family for direct comparison.
- evidence files:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/02-requisitos-seguranca/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/11-deploy-seguro/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/13-formacao-onboarding/canon/25-rastreabilidade.md`

### authorization_and_least_privilege

- adjudication: `comparison_gap_not_manual_gap`
- traceability surface status: `published_surface_semantic_support`
- item count: `13`
- section ids: `V8.1, V8.2, V8.3, V8.4`
- reason: Authorization and least-privilege semantics are present, but not yet packaged as one dedicated published family for ASVS comparison.
- evidence files:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/04-arquitetura-segura/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/11-deploy-seguro/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/14-governanca-contratacao/canon/25-rastreabilidade.md`

### backend_component_authentication

- adjudication: `comparison_gap_not_manual_gap`
- traceability surface status: `published_surface_semantic_support`
- item count: `4`
- section ids: `V13.2`
- reason: Backend-component authentication is supported by architecture, infrastructure and deployment semantics, but not exposed as a dedicated published family.
- evidence files:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/04-arquitetura-segura/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/08-iac-infraestrutura/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/11-deploy-seguro/canon/25-rastreabilidade.md`

### backend_least_privilege

- adjudication: `comparison_gap_not_manual_gap`
- traceability surface status: `published_surface_semantic_support`
- item count: `1`
- section ids: `V13.2`
- reason: Backend least-privilege semantics are present, but the current published surface is broader than the ASVS requirement phrasing.
- evidence files:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/04-arquitetura-segura/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/11-deploy-seguro/canon/25-rastreabilidade.md`

### business_logic_security_projection_gap

- adjudication: `comparison_gap_not_manual_gap`
- traceability surface status: `published_surface_semantic_support`
- item count: `5`
- section ids: `V2.3`
- reason: Business-logic security is adjacent to requirements, architecture and threat-modeling semantics, but is not yet packaged as one direct published ASVS family.
- evidence files:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/02-requisitos-seguranca/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/03-threat-modeling/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/04-arquitetura-segura/canon/25-rastreabilidade.md`

### controlled_failure_and_non_revealing_errors

- adjudication: `comparison_gap_not_manual_gap`
- traceability surface status: `published_surface_semantic_support`
- item count: `1`
- section ids: `V16.5`
- reason: Controlled failure behavior is supported by secure-development and validation semantics, but not yet emitted as one direct ASVS family.
- evidence files:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/06-desenvolvimento-seguro/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/10-testes-seguranca/canon/25-rastreabilidade.md`

### encoding_architecture_projection_gap

- adjudication: `comparison_gap_not_manual_gap`
- traceability surface status: `published_surface_semantic_support`
- item count: `2`
- section ids: `V1.1`
- reason: Encoding and sanitization architecture is semantically supported through requirements, threat-modeling and secure-development links, but not yet published as one direct ASVS family.
- evidence files:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/02-requisitos-seguranca/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/03-threat-modeling/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/06-desenvolvimento-seguro/canon/25-rastreabilidade.md`

### error_handling_and_sensitive_logging_hygiene

- adjudication: `comparison_gap_not_manual_gap`
- traceability surface status: `published_surface_semantic_support`
- item count: `3`
- section ids: `V16.5`
- reason: Error handling and sensitive-logging hygiene are already adjacent to secure-development, testing and monitoring semantics, but not yet a dedicated published family.
- evidence files:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/06-desenvolvimento-seguro/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/10-testes-seguranca/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/12-monitorizacao-operacoes/canon/25-rastreabilidade.md`

### file_download_and_content_serving_projection_gap

- adjudication: `comparison_gap_not_manual_gap`
- traceability surface status: `published_surface_semantic_support`
- item count: `3`
- section ids: `V5.4`
- reason: File download and content-serving controls are adjacent to published validation and secure-development surfaces, but not yet emitted as a dedicated ASVS family.
- evidence files:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/06-desenvolvimento-seguro/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/10-testes-seguranca/canon/25-rastreabilidade.md`

### file_handling_documentation_projection_gap

- adjudication: `comparison_gap_not_manual_gap`
- traceability surface status: `published_surface_semantic_support`
- item count: `1`
- section ids: `V5.1`
- reason: File-handling documentation is adjacent to secure-development and validation surfaces, but not yet expressed as one clean published family.
- evidence files:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/06-desenvolvimento-seguro/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/10-testes-seguranca/canon/25-rastreabilidade.md`

### frontend_browser_security_projection_gap

- adjudication: `comparison_gap_not_manual_gap`
- traceability surface status: `published_surface_semantic_support`
- item count: `31`
- section ids: `V3.1, V3.2, V3.3, V3.4, V3.5, V3.6, V3.7`
- reason: Frontend and browser-security semantics put pressure on scope and packaging, but the current state is still best read as comparison pressure rather than proven manual absence.
- evidence files:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/02-requisitos-seguranca/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/04-arquitetura-segura/canon/25-rastreabilidade.md`

### identity_provider_and_federated_authentication

- adjudication: `comparison_gap_not_manual_gap`
- traceability surface status: `published_surface_semantic_support`
- item count: `4`
- section ids: `V6.8`
- reason: Federated authentication and identity-provider trust are semantically supported, but not yet emitted as a clean published comparison family.
- evidence files:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/04-arquitetura-segura/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/11-deploy-seguro/canon/25-rastreabilidade.md`

### injection_and_sanitization_discipline

- adjudication: `not_manual_gap`
- traceability surface status: `published_traceability_explicit`
- item count: `22`
- section ids: `V1.2, V1.3`
- reason: Injection prevention and sanitization are already explicit published manual semantics across requirements, secure development and testing surfaces.
- evidence files:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/02-requisitos-seguranca/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/06-desenvolvimento-seguro/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/10-testes-seguranca/canon/25-rastreabilidade.md`

### input_contract_validation

- adjudication: `not_manual_gap`
- traceability surface status: `published_traceability_explicit`
- item count: `8`
- section ids: `V2.2, V4.2`
- reason: Structured input and message-contract validation already has explicit published support in requirements and secure-development surfaces.
- evidence files:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/02-requisitos-seguranca/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/06-desenvolvimento-seguro/canon/25-rastreabilidade.md`

### integration_contract_assurance

- adjudication: `comparison_gap_not_manual_gap`
- traceability surface status: `published_surface_semantic_support`
- item count: `5`
- section ids: `V4.1`
- reason: Generic web-service assurance is already present in requirements and architecture semantics, but not emitted as one dedicated ASVS section family.
- evidence files:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/02-requisitos-seguranca/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/04-arquitetura-segura/canon/25-rastreabilidade.md`

### log_integrity_and_protection

- adjudication: `not_manual_gap`
- traceability surface status: `published_traceability_explicit`
- item count: `3`
- section ids: `V16.4`
- reason: Log protection and auditability are already explicit published manual semantics.
- evidence files:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/12-monitorizacao-operacoes/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/07-cicd-seguro/canon/25-rastreabilidade.md`

### logging_documentation_projection_gap

- adjudication: `comparison_gap_not_manual_gap`
- traceability surface status: `published_surface_semantic_support`
- item count: `1`
- section ids: `V16.1`
- reason: Logging strategy and documentation are already implied by the published monitoring surface, but not yet separated as one direct family.
- evidence files:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/12-monitorizacao-operacoes/canon/25-rastreabilidade.md`

### oauth_and_oidc_service_trust

- adjudication: `comparison_gap_not_manual_gap`
- traceability surface status: `published_surface_semantic_support`
- item count: `36`
- section ids: `V10.1, V10.2, V10.3, V10.4, V10.5, V10.6, V10.7`
- reason: OAuth and OIDC trust semantics are present via architecture and secure execution surfaces, but not yet published as one dedicated ASVS family.
- evidence files:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/04-arquitetura-segura/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/11-deploy-seguro/canon/25-rastreabilidade.md`

### protected_secret_storage

- adjudication: `comparison_gap_not_manual_gap`
- traceability surface status: `published_surface_semantic_support`
- item count: `2`
- section ids: `V13.3`
- reason: Secret handling is already present in infrastructure and governance surfaces, but not as one dedicated ASVS comparison family.
- evidence files:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/08-iac-infraestrutura/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/14-governanca-contratacao/canon/25-rastreabilidade.md`

### secret_leak_prevention

- adjudication: `comparison_gap_not_manual_gap`
- traceability surface status: `published_surface_semantic_support`
- item count: `1`
- section ids: `V13.3`
- reason: Secret leakage prevention is semantically supported, but the published rows remain broader than the ASVS statement shape.
- evidence files:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/08-iac-infraestrutura/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/14-governanca-contratacao/canon/25-rastreabilidade.md`

### secret_usage_isolation

- adjudication: `comparison_gap_not_manual_gap`
- traceability surface status: `published_surface_semantic_support`
- item count: `1`
- section ids: `V13.3`
- reason: Secret usage isolation is semantically present, but the current top-down publication does not isolate it as one clean ASVS family.
- evidence files:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/08-iac-infraestrutura/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/14-governanca-contratacao/canon/25-rastreabilidade.md`

### secure_coding_and_architecture_documentation_projection_gap

- adjudication: `comparison_gap_not_manual_gap`
- traceability surface status: `published_surface_semantic_support`
- item count: `5`
- section ids: `V15.1`
- reason: Secure coding and architecture documentation are present in the manual, but not yet emitted as one clean published ASVS-oriented family.
- evidence files:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/04-arquitetura-segura/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/06-desenvolvimento-seguro/canon/25-rastreabilidade.md`

### secure_coding_discipline_gap

- adjudication: `likely_appsec_core_gap_or_traceability_gap`
- traceability surface status: `published_traceability_no_explicit_hit_but_manual_semantics_present`
- item count: `7`
- section ids: `V15.3`
- reason: Generic defensive coding discipline is clearly present in the manual, but it is not yet exposed as one reusable published family or clean core landing zone; treat it as AppSec Core or packaging pressure, not manual absence.
- evidence files:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/02-requisitos-seguranca/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/06-desenvolvimento-seguro/canon/25-rastreabilidade.md`

### secure_configuration_baseline_gap

- adjudication: `likely_appsec_core_gap_or_traceability_gap`
- traceability surface status: `published_traceability_no_explicit_hit_but_manual_semantics_present`
- item count: `12`
- section ids: `V13.1, V13.2, V13.4`
- reason: Secure configuration, unintended information leakage by configuration, and baseline integrity have supporting manual semantics, but no clean dedicated published family yet; this remains pressure on AppSec Core or traceability packaging, not proven manual absence.
- evidence files:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/02-requisitos-seguranca/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/08-iac-infraestrutura/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/09-containers-imagens/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/11-deploy-seguro/canon/25-rastreabilidade.md`

### secure_transport

- adjudication: `comparison_gap_not_manual_gap`
- traceability surface status: `published_surface_semantic_support`
- item count: `7`
- section ids: `V12.1, V12.2`
- reason: Secure transport semantics are adjacent to architecture, deploy and integration-trust controls, but not emitted as one ASVS-specific published family.
- evidence files:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/04-arquitetura-segura/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/11-deploy-seguro/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/08-iac-infraestrutura/canon/25-rastreabilidade.md`

### security_event_logging_coverage

- adjudication: `not_manual_gap`
- traceability surface status: `published_traceability_explicit`
- item count: `4`
- section ids: `V16.3`
- reason: Security-event logging is already an explicit published surface in the monitoring chapter.
- evidence files:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/12-monitorizacao-operacoes/canon/25-rastreabilidade.md`

### self_contained_token_trust

- adjudication: `comparison_gap_not_manual_gap`
- traceability surface status: `published_surface_semantic_support`
- item count: `7`
- section ids: `V9.1, V9.2`
- reason: Token integrity and token-content trust are semantically supported, but the current published surface is broader than the ASVS token family.
- evidence files:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/04-arquitetura-segura/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/11-deploy-seguro/canon/25-rastreabilidade.md`

### service_to_service_auth_and_transport

- adjudication: `comparison_gap_not_manual_gap`
- traceability surface status: `published_surface_semantic_support`
- item count: `5`
- section ids: `V12.3`
- reason: Service-to-service trust is already semantically present, but the published traceability rows do not yet expose it as a clean ASVS-specific family.
- evidence files:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/04-arquitetura-segura/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/08-iac-infraestrutura/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/11-deploy-seguro/canon/25-rastreabilidade.md`

### session_and_token_trust

- adjudication: `comparison_gap_not_manual_gap`
- traceability surface status: `published_surface_semantic_support`
- item count: `19`
- section ids: `V7.1, V7.2, V7.3, V7.4, V7.5, V7.6`
- reason: Session-management semantics are already present, but the published manual surface does not expose them as one dedicated ASVS-style family.
- evidence files:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/04-arquitetura-segura/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/11-deploy-seguro/canon/25-rastreabilidade.md`

### structured_logging_shape

- adjudication: `not_manual_gap`
- traceability surface status: `published_traceability_explicit`
- item count: `5`
- section ids: `V16.2`
- reason: General logging structure is already an explicit published surface in monitoring and operational telemetry.
- evidence files:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/12-monitorizacao-operacoes/canon/25-rastreabilidade.md`

### validation_before_internal_use

- adjudication: `not_manual_gap`
- traceability surface status: `published_traceability_explicit`
- item count: `12`
- section ids: `V1.5, V5.2, V5.3`
- reason: Validation before deserialization, upload handling and internal file use is already explicit in published validation and secure-development surfaces.
- evidence files:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/02-requisitos-seguranca/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/06-desenvolvimento-seguro/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/10-testes-seguranca/canon/25-rastreabilidade.md`

### validation_documentation_projection_gap

- adjudication: `comparison_gap_not_manual_gap`
- traceability surface status: `published_surface_semantic_support`
- item count: `3`
- section ids: `V2.1`
- reason: Validation documentation and validation strategy are already supported, but the published manual surface does not emit them as one ASVS-specific family.
- evidence files:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/02-requisitos-seguranca/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/10-testes-seguranca/canon/25-rastreabilidade.md`

