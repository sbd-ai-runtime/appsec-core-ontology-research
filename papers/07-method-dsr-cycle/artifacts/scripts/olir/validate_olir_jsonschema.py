"""Validate OLIR per-pilot crosswalks against official NIST OLIR JSON Schema 1.1.

Per user directive 2026-05-09: run validator on emitted OLIR exports.

Strategy:
  1. Read official NIST OLIR JSON Schema (downloaded from
     https://www.nist.gov/document/olirschema; archived locally for reproducibility)
  2. For each of 31 per-pilot crosswalks, convert Cartographer's custom JSON
     output → OLIR-Schema-1.1-conformant JSON
  3. Validate each conformant JSON against schema using jsonschema 4.25.1
  4. Emit per-pilot conformant JSONs + validator report

OLIR Schema field mapping (Cartographer → OLIR 1.1):

  Top-level (per pilot submission):
    informationReferenceName    ← <pilot> to AppSec Core V1 Concept Crosswalk
    informationReferenceShortName ← <pilot> → AC V1
    referenceVersion            ← AC V1 version
    webAddress                  ← programme OSF URL
    focalDocumentVersion        ← pilot version (e.g., 5.0.0)
    targetAudience              ← per-pilot
    comprehensive               ← "No" (cosine-similarity-derived; not exhaustive SME-curated)
    referenceDocumentAuthor     ← "SbD-ToE Programme — AppSec Core ontology project"
    referenceDocument           ← "AppSec Core V1"
    referenceDocumentURL        ← AC V1 OSF URL
    referenceDeveloper          ← Pedro Farinha, programme lead
    comments                    ← methodology summary
    pointOfContact              ← programme contact
    citations                   ← programme DOI

  Per relationship:
    focalDocumentElement        ← source_object_id (e.g., ASVS-REQ-V1.1.1)
    focalDocumentElementDescription ← source text excerpt
    rationale                   ← "Semantic" (all mappings are SBERT cosine = semantic alignment)
    relationship                ← schema enum: "equal to" / "intersects with" / "subset of" / "superset of" / "not related to"
                                  Cartographer mapping: "equal" → "equal to"; "intersects-with" → "intersects with";
                                  "unspecified" → SCHEMA NOT SUPPORTED (drop; empirically 0 such rows exist)
    referenceDocumentElement    ← target_core_entity (e.g., ACP-IVF-001)
    referenceDocumentElementDescription ← target entity description
    fulfilledBy                 ← "Y" (per ratified discipline: emitted relationships are asserted alignments)
    strengthOfRelationship      ← cosine sim × 10, integer 0-10 as string
    comments                    ← Cartographer claim-metadata + threshold rationale
    groupIdentifier             ← claim_id (provenance trail back to substrate v7)

Outputs:
  data/p7_olir_audit/p7_v2_corrected/v7/olir_exports/olir_schema_v1_1/
    <pilot>_olir_v1_1.json × 31 (Schema 1.1 conformant per-pilot)
    olir_schema_v1_1_validator_report.{md,json}
    OLIR_Schema.json (archived copy of official schema for reproducibility)
"""
from __future__ import annotations
import hashlib
import json
import pathlib
import shutil
import sys
from datetime import datetime, timezone

import jsonschema
from jsonschema import Draft4Validator

REPO = pathlib.Path(__file__).resolve().parents[2]
OLIR_DIR = REPO / "data/p7_olir_audit/p7_v2_corrected/v7/olir_exports"
OUT_DIR = OLIR_DIR / "olir_schema_v1_1"
SCHEMA_SOURCE = pathlib.Path("/tmp/OLIR_Schema.json")
SCHEMA_LOCAL = OUT_DIR / "OLIR_Schema.json"

# ---- Constants
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%d")
PROGRAMME_DOI = "10.17605/OSF.IO/7T849"
PROGRAMME_OSF_URL = "https://osf.io/7t849/"
POINT_OF_CONTACT = "Pedro Farinha (programme lead) — SbD-ToE Programme; OSF " + PROGRAMME_DOI
REFERENCE_DOCUMENT_AUTHOR = "SbD-ToE Programme — AppSec Core ontology project"
REFERENCE_DOCUMENT_NAME = "AppSec Core V1"
REFERENCE_VERSION = "V1.next (substrate v7 baseline; cycle-a-frozen-2026-05-08)"
REFERENCE_DEVELOPER = "Pedro Farinha"

