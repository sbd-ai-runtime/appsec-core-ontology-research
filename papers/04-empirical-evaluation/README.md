# Paper 4 — Empirical Evaluation Design (OSF Mirror)

> **Canonical version**: OSF DOI [10.17605/OSF.IO/H5AJE](https://doi.org/10.17605/OSF.IO/H5AJE)
> **OSF Registration**: https://osf.io/h5aje
> **OSF Project**: https://osf.io/yxvmh
> **Internet Archive**: https://archive.org/details/osf-registrations-h5aje-v1
>
> **This folder**: Frozen mirror for citation convenience, backup, and offline access.
> **Last sync**: 2026-04-10
> **Status**: Paper 4 design pre-registered 2026-04-07; experiment not yet executed.

## What this is

This folder contains a frozen mirror of the Paper 4 experimental design as
pre-registered on the Open Science Framework. The OSF registration is
**immutable** — its protocol cannot be modified after approval. This mirror
exists in the public publication repository for three reasons:

1. **Citability**: Papers 1-3 (and forthcoming Paper 5 instrument paper) reference
   Paper 4 as a companion pre-registration. Having the design document in the
   same repository as the related papers simplifies cross-reference and review.
2. **Backup**: The OSF platform is reliable but not invulnerable. Mirroring
   in GitHub provides redundancy.
3. **Reproducibility**: When researchers clone the release for replication, the
   design is immediately available without requiring a separate OSF lookup.

## Discrepancy policy

If files in this folder differ in any way from the OSF registration, the
**OSF version is authoritative**. This mirror is read-only by convention
(see frontmatter on each file) and by CODEOWNERS protection (see
`.github/CODEOWNERS` in the repository root).

## Contents

| File | Type | Description |
|------|------|-------------|
| `source/DESIGN-empirical-evaluation-v1.md` | Markdown source | Design document as pre-registered (v1, dated 2026-04-07) |
| `header.tex` | LaTeX header | Header used to render the PDF from markdown |
| `DESIGN-empirical-evaluation-v1.pdf` | Rendered PDF | The PDF as registered on OSF |

## What is NOT included

The `DESIGN-DRIFT-from-OSF-registration.md` document, which tracks factual
corrections (entity types and traceability percentages) made after the
registration, is **not** mirrored in this folder. It exists only in the
private authoring repository because:

- The corrections are factual clarifications, not protocol changes
- The hypotheses, statistical plan, task set, groups, metrics, and
  infrastructure described in the registered design are unchanged
- Including the drift document here would suggest the protocol was modified,
  which it was not — only adjacent factual statements were corrected

The drift document remains visible and accessible in the authoring repository
for transparency. Reviewers and replicators who need the full corrections
record can request access.

## Verification

The mirror files are frozen at the SHA-256 hashes below. To verify that a
local copy matches this exact mirror version, run:

```bash
shasum -a 256 DESIGN-empirical-evaluation-v1.pdf header.tex source/DESIGN-empirical-evaluation-v1.md
```

The output must match these values exactly:

| File | SHA-256 |
|------|---------|
| `DESIGN-empirical-evaluation-v1.pdf` | `3880c8bd056ddae7b819137a3a45015e2a8c360bc198a6082f6e811e83ab457d` |
| `header.tex` | `6a9025c6da3a00d2b711a9ad03f25fb33fd90a4f157a204840532abaff5da5f6` |
| `source/DESIGN-empirical-evaluation-v1.md` | `45c5542176cfd8146b798881efb3a6cc7d40661f933886031ab51b350f448e19` |

**Frozen as of**: 2026-04-10

If any local file's hash differs from the value above, the file has been
modified — either by accident or by an unauthorized sync. Compare against
the OSF canonical version at https://osf.io/h5aje and restore from there.

The same SHA-256 hashes are also recorded in `MOVED-TO-PUBLISH-LOG.md` in
the authoring repository, providing a cross-repository verification chain.

## Sync workflow

This folder is updated only when:

1. The OSF design itself is amended (which has not happened and is not
   expected — the registration is closed)
2. A factual correction important enough to publish is added to the OSF
   registration through OSF's official correction mechanism

In either case, the sync is **manual** and requires:

1. Comparison against the canonical OSF version
2. Update of the `Last sync` date in this README and in each file's frontmatter
3. Entry in `MOVED-TO-PUBLISH-LOG.md` in the authoring repository
4. CODEOWNERS approval for the change

Automatic sync from the authoring repository is **not** permitted.

## Citation

When citing Paper 4, use the OSF DOI as the primary citation:

```
Farinha, P. (2026). Empirical Research Design: A Security-by-Design Evaluation
Framework for Ontology-Grounded Code Generation [Pre-registered design]. Open
Science Framework. https://doi.org/10.17605/OSF.IO/H5AJE
```

The mirror in this repository may be cited as a secondary location for
convenience, but the OSF DOI must always be present.
