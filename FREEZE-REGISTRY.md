# FREEZE REGISTRY — appsec-core-ontology-research

**Repository:** `appsec-core-ontology-research` — https://github.com/sbd-ai-runtime/appsec-core-ontology-research
**Part of programme:** SbD-ToE / AppSec Core (P0 DOI 10.17605/OSF.IO/7T849)
**Governed by:** `PROGRAMME-PRESERVATION-PROTOCOL.md` v1.0
**Last updated:** 2026-06-07

**Role in programme:** curated public publication surface and frozen reference mirror for the five-paper core arc (P1, P2, P3) plus P0 prospectus, P4 registered design, and P5 apparatus companion. Derives its artifacts from upstream execution repos (`sbd-toe-knowledge-graph`, `ExternalSourcesInventory`, `sbd-toe-ontology`, `appsec-core-ontology-research-authoring`). Classed as a **read-only post-freeze** surface per Curator's `AGENTS.md`; any modification of tag-protected state is a Class A violation under §9.2.

---

## Published states

**Verifiable alignment basis:** each paper's `artifacts/` directory here is sourced from a specific upstream commit declared in `MANIFEST-v1.0.md`. Upstream FREEZE-REGISTRY files cross-reference the exact commit whose artifacts were copied forward.

| Tag | Commit | Date | Paper/event | DOI | Archives |
|-----|--------|------|-------------|-----|----------|
| `paper-p0-published` | `4977c5b` | 2026-04-12 | P0 Research Programme Prospectus mirror with real DOI + Zenodo config | OSF 10.17605/OSF.IO/7T849 | figshare:10.6084/m9.figshare.32043771 (inherited via v1.0.0); B2SHARE:10.23728/b2share.b2wc1-tf049 (inherited via v1.0.1) |
| `paper-p1-published` | `e28d3b1` | 2026-04-16 | P1 "AppSec Core Normalized Ontology" at v1.0.0 release state | OSF 10.17605/OSF.IO/WG8PV | figshare:10.6084/m9.figshare.32043771 (v1.0.0); B2SHARE:10.23728/b2share.b2wc1-tf049 (v1.0.1) |
| `paper-p2-published` | `e28d3b1` | 2026-04-16 | P2 "Coverage-Preserving Knowledge Compilation" at v1.0.0 release state | OSF 10.17605/OSF.IO/A6ZFJ | figshare + B2SHARE (as above) |
| `paper-p3-published` | `e28d3b1` | 2026-04-16 | P3 "Ontology-Grounded Retrieval" at v1.0.0 release state | OSF 10.17605/OSF.IO/S3HET | figshare + B2SHARE (as above) |
| `paper-p4-registered` | `16f23a9` | 2026-04-16 | P4 "Empirical Evaluation Design" frozen mirror with SHA-256 verification chain | OSF registration 10.17605/OSF.IO/H5AJE | figshare + B2SHARE (as above) |
| `paper-p5-frozen` | `33d8b11` | 2026-04-17 | P5 "MCP Instrument Specification" frozen mirror with freeze-guard CI | OSF component 10.17605/OSF.IO/KH8Y7 | figshare + B2SHARE (as above) |

---

## Frozen states

| Tag | Commit | Date | Description | Freeze reason | Archives |
|-----|--------|------|-------------|---------------|----------|
| `v1.0.0` (existing) | `e28d3b1` | 2026-04-16 | First curated public release — 3 arXiv-ready papers + OSF preprint DOIs + Zenodo config aligned to v1.0.0. **Content baseline** for the frozen scientific record | Initial publication of the frozen scientific record | figshare:10.6084/m9.figshare.32043771 (DOI recorded via metadata bump v1.0.1) |
| `v1.0.1` (existing) | `f803a45` | 2026-04-17 | Metadata-only version bump recording the figshare archive DOI. Content is v1.0.0 + DOI field | Archive DOI recording; content of v1.0.0 is archived at figshare | figshare (same as v1.0.0) |
| `v1.0.2` (existing) | `880654f` | 2026-04-17 | Metadata-only version bump recording the B2SHARE archive DOI. Content is v1.0.0 + both DOI fields. Zenodo deposit pending (external block on account) | Second-service DOI recording; content of v1.0.0 is also archived at B2SHARE | figshare + B2SHARE:10.23728/b2share.b2wc1-tf049 |