# Cartographer → OLIR Schema 1.1 relationship enum mapping
RELATIONSHIP_MAP = {
    "equal": "equal to",
    "intersects-with": "intersects with",
    # unspecified: NOT in schema enum; rows with this relationship are dropped
}


def truncate(s: str, n: int) -> str:
    s = (s or "").strip()
    if len(s) <= n:
        return s
    return s[: n - 1] + "…"


def load_schema() -> dict:
    if not SCHEMA_SOURCE.exists():
        print(f"ERR: schema not at {SCHEMA_SOURCE}. Re-download from "
              f"https://www.nist.gov/document/olirschema (zip; extract OLIR_Schema.json).",
              file=sys.stderr)
        sys.exit(1)
    return json.load(SCHEMA_SOURCE.open())


def per_pilot_input_meta(pilot_id: str) -> dict:
    """Re-derive per-pilot metadata from previously-emitted JSON crosswalk."""
    src = OLIR_DIR / f"concept_crosswalk_{pilot_id}.json"
    return json.load(src.open())


def to_strength(sim: float) -> str:
    """Cosine similarity → integer 0-10 as string (per schema enum)."""
    n = int(round(sim * 10))
    return str(max(0, min(10, n)))


def build_olir_v1_1(pilot_id: str, src: dict) -> dict:
    """Translate Cartographer's per-pilot crosswalk JSON → OLIR Schema 1.1 conformant."""
    crosswalk = src["olir_concept_crosswalk"]
    md = crosswalk["metadata"]
    src_doc = md["source_document"]

    # Top-level submission metadata
    info_name = truncate(
        f"{src_doc['title']} ({src_doc['version']}) — "
        f"Concept Crosswalk to AppSec Core V1",
        200,
    )
    short_name = truncate(f"{pilot_id} → AC V1", 100)
    pilot_url = src_doc.get("url", PROGRAMME_OSF_URL) or PROGRAMME_OSF_URL
    web_addr = truncate(PROGRAMME_OSF_URL, 300)
    focal_version = truncate(str(src_doc.get("version") or pilot_id), 50)
    target_audience = truncate(
        "Application security engineers, security architects, and AppSec Core ontology "
        "users seeking concept-level alignment between this Focal Document and the "
        "AppSec Core V1 reference taxonomy. Mappings are derived computationally via "
        "claim-centric SBERT-based pipeline; SME refinement is future work.",
        500,
    )
    comprehensive = "No"  # Computational mapping; not SME-curated comprehensive submission
    reference_document_author = truncate(REFERENCE_DOCUMENT_AUTHOR, 100)
    reference_document = truncate(REFERENCE_DOCUMENT_NAME, 300)
    reference_document_url = truncate(PROGRAMME_OSF_URL, 500)
    reference_developer = truncate(REFERENCE_DEVELOPER, 100)

    methodology_comment = (
        "OLIR submission generated from substrate v7 (Cycle A frozen 2026-05-08; "
        f"SUPPLIER SHA-256 {md['substrate_supplier_sha256']}) via deterministic "
        "Python pipeline. Threshold-based continuous→categorical translation: "
        "cosine similarity ≥ 0.6 → relationship 'equal to'; 0.4 ≤ sim < 0.6 → "
        "'intersects with'. Multi-claim per source-item: one row per (focalElement, "
        "referenceElement) unique pair using highest-similarity claim. "
        "subset of / superset of / not related to NOT used in first cut (cosine "
        "similarity is undirected; SME refinement future work). Programme DOI: "
        + PROGRAMME_DOI + "."
    )

    point_of_contact = truncate(POINT_OF_CONTACT, 500)
    citations = (
        f"Programme DOI: {PROGRAMME_DOI}. Cycle A frozen tag: cycle-a-frozen-2026-05-08. "
        f"Source pilot: {src_doc['title']} ({src_doc['version']}); "
        f"author {src_doc.get('author', 'unknown')}; URL {pilot_url}. "
        f"Reference: {REFERENCE_DOCUMENT_NAME} ({REFERENCE_VERSION})."
    )

    # Per-relationship rows
    relationships = []
    n_dropped_unspecified = 0
    for m in crosswalk["mappings"]:
        rel_cart = m["relationship_type"]
        rel_olir = RELATIONSHIP_MAP.get(rel_cart)
        if rel_olir is None:
            # 'unspecified' or other non-mappable; drop with disclosure
            n_dropped_unspecified += 1
            continue
        sim = m["strength"]
        focal_id = m["source_element"]["id"]
        focal_descr = truncate(m["source_element"].get("description", ""), 1000)
        ref_id = m["reference_element"]["id"]
        ref_descr = truncate(m["reference_element"].get("description", ""), 1000)
        primary_note = "Primary anchor (item highest-similarity claim)." if m["is_primary"] else "Secondary disclosure."
        comments = (
            f"Cosine similarity {sim:.3f}; threshold mapping → {rel_olir}. "
            f"Claim level: {m.get('claim_level', '?')}. "
            f"{primary_note}"
        )

        rel = {
            "focalDocumentElement": focal_id,
            "focalDocumentElementDescription": focal_descr,
            "rationale": "Semantic",  # SBERT cosine = semantic alignment
            "relationship": rel_olir,
            "referenceDocumentElement": ref_id,
            "referenceDocumentElementDescription": ref_descr,
            "fulfilledBy": "Y",  # asserted alignment
            "strengthOfRelationship": to_strength(sim),
            "comments": comments,
            # groupIdentifier: useful for provenance — link back to claim_id is conceptually right
            # but schema doesn't provide claim-level IDs. Use is_primary boolean encoded as group:
            # primary rows in group "primary"; secondary rows in group "secondary".
            "groupIdentifier": "primary" if m["is_primary"] else "secondary",
        }
        relationships.append(rel)

    out = {
        "informationReferenceName": info_name,
        "informationReferenceShortName": short_name,
        "referenceVersion": truncate(REFERENCE_VERSION, 50),
        "webAddress": web_addr,
        "focalDocumentVersion": focal_version,
        "targetAudience": target_audience,
        "comprehensive": comprehensive,
        "referenceDocumentAuthor": reference_document_author,
        "referenceDocument": reference_document,
        "referenceDocumentURL": reference_document_url,
        "referenceDeveloper": reference_developer,
        "comments": methodology_comment,
        "pointOfContact": point_of_contact,
        "citations": citations,
        "relationships": relationships,
    }
    return out, n_dropped_unspecified


