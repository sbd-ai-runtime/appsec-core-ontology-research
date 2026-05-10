# AppSec Core SHACL Validation Report

- Status: `conforms`
- Validator: `bounded_subset_validator`
- Scope: `AppSec Core v0 bounded OWL/SHACL workbench`
- Data graph: `/Volumes/G-DRIVE/Shared/SecurityByDesign-TheoryOfEverything/sbd-toe-ontology/formal/appsec_core/02-owl/exports/appsec-core-v0-bounded-v1.ttl`
- Shapes graph: `/Volumes/G-DRIVE/Shared/SecurityByDesign-TheoryOfEverything/sbd-toe-ontology/formal/appsec_core/03-shacl/shapes/appsec-core-v0-shapes.ttl`
- Data triples: 1970
- Shape triples: 298
- Shapes: 6
- Violations: 0

## Notes

- This validator evaluates the SHACL subset emitted by the local workbench.
- Supported constraints: sh:minCount, sh:maxCount, sh:datatype, sh:class, sh:pattern and sh:in.
- It is sufficient for the bounded generated shape set, but it is not a general-purpose SHACL engine.

## Shape Coverage

- `SliceShape` targets 10 node(s), applies 8 constraint(s), violations: 0
- `ControlObjectiveShape` targets 75 node(s), applies 11 constraint(s), violations: 0
- `PracticeShape` targets 69 node(s), applies 6 constraint(s), violations: 0
- `MechanismShape` targets 58 node(s), applies 6 constraint(s), violations: 0
- `ArtifactShape` targets 57 node(s), applies 7 constraint(s), violations: 0
- `EvidencePatternShape` targets 0 node(s), applies 9 constraint(s), violations: 0

## Violations

- none
