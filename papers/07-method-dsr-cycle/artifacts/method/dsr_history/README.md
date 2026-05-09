# DSR History — P2-v2 iteration log

**Purpose:** chronological record of Design Science Research (DSR) iterations conducted during P2-v2 preparation. Each round compares the current external-source corpus (27 pilots, V1-normalized) against the then-current state of `sbd-toe-manual` and `sbd-toe-knowledge-graph`, produces a gap roll-up, and records a programme-lead decision (Author / Accept / Stop).

**Relationship to other docs:**
- Method and scope: `../../EXECUTION-PLAN-P2v2.md`.
- Preservation and tag governance: `../../PROGRAMME-PRESERVATION-PROTOCOL.md` + `../../FREEZE-REGISTRY.md`.
- v2.0 release surface: `sbd-toe-ontology/MANIFEST-v2.0-DRAFT.md` (staging) → `appsec-core-ontology-research/MANIFEST-v2.0.md` on promotion.

## File naming convention

`round-<N>-<YYYY-MM-DD>.md` — one file per round, named by round index and round-start date.

`TEMPLATE.md` — skeleton for new rounds. Copy and fill.

## Round index

| Round | Start date | Status | Decision | File |
|---|---|---|---|---|
| 1 | (pending scheduling) | — | — | `round-1-<YYYY-MM-DD>.md` (to be created at Round 1 start) |

## Input tagging conventions

At the start of each round, create (with programme-lead authorisation) reference tags on the input repositories:

- `p2v2-manual-input-round-<N>-<YYYY-MM-DD>` in `sbd-toe-manual` at `main`.
- `p2v2-kg-input-round-<N>-<YYYY-MM-DD>` in `sbd-toe-knowledge-graph` at `main`.
- `p2v2-corpus-input-round-<N>-<YYYY-MM-DD>` in this repo at the commit consumed by the pipeline.

These are reference tags (non-semver, non-publish). Record all three in the round's history file under "Inputs".

## Output tagging

At the end of each round (when outputs are complete), propose (with programme-lead authorisation) an output tag in this repo:

- `p2v2-gap-analysis-round-<N>-frozen` on the commit that contains the round's `data/<pilot>/stubs/manual_gap_analysis.json` (27 files), `data/<pilot>/stubs/traceability_publication_candidates.json` (27 files), and `data/cross_pilot/gap_rollup_round_<N>.json`.

Record in FREEZE-REGISTRY.md under "Frozen states" (not "Published states" — these are iteration milestones, not paper references).

## Decision conventions

At the close of each round, the programme lead selects one of:

- **Author** — commission authoring changes in `sbd-toe-manual`. The DSR-HISTORY entry links to the resulting authoring PR(s). Round N+1 will re-compare against the post-authoring manual.
- **Accept** — current gap set is acceptable as-is. The round freezes and the next round (N+1) consumes a refreshed input snapshot to verify stability.
- **Stop** — no further iteration needed. Triggers the P2-v2 bundle preparation and archive events in the execution plan.

Each decision includes a short rationale and the programme lead's signature line (name + date).
