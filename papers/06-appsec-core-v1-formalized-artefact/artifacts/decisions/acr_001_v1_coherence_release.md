# AppSec Core v1.0 Release — Coherence Rename

Date: `2026-04-15`
Status: `active_handover`
Scope: `Rename v1-draft to v1.0, update namespace and metadata for coherence`

## What happened

After executing the 3-prompt sequence (4 mechs + ACR-002 revised + OWL
relations), the ontology was promoted to **v1.0**. All version
metadata was aligned for coherence.

## Coherence changes

### Namespace & Ontology ID

- Namespace URI: `https://securitybydesign.dev/ontology/appsec-core/v0#` → `v1#`
- Ontology ID: `ac:AppSecCoreV0` → `ac:AppSecCoreV1`
- SHACL shape set: `AppSecCoreV0ShapeSet` → `AppSecCoreV1ShapeSet`

### Version strings

- `rdfs:label` — "AppSec Core v1.0 bounded ontology cut"
- `rdfs:comment` — reflects v1.0 entity counts (74/68/57/57)
- `owl:versionInfo` — `"1.0"`
- YAML `meta.version` — `'0.1'` → `'1.0'` in:
  - `ontology/appsec-core-v0-surface-contract.yaml`
  - `ontology/appsec-core-v0-consolidated.yaml`
  - `ontology/appsec-core-v0-draft.yaml`
  - `ontology/appsec-core-v0-instance-index.yaml`
  - `ontology/appsec-core-slice-registry-v0-draft.yaml`

### Folder renames

- `ontology/v1-draft/` → `ontology/v1.0/`
- `packages/ontology/appsec-core/v1-draft/` → `packages/ontology/appsec-core/v1.0/`

### Export formats regenerated

- `formal/appsec_core/02-owl/exports/alt-formats/`:
  - `appsec-core-v1.0.owl` (RDF/XML)
  - `appsec-core-v1.0.jsonld`
  - `appsec-core-v1.0.nt`
- (`appsec-core-v1-draft.*` versions removed)

## What was kept as v0 (intentional)

### Filenames with `-v0-*`

Files like `appsec-core-v0-draft.yaml`, `appsec-core-v0-consolidated.yaml`,
etc. keep their `-v0-*` naming. The `v0` here is a historical artifact
of file naming, not a statement about content. Renaming all filenames
would create a massive churn across the repo; the content inside is
unambiguously v1.0. Filename sweep deferred to a separate PR if desired.

### Frozen snapshots

- `ontology/v0/` — v0 frozen baseline (tag `v0-frozen`)
- `packages/ontology/appsec-core/v0/` — v0 publication snapshot
- `packages/ontology/appsec-core/v0.1/` — v0.1 publication snapshot

These remain untouched. They represent historical releases.

## Validation

- OWL regenerated with new namespace (1808 triples)
- SHACL conforms (0 violations)
- 18 tests passing

## Files changed

- `formal/appsec_core/python/src/appsec_core_formalization/build_owl.py` — namespace, IDs, labels
- `formal/appsec_core/python/src/appsec_core_formalization/build_shacl.py` — namespace, shape set name
- `ontology/appsec-core-v0-*.yaml` — version bumps to `'1.0'`
- `ontology/v1.0/CHANGELOG.md` — renamed folder + header updated
- `packages/ontology/appsec-core/v1.0/` — renamed folder + README rewritten
- `docs/handover/README.md` — v1-draft references updated to v1.0
- `formal/appsec_core/02-owl/exports/*` — regenerated
- `formal/appsec_core/03-shacl/shapes/*` — regenerated
- `formal/appsec_core/05-validation/reports/*` — regenerated
- `formal/appsec_core/02-owl/exports/alt-formats/` — regenerated with v1.0 naming

## Next steps

1. Tag `v1.0` after this commit
2. ExternalSourcesInventory re-run
3. SSDF/SAMM/PCI mapping corrections
4. P1-v2 manuscript