**Two-service rule satisfaction (§4.1):** the content at `e28d3b1` (v1.0.0 state) is the scientific record referenced by P1, P2, P3 DOIs. That content is archived at **figshare** (10.6084/m9.figshare.32043771) and at **B2SHARE** (10.23728/b2share.b2wc1-tf049). The v1.0.1 and v1.0.2 git tags are metadata-only version bumps that record those DOIs in the repository's config — they do not introduce new content states. Two-service rule is **satisfied**. Zenodo (pending account unblock) is planned as additional redundancy, not required for compliance.

### v2.0.x wave (added retroactively to this registry 2026-06-07)

| Tag | Commit | Date | Description | Freeze reason | Archives |
|-----|--------|------|-------------|---------------|----------|
| `v2.0.0` | `487148a` | 2026-05-16 | Second curated public release — P6 (AppSec Core v1, OSF U9CRD) + P7 (Pressure-Testing, OSF 3E8G5) + P8 (Compilation v2, OSF TXW8P) wave consolidation, with supporting bundle artefacts. Preceded by 6 immutable `v2.0.0-construction-*` tags | Publication of the v2.0 wave scientific record | figshare:10.6084/m9.figshare.32307669 (primary, via v2.0.1); B2SHARE:10.23728/b2share.p2kzz-hpk37 (secondary, via v2.0.2) |
| `v2.0.1` | `18e65a0` | 2026-05-17 | Metadata-only bump recording the figshare archive DOI of the v2.0.0 snapshot | Archive DOI recording | figshare (same as v2.0.0) |
| `v2.0.2` | `5f10e5f` | 2026-05-17 | Metadata-only bump recording the B2SHARE archive DOI of the v2.0.0 snapshot | Second-service DOI recording | figshare + B2SHARE (as above) |
| `v2.0.3` | `893e951` | 2026-06-04 | Content patch — P6/P7 ACR promotion-threshold correction (ADR 0004) + purge of 43 research-process bundle mappings (ADR 0005/0011) | Correction patch on the v2.0 wave | **None yet** — v2.0.3 content state (ACR-corrected P6/P7) has no external archive; see Open items |
| `v2.0.4` | (this release) | 2026-06-07 | Additive — ICSME 2026 Tool Demonstration submitted manuscript surfaced under `submitted-peer-reviewed/`; SUBMITTED-PEER-REVIEWED.md index; first commit of this registry | First venue submission surfaced publicly | **None yet** — inherits the v2.0.3 archive gap; see Open items |

**Two-service rule for v2.0.x (§4.1):** the v2.0.0 content state is **satisfied** (figshare + B2SHARE). The v2.0.3 content state (ACR-corrected P6/P7 manuscripts) and v2.0.4 are **not yet archived externally** — the corrected P6/P7 also require their OSF (U9CRD/3E8G5) and figshare deposit updates. These must be remediated before any next paper-publication freeze event that cites the corrected state.

---

## Pre-protocol tags (retained for historical continuity)

Per `PROGRAMME-PRESERVATION-PROTOCOL.md` §10.3, states tagged under pre-protocol conventions remain validly tagged. All three `v1.0.x` tags predate the protocol (effective 2026-04-17) and are preserved as-is.

