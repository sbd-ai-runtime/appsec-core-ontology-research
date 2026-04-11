# Paper 5 — MCP Instrument Specification (Frozen Companion Mirror)

> **Companion role**: apparatus-specification companion to the Paper 4 study
> **Paper 4 OSF DOI**: [10.17605/OSF.IO/H5AJE](https://doi.org/10.17605/OSF.IO/H5AJE)
> **Public repository**: https://github.com/sbd-ai-runtime/appsec-core-ontology-research
>
> **This folder**: Frozen companion mirror for citation convenience, backup, reviewer support, and offline access.
> **Last sync**: 2026-04-11
> **Status**: Public mirror of the current Paper 5 apparatus-specification manuscript; not an OSF registration and not an execution-grade bundle.

## What this is

This folder contains a frozen public mirror of the Paper 5 apparatus-specification
manuscript. Paper 5 defines the transparent MCP-based apparatus used to execute
the companion Paper 4 evaluation. It is included in the public research-program
repository for four reasons:

1. **Citability**: the manuscript can be cited and inspected alongside Papers
   1–4 without requiring access to the private authoring repository.
2. **Reviewer support**: reviewers can inspect the apparatus specification,
   build assumptions, and mirror policy from the same public release surface.
3. **Backup**: the mirror provides redundancy for the current frozen public
   copy of the manuscript and its rendering assets.
4. **Offline access**: when researchers clone the release for inspection, the
   apparatus specification is immediately available together with the companion
   study design and the supporting core papers.

## What this is not

This folder is **not**:

- an OSF registration
- the canonical day-to-day authoring location
- an execution-grade software bundle
- a public release of the future MCP/software distribution

The manuscript here is a frozen companion mirror. The private authoring
repository remains the working environment for future revisions. Those future
revisions do not retroactively modify this public copy.

## Discrepancy policy

This mirror is read-only by convention (see frontmatter on each text file) and
by CODEOWNERS protection.

If files in this folder differ from later working copies in the authoring
repository, the interpretation is:

- this folder is the authoritative public copy for the current public release
- the authoring repository is the working source for possible future revisions
- any future public update requires an explicit new freeze/sync step

Unlike Paper 4, there is no external immutable registration that outranks this
mirror. The mirror itself is therefore the citable public release surface for
this specific frozen version.

## Contents

| File | Type | Description |
|------|------|-------------|
| `source/PAPER-mcp-instrument-specification-v1.md` | Markdown source | Frozen public mirror of the Paper 5 manuscript |
| `PAPER-mcp-instrument-specification-v1.pdf` | Rendered PDF | Public reading PDF for the frozen mirror |
| `header.tex` | LaTeX header | Header used to render the public PDF mirror |
| `source/images/figure-1-g2-pipeline.svg` | Figure asset | Vector figure referenced by the manuscript |
| `source/images/figure-1-g2-pipeline.dot` | Figure source | Graphviz source for the vector figure |

## What is NOT included

The following remain in the private authoring repository and are deliberately
excluded from this public mirror:

- review notes
- co-author action notes
- scope-review notes
- reference-correction prompts
- execution-time support artifacts not yet part of the public `v1` tree
- any future software/tooling bundle associated with the apparatus

## Verification

The mirror files are frozen at the SHA-256 hashes below. To verify that a local
copy matches this exact mirror version, run:

```bash
shasum -a 256 \
  PAPER-mcp-instrument-specification-v1.pdf \
  header.tex \
  source/PAPER-mcp-instrument-specification-v1.md \
  source/images/figure-1-g2-pipeline.svg \
  source/images/figure-1-g2-pipeline.dot
```

The output must match these values exactly:

| File | SHA-256 |
|------|---------|
| `PAPER-mcp-instrument-specification-v1.pdf` | `fe34566c22d151c12f5e4a8d11a43de415dcace8594073108295f1cfe3f95a49` |
| `header.tex` | `655ae0a07296d16e09e43248c9f2e38ad9eff090f5243c7efc044edb7f5a6a96` |
| `source/PAPER-mcp-instrument-specification-v1.md` | `00818dd66fabf3c4e393948f32dda8f545187521e874b42cf7816813ffcc80bf` |
| `source/images/figure-1-g2-pipeline.svg` | `a8dae78a2b2f9bcc32639e02da5352c01acb795ca2951882d22e02a121625307` |
| `source/images/figure-1-g2-pipeline.dot` | `846fbd23be926883ffcf7f94144fe42eab4b943bd591e86c7f8d7c7789125d95` |

**Frozen as of**: 2026-04-11

If any local file's hash differs from the value above, the file has been
modified after the freeze and no longer matches the current public mirror.

The same hashes should also be recorded in `MOVED-TO-PUBLISH-LOG.md` in the
authoring repository, providing a cross-repository verification chain.

## Sync workflow

This folder is updated only when:

1. a new public freeze of the Paper 5 manuscript is explicitly approved
2. the PDF is re-rendered from the approved frozen manuscript
3. the README hashes and the authoring move log are updated in the same sync

Automatic sync from the authoring repository is **not** permitted.

## Citation

Until a separate paper-specific archival identifier exists, cite:

1. the manuscript title as it appears in this folder
2. the shared repository release DOI once minted
3. the Paper 4 OSF DOI when referring to the companion registered study design

This keeps study registration, apparatus specification, and repository-release
citations clearly separated.
