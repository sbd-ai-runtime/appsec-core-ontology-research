# Pilot Brief — OWASP SAMM

Date: `2026-04-05`

Status: `published_traceability_surface_compared`

## Goal

Open the first maturity-heavy external pilot that can test whether current
`AppSec Core v0` semantics are sufficient for:

- `OWASP SAMM` domain content
- chapter-level `achievable-maturity` claims in the current manual

## Source Choice

This pilot starts from the current `OWASP SAMM` version-2 model line.

Current internal read:

- chapter authoring currently cites `OWASP SAMM v2.1`
- official public project pages still describe the live model primarily as
  `version 2`
- the frozen source cut is now recorded as:
  - website model page `https://owaspsamm.org/model/`
  - version-2 release notes `https://owaspsamm.org/release-notes-v2/`
  - `owaspsamm/core` commit
    `8afa059004fa4abc2b15c714a3a0113548e1881c`

## Why This Pilot

Compared with `SSDF`, `ASVS` and `SLSA`, `SAMM` should stress:

- maturity progression and level semantics
- institutionalization and practice quality
- roadmap-oriented capability shaping
- domain decomposition across governance, design, implementation, verification
  and operations

## What This Pilot Needed To Answer

1. Which `SAMM` objects land cleanly in current `ControlObjective`,
   `Practice`, `Mechanism`, `Artifact` and `EvidencePattern` surfaces?
2. Which `SAMM` pressures are actually maturity or capability semantics rather
   than missing domain semantics?
3. Do the current chapter `achievable-maturity` claims remain credible when
   compared against explicit `SAMM` source objects?
4. Does any repeated residual pressure justify a later maturity or capability
   layer beside the core?

## Current Read

- no direct `manual_gap` is asserted after comparison against the published
  manual traceability surface
- the strongest residual pressure remains localized around
  `Security Requirements` and `Environment Management`
- those two now read primarily as `AppSec Core` or traceability-granularity
  tension, not as proof that the published manual is missing the SAMM surface
- governance, training and operations-heavy SAMM lines are already published in
  the manual, but they behave mainly as overlay or scope-boundary pressure for
  the current `AppSec Core v0`

## Expected Outputs

- source inventory
- normalized external objects
- manual coverage read
- chapter maturity claim review
- gap analysis summary
- published manual traceability comparison

## Non-Goal

This pilot does not yet decide to expand the `AppSec Core` or to introduce a
new maturity model layer.
