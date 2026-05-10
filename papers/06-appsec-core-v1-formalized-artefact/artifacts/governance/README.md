# sbd-toe-ontology

This repository is the canonical ontology home for the SbD-ToE program.

It exists to keep the semantic model of the program separate from:

- editorial manual authoring
- semantic compilation and indexing
- downstream consultation or intervention products

## Scope

This repository is intended to own:

- the SbD-ToE ontology
- the AppSec Core ontology
- semantic mappings and alignment artifacts
- ontology governance material
- the formalization track for `OWL` and `SHACL`

It should not own:

- the manual as editorial source
- the knowledge graph compilation pipeline
- downstream MCP behavior
- temporary working notes from execution repos

## Structure

- [docs/ontology-role.md](docs/ontology-role.md)
  - repo role and boundaries
- [docs/artifact-scope.md](docs/artifact-scope.md)
  - what artifacts belong here
- [docs/formalization-roadmap.md](docs/formalization-roadmap.md)
  - path toward `OWL` and `SHACL`
- [docs/ontology-reconstruction-workflow.md](docs/ontology-reconstruction-workflow.md)
  - reconstruction and refresh runbook for `SbD-ToE` and `AppSec Core`
- [docs/governance.md](docs/governance.md)
  - ontology governance rules
- [docs/handover/README.md](docs/handover/README.md)
  - dated repo-state and publication-surface handovers
- [docs/decisions/README.md](docs/decisions/README.md)
  - ontology-level ADR discipline
- [ontology/README.md](ontology/README.md)
  - canonical ontology artifact area
- [packages/README.md](packages/README.md)
  - versioned ontology packages separated by ontology family
- [mappings/README.md](mappings/README.md)
  - mappings and alignment area
- [formal/README.md](formal/README.md)
  - formal semantic artifacts area

## Current Baseline

The initial ontology baseline has already been imported from the former ontology workspace inside `SbD-ToE/sbd-toe-knowledge-graph`.

This means the repository now contains:

- the current SbD-ToE ontology baseline
- the current AppSec Core ontology baseline
- the modular AppSec Core draft set
- supporting ontology working notes needed to understand the present v0 review surface
- the first migrated package of ontology-owned code and tests

The next step is not to invent a new ontology here from scratch.

The next step is to progressively make this repository the canonical home for those artifacts and the code that governs them.

## Current Code Baseline

The repository now also contains a first self-contained Python package under `src/sbdtoe_indexing/`.

This first migration wave includes:

- ontology engine code
- canonical control-building logic
- ontology discovery and fit evaluation workflows
- ontology publication and requirement-to-control linking workflows
- ontology-owned tests that do not require the full manual-compilation pipeline

It does not yet include the full manual-analysis pipeline from the former knowledge-graph workspace.

## Relation to Other Repositories

- `SbD-ToE/sbd-toe-manual`
  - editorial source of truth
- `SbD-ToE/sbd-toe-knowledge-graph`
  - semantic compiler and publisher
- `SbD-ToE/external-sources-inventory`
  - external evidence and validation layer
- `SbD-ToE/sbd-toe-mcp-poc`
  - OSS consultative consumer

## Operating Rule

If the question is about semantic truth, ontology shape, ontology governance, or formal semantic representation, it belongs here.

If the question is about compiling the manual into published artifacts, it belongs in the knowledge graph.
