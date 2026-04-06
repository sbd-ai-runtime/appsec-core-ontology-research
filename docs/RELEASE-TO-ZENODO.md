# GitHub to Zenodo Release Notes

This document describes the recommended release flow for the curated public repository.

## Recommended Strategy

Use:

- **GitHub** as the public, organized, live repository
- **Zenodo** as the immutable, citable archival layer

Do **not** upload the internal development repository directly.

For the current program state, use:

- **one curated public GitHub repository now**
- **one Zenodo deposition stream tied to that repository's releases**

Do not create multiple public repositories for `v1.0.0` unless there is a separately maintained public software distribution. That condition is not met yet.

## Pre-Release Checklist

Before creating the first public release:

1. finalize the curated repository structure
2. ensure the included artifacts match `MANIFEST-v1.0.md`
3. confirm that all paper PDFs are final
4. confirm that `README.md`, `LICENSE`, `CITATION.cff`, and release notes are complete
5. remove any internal notes, prompts, or temporary files
6. verify that the release contains only the current `V1` paper-supporting surface

## Recommended Metadata Approach

For the first release:

- use `CITATION.cff`
- do **not** add `.zenodo.json` unless you need metadata fields that `CITATION.cff` cannot express cleanly

Important Zenodo note:

- Zenodo supports both `CITATION.cff` and `.zenodo.json`
- if both are present, Zenodo uses `.zenodo.json` and ignores `CITATION.cff` for GitHub release archiving

For a simple first release, keeping only `CITATION.cff` is the cleaner option.

## GitHub -> Zenodo Flow

Recommended workflow:

1. create the new curated public repository on GitHub
2. push the curated `v1.0.0` content
3. connect the repository in Zenodo
4. create a GitHub release such as `v1.0.0`
5. wait for Zenodo to ingest the release
6. verify the Zenodo record, DOI, and metadata
7. use the version DOI in the paper package and keep the concept DOI for the project landing page

## Step-by-Step

### 1. Enable the GitHub repository in Zenodo

According to the Zenodo GitHub documentation:

- connect your GitHub account to Zenodo
- sync the repository list
- enable the specific repository for archiving

Official Zenodo guide:

- https://help.zenodo.org/docs/github/enable-repository/

### 2. Create the GitHub release

Once the repository is enabled in Zenodo:

- create a release in GitHub
- use a stable tag such as `v1.0.0`
- attach release notes that match `RELEASE-NOTES-v1.0.md`

Official Zenodo guide:

- https://help.zenodo.org/docs/github/archive-software/github-upload/

### 3. Wait for Zenodo ingestion

Zenodo will process the GitHub release and create a software record.

Then:

- verify the DOI
- verify the title, creators, version, and description
- verify the archival status

## Manual Upload Fallback

If GitHub integration is not available or fails, Zenodo also supports manual software upload.

Important constraint from Zenodo:

- a manual software record should contain **a single compressed file**

Official Zenodo guide:

- https://help.zenodo.org/docs/github/archive-software/manual-upload/

Because this project is intended to remain live on GitHub, manual upload should be treated as fallback, not the default.

## Best Practical Recommendation

For the current research program, the cleanest path is:

1. build one new curated public GitHub repository
2. tag `v1.0.0`
3. let Zenodo archive that release
4. cite the Zenodo DOI in the papers

## Release Policy Recommendation

Use semantic, human-readable release tags:

- `v1.0.0`
- `v1.0.x`
- `v2.0.0`

Recommended release policy:

- `v1.0.0`: first stable release containing only the current `V1` paper-supporting artifact set
- `v1.0.x`: only bounded curation fixes or omissions within the same `V1` release line
- `v2.0.0`: a later full release line for revised papers or materially expanded artifact scope, explicitly referencing `v1`

## Source Notes

Zenodo documentation consulted:

- Enable a repository: https://help.zenodo.org/docs/github/enable-repository/
- Archive a release from GitHub: https://help.zenodo.org/docs/github/archive-software/github-upload/
- Describe software: https://help.zenodo.org/docs/github/describe-software/
- Upload software manually: https://help.zenodo.org/docs/github/archive-software/manual-upload/
