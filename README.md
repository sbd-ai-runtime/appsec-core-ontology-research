# AppSec Core Research

Curated public repository for the current `V1` AppSec Core paper set and its release-grade supporting artifacts.

This repository is intentionally **not** the internal development repository. It is a clean public publication surface prepared for:

- academic review
- paper and preprint support
- stable public citation
- GitHub release management
- Zenodo archival and DOI minting

This repository should be read as a **research program release (`v1.0.0`)**: one curated versioned object containing three tightly related papers plus the minimum artifact surface needed to support them.

## What This Repository Is

This repository is the **public, curated publication surface** for a small set of research outputs in:

- application security ontology design
- coverage-preserving knowledge compilation
- ontology-grounded retrieval for LLM-assisted security workflows

It is designed to support a paper-facing release with a structure that is easy for reviewers and readers to inspect.

## What This Repository Is Not

This repository is **not**:

- the internal working repository
- the full development environment
- a dump of notes, pilots, or experiments
- a mirror of `sbd-toe-knowledge-graph`
- a mirror of `ExternalSourcesInventory`
- a general-purpose software distribution

Internal notes, drafts, temporary scripts, raw captures, source working copies, and contradictory intermediate states are deliberately excluded.

## Publication Model

The publication strategy separates three layers:

1. **Internal private repositories**
   - laboratory and day-to-day development
   - not published directly
2. **This public GitHub repository**
   - curated, human-readable, stable enough for review
   - the public home of the released research artifacts
3. **Zenodo release snapshots**
   - immutable versioned releases
   - DOI-backed citation targets
   - archival records for tagged GitHub releases

In short:

- private repos = laboratory
- public GitHub repo = curated research surface
- Zenodo = canonical archival snapshot

## DOI Model

For `v1.0.0`, the publication model is:

- **one Zenodo DOI for the repository release**
- **three papers inside that release**

The DOI resolves to the curated repository snapshot as a whole, not to three separate Zenodo records. Each paper is part of the same research-program release and should cite the shared repository release alongside any paper-specific bibliographic reference.

## Current Repository Topology Decision

For `v1.0.0`, the best option is:

- **one new curated public GitHub repository**
- **not** one repository per paper
- **not** one repository per pilot family
- **not** a direct publication of any current internal repository

This follows from the current state of:

- `sbd-toe-knowledge-graph`
- `ExternalSourcesInventory`
- `sbd-toe-papers`

The material is internally rich but publicly noisy. A single curated repository is the cleanest option because it:

- gives one clear citation target
- avoids cross-repository version drift
- keeps GitHub release management simple
- keeps Zenodo ingestion simple
- gives reviewers one coherent surface

A second public repository may make sense later only if a stable public tooling or software distribution is intentionally released. That is **not** needed for `v1.0.0`.

## Scope of `v1.0.0`

The first public release should be **artifact-first, conservative, and V1-bounded**.

It should support the current `V1` paper set:

1. AppSec Core ontology / normalization
2. coverage-preserving knowledge compilation
3. ontology-grounded retrieval

It should do so with the **minimum clean artifact set**, not by publishing the whole internal program.

This means:

- include only artifacts that support claims made in the current `V1` papers
- exclude later pilot waves unless the released `V1` text explicitly depends on them
- exclude `V2` prompt packs, delta notes, and editor material
- treat a later `V2` as a **complete later release**, not as an incremental add-on mixed into `v1.0.0`

## Proposed Structure

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
  paper_sources/
    paper1_appsec_core.md
    paper2_compilation.md
    paper3_ontology_grounded_retrieval.md
  papers/
    appsec_core_normalized_ontology.pdf
    coverage_preserving_knowledge_compilation.pdf
    ontology_grounded_retrieval.pdf
  paper1_artifacts/
    ontology/
    schema/
    slice_contracts/
    normalized_examples/
  paper2_artifacts/
    pilot_manifests/
    pilot_outputs/
    cross_pilot/
    method_notes/
  paper3_artifacts/
    retrieval_contract/
    runtime_snapshot/
    worked_examples/
    verification_examples/
