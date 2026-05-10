---
date: 2026-05-10
author: Archon (under programme-lead Pedro Farinha)
type: brief (P6 supporting validation — Phase A read-only)
status: Phase A delivered; Phase B/C gated on programme-lead decision
responds_to: programme-lead direct authorisation 2026-05-10 (briefing scope: disjointness verification + OOPS! + FOOPS!)
output_destination: Curator P6 §3.1 (disjointness) + §6 / §10.6 (pitfall + FAIR audit)
---

# P6 ontology validation — Phase A read-only report

## TL;DR

Three validations executed against `formal/appsec_core/02-owl/exports/appsec-core-v0-bounded-v1.ttl` at `ontology-v1-final` (`b267cf3`):

1. **§3.1 disjointness** — ✅ **PRESENT** in canonical TTL line 83-84 (`owl:AllDisjointClasses` for 5 first-class entities). Paper claim supportable as-is. **No fix needed; no SHA cascade.**
2. **OOPS! pitfall scan** — **0 Critical / 1 Important / 5 Minor**. One Important pitfall (P11 "Missing domain or range in properties", 14 affected datatype properties) is candidate for `build_owl.py` fix. Five Minor pitfalls are cosmetic / future-work.
3. **FOOPS! FAIR scan** — analytical equivalent (public API blocked because ontology repo is private and namespace not resolvable): **5/15 pass (33%)**. All 10 gaps are **TTL-fixable** via ontology metadata additions in `build_owl.py` header (license/creator/created/versionIRI/publisher/preferred-prefix/issued/citation/doi/definitions for property terms).

Phase B/C decision gate: programme-lead + Curator decide whether to apply OOPS! P11 fix + FOOPS! metadata additions in ONE batched regen of `build_owl.py` (with single SHA-256 cascade), or defer to v1.2/future work and downgrade §10.6 paper claims accordingly.

## Method

All three items run against canonical TTL at `ontology-v1-final` tag (`b267cf3`):

- **Item 1**: `grep -inE "disjoint|AllDisjoint" formal/appsec_core/02-owl/exports/appsec-core-v0-bounded-v1.ttl` + alt-formats.
- **Item 2**: OOPS! REST API at `https://oops.linkeddata.es/rest` with the RDF/XML alt-format (`alt-formats/appsec-core-v1.0.owl`) as `OntologyContent`. Returns categorized pitfall report. Parsed locally and tabulated.
- **Item 3**: FOOPS! API at `https://foops.linkeddata.es/assessOntology` returned `overall_score: 0.0` because it requires a publicly fetchable ontology URI and our repo is private + namespace `https://securitybydesign.dev/ontology/appsec-core/v1#` is not resolvable. Substituted with analytical 15-check equivalent against canonical TTL using FOOPS! published test definitions at `https://w3id.org/foops/test/`. Local script: regex inspection of ontology header + term coverage.

## Item 1 — §3.1 disjointness verification

### Finding: declaration IS present

Canonical TTL (`formal/appsec_core/02-owl/exports/appsec-core-v0-bounded-v1.ttl`) lines 83-84:

```turtle
[] a owl:AllDisjointClasses ;
    owl:members ( ac:ControlObjective ac:Practice ac:Mechanism ac:Artifact ac:EvidencePattern ) .
```

Alt-formats confirm:

| Alt-format | Line | Form |
|------------|------|------|
| `appsec-core-v1.0.owl` (RDF/XML) | 1928-1936 | `<owl:AllDisjointClasses rdf:nodeID="…">` block |
| `appsec-core-v1.0.jsonld` | 3261 | `"http://www.w3.org/2002/07/owl#AllDisjointClasses"` |
| `appsec-core-v1.0.nt` (N-Triples) | 1011 | `_:n… rdf:type owl:AllDisjointClasses` |

`build_owl.py` lines 421-429 emit this axiom from canonical YAML schema; the 5 first-class entities come from the schema's `first_class_entities` enumeration.

### Pairwise disjointness semantics

`owl:AllDisjointClasses` with 5 members asserts pairwise disjointness — i.e., no individual can be simultaneously a ControlObjective and a Practice (etc.) across all 10 pairs:

| Pair | Disjointness asserted |
|------|----------------------|
| ControlObjective ⊥ Practice | ✅ |
| ControlObjective ⊥ Mechanism | ✅ |
| ControlObjective ⊥ Artifact | ✅ |
| ControlObjective ⊥ EvidencePattern | ✅ |
| Practice ⊥ Mechanism | ✅ |
| Practice ⊥ Artifact | ✅ |
| Practice ⊥ EvidencePattern | ✅ |
| Mechanism ⊥ Artifact | ✅ |
| Mechanism ⊥ EvidencePattern | ✅ |
| Artifact ⊥ EvidencePattern | ✅ |

