# Build the v2.0.0 figshare/B2SHARE deposit archive

This document describes the deterministic procedure to obtain the `v2.0.0` repository snapshot for archival deposit at figshare and B2SHARE.

**Recommended path:** Use the GitHub Release auto-generated archive at <https://github.com/sbd-ai-runtime/appsec-core-ontology-research/releases/tag/v2.0.0> (asset: `appsec-core-ontology-research-v2.0.0.zip`). This is the canonical archive reference.

**Local reproduction path:** Use `git archive v2.0.0` to reproduce the same snapshot deterministically (described in §3 below).

---

## 1. Pre-conditions

- The `v2.0.0` tag must exist at the canonical commit `487148a` on the public repository main branch.
- The GitHub Release page should show the tag + auto-archive asset (already created by repo workflow at tag push).

Verify (optional):

```bash
git tag -v v2.0.0       # annotated tag verification
git log -1 v2.0.0       # commit at the tag
gh release view v2.0.0  # release metadata + asset listing
```

## 2. Path A — Use GitHub Release archive (recommended)

GitHub auto-attaches a `.zip` archive of the tagged tree to each release:

- **Asset URL:** `https://github.com/sbd-ai-runtime/appsec-core-ontology-research/archive/refs/tags/v2.0.0.zip`
- **Auto-attached on Release page:** `appsec-core-ontology-research-v2.0.0.zip`

For figshare deposit:

1. Open the figshare web UI → New Item or New Version of existing item.
2. Choose "Import from GitHub" option (figshare for GitHub integration) OR paste the GitHub Release URL.
3. Fill metadata (use `README.md` + `MANIFEST.md` in this folder as content reference).
4. Submit; figshare assigns DOI.

For B2SHARE deposit:

1. Open the B2SHARE web UI → New Record (or new version of existing record `10.23728/b2share.b2wc1-tf049` from v1.0.1).
2. Upload the `.zip` archive from GitHub Release page OR provide the Release URL.
3. Fill metadata (use `README.md` + `MANIFEST.md` in this folder as content reference).
4. Submit; B2SHARE assigns DOI.

For both: after DOI assignment, return DOI to programme-lead for v2.0.1 (figshare) and v2.0.2 (B2SHARE) back-stamp via patch tag.

## 3. Path B — Reproduce archive locally

```bash
cd /Volumes/G-DRIVE/Shared/sbd-ai-runtime/appsec-core-ontology-research

# Verify tag
git tag -v v2.0.0
git log -1 v2.0.0

# Create archive locally (mirror of GitHub auto-archive)
git archive --format=zip --output=appsec-core-ontology-research-v2.0.0.zip v2.0.0
# Or tar.gz alternative:
git archive --format=tar.gz --output=appsec-core-ontology-research-v2.0.0.tar.gz v2.0.0

# Compute SHA-256
shasum -a 256 appsec-core-ontology-research-v2.0.0.zip
shasum -a 256 appsec-core-ontology-research-v2.0.0.tar.gz
```

The local archive should be bit-identical (modulo timestamp metadata embedded in some compression formats) to the GitHub Release auto-archive. SHA-256 mismatch indicates either a non-deterministic compression option or a divergent tag state — investigate before deposit.

## 4. Metadata field guidance (figshare + B2SHARE submission forms)

| Field | Recommended value |
|---|---|
| Title | AppSec Core Ontology Research v2.0.0: Curated Research Program Release (P6+P7+P8 Wave) |
| Authors | Pedro Farinha (Independent Researcher / Shiftleft - Secure Software Engineering, Lda.); ORCID `0009-0001-0569-9020` |
| Type | Software / Research artefact bundle |
| License | CC-BY-4.0 (CITATION.cff declaration) |
| Date | 2026-05-16 |
| Version | v2.0.0 |
| Tags / Keywords | application security; ontology; knowledge compilation; retrieval; reproducibility; AppSec Core; research program; SHACL; OWL; design science research; knowledge graph; SbD-ToE |
| Description | Use the abstract from `README.md` §1 + cross-cite paper DOIs from §2 |
| Related identifiers | The 8 paper OSF DOIs (P1=WG8PV, P2=A6ZFJ, P3=S3HET, P4=H5AJE, P5=KH8Y7, P6=U9CRD, P7=3E8G5, P8=TXW8P); programme prospectus OSF DOI 7T849; v1.0.0 figshare 32043771; v1.0.1 B2SHARE b2wc1-tf049 |

## 5. Versioning relative to v1.0.x deposits

The v1.0.0 figshare deposit (`10.6084/m9.figshare.32043771`) and v1.0.1 B2SHARE deposit (`10.23728/b2share.b2wc1-tf049`) cover the P1+P2+P3 wave at the v1.0.x snapshot. The v2.0.0 deposit is the **incremental snapshot** of the same repository extended with P6+P7+P8 wave.

Two valid approaches (programme-lead chooses per archive system):

**Approach A — New deposit per release wave (preserves v1.0.x deposit DOIs as historical anchors):**
- v1.0.0 figshare deposit `32043771` remains the canonical v1.0.x snapshot
- v2.0.0 gets a new figshare deposit with a new DOI
- Both DOIs cite-able; v2.0.x discoverability via repository CITATION.cff
- B2SHARE: same pattern (new record OR new version of existing record `b2wc1-tf049`)

**Approach B — New version of existing deposit (DOI continuity; appended version suffix):**
- v2.0.0 becomes "Version 2.0.0" of the existing figshare deposit `32043771`
- DOI raíz mantém-se; figshare assigns versioned DOI suffix (e.g., `.v2`)
- Reader navigates between versions via figshare deposit page

Per v1.0.x precedent + Pedro's incremental framing, **Approach B (new version of existing deposit)** is recommended. Programme-lead confirms at deposit time.

## 6. Post-deposit back-stamp

Once figshare and/or B2SHARE assign DOIs:

1. Programme-lead returns DOI(s) to Orchestrator.
2. Orchestrator updates `CITATION.cff`:
   - Adds `identifiers` entry per assigned DOI with description
   - Updates `preferred-citation.doi` if appropriate (or adds note)
3. Update `CHANGELOG.md` with the assigned DOI(s).
4. Commit + annotated tag (`v2.0.1` for figshare back-stamp; `v2.0.2` for B2SHARE back-stamp; per v1.0.x precedent).
5. Push origin main + tags.

The `v2.0.x` patch tags themselves do not require new figshare/B2SHARE deposits — they are pure DOI-back-stamp commits, identical to the v1.0.0 → v1.0.1 → v1.0.2 chain.
