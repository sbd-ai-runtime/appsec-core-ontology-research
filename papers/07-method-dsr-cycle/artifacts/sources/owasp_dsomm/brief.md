# Pilot Brief — OWASP DSOMM

Date: `2026-04-05`

Status: `published_traceability_surface_compared`

## Goal

Open the first DevSecOps-maturity pilot that can test whether current
`AppSec Core v0` semantics are sufficient for:

- `OWASP DSOMM` domain content
- chapter-level `achievable-maturity` claims in the current manual

## Source Choice

This pilot starts from the official `OWASP DevSecOps Maturity Model` project
and its public DSOMM content line.

Current public read:

- the official OWASP project page points to `dsomm.owasp.org`
- the public codebase lives in the `devsecopsmaturitymodel` GitHub
  organization
- the frozen source cut is now recorded as:
  - official project page `https://devsecops.owasp.org/`
  - live DSOMM site `https://dsomm.owasp.org/`
  - generated model snapshot `4.2.0`
  - `DevSecOps-MaturityModel-data` commit
    `fda3b250ae9325b8c10f23318c9f0768eaa60b98`

## Why This Pilot

Compared with `SAMM`, `DSOMM` should stress:

- DevSecOps workflow and automation semantics
- implementation levels across build, deploy, operate and govern surfaces
- evidence-oriented maturity assertions
- the boundary between domain semantics and organization-specific rollout

## What This Pilot Needed To Answer

1. Which `DSOMM` activities land cleanly in current `AppSec Core` surfaces?
2. Which `DSOMM` items are actually maturity progression, measurement or
   rollout semantics rather than reusable domain semantics?
3. Do the current chapter `achievable-maturity` claims remain credible when
   compared against explicit `DSOMM` source objects?
4. Does `DSOMM` create repeated pressure for a separate maturity or capability
   layer that should stay outside the current core?

## Current Read

- no direct `manual_gap` is asserted after comparison against the published
  manual traceability surface
- the strongest repeated residual pressure remains
  `Application Hardening`
- that pressure now reads primarily as `AppSec Core` or
  traceability-granularity tension, not as proof that the published manual
  lacks DSOMM-aligned coverage
- most remaining DSOMM friction is better explained by
  `traceability_repair`, `comparison_method_refinement` or `scope boundary`
  than by missing manual publication

## Expected Outputs

- source inventory
- normalized external objects
- manual coverage read
- chapter maturity claim review
- gap analysis summary
- published manual traceability comparison

## Non-Goal

This pilot does not yet decide to change the `AppSec Core` or to publish a
separate maturity overlay.
