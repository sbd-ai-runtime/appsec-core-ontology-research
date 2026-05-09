# Pilot Brief - OWASP MCP Top 10 v0.1 (2025 Beta)

Status: published_traceability_surface_compared
Date: 2026-04-04

## Goal
Use the OWASP MCP Top 10 beta as an AI/MCP-specific stress-test source to identify:
- clean AppSec coverage already present in the manual
- MCP and agentic packaging that pressures the comparison method
- scope-boundary cases between AppSec, local runtime, and broader AI governance

## Why this source
This source is deliberately more risk-packaged than the official MCP specifications and should therefore be read after the MCP normative pilot.
It is useful for testing pressure from:
- token and secret handling
- scope creep and privilege escalation
- tool poisoning and supply chain
- command injection and intent or context subversion
- audit, telemetry and shadow servers
- context injection and over-sharing

## Stable source choice
- Publisher: OWASP Foundation
- Source family: project page snapshot
- Version signal on page: v0.1
- Editorial state on page: beta / pilot-testing phase
- Format: HTML page captured locally for deterministic extraction

## Expected pipeline
1. capture current beta source plus provenance
2. extract section units and curated Top 10 objects
3. normalize to AppSec Core
4. classify outcomes conservatively
5. compare against the published SbD-ToE traceability surface
6. compare against MCP normative and OWASP MCP secure-server pilots

## Current Read
- `0` direct `manual_gap`
- strongest clean support:
  - `MCP04` supply-chain tampering
  - `MCP05` command injection
  - `MCP07` insufficient authentication and authorization
  - `MCP08` audit and telemetry
- strongest residual pressure:
  - `MCP01` token/secret exposure packaging
  - `MCP02` scope-creep privilege packaging
  - `MCP03` tool poisoning and schema-shadowing semantics
  - `MCP06` prompt/context interpreter risks
  - `MCP09` shadow MCP servers
  - `MCP10` context injection and over-sharing
