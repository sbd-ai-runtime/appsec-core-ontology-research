# Manifest v1.0

This manifest defines the recommended content selection for the first curated public release.

Publication rule for this manifest:

- `v1.0.0` contains only artifacts that support claims made in the current `V1` papers
- later `V2` waves belong to later full releases, not to incremental additions inside `v1.0.0`

## 1. Repository Topology Decision

For the current state of the program, the recommended public topology is:

- **one curated public repository now**

Do not create, for `v1.0.0`:

- one public repository per paper
- one public repository per pilot family
- one public repository mirroring `sbd-toe-knowledge-graph`
- one public repository mirroring `ExternalSourcesInventory`

A second public repository may be justified later only for intentionally maintained public tooling or software. It is not needed for the current `V1` publication surface.

## 2. Final Public Repository Structure

```text
appsec-core-research/
  README.md
  LICENSE
  CITATION.cff
  CHANGELOG.md
  RELEASE-NOTES-v1.0.md
  MANIFEST-v1.0.md
  docs/
    RELEASE-TO-ZENODO.md
  papers/
    README.md
    appsec-core-normalized-ontology/
      source/
        manuscript.md
      pdf/
        appsec_core_normalized_ontology.pdf
      arxiv/
        main.tex
        appsec_core_normalized_ontology-arxiv.tar.gz
      artifacts/
        ontology/
        schema/
        slice_contracts/
        normalized_examples/
    coverage-preserving-knowledge-compilation/
      source/
        manuscript.md
      pdf/
        coverage_preserving_knowledge_compilation.pdf
      arxiv/
        main.tex
        coverage_preserving_knowledge_compilation-arxiv.tar.gz
      artifacts/
        pilot_manifests/
        pilot_outputs/
        cross_pilot/
        method_notes/
    ontology-grounded-retrieval/
      source/
        manuscript.md
      pdf/
        ontology_grounded_retrieval.pdf
      arxiv/
        main.tex
        ontology_grounded_retrieval-arxiv.tar.gz
      artifacts/
        retrieval_contract/
        runtime_snapshot/
        worked_examples/
        verification_examples/
    04-empirical-evaluation/
      source/
        DESIGN-empirical-evaluation-v1.md
      DESIGN-empirical-evaluation-v1.pdf
      header.tex
      README.md
    05-mcp-se-engineering/
      source/
        PAPER-mcp-instrument-specification-v1.md
        images/
          figure-1-g2-pipeline.svg
          figure-1-g2-pipeline.dot
      PAPER-mcp-instrument-specification-v1.pdf
      header.tex
      README.md
```

## 3. Mandatory Content for `v1.0.0`

### Repository Metadata

- `README.md`
- `LICENSE`
- `CITATION.cff`
- `CHANGELOG.md`
- `RELEASE-NOTES-v1.0.md`
- `MANIFEST-v1.0.md`
- `docs/RELEASE-TO-ZENODO.md`

### Papers

- final PDF for Paper 1
- final PDF for Paper 2
- final PDF for Paper 3
- curated Markdown source for Paper 1
- curated Markdown source for Paper 2
- curated Markdown source for Paper 3

If stable paper sources exist, add them as supplementary material, not as a substitute for the PDFs.

### Paper 1 Artifacts

Source repository: `sbd-toe-knowledge-graph`

Mandatory selections:

- `ontology/appsec-core-v0-consolidated.yaml`
- `ontology/appsec-core-v0-surface-contract.yaml`
- `ontology/appsec-core-slice-registry-v0-draft.yaml`
- `ontology/appsec-core-entity-schema-v0-draft.yaml`
- `ontology/appsec-core-cross-slice-vocabulary-v0-draft.yaml`
- `ontology/appsec-core-v0-instance-index.yaml`
- all ten `ontology/*slice-contract.yaml` files

Destination mapping:

- `papers/01-appsec-core-normalized-ontology/artifacts/ontology/`
- `papers/01-appsec-core-normalized-ontology/artifacts/schema/`
- `papers/01-appsec-core-normalized-ontology/artifacts/slice_contracts/`

For `v1.0.0`, no extra Paper 1 supplement is mandatory beyond these ontology and contract files. If reviewer-friendly example extracts are later prepared, place them in `papers/01-appsec-core-normalized-ontology/artifacts/normalized_examples/`.

### Paper 2 Artifacts

Source repository: `ExternalSourcesInventory`

Mandatory first-wave pilot set, because this is what the current `V1` papers actually rely on:

- `ssdf_sp800_218_v1_1`
- `asvs_v5_0_0`
- `slsa_spec_v1_0_build_track`
- `cis_controls_v8_1`
- `capec_supply_chain_risks_v3_9`

For each mandatory pilot, include:

- `pilots/<pilot>/brief.md`
- `pilots/<pilot>/source_manifest.yaml`
- `pilots/<pilot>/indexing_contract.yaml`
- `data/<pilot>/stubs/source_retrieval_receipt.json`
- `data/<pilot>/stubs/source_unit_inventory.json`
- `data/<pilot>/stubs/source_object_inventory.json`
- `data/<pilot>/stubs/appsec_core_normalization.json`
- `data/<pilot>/stubs/manual_gap_analysis.json`
- the final comparison output when it exists as the paper-supporting terminal artifact

Destination mapping:

- `papers/02-coverage-preserving-knowledge-compilation/artifacts/pilot_manifests/`
- `papers/02-coverage-preserving-knowledge-compilation/artifacts/pilot_outputs/`

### Paper 3 Artifacts

Source repository: `sbd-toe-knowledge-graph`

Mandatory minimum:

- `docs/operations/consumer_contract.md`
- `docs/operations/output_policy.md`
- selected runtime snapshot from `data/publish/runtime/`:
  - `requirements.json`
  - `controls.json`
  - `practices.json`
  - `artifacts.json`
  - `threats.json`
  - `evidence_patterns.json`
  - `requirement_control_links.json`
  - `signal_evidence_links.json`
  - `antipatterns.json`
  - `antipattern_requirement_links.json`
  - `antipattern_threat_links.json`

Worked examples and verification examples are **not mandatory** for `v1.0.0` unless they are explicitly curated as clean public artifacts. If they are not ready, do not publish noisy surrogates.

## 4. Recommended but Not Mandatory for `v1.0.0`

### First-Wave Paper Support Extras

Recommended only if directly cited in the released `V1` paper text:

- source files of the released papers
- compact first-wave method notes
- compact curated cross-pilot notes tied to the five first-wave pilots

### Additional Pilot Wave

Do **not** include these in `v1.0.0` unless the released `V1` text explicitly depends on them:

- `owasp_samm_v2_1`
- `owasp_dsomm`
- `cwe_software_development_view_v4_19_1`
- `enisa_multilayer_ai_cybersecurity_practices_2023`
- selected MCP pilots

### Structural Supplements

Do **not** include these in `v1.0.0` unless the released `V1` text explicitly depends on them:

- `ACR-001` draft and consumer-trial material
- `ACR-002` draft material
- curated cross-pilot synthesis beyond the first-wave pilot set
- curated regulatory overlay synthesis

These should never be published as raw working notes.

### V2 Preparation Material

Do not include:

- `papers/*/v2/**`
- prompt packs
- delta notes
- editor guidance
- companion-paper preparation material

These belong to the internal writing workflow, not to `v1.0.0`.

## 5. Do Not Publish

### Internal Notes and Drafts

- `docs/project/working-notes/**`
- prompt files
- delta notes
- paper review scratchpads
- unfinished `v2` or `v3` branching material not tied to a released paper

### Raw Source Material

- `ExternalSourcesInventory/sources/**`
- raw PDFs or HTML dumps from third-party frameworks
- source captures that reproduce copyrighted upstream content

### Internal Tooling and Noise

- full `ExternalSourcesInventory/scripts/**`
- full internal `src/**` and `tests/**`
- environment files
- `.DS_Store`
- temporary archives
- `.env`
- `Archive.zip`
- `ontology.zip`

### Internal Publish Surfaces Not Needed for Paper Support

Do not publish by default:

- `data/publish/algolia_*`
- `data/publish/indexes/canonical_chunks.jsonl`
- `data/publish/indexes/chunk_entity_mentions.jsonl`
- `data/publish/indexes/chunk_relation_hints.jsonl`
- `data/publish/indexes/mcp_chunks.jsonl`
- `data/publish/indexes/vector_chunks.jsonl`
- `data/publish/semantic/**`

These are implementation-heavy and reviewer-hostile unless a later release explicitly targets system reproducibility beyond the current paper support surface.

## 6. Best Current Publication Decision

Given the current state of:

- `sbd-toe-knowledge-graph`
- `ExternalSourcesInventory`
- `sbd-toe-papers`

the most credible `v1.0.0` is:

- **artifact-first**
- **paper-supporting**
- **conservative**
- **single-repository**
- **strictly V1-bounded**

That means:

- publish a curated subset
- privilege clarity over completeness
- exclude most internal tooling
- exclude raw captures
- include only artifacts directly tied to the released `V1` paper claims
- exclude later waves even if already available internally

## 7. Release Gate Before Publishing

Before creating `v1.0.0`, verify that:

1. all paper PDFs are final
2. all included artifacts have stable filenames
3. all included artifacts are explicitly referenced in the released papers or their supplements
4. no internal note or scratch artifact leaked into the public tree
5. Zenodo-facing metadata is validated
6. no `V2`-only paper material entered the release tree
7. no later-wave pilot or regulatory artifact entered the release tree unless explicitly required by the released `V1` text