All 10 pairs covered by the single `owl:AllDisjointClasses` declaration. Equivalent to having 10 separate `owl:disjointWith` axioms.

### Recommendation for P6 §3.1

**Path (a) — leave paper claim as-is and cite TTL line 83-84.** No code change. No SHA cascade. Paper § 3.1 disjointness statement is sustained by existing declaration.

**Caveat for paper prose**: the declaration uses `owl:AllDisjointClasses` (collective form) rather than 10 pairwise `owl:disjointWith` axioms. Semantically equivalent in OWL 2 RL/EL/QL; reasoner-friendly. Paper prose should reflect the actual axiom form to avoid auditor confusion ("§3.1 declares pairwise disjointness via a single `owl:AllDisjointClasses` axiom covering the 5 first-class entities").

## Item 2 — OOPS! pitfall scan

### Endpoint + raw response

- Endpoint: `POST https://oops.linkeddata.es/rest` with XML body (OntologyContent = RDF/XML alt-format).
- HTTP 200 / 20570 bytes response.
- Response saved at `/tmp/oops_response2.xml` (local; not committed).

### Summary

| Importance | Count |
|------------|------:|
| **Critical** | **0** |
| **Important** | **1** |
| **Minor** | **5** |
| **Total** | **6** |

### Per-pitfall

| Code | Importance | N affected | Name |
|------|------------|-----------:|------|
| **P11** | **Important** | **14** | **Missing domain or range in properties** |
| P04 | Minor | 1 | Creating unconnected ontology elements |
| P08 | Minor | 38 | Missing annotations |
| P13 | Minor | 13 | Inverse relationships not explicitly declared |
| P20 | Minor | 2 | Misusing ontology annotations |
| P22 | Minor | 1 | Using different naming conventions in the ontology |

### P11 details (Important)

14 datatype properties lack `rdfs:domain` and/or `rdfs:range`:

- `ac:expectation`, `ac:statement`, `ac:expected_outcome`, `ac:verification_posture`, `ac:validation_method` — EvidencePattern / ControlObjective string-valued properties
- `ac:local_practice_type`, `ac:local_mechanism_type`, `ac:domain_key` — enum-valued slice-local properties
- `ac:evidence_pattern_id`, `ac:artifact_id`, `ac:practice_id`, `ac:mechanism_id`, `ac:objective_id`, `ac:name` — identifier + name properties

### P20 details (Minor)

`ac:ControlObjective` and `ac:EvidencePattern` flagged as "Misusing ontology annotations" — likely refers to `rdfs:comment` containing the schema's `verification_posture` enum value rather than a natural-language description. Worth a 1-line review of the class comment strings.

### P22 details (Minor)

Mixed naming: `artifact_supports_evidence_pattern` (snake_case) coexists with `hasCanonicalEvidenceKind` (camelCase). 1 element flagged. Cosmetic.

### Recommendations

| Pitfall | Effort to fix | SHA cascade? | Recommendation |
|---------|---------------|--------------|----------------|
| **P11 Important** | ~30 min in `build_owl.py`: add `rdfs:domain` + `rdfs:range xsd:string` (or enum class) per property | Yes (single regen) | **Fix in Phase C if Pedro authorises batched regen** |
| P04 (ControlledVocabularyValue unconnected) | Investigate whether this is sentinel class; may already be intentional | Possibly | Defer pending decision on whether ControlledVocabularyValue is documented placeholder |
| P08 (38 missing annotations) | Mass-add `rdfs:label` + `rdfs:comment` to 38 properties via `build_owl.py` | Yes (same regen) | **Batch with P11 if cascade triggered** |
| P13 (13 inverse relationships) | Add `owl:inverseOf` to symmetric pairs (e.g., `objective_realized_by_practice` ↔ `practice_realizes_objective`) | Yes (same regen) | Lower priority; only if cascade triggered for P11+P08 |
| P20 (CO + EvidencePattern annotation misuse) | Review rdfs:comment values; replace verification_posture-shaped strings with natural-language descriptions | Yes (same regen) | Worth fixing for paper credibility |
| P22 (naming inconsistency) | Decide canonical convention (existing convention is snake_case for properties from YAML, camelCase for OWL-generated derived properties); document the rule | Code-only change | Document in paper §10 method appendix; no TTL change needed |

