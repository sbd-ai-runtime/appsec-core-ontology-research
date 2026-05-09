# Pilot Brief — OWASP MCP Secure Server Development v1.0

Status: source_captured
Date: 2026-04-03

## Goal
Use the OWASP guide `A Practical Guide for Secure MCP Server Development` as a second external-source pilot to test whether current AppSec Core normalization can distinguish:
- true manual gaps
- AppSec Core landing-zone gaps
- comparison-method gaps
- source material that is outside the intended AppSec Core scope

## Why this source
This source is close enough to AppSec/AppSec-adjacent engineering to stress the current model, but different enough from the existing manual to expose gaps around MCP-specific architecture, tool governance, delegated identity, isolation, prompt-injection controls, and secure deployment.

## Stable source choice
- Publisher: OWASP Gen AI Security Project
- Title: A Practical Guide for Secure MCP Server Development
- Version: 1.0
- Publication date: 2026-02
- Format: PDF

## Expected pipeline
1. capture stable source + provenance
2. extract source units and source objects
3. normalize to AppSec Core
4. classify outcomes as `manual_gap`, `appsec_core_gap`, `comparison_gap`, or `out_of_scope_for_appsec_core`
5. compare surviving candidates against the published SbD-ToE traceability surface
