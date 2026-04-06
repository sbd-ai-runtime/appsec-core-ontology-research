# arXiv Submission Notes

This repository is structured as a research-program release, but arXiv submission is paper-centric. For this repository, the practical path is:

1. submit **three separate arXiv entries**
2. upload **TeX source bundles**, not the current repository PDFs
3. keep the GitHub/Zenodo release as the shared artifact surface referenced by the papers

## Why Not Upload the Current PDFs?

The public PDFs in [`papers/`](../papers/) were generated via Pandoc with a LaTeX engine. arXiv's current guidance says TeX/LaTeX is the preferred archival format, and its submission guidelines say it does **not** accept PDFs created from TeX/LaTeX source as the submission format.

Relevant sources:

- <https://info.arxiv.org/help/submit/index.html>
- <https://info.arxiv.org/help/faq/whytex.html>

## Repo-Specific Decision

Use [`scripts/create_arxiv_bundle.py`](../scripts/create_arxiv_bundle.py) to generate arXiv-ready bundles from the Markdown paper sources.

This export intentionally differs from the public PDF build:

- it generates standalone `main.tex` files for submission
- it uses [`styles/paper-arxiv.tex`](../styles/paper-arxiv.tex), not the public PDF font configuration
- it avoids relying on the font names configured in [`publish_docs.json`](../publish_docs.json)
- it normalizes the box-drawing characters that compile locally but are brittle in arXiv-style TeX environments

## Generate Bundles

List the configured papers:

```bash
python3 scripts/create_arxiv_bundle.py --list
```

Generate all three bundles:

```bash
python3 scripts/create_arxiv_bundle.py
```

Generate a single bundle:

```bash
python3 scripts/create_arxiv_bundle.py --document paper3
```

By default, output is written into each paper's own `arxiv/` directory:

- `papers/01-appsec-core-normalized-ontology/arxiv/main.tex`
- `papers/02-coverage-preserving-knowledge-compilation/arxiv/main.tex`
- `papers/03-ontology-grounded-retrieval/arxiv/main.tex`

To also write upload-ready archives inside each paper folder:

```bash
python3 scripts/create_arxiv_bundle.py --write-archive
```

The script verifies the generated TeX locally with `xelatex` unless `--skip-verify` is passed.

## Processor Choice

The generated bundles are meant to be submitted as `xelatex`.

Important nuance:

- the current arXiv TeX Live page says `xelatex` is supported and notes that XeLaTeX support was introduced in November 2025
- older arXiv FAQ pages still contain advice written before that change

For current behavior, prefer:

- <https://info.arxiv.org/help/faq/texlive.html>

Over this older troubleshooting page when they conflict:

- <https://info.arxiv.org/help/faq/mistakes.html>

## Fonts

arXiv's XeLaTeX environment has limited fontconfig support. Loading fonts by human-readable font name is brittle there. This is why the arXiv export does not use the `STIX Two Text`, `STIX Two Math`, and `Menlo` settings from the public PDF build.

Relevant source:

- <https://info.arxiv.org/help/faq/texlive.html>

## Metadata and Submission Checklist

Before uploading each paper:

1. create or log into the arXiv author account that will submit the work
2. confirm endorsement status for the target category if needed
3. upload the generated `.tar.gz` bundle, not the PDF
4. choose `xelatex` during submission
5. paste plain-text title, abstract, and author list into arXiv metadata fields
6. inspect the generated arXiv PDF carefully before finalizing
7. after posting, add DOI and journal reference later if applicable

Helpful references:

- <https://info.arxiv.org/help/submit/index.html>
- <https://info.arxiv.org/help/faq/whytex.html>
- <https://info.arxiv.org/help/faq/mistakes.html>
- <https://trevorcampbell.me/html/arxiv.html>

## Endorsement

If the submitting account is not already endorsed in the target category, arXiv may require endorsement before the submission can proceed.

Relevant source:

- <https://info.arxiv.org/help/endorsement.html>
