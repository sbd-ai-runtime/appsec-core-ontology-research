# AI-Assisted Authoring and Execution — Disclosure

This document discloses the use of AI-assisted tools across the AppSec Core
research programme, in line with the disclosure expectations of ACM, IEEE,
SIGSOFT, Springer-Nature, and Elsevier publishing policies, and the ICMJE
recommendations on AI in scholarly publishing.

The disclosure distinguishes between **authoring use** (AI as a writing and
review assistant) and **experimental use** (AI as a controlled component of the
empirical apparatus described in the papers themselves).

## Tools Used

| Tool | Provider | Used for |
|------|----------|----------|
| **Claude** (Opus 4.6 and Sonnet 4.6) | Anthropic | Manuscript drafting, structural consistency checking, reference cross-validation, governance and stream documentation |
| **Codex** | OpenAI | Implementation of code components, including the experimental apparatus described in Paper 5 (the dual-mode MCP server) and supporting evaluation pipeline |
| **Custom MCP servers** | (this research) | Described in Paper 5 as the experimental apparatus itself; not authoring tools |

## Authoring Use

Claude was used to support manuscript preparation across the research programme,
including:

- Initial drafting and structural revision of manuscript sections
- Cross-reference checking between papers in the programme
- Terminology consistency across Papers 1-3 (and forthcoming Papers 4-5)
- Editorial review of governance, methodology, and discussion sections
- Reference verification and bibliography organization

All AI outputs were reviewed, verified, and edited by the author. Where AI
suggestions were accepted, they passed human review against the ACM SIGSOFT
Empirical Standards (Ralph et al., 2021), the empirical software engineering
methodology in Wohlin et al. (2012), and the canonical vocabulary defined for
the research programme.

The author retains full responsibility for the content, claims, conclusions,
and bibliographic accuracy of every paper.

### What AI Was NOT Used For

AI was explicitly **not** used to:

- Generate or fabricate empirical data
- Generate citations or bibliographic entries (all references are human-verified
  through the bibliography database; see `Bibliography/` in the research-program
  workspace)
- Make scientific judgements about hypotheses, experimental design, statistical
  analysis, or results interpretation
- Define experimental variables, metrics, or evaluation criteria — these were
  pre-registered on OSF (DOI 10.17605/OSF.IO/H5AJE) prior to data collection
- Author this disclosure document (it was reviewed and edited by the author
  before publication)

## Experimental Use

Where AI is part of the experimental apparatus (Paper 4 evaluation, Paper 5
instrument paper), it is treated as a **controlled component** of the apparatus,
not as an independent source of judgement.

The dual-mode MCP server described in Paper 5 (G1 plain RAG and G2 ontology-grounded
retrieval) operates with:

- **Documented controlled and variable factors** — what is held constant between
  the two modes (prompt, token budget, corpus, model, decoding parameters) and
  what is deliberately manipulated (retrieval method, context structure,
  completeness guarantee)
- **Deterministic configuration where possible** — temperature=0, fixed maximum
  tokens, fixed stop sequences, versioned model identifiers
- **Full instrumentation logging** — every retrieval call, token count, timing
  measurement, and delivered context is logged for post-hoc auditability and
  for the M_recall metric defined in the experimental design
- **Pre-registration of the apparatus** — Paper 5 will be registered as an
  instrument addon on OSF (project osf.io/yxvmh) before P4 data collection,
  freezing the apparatus specification independently of the experimental results

The selection of the LLM under test (Claude Sonnet 4.6 in Phase 1), the
experimental groups (G0/G1/G2), the metrics (M_SbD, M_audit, M_recall, M_func,
M_tool), the task set (12 tasks across 7 of 10 AppSec Core slices), and the
statistical plan (Friedman test with Wilcoxon signed-rank pairwise contrasts,
Bonferroni-corrected) were defined by the author and **pre-registered on OSF**
(DOI 10.17605/OSF.IO/H5AJE) prior to apparatus implementation and data collection.

Codex was used to assist the implementation of the apparatus code itself, but
the apparatus design, factor specifications, and validation procedures are the
author's design decisions. All apparatus code is reviewed and tested before use
in any data collection.

## Authorship and Accountability

In line with **ICMJE**, **ACM**, **IEEE**, **Springer-Nature**, and
**Elsevier** policies on AI in scholarly publishing:

- **AI tools are not credited as authors** of any paper or artifact in this
  research programme
- **AI tools do not bear authorship responsibility** for the content
- **The author bears full scientific responsibility** for the ontology design,
  the compilation method, the retrieval contract, the experimental design, the
  instrument specification, the empirical results (when produced), and all
  conclusions across Papers 1-5

This disclosure applies to all papers and artifacts released under the
AppSec Core Research Programme, including but not limited to:

- Paper 1 — AppSec Core: A Normalized Ontology for Security Requirements
- Paper 2 — Coverage-Preserving Compilation of Normative and Empirical
  Security Knowledge
- Paper 3 — Ontology-Grounded Retrieval for Auditable LLM-Assisted Secure
  Code Generation
- Paper 4 — Empirical Evaluation (pre-registered design, OSF DOI
  10.17605/OSF.IO/H5AJE)
- Paper 5 — MCP Dual-Mode Instrument Paper (in preparation)

## Compliance References

| Body | Policy / Statement |
|------|--------------------|
| ACM | [Authorship Policy on Generative AI](https://www.acm.org/publications/policies/new-acm-policy-on-authorship) (2023+) |
| IEEE | [Submission and Peer Review Policies on AI](https://journals.ieeeauthorcenter.ieee.org/become-an-ieee-journal-author/publishing-ethics/guidelines-and-policies/submission-and-peer-review-policies/) |
| Springer-Nature | [Editorial policies on AI](https://www.springernature.com/gp/editorial-policies/ai) |
| Elsevier | [Generative AI policies for journals](https://www.elsevier.com/about/policies-and-standards/the-use-of-generative-ai-and-ai-assisted-technologies-in-scientific-writing) |
| ICMJE | [Recommendations: AI in scholarly publishing](https://www.icmje.org/recommendations/) |
| SIGSOFT | Ralph et al. (2021), *ACM SIGSOFT Empirical Standards for Software Engineering Research*, arXiv:2010.03525 |

## Updates

This disclosure will be updated if:

- New AI tools are introduced into the authoring or experimental workflow
- The role of an AI tool materially changes
- A new paper or artifact is added to the research programme
- Venue-specific disclosure requirements differ from this baseline

Last updated: 2026-04-10