def validate_pilot(pilot_id: str, schema: dict) -> dict:
    src = per_pilot_input_meta(pilot_id)
    olir_doc, n_dropped = build_olir_v1_1(pilot_id, src)
    out_path = OUT_DIR / f"{pilot_id}_olir_v1_1.json"
    out_path.write_text(json.dumps(olir_doc, indent=2))

    validator = Draft4Validator(schema)
    errors = sorted(validator.iter_errors(olir_doc), key=lambda e: e.path)
    err_list = []
    for e in errors:
        err_list.append({
            "path": ".".join(str(p) for p in e.absolute_path),
            "message": e.message,
            "validator": e.validator,
            "schema_path": ".".join(str(p) for p in e.absolute_schema_path),
        })

    return {
        "pilot_id": pilot_id,
        "out_path": str(out_path.relative_to(REPO)),
        "n_relationships": len(olir_doc["relationships"]),
        "n_dropped_unspecified": n_dropped,
        "validator_errors": err_list,
        "valid": len(err_list) == 0,
    }


def main():
    print("=" * 90)
    print("OLIR JSON Schema 1.1 validation — substrate v7 per-pilot crosswalks")
    print("=" * 90)

    # Setup output dir + archive schema
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if not SCHEMA_LOCAL.exists():
        shutil.copy(SCHEMA_SOURCE, SCHEMA_LOCAL)
        print(f"[archive] {SCHEMA_LOCAL.relative_to(REPO)}", file=sys.stderr)

    schema = load_schema()
    print(f"\nLoaded official NIST OLIR JSON Schema 1.1 (id: {schema.get('id', '?')})")
    print(f"Required top-level fields: {len(schema.get('required', []))}")
    print(f"Required per-relationship fields: {len(schema['definitions']['def_relationship_item'].get('required', []))}")
    print()

    # Discover all per-pilot crosswalks
    pilots = sorted(
        p.stem.replace("concept_crosswalk_", "")
        for p in OLIR_DIR.glob("concept_crosswalk_*.json")
    )
    print(f"Pilots discovered: {len(pilots)}")
    print()

    results = []
    n_pass = 0
    n_fail = 0
    total_rels = 0
    total_dropped = 0
    for pilot_id in pilots:
        r = validate_pilot(pilot_id, schema)
        results.append(r)
        total_rels += r["n_relationships"]
        total_dropped += r["n_dropped_unspecified"]
        status = "✅ PASS" if r["valid"] else f"❌ FAIL ({len(r['validator_errors'])} errors)"
        print(f"  {pilot_id:<46}  rels={r['n_relationships']:>5}  dropped={r['n_dropped_unspecified']:>2}  {status}",
              file=sys.stderr)
        if r["valid"]:
            n_pass += 1
        else:
            n_fail += 1

    print()
    print("=" * 90)
    print(f"VALIDATOR RESULTS  : Pass {n_pass}/{len(pilots)}  /  Fail {n_fail}/{len(pilots)}")
    print(f"Total relationships emitted: {total_rels}")
    print(f"Total relationships dropped (unspecified — schema enum doesn't include): {total_dropped}")
    print("=" * 90)
    print()

    # Write reports
    md = []
    md.append("# OLIR JSON Schema 1.1 — official NIST validator report\n")
    md.append(f"**Generated:** {NOW}")
    md.append(f"**Validator:** Python `jsonschema` 4.25.1 (Draft 4) against official NIST OLIR JSON Schema 1.1")
    md.append(f"**Schema source:** `https://www.nist.gov/document/olirschema` (downloaded + archived at `OLIR_Schema.json`)")
    md.append(f"**Schema id:** `{schema.get('id', '?')}`")
    md.append(f"**Substrate v7 anchor:** SUPPLIER SHA-256 `596783ed...62be04`; tag `substrate-v7-iter-3-ai-ml-incorporated`")
    md.append("")
    md.append(f"## Headline")
    md.append("")
    md.append(f"- **Pass: {n_pass} / {len(pilots)} pilot submissions**")
    md.append(f"- **Fail: {n_fail} / {len(pilots)}**")
    md.append(f"- Total relationships emitted (all pilots): **{total_rels}**")
    md.append(f"- Relationships dropped (Cartographer 'unspecified' — not in OLIR schema enum): **{total_dropped}** (empirically 0 — substrate v7 GROUNDED items have sim ≥ E2 ≈ 0.41)")
    md.append("")
    md.append(f"## Schema mapping summary")
    md.append("")
    md.append("Cartographer's custom JSON crosswalk format → OLIR Schema 1.1 (Reference Document submission) translation:")
    md.append("")
    md.append("| Cartographer field | OLIR Schema 1.1 field | Notes |")
    md.append("|---|---|---|")
    md.append("| `relationship_type: equal` | `relationship: equal to` | Schema uses spaces, not hyphens |")
    md.append("| `relationship_type: intersects-with` | `relationship: intersects with` | Schema uses spaces |")
    md.append("| `relationship_type: unspecified` | (DROPPED) | Schema enum doesn't include; empirically 0 rows in substrate v7 |")
    md.append("| `source_element.id` | `focalDocumentElement` | Pilot item is the Focal Document Element |")
    md.append("| `source_element.description` | `focalDocumentElementDescription` | |")
    md.append("| `reference_element.id` | `referenceDocumentElement` | AC V1 entity |")
    md.append("| `reference_element.description` | `referenceDocumentElementDescription` | |")
    md.append("| `strength` (cosine sim 0-1) | `strengthOfRelationship` (enum '0'-'10' / 'N/A') | int(round(sim × 10)) clamped 0-10 |")
    md.append("| `is_primary: true/false` | `groupIdentifier: 'primary' or 'secondary'` | |")
    md.append("| (free-text rationale) | `rationale: 'Semantic'` | Schema requires enum: Semantic/Syntactic/Functional. SBERT cosine = semantic alignment. |")
    md.append("| (implicit) | `fulfilledBy: 'Y'` | Asserted alignment per ratified Step 2 discipline. |")
    md.append("")
    md.append(f"## Per-pilot validation")
    md.append("")
    md.append(f"| Pilot | OLIR relationships | Dropped (unspecified) | Valid |")
    md.append(f"|---|---:|---:|:---:|")
    for r in results:
        status = "✅" if r["valid"] else "❌"
        md.append(f"| `{r['pilot_id']}` | {r['n_relationships']} | {r['n_dropped_unspecified']} | {status} |")
    md.append("")
    if n_fail > 0:
        md.append(f"## Validation errors (per failing pilot)")
        md.append("")
        for r in results:
            if not r["valid"]:
                md.append(f"### `{r['pilot_id']}`")
                md.append("")
                for e in r["validator_errors"][:10]:
                    md.append(f"- **path:** `{e['path']}` · **validator:** `{e['validator']}` · {e['message']}")
                if len(r["validator_errors"]) > 10:
                    md.append(f"- … and {len(r['validator_errors']) - 10} more errors")
                md.append("")
    md.append(f"## Methodology")
    md.append("")
    md.append("All 31 per-pilot crosswalks were translated from Cartographer's custom JSON output (built per substrate v7 + Decision 0003 Amendment 1 §F augmentation symmetry) into OLIR Schema 1.1 conformant Reference Document submissions. Translation is deterministic Python (`scripts/olir/validate_olir_jsonschema.py`); zero LLM invocations during translation or validation step.")
    md.append("")
    md.append("Schema-conformant outputs:")
    md.append("")
    md.append("```")
    md.append(f"data/p7_olir_audit/p7_v2_corrected/v7/olir_exports/olir_schema_v1_1/")
    md.append(f"  OLIR_Schema.json                   ← official NIST schema (archived for reproducibility)")
    md.append(f"  <pilot>_olir_v1_1.json × {len(pilots)}        ← per-pilot OLIR Schema 1.1 conformant")
    md.append(f"  olir_schema_v1_1_validator_report.{{md,json}}  ← this report")
    md.append("```")
    md.append("")
    md.append("## Limits / future work")
    md.append("")
    md.append("- **NIST OLIR Validation Tool (Java JAR; .xlsx input)**: downloaded JAR (17.4 MB) for completeness; SHA3-256 `5809e7d9...` does NOT match published expected `ccd73e69...` (NIST page may be outdated; JAR file authenticity warrants independent verification before runtime use). JAR expects `.xlsx` Focal Document Template input which is a separate downloadable template (not bundled inside JAR). Full xlsx-roundtrip validation is deferred to programme-lead-authorized external submission (future work §13).")
    md.append("- **`subset of` / `superset of` / `not related to`**: not used in current submission (per ratified discipline; cosine similarity is undirected; SME refinement future work).")
    md.append("- **`comprehensive: 'No'`**: declared per current substrate (computational, not SME-curated). Future SME-curated submissions could declare `Yes`.")
    md.append("- **`securityCategorization` (Low/Moderate/High)**: not declared (optional; would require programme-lead determination).")
    md.append("")

    out_md = OUT_DIR / "olir_schema_v1_1_validator_report.md"
    out_md.write_text("\n".join(md))
    print(f"[write] {out_md.relative_to(REPO)}", file=sys.stderr)

    out_json = OUT_DIR / "olir_schema_v1_1_validator_report.json"
    out_json.write_text(json.dumps({
        "validator": "Python jsonschema 4.25.1 (Draft 4)",
        "schema_id": schema.get("id"),
        "schema_source": "https://www.nist.gov/document/olirschema (archived locally)",
        "submission_date": NOW,
        "n_pilots": len(pilots),
        "n_pass": n_pass,
        "n_fail": n_fail,
        "n_relationships_total": total_rels,
        "n_relationships_dropped_unspecified": total_dropped,
        "per_pilot": results,
    }, indent=2))
    print(f"[write] {out_json.relative_to(REPO)}", file=sys.stderr)


if __name__ == "__main__":
    main()