```

## Mapping from Current Internal Repositories

This public repository should be populated by a **curated subset** extracted from:

- `sbd-toe-knowledge-graph`
- `ExternalSourcesInventory`
- `sbd-toe-papers`

The detailed selection is defined in [MANIFEST-v1.0.md](./MANIFEST-v1.0.md).

## Recommended Inclusion Policy

### Mandatory

- final paper PDFs
- curated paper source Markdown files used to generate those PDFs
- AppSec Core ontology and slice contracts
- selected first-wave pilot outputs that directly support the current `V1` papers
- minimal retrieval artifacts for the retrieval paper
- repository metadata files

### Recommended

- source paper files (`.md` or `.tex`) in addition to PDFs
- small curated worked examples and verification examples
- curated first-wave method notes if directly supportive

### Do Not Publish

- internal working notes
- raw source captures from frameworks
- temporary scripts and one-off utilities
- environment files and credentials
- full build/test toolchains from the internal repos
- noisy indexes not directly needed for paper support
- later pilot waves and regulatory validation material not used by the released `V1` papers
- `V2` prompts, delta notes, or companion-paper preparation material

## Relationship to the Papers

### Paper 1 → Ontology

The ontology paper should be supported by:

- `paper1_artifacts/ontology/`
- `paper1_artifacts/schema/`
- `paper1_artifacts/slice_contracts/`
- selected normalized examples only if curated as reviewer-friendly supplements

### Paper 2 → Normalization

The knowledge-compilation paper should be supported by:

- selected first-wave pilot manifests
- selected normalization outputs
- selected gap and comparison outputs
- method notes only where directly supportive of the released `V1` paper text

### Paper 3 → Grounded Retrieval

The retrieval paper should be supported by:

- the retrieval contract
- a minimal runtime snapshot
- worked examples only if explicitly curated for `v1.0.0`
- verification examples only if explicitly curated for `v1.0.0`

## Important Publication Decision

Based on the current state of the internal repositories, the most credible first public release is:

- **one single curated public repository**
- **strictly limited to the current `V1` paper-supporting surface**
- **fully curated for Paper 1 and Paper 2**
- **Paper 3 included in minimal form unless its examples are explicitly curated**

If the richer Paper 3 artifacts are not ready, the safest option is:

- include the paper PDF
- include the retrieval contract
- include the minimal runtime snapshot
- defer richer examples to a later full release

## Citation Guidance

For `v1.0.0`, cite:

1. the relevant paper, when referring to a specific argument or method
2. the shared Zenodo-backed repository release, when referring to the released artifact package

This keeps the citation model aligned with the actual publication structure:

- one release
- one DOI
- three related papers
- one coherent artifact surface

## Citation

Please cite:

1. the specific paper you used
2. the versioned repository release archived in Zenodo

Repository-level citation metadata is provided in [CITATION.cff](./CITATION.cff).

## GitHub and Zenodo

The recommended publication flow is:

1. curate the public repository on GitHub
2. tag a release such as `v1.0.0`
3. let Zenodo archive that GitHub release
4. cite the resulting Zenodo DOI in papers and related outputs

Operational guidance is provided in [docs/RELEASE-TO-ZENODO.md](./docs/RELEASE-TO-ZENODO.md).

## PDF Build

If the paper source Markdown files are available locally, the repository can generate the release PDFs from [publish_docs.json](./publish_docs.json) using:

```bash
python3 scripts/create_pdf.py
```

The script reads the document manifest from `publish_docs.json`, resolves paths relative to the repository root, and invokes `pandoc`. The manifest supports per-document metadata, output paths, source lists, optional per-document `pandoc_args`, and global defaults. In the current curated `v1` package, the manifest points to repository-local paper sources so the PDF build does not depend on the private paper-writing repository.

If you later need to draft against external paper sources during internal writing, keep that as a temporary internal workflow and switch the manifest back to repository-local sources before publishing a release.

## Artifact Sync

The curated artifact files can be copied from the internal source repositories using:

```bash
python3 scripts/sync_artifacts.py
```

The sync manifest lives in [publish_artifacts.json](./publish_artifacts.json). It defines the exact `V1` artifact set to copy into this repository from sibling source repositories such as `../sbd-toe-knowledge-graph` and `../ExternalSourcesInventory`.

## License

For this first artifact-first release, the recommended default license is **CC BY 4.0** for the curated papers and research artifacts in this repository.

If executable code is later added as a maintained public surface, a split license model should be adopted:

- `CC BY 4.0` for papers, documentation, and curated research artifacts
- `Apache-2.0` for maintained code

## Status

This staging package is a **publication plan and skeleton**, not yet the final public release repository.

Before public release:

- fill in final author metadata
- generate final paper PDFs
- copy the selected artifacts into the release structure
- validate `CITATION.cff`
- create the GitHub release
- verify Zenodo ingestion
- verify that no `V2`-only material entered `v1.0.0`
