# Pilot Brief — MCP Official Security Foundations 2025

Status: published_traceability_surface_compared
Date: 2026-04-04

## Goal
Use official MCP security documentation as a normative pilot to test whether the current AppSec Core and comparison method can distinguish:
- clean AppSec coverage already present in the manual
- MCP-specific comparison/packaging gaps
- AppSec Core landing-zone pressure
- legitimate scope boundaries between AppSec and broader agent/runtime governance

## Why this source
This source is more normative than the existing OWASP MCP guide and gives a stronger baseline for:
- authorization flows
- token handling and least privilege
- confused deputy and token passthrough risks
- transport and callback security
- audit and monitoring expectations
- server/tool security best practices

## Stable source choice
- Publisher: Model Context Protocol
- Source family: official specification/docs site
- Documents:
  - Authorization (`2025-11-25`)
  - Security Best Practices (`2025-06-18`)
- Format: HTML pages captured locally for deterministic extraction

## Expected pipeline
1. capture stable source + provenance
2. extract source units and source objects
3. normalize to AppSec Core
4. classify outcomes conservatively
5. compare surviving candidates against the published SbD-ToE traceability surface
6. compare the normative MCP read against the existing OWASP MCP pilot
