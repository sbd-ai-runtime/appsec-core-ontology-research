# Pilot Brief - ENISA Multilayer Framework for Good Cybersecurity Practices for AI

Status: published_traceability_surface_compared
Date: 2026-04-04

## Goal

Use the ENISA `Multilayer Framework for Good Cybersecurity Practices for AI` as a European AI-specific reference to test:
- how much of the AI security pressure remains classical AppSec versus AI-specific extension;
- whether the manual and `AppSec Core` still hold under an EU-oriented AI good-practice framing;
- whether the remaining pressure is mainly on method, on scope boundary, or on the `AppSec Core`.

## Why this source

This is the right next AI source after the MCP/OWASP line because it is:
- official and stable;
- broader than MCP but still cybersecurity-focused;
- structured around cybersecurity practices rather than only threat narratives;
- explicitly lifecycle-aware and supply-chain-aware.

## Stable source choice

- Publisher: ENISA
- Title: `Multilayer Framework for Good Cybersecurity Practices for AI`
- Publication date: `2023-06-07`
- Format captured locally:
  - landing page HTML
  - PDF

## Expected pipeline

1. capture stable source + provenance
2. extract page-level units and curate source objects
3. normalize to `AppSec Core`
4. classify outcomes conservatively
5. compare surviving pressure against the published SbD-ToE traceability surface
6. fold the result back into the AI/MCP/IA comparison-method line

## Current Read

- source capture completed:
  - landing page HTML
  - PDF
- page-unit extraction completed:
  - `46` page units
- curated framework surface completed:
  - `6` source objects
  - `4` comparison targets
  - `2` context/supporting surfaces
- first-pass normalization split into:
  - `4` `comparison_gap`
  - `2` `context_only`
- published-traceability comparison then reviewed the surviving `4` surfaces:
  - `1` `transversal_enterprise_control_partially_supported_by_appsec_scope`
  - `2` `comparison_gap_or_scope_extension`
  - `1` `comparison_gap_not_manual_gap`
  - `0` `manual_gap`

Surface read:
- `ENISA-AI-FAICP-LAYER-I` -> broad classical cybersecurity foundations for AI-hosting ICT; partially supported but broader than AppSec scope
- `ENISA-AI-FAICP-LAYER-II` -> AI-specific packaging pressure; not a direct manual absence signal
- `ENISA-AI-FAICP-LAYER-III` -> sector-specific extension beyond the current AppSec publication surface
- `ENISA-AI-FAICP-CONCLUSIONS` -> semantically supported, but broader than one clean published manual family

Important consequence:
- ENISA behaves more like `scope and framework packaging stress` than `manual gap discovery`
- it reinforces the current project-wide read: the manual remains stronger than broad external AI framework packaging suggests at first glance
