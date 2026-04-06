# CIS Controls Pilot Brief

## Pilot

- corpus: `CIS Critical Security Controls v8.1`
- publication: `CIS Critical Security Controls`
- publisher: `Center for Internet Security`

## Goal

Prove that a broad control-oriented external corpus can be:

1. captured as a stable published source artifact
2. extracted into deterministic control-level source objects
3. normalized conservatively into `AppSec Core`
4. used to test where the comparison line starts to pick up enterprise-wide noise instead of AppSec-specific signal

## Why CIS Controls Now

- official public version and controls-list pages exist and are stable enough for deterministic capture
- the corpus is broad and should stress the scope boundary of the current `AppSec Core`
- it is a better next step after `ASVS` because it tests transversal packaging without dropping immediately into safeguard-level detail

## Granularity Decision

This pilot is intentionally `Control`-level, not `Safeguard`-level.

That keeps the first pass comparable with the published manual traceability surfaces and avoids mixing AppSec semantics too early with full-enterprise implementation detail.

## Expected Outputs

- source inventory
- source unit inventory
- source object inventory
- normalized external objects
- first-pass read on scope pressure versus AppSec signal

## Non-Goal

This pilot does not yet claim safeguard-level traceability and does not update the manual automatically.
