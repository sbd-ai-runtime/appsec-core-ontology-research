# Paper 0 — Research Programme Prospectus (Public Mirror)

> **Canonical version**: OSF DOI [10.17605/OSF.IO/7T849](https://doi.org/10.17605/OSF.IO/7T849)
> **OSF Project**: https://osf.io/yxvmh
>
> **This folder**: Frozen mirror for citation convenience, backup, and offline access.
> **Last sync**: 2026-04-16
> **Status**: Programme-level public component; NOT a preregistration; does NOT amend the registered P4 empirical design.

## What this is

This folder contains a frozen mirror of the P0 Research Programme Prospectus
for the SbD-ToE / AppSec Core research line. P0 is the programme-level
methodological architecture and validation strategy document — a citable
programme-level synthesis that sits above the individual papers P1-P5.

This mirror exists in the public publication repository for three reasons:

1. **Citability**: Papers 1-5 and their companions can reference P0 as the
   programme-level methodological architecture. Having it in the same
   repository simplifies cross-reference and review.
2. **Backup**: Mirroring in GitHub provides redundancy alongside the
   intended OSF component.
3. **Reproducibility**: When researchers clone the release for replication,
   the programme-level framing is immediately available.

## Discrepancy policy

Once the OSF component is created and its DOI minted, the **OSF version
will be authoritative**. Until then, the files in this folder are the
canonical public surface. This mirror is read-only by convention (see
CODEOWNERS protection in the repository root).

## Contents

| File | Type | Description |
|------|------|-------------|
| `source/RESEARCH-PROGRAM-PLAN.md` | Markdown source | Prospectus manuscript |
| `RESEARCH-PROGRAM-PLAN.pdf` | Rendered PDF | PDF generated via Pandoc/xelatex (42 pages) |
| `source/images/diagram-01-layer-programme-flow.dot` | Graphviz source | Figure 1: Layer / programme flow |
| `source/images/diagram-01-layer-programme-flow.svg` | SVG | Figure 1 rendered |
| `source/images/diagram-02-paper-artifact-publication-map.dot` | Graphviz source | Figure 2: Paper / artifact / publication map |
| `source/images/diagram-02-paper-artifact-publication-map.svg` | SVG | Figure 2 rendered |

## What is NOT included

The following files exist only in the private authoring repository and are
not mirrored here:

- `WORK-GOVERNANCE.md` — internal work governance and task tracking
- `handover/` — internal handover notes
- PNG preview files for diagrams (convenience renders, not canonical)

## Verification

The mirror files are frozen at the SHA-256 hashes below. To verify that a
local copy matches this exact mirror version, run:

```bash
shasum -a 256 RESEARCH-PROGRAM-PLAN.pdf source/RESEARCH-PROGRAM-PLAN.md source/images/*.dot source/images/*.svg
```

Expected output:

```
89a799d0b20b4cb85ef27c78f03657ce76f4436c4398d1aabd3999fa88dde01b  RESEARCH-PROGRAM-PLAN.pdf
cb8ed2bead87f81e8c7bbfe42fe106109b51193d3911d6ff48de2db4e35e234a  source/RESEARCH-PROGRAM-PLAN.md
# DOIs de P1, P2, P3 adicionados à tabela §13.4 — correcção editorial, sem alteração de conteúdo científico
491a5ea9d3a6d671add01b95394a2a6b8f50a4e271b7322201cea141e6d85288  source/images/diagram-01-layer-programme-flow.dot
4286a286c17ef71ebbf4bb59dfec7124eae7651566196d46db4b134467246ab0  source/images/diagram-02-paper-artifact-publication-map.dot
58f19d58b28e16d81fae8124ba624321b081d5dd5909c79dc2e77dfa0de084c9  source/images/diagram-01-layer-programme-flow.svg
2470de21aaf2c5260bd4f88cdce7677da2ce824bf0d483fef5c736bb6692a93c  source/images/diagram-02-paper-artifact-publication-map.svg
```

## Related objects

| Object | Identifier | Status |
|--------|-----------|--------|
| P0 OSF component | [10.17605/OSF.IO/7T849](https://doi.org/10.17605/OSF.IO/7T849) | Not yet created |
| P4 Empirical Design | [10.17605/OSF.IO/H5AJE](https://doi.org/10.17605/OSF.IO/H5AJE) | Registered |
| P5 Apparatus Companion | [10.17605/OSF.IO/KH8Y7](https://doi.org/10.17605/OSF.IO/KH8Y7) | Frozen |
| OSF Umbrella Project | [osf.io/yxvmh](https://osf.io/yxvmh) | Active |