| Tag | Commit | Date | Annotation | Notes |
|-----|--------|------|------------|-------|
| `v1.0.0` | `e28d3b1` | 2026-04-16 | To verify (`git cat-file -t v1.0.0`) | Release tag published via GitHub Releases (https://github.com/sbd-ai-runtime/appsec-core-ontology-research/releases/tag/v1.0.0). Anchors the content state referenced by P0/P1/P2/P3/P4/P5 DOIs |
| `v1.0.1` | `f803a45` | 2026-04-17 | To verify | Metadata bump adding figshare DOI. Content equivalent to v1.0.0 |
| `v1.0.2` | `880654f` | 2026-04-17 | To verify | Metadata bump adding B2SHARE DOI. Content equivalent to v1.0.0 |

No annotated-tag gap under §10.3 (pre-protocol naming is retained). If annotation status is lightweight, programme lead may optionally create supplementary annotated tags; not a Class B violation under §10.3 backward compatibility.

---

## Protected tags

Per `PROGRAMME-PRESERVATION-PROTOCOL.md` §3.2, tags listed here are permanently immutable: no deletion, no move, no force-push affecting them.

Upon authorization by programme lead and creation, these annotated tags are protected:

- `paper-p0-published`
- `paper-p1-published`
- `paper-p2-published`
- `paper-p3-published`
- `paper-p4-registered`
- `paper-p5-frozen`

Pre-protocol release tags `v1.0.0`, `v1.0.1`, and `v1.0.2` are also treated as immutable per §10.3.

Post-protocol release tags, immutable per §3.2: `v2.0.0`, `v2.0.1`, `v2.0.2`, `v2.0.3`, the six `v2.0.0-construction-*` tags, and `v2.0.4` (upon creation).

**Note (2026-06-07):** the six `paper-<id>-*` annotated tags proposed in the Published-states table above were never created (open item 1 below remains open). The Published-states table records the *proposed* tag names and target commits; until creation, the `v1.0.0` tag at `e28d3b1` anchors the published P0–P5 record. Tag-type verification (2026-06-07): `v1.0.0` and four `v2.0.0-construction-*` tags are lightweight; all other release tags are annotated — covered by §10.3 backward compatibility for pre-protocol tags, and to correct going forward (all new tags annotated).

---

## Current working state

**Current branch:** `main`
**Most recent commit:** `893e951` (2026-06-04) — "v2.0.3: P6/P7 ACR threshold correction + purge 43 research-process bundle mappings"
**Most recent release tag:** `v2.0.3` at `893e951`
**Expected next freeze event:** `v2.0.4` (this commit) — ICSME 2026 Tool Demonstration submission surfaced under `submitted-peer-reviewed/`. Thereafter: JOWO 2026 papers enter after EasyChair submission (deadline 2026-06-17); archive remediation of the v2.0.3/v2.0.4 content state.

---

## Cross-references

This repository mirrors and is referenced by:

- **P0 Research Programme Prospectus** — OSF 10.17605/OSF.IO/7T849. Source authoring: `appsec-core-ontology-research-authoring/papers/00-research-programme-statement/`.
- **P1 v1** — OSF 10.17605/OSF.IO/WG8PV. Ontology upstream: `sbd-toe-ontology` (current state bootstrapped from `sbd-toe-knowledge-graph` and migrated; confirm specific P1 input commit during retroactive tagging).
- **P2 v1** — OSF 10.17605/OSF.IO/A6ZFJ. Pilots upstream: `ExternalSourcesInventory` at commit `a0c1c2d7` (4 of 5 first-wave pilots bit-identical verified per ESI registry); CAPEC pilot authoritative at `sbd-toe-knowledge-graph` (requires commit identification).
- **P3 v1** — OSF 10.17605/OSF.IO/S3HET. Runtime snapshot upstream: `sbd-toe-knowledge-graph`.
- **P4 design registration** — OSF 10.17605/OSF.IO/H5AJE. Manuscript upstream: `appsec-core-ontology-research-authoring/papers/04-empirical-evaluation/`.
- **P5 apparatus specification** — OSF 10.17605/OSF.IO/KH8Y7. Manuscript upstream: `appsec-core-ontology-research-authoring/papers/05-mcp-se-engineering/`.

This repository depends on (upstream inputs preserved for reproducibility):

- `sbd-toe-ontology` at commit to be determined during retroactive tagging of P1's ontology input. Candidate: ontology's `v0-frozen` tag at commit `bd78a93`.
- `ExternalSourcesInventory` at commit `a0c1c2d7` (per ESI registry `paper-2-v0-published` tag).
- `sbd-toe-knowledge-graph` at commit to be determined during retroactive tagging of P3's runtime input. Candidate: KG's `v1.4.2` tag at commit `7f6a340` (2026-04-07 manual v0.2.8 refresh).
- `appsec-core-ontology-research-authoring` at per-paper staging commits (P0/P4/P5 manuscripts).

---

## Open items for programme-lead decision

### Critical — deadline 2026-05-15 (protocol §8.1)

1. **Create all 6 `paper-<id>-*` annotated tags** listed above under programme-lead authorization.
2. **Verify annotation type of `v1.0.0`, `v1.0.1`, `v1.0.2`** with `git cat-file -t <tag>`. If lightweight, optionally supplement with annotated tags (not a Class B violation per §10.3; but annotation is preferred going forward).
3. **Enable branch protection on `main`** in the GitHub remote (`git@github.com:sbd-ai-runtime/appsec-core-ontology-research.git`): prevent force-push, prevent tag deletion, require PR review for `FREEZE-REGISTRY.md` and `PROGRAMME-PRESERVATION-PROTOCOL.md`.

### Archive discipline (protocol §4.1) — SATISFIED

4. **Zenodo archive** — pending account unblock. When available, deposit v1.0.0 content as additional redundancy (not required for compliance, since figshare + B2SHARE already satisfy the two-service rule for the v1.0.0 content state).

### Content correction (Class B — scheduled)

5. **Legacy `sbd-toe-papers` reference** — `README.md` lines 98-100, 209-211, 280-282 and `MANIFEST-v1.0.md` line 282 reference an upstream named `sbd-toe-papers`. The actual current upstream is `appsec-core-ontology-research-authoring`; `sbd-toe-papers` is legacy, preserved as an append-only backup at `/Volumes/G-DRIVE/Shared/BACKUP-SBD-AOS-STUFF/sbd-toe-papers/` (last commit 2026-04-05). Class B violation per §9.2. **Remediation scheduled by programme lead (Pedro Farinha) "atempadamente".**

### Checklist completion (protocol Appendix A)

6. `CITATION.cff` — present at repo root. Verify metadata parity with all published papers during retroactive tagging.
7. `LICENSE` — present (CC BY 4.0 per `README.md`). No action.
8. `README.md` — present. No action beyond item 5 above.

---

## Violations detected

| Class | Description | Status |
|-------|-------------|--------|
| **B (reversible)** | Legacy `sbd-toe-papers` reference in README.md + MANIFEST-v1.0.md | Programme lead has scheduled remediation "atempadamente" (open item 5) |
| **B (reversible)** | This registry existed at the repo root since 2026-04-17 but was **never committed**; releases v2.0.0, v2.0.1, v2.0.2, and v2.0.3 were tagged without the registry in the same commit (Protocol Rule 5 violation). | Remediated 2026-06-07: registry enters version control in the v2.0.4 commit, retroactively recording the v2.0.x states. Detected and self-reported per Rule 8 |
| **B (reversible)** | v2.0.3 content state (ACR-corrected P6/P7) has no external archive (§4.1); corrected P6/P7 also pending OSF (U9CRD/3E8G5) + figshare deposit updates. | Open — remediate before any next paper-publication freeze event citing the corrected state |

---

## Change log for this registry

| Date | Change | Author |
|------|--------|--------|
| 2026-06-07 | First commit of this registry (v2.0.4 release). Added v2.0.x frozen-states table (v2.0.0–v2.0.3 retroactive + v2.0.4); updated protected-tags list; noted that the six proposed `paper-<id>-*` tags were never created and recorded tag-type verification; updated current working state; documented two Class B items (registry never committed through v2.0.0–v2.0.3, remediated; v2.0.3/v2.0.4 archive gap, open). | Curator under Pedro Farinha |
| 2026-04-17 | Initial registry draft under §8.1 retroactive application. Proposes 6 `paper-<id>-*` annotated tags. Preserves 3 pre-protocol release tags `v1.0.0`, `v1.0.1`, `v1.0.2` per §10.3. Documents 1 Class B violation (legacy `sbd-toe-papers` reference) with programme-lead-scheduled remediation. Two-service rule clarified as SATISFIED (figshare + B2SHARE cover v1.0.0 content; v1.0.1 and v1.0.2 are metadata-only bumps). Draft produced by Orchestrator; tag creation and registry commit require explicit programme-lead authorization. | Orchestrator under Pedro Farinha |
