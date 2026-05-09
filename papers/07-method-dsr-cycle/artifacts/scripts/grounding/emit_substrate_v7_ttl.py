"""Emit substrate v7 as RDF TTL for SHACL validation."""
from __future__ import annotations
import json, pathlib

REPO = pathlib.Path(__file__).resolve().parents[3]
V7 = REPO / "data/p7_olir_audit/p7_v2_corrected/v7"
SUPPLIER = V7 / "SUPPLIER_v7_0.json"
OUT = V7 / "reports/v7-substrate-claims.ttl"

AC = "https://securitybydesign.dev/ontology/appsec-core/v1#"
EX = "https://securitybydesign.dev/consumer/v7/"

SLICE_TO_ASC = {
    "ACO-SCBI": "SliceASC01", "ACO-IAT":  "SliceASC02", "ACO-ATB":  "SliceASC03",
    "ACO-TSV":  "SliceASC04", "ACO-TMR":  "SliceASC05", "ACO-SPC":  "SliceASC06",
    "ACO-IVF":  "SliceASC07", "ACO-ITS":  "SliceASC08", "ACO-RPR":  "SliceASC09",
    "ACO-SLG":  "SliceASC10",
}


def main():
    sup = json.load(SUPPLIER.open())
    items = sup["items"]
    seen_items = set()
    out = []
    out.append(f"@prefix ac: <{AC}> .")
    out.append(f"@prefix ex: <{EX}> .")
    out.append("@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .")
    out.append("")
    for it in items:
        item_iri = f"item-{it['source']}_{it['source_object_id']}"
        if item_iri not in seen_items:
            out.append(f"ex:{item_iri} a ac:Item ;")
            out.append(f"    ac:source \"{it['source']}\" ;")
            out.append(f"    ac:source_object_id \"{it['source_object_id']}\" .")
            out.append("")
            seen_items.add(item_iri)
        for cl in it["claims"]:
            tgt = cl["target_id"].replace("-", "_")
            slice_asc = SLICE_TO_ASC.get(cl["slice"], "SliceUNKNOWN")
            cid = cl["claim_id"]
            level_short = "CO" if cl["level"] == "ControlObjective" else cl["level"]
            out.append(f"ex:claim-{cid} a ac:Claim ;")
            out.append(f"    ac:claim_id \"{cid}\" ;")
            out.append(f"    ac:disambiguation_margin {cl['disambiguation_margin']} ;")
            out.append(f"    ac:item_ref ex:{item_iri} ;")
            out.append(f"    ac:level \"{level_short}\" ;")
            out.append(f"    ac:lifted_row_ref \"{cl['lifted_row_ref']}\" ;")
            out.append(f"    ac:similarity_score {cl['similarity_score']} ;")
            out.append(f"    ac:slice ac:{slice_asc} ;")
            out.append(f"    ac:target_core_entity ac:{tgt} .")
            out.append("")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(out) + "\n")
    print(f"[emit-v7-ttl] wrote {OUT} ({sum(1 for it in items for cl in it['claims'])} claims, {len(seen_items)} items)")


if __name__ == "__main__":
    main()
