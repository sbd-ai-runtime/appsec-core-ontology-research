# CAPEC Supply Chain Risks v3.9 Pilot

Date: `2026-04-03`

Status: `source_captured`

## Purpose

Run the first bottom-up external-source pilot using MITRE CAPEC to test a different comparison line from the existing top-down pilots.

This pilot asks:

- which software supply-chain attack patterns are already mitigated by the published SbD-ToE manual threat surfaces;
- which items stress AppSec Core granularity;
- which items are better read as comparison-method gaps rather than as manual absence.

## Why this pilot exists

The top-down pilots (`SSDF`, `OWASP MCP`, `SLSA`) proved useful, but they mainly pressure traceability packaging.

A bottom-up pilot is needed to answer a different question:

- `top-down`: does the manual cover an external framework statement?
- `bottom-up`: which concrete attack patterns does the manual already mitigate, and where?

## Scope

This pilot is intentionally narrow.

Included:
- `CAPEC View 683: Supply Chain Risks`
- a curated set of software-relevant child patterns from that view

Excluded:
- hardware-specific supply-chain content
- acquisition-only content with no clear AppSec/manual landing zone
- live vulnerability feeds

## Comparison Target

This pilot compares against the published manual threat surfaces:

- `canon/50-ameacas-mitigadas`

It does **not** compare against:

- `canon/25-rastreabilidade`
- runtime or V3 verification history
- provenance-layer semantics beyond minimal source capture metadata

## Expected outputs

- source capture receipt
- external source inventory
- source unit inventory
- source object inventory
- AppSec Core normalization
- pre-comparison gap read
- published manual threat-surface comparison