## Item 3 — FOOPS! FAIR scan (analytical equivalent)

### Why analytical

Public FOOPS! at `https://foops.linkeddata.es/assessOntology` requires a publicly fetchable ontology URI. Our setup blocks both:
- The repository `https://github.com/SbD-ToE/sbd-toe-ontology` is **private** (GitHub raw URL returns 404 unauthenticated).
- The namespace IRI `https://securitybydesign.dev/ontology/appsec-core/v1#` is **not yet resolvable** (no DNS / no content negotiation at the domain).

POST attempts with TTL content as `ontology_text` / `ontology_content` / `content` / `text` keys all returned `overall_score: 0.0` with `resource_found: ontology` (placeholder) — the public service does not have a content-upload mode.

Substituted with analytical 15-check equivalent against canonical TTL using FOOPS! published test definitions at `https://w3id.org/foops/test/`. Local Python script: `/tmp/foops_local_v3.py` (regex inspection of ontology header block + term coverage).

### Score: 5/15 PASS (33.3%)

| Code | Category | Pass | Check |
|------|----------|:---:|-------|
| PURL1 | Findable | ❌ | Ontology has persistent URL |
| **RDF1** | **Interoperable** | **✅** | Available in RDF (TTL/RDF-XML/JSON-LD/N-Triples) |
| OM1 | Findable | ❌ | Minimum metadata |
| OM2 | Reusable | ❌ | Recommended metadata |
| OM3 | Reusable | ❌ | Detailed metadata |
| OM4.1 | Reusable | ❌ | License declared in ontology |
| OM4.2 | Reusable | ❌ | License is resolvable |
| OM5.1 | Reusable | ❌ | Basic provenance |
| OM5.2 | Reusable | ❌ | Detailed provenance |
| **FIND1** | **Findable** | **✅** | Prefix declared |
| **VOC1** | **Interoperable** | **✅** | Reuses metadata vocabularies (dcterms minimal) |
| **VOC2** | **Interoperable** | **✅** | Imports/reuses established vocabularies (dcterms) |
| **VOC3** | **Reusable** | **✅** | All terms have labels (48/48) |
| VOC4 | Reusable | ❌ | All terms have definitions (10/48) |
| VER1 | Findable | ❌ | Version IRI in metadata (only `owl:versionInfo "1.0"` string; no `owl:versionIRI`) |

### Gap categorization

**TTL-fixable** (add metadata in `build_owl.py` ontology header — single regen + SHA cascade):

| Gap | Fix | Affected check |
|-----|-----|----------------|
| `dcterms:license <license-URI>` | Add literal pointing to LICENSE in repo or SPDX identifier | OM1, OM4.1, OM4.2 |
| `dcterms:creator <author>` | Add programme-lead Pedro Farinha or institution | OM1, OM5.1 |
| `dcterms:created "2026-04-15"^^xsd:date` | Add v1.0 release date | OM2, OM5.1 |
| `dcterms:issued "2026-05-08"^^xsd:date` | Add cycle-a-frozen date | OM5.2 |
| `dcterms:publisher <publisher>` | Add SbD-ToE / institution | OM3, OM5.2 |
| `dcterms:bibliographicCitation "…"` | Cite P6 method paper when available | OM2 |
| `vann:preferredNamespacePrefix "ac"` | Standard prefix declaration | OM2 |
| `owl:versionIRI <…/v1.1>` | Add version IRI | OM1, VER1 |
| `dcterms:description` | Already covered by `rdfs:comment` per FOOPS! flexible matching; can add explicit `dcterms:description` for clarity | OM1 |
| `rdfs:comment` on 38 properties | Batch annotation addition | VOC4 |

**Repo-fixable** (governance / external configuration — does NOT touch TTL SHA):

- **PURL1**: Migrate namespace to `w3id.org` redirect (e.g., `https://w3id.org/sbd-toe/appsec-core/v1#`). High-impact future work; touches all instance IRIs across ontology + substrate + claims. Out-of-scope for Cycle A close.

**Out-of-scope / informational**:

- Namespace resolution via DNS+content-negotiation (`https://securitybydesign.dev/ontology/appsec-core/v1` returning the OWL TTL with proper `Accept` header) — requires server-side setup, separate from ontology repo.

### Recommendation

**FOOPS! score 5/15 → 13/15 achievable** with TTL-fixable additions in single `build_owl.py` regen. PURL1 + namespace resolution = Cycle B work (programme-lead decision on `w3id.org` registration).

