# Pilot Brief - OWASP Third-Party MCP Servers Guide v1.0

Status: published_traceability_surface_compared
Date: 2026-04-04

## Goal
Use the OWASP guide for securely using third-party MCP servers as a practical AI/MCP pilot to test:
- client-side trust minimization
- third-party server discovery and verification
- sandboxing and containment expectations
- approval and registry workflows
- how much of this pressure is AppSec-shaped vs runtime/governance boundary

## Why this source
This guide is the best next MCP source after the official MCP docs and the MCP Top 10 because it is:
- practical rather than purely normative
- narrower than enterprise-wide control frameworks
- focused on using untrusted third-party MCP servers rather than building MCP servers
- likely to expose where the manual supports the substance but not the third-party/MCP packaging

## Stable source choice
- Publisher: OWASP GenAI Security Project
- Title: `A Practical Guide for Securely Using Third-Party MCP Servers`
- Version: `1.0`
- Publication date: `2025-11-04`
- Formats captured locally:
  - landing page HTML
  - PDF

## Expected pipeline
1. capture stable source + provenance
2. extract page-level units and then curate source objects
3. normalize to AppSec Core
4. classify outcomes conservatively
5. compare surviving candidates against the published SbD-ToE traceability surface
6. compare against the MCP normative, MCP Top 10 and MCP secure-server pilots

## Current Read

- `9` curated source objects were extracted:
  - `4` risk surfaces
  - `2` control surfaces
  - `1` governance surface
  - `1` supporting surface
  - `1` context surface
- first-pass normalization split into:
  - `6` `comparison_gap`
  - `1` `mapped`
  - `2` `context_only`
- conservative published-traceability comparison then reviewed the surviving `7` items:
  - `3` `comparison_gap_not_manual_gap`
  - `4` `comparison_gap_or_scope_extension`
  - `0` `manual_gap`
- strongest residual pressure now sits in:
  - tool poisoning and tool-manifest trust
  - prompt injection and memory poisoning
  - tool interference across multiple third-party servers
  - consumer-side discovery, verification and containment
  - trusted registry and approval workflow packaging

Important consequence:
- this source behaves as another AI/MCP method stress pilot, not as evidence of direct manual absence
- it strengthens the consumer-side and agentic-risk branches of the comparison-method backlog
