# Pilot Brief — SLSA v1.0 Build Track

Date: `2026-04-03`

Status: `captured_pending_normalization`

## Goal

Test the external-source indexing line against a stable, versioned supply-chain source
that should overlap strongly with the current AppSec Core v0 and the published SbD-ToE
traceability surface.

## Source Choice

This pilot uses versioned SLSA v1.0 HTML pages rather than the moving current alias.
The scope is deliberately narrow:

- security levels / build track
- guiding principles relevant to provenance and trust
- producing artifacts
- verifying artifacts

## Why This Pilot

Compared with SSDF and the OWASP MCP guide, SLSA should stress:

- build definition and execution integrity
- artifact attestation and provenance integrity
- verification expectations before promotion
- isolation and hosted build semantics

## Expected Value

This pilot should help distinguish between:

- real manual traceability gaps
- AppSec Core granularity gaps
- comparison-method gaps on provenance / verification language
- source-specific concepts that remain out of scope for the current core