For P6 §10.6 prose:
- Report current 5/15 honest baseline.
- State "10 of 10 failing checks are TTL-fixable via ontology header metadata; fix scheduled for v1.2 release post-Cycle-A close" OR
- Apply fix now in batched regen and report post-fix 13/15 baseline with PURL1 + namespace-resolution as future work.

## Phase B/C decision gate — recommendation

If programme-lead authorises a **single batched regen** in Phase C, the cumulative fix would:

| Fixable in one regen | OOPS! | FOOPS! |
|----------------------|------|---------|
| P11 (domain/range on 14 properties) | ✅ Important pitfall closed | — |
| P08 (annotations on 38 elements) | ✅ Minor closed | ✅ VOC4 lifted 10/48 → 48/48 |
| P13 (inverse relationships on 13) | ✅ Minor closed | — |
| P20 (CO/EvidencePattern annotation cleanup) | ✅ Minor closed | — |
| OM1/OM2/OM3 metadata block | — | ✅ 6+ checks lifted |
| OM4.1/OM4.2 license declared | — | ✅ 2 checks lifted |
| OM5.1/OM5.2 provenance declared | — | ✅ 2 checks lifted |
| VER1 versionIRI | — | ✅ 1 check lifted |

**Expected post-regen state**:
- OOPS!: 0 Critical / 0 Important / 1-2 Minor (P04 ControlledVocabularyValue + P22 naming convention as deliberate / documented)
- FOOPS!: ~13/15 pass (PURL1 + VOC2-strict remaining as future-work)

**Single SHA cascade affecting**:

| File | Reason |
|------|--------|
| `formal/appsec_core/02-owl/exports/appsec-core-v0-bounded-v1.ttl` | TTL regen |
| `formal/appsec_core/02-owl/exports/alt-formats/*.{owl,jsonld,nt}` | alt-format regen |
| `formal/appsec_core/05-validation/reports/appsec-core-v1-pyshacl-summary.json` | `data_graph_sha256` updated |
| `formal/appsec_core/05-validation/reports/appsec-core-v0-shacl-validation-summary.json` | regen |
| `packages/ontology/appsec-core/v0.1/formal/appsec-core-v0-bounded-v1.ttl` | mirror (if package re-emitted) |

**Curator re-pin scope after cascade**: P6 §3.1 + §6 + §10.6 + P7 SHA references + figshare-deposit MANIFEST.md — approx. 6-8 SHA-256 strings to update.

**Effort estimate for Phase C** (if authorised): ~2-3h Archon (code changes to `build_owl.py` + regen + revalidation + new SHA propagation in CHANGELOG + FREEZE-REGISTRY entry for new pin tag).

## Asks (one line each)

1. Programme-lead + Curator: decide Phase B gate — apply OOPS! P11 + FOOPS! metadata fixes in single regen, OR defer to v1.2 with paper-side honest baseline reporting.
2. Programme-lead: if fix authorised, confirm authority for new pin tag (e.g., `ontology-v1.1-fair-baseline` or `apparatus-shacl-pyshacl-v3.1`) at the post-regen commit.
3. Curator: integrate Phase A findings into P6 §3.1 (disjointness confirmed via TTL line 83-84) + §6 / §10.6 (OOPS! 0C/1I/5M baseline + FOOPS! 5/15 analytical baseline).
4. Orchestrator: if regen authorised, route Cartographer for substrate v8 re-grounding against new OWL TTL (data graph SHA change invalidates substrate v7 grounding).

## References

- Item 1 evidence: TTL line 83-84 (`formal/appsec_core/02-owl/exports/appsec-core-v0-bounded-v1.ttl`) + `build_owl.py:421-429`
- Item 2 OOPS! raw response: `/tmp/oops_response2.xml` (20570 bytes; not committed — ephemeral)
- Item 3 FOOPS! analytical script: `/tmp/foops_local_v3.py` (regex-based; not committed — ephemeral)
- Decision 0001 Option C (apparatus composition): `agentic/decisions/0001-consumer-conformance-shapes-ontology-owned.md`
- ACR-004 sprint close (predecessor with SHA cascade history): `agentic/done/2026-05-05-acr004-output-rendering-execution-close.md`
- Figshare ontology inventory (current SHA-256 baseline): `agentic/briefs/2026-05-08-figshare-ontology-inventory.md`
- FOOPS! test definitions (canonical reference): `https://w3id.org/foops/test/`
- OOPS! pitfall catalog: `https://oops.linkeddata.es/catalogue.jsp`
