# CIS Controls Published Manual Traceability Comparison

Status: `published_traceability_surface_control_compared`

## Summary

- items: `8`
- adjudication `comparison_gap_not_manual_gap`: `4`
- adjudication `not_manual_gap`: `3`
- adjudication `transversal_enterprise_control_partially_supported_by_appsec_scope`: `1`

## Decisions

- `CIS-2`: `comparison_gap_not_manual_gap`
  reason: Software inventory and dependency visibility are already present in the manual, but CIS Control 2 bundles authorization and execution-control semantics across enterprise software assets more broadly than the current published AppSec traceability surface.
  evidence:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/05-dependencias-sbom-sca/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/07-cicd-seguro/canon/25-rastreabilidade.md`

- `CIS-4`: `transversal_enterprise_control_partially_supported_by_appsec_scope`
  reason: Secure configuration and baseline integrity clearly have supporting manual semantics across architecture, IaC and secure deployment, but CIS Control 4 also spans enterprise hardening and ongoing IT-admin configuration management beyond the intended AppSec publication scope; this is partial AppSec support, not proven manual absence.
  evidence:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/04-arquitetura-segura/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/08-iac-infraestrutura/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/11-deploy-seguro/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/02-requisitos-seguranca/canon/25-rastreabilidade.md`

- `CIS-5`: `comparison_gap_not_manual_gap`
  reason: Account-management semantics are already present in requirements, secure execution and governance surfaces, but the broad CIS control is not yet emitted as one dedicated published AppSec family.
  evidence:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/02-requisitos-seguranca/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/11-deploy-seguro/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/14-governanca-contratacao/canon/25-rastreabilidade.md`

- `CIS-6`: `not_manual_gap`
  reason: Access-control management is already explicit in the published manual surface through requirements and secure-execution traceability.
  evidence:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/02-requisitos-seguranca/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/11-deploy-seguro/canon/25-rastreabilidade.md`

- `CIS-7`: `comparison_gap_not_manual_gap`
  reason: Continuous vulnerability management is already supported in dependency, testing and operational surfaces, but the CIS control remains broader than the current AppSec publication shape.
  evidence:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/05-dependencias-sbom-sca/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/10-testes-seguranca/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/12-monitorizacao-operacoes/canon/25-rastreabilidade.md`

- `CIS-8`: `not_manual_gap`
  reason: Audit-log management is already explicit in the published monitoring and operations traceability surface.
  evidence:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/12-monitorizacao-operacoes/canon/25-rastreabilidade.md`

- `CIS-16`: `comparison_gap_not_manual_gap`
  reason: Application software security is clearly covered in substance, but CIS Control 16 bundles requirements, coding, testing, pipeline and deploy concerns more broadly than the current published AppSec packaging.
  evidence:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/02-requisitos-seguranca/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/06-desenvolvimento-seguro/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/07-cicd-seguro/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/10-testes-seguranca/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/11-deploy-seguro/canon/25-rastreabilidade.md`

- `CIS-18`: `not_manual_gap`
  reason: Penetration testing and security validation are already explicit in the published testing and monitoring surfaces.
  evidence:
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/10-testes-seguranca/canon/25-rastreabilidade.md`
  - `data/source/SbD-ToE-Manual/manuals_src/docs/sbd-toe/010-sbd-manual/12-monitorizacao-operacoes/canon/25-rastreabilidade.md`
