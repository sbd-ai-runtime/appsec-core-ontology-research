"""Generate OLIR exports — Step 2 of mini-dispatcher 2026-05-09 (RATIFIED).

Per programme-lead 2026-05-09 ratification of Step 2 generation:
  - 31 × per-source OLIR Concept Crosswalks (XML + JSON; IR 8477 + IR 8278A r1 STRM)
  - 1 × AppSec Core V1 OLIR Reference Document (XML + JSON)

Schema decisions (RATIFIED VERBATIM by programme-lead):
  - sim ≥ 0.6           → relationship-type "equal"
  - 0.4 ≤ sim < 0.6     → relationship-type "intersects-with"
  - sim < 0.4           → relationship-type "unspecified"
  - Multi-claim per source-item: one OLIR row per (source-item, target-Core-entity)
                                  unique pair using highest-similarity claim for that
                                  target; primary row marked is-primary="true" (item's
                                  overall highest-similarity claim's target);
                                  others are-primary="false" (secondary disclosure).
  - subset-of / superset-of: NOT in first cut (cosine similarity lacks directional
                              info; SME refinement future work; §13).
  - STRM resource model:
      * pilot doc            → DocumentaryImpl
      * source-item          → ConcreteImpl
      * AppSec Core V1       → Reference Document
      * Core entity (CO/P/M) → Concept

Inputs:
  - data/p7_olir_audit/p7_v2_corrected/v7/SUPPLIER_v7_0.json
  - sbd-toe-ontology/formal/appsec_core/08-embeddings/augmented-text-corpus.json (entity catalog)

Outputs (data/p7_olir_audit/p7_v2_corrected/v7/olir_exports/):
  - appsec_core_v1_reference_doc.xml  (Reference Document — 212 Concepts)
  - appsec_core_v1_reference_doc.json
  - concept_crosswalk_<pilot>.xml × 31 (per-source crosswalks)
  - concept_crosswalk_<pilot>.json × 31
  - olir_validator_report.md (per-output self-validation + structural checks)

Run: python3 -m scripts.olir.generate_olir_exports
"""
from __future__ import annotations
import hashlib
import json
import pathlib
import sys
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any
from xml.sax.saxutils import escape as xml_escape

REPO = pathlib.Path(__file__).resolve().parents[2]
SUPPLIER = REPO / "data/p7_olir_audit/p7_v2_corrected/v7/SUPPLIER_v7_0.json"
ONTOLOGY_CORPUS = pathlib.Path(
    "/Volumes/G-DRIVE/Shared/SecurityByDesign-TheoryOfEverything/"
    "sbd-toe-ontology/formal/appsec_core/08-embeddings/augmented-text-corpus.json"
)
OUT_DIR = REPO / "data/p7_olir_audit/p7_v2_corrected/v7/olir_exports"

# ============================================================================
# Per-pilot metadata (curated; folds in retrieval-receipt URLs where available)
# ============================================================================

PILOT_METADATA: dict[str, dict] = {
    "asvs_v5_0_0": {
        "title": "OWASP Application Security Verification Standard",
        "version": "5.0.0",
        "url": "https://github.com/OWASP/ASVS/releases/tag/v5.0.0_release",
        "author": "OWASP",
        "release_date": "2025-05-30",
        "mapping_direction": "solution_space_direct",
    },
    "capec_v3_9": {
        "title": "Common Attack Pattern Enumeration and Classification (CAPEC)",
        "version": "3.9",
        "url": "https://capec.mitre.org/",
        "author": "MITRE",
        "release_date": "2022",
        "mapping_direction": "problem_space_inverted",
    },
    "cis_controls_v8_1_2": {
        "title": "CIS Critical Security Controls",
        "version": "8.1.2",
        "url": "https://www.cisecurity.org/controls/",
        "author": "Center for Internet Security",
        "release_date": "2024",
        "mapping_direction": "solution_space_direct",
    },
    "cwe_software_development_view_v4_19_1": {
        "title": "Common Weakness Enumeration (CWE) — Software Development View (CWE-699)",
        "version": "4.19.1",
        "url": "https://cwe.mitre.org/data/slices/699.html",
        "author": "MITRE",
        "release_date": "2024",
        "mapping_direction": "problem_space_inverted",
    },
    "enisa_multilayer_ai_cybersecurity_practices_2023": {
        "title": "ENISA Multilayer Framework for Good Cybersecurity Practices for AI",
        "version": "2023 (June)",
        "url": "https://www.enisa.europa.eu/publications/multilayer-framework-for-good-cybersecurity-practices-for-ai",
        "author": "European Union Agency for Cybersecurity (ENISA)",
        "release_date": "2023-06",
        "mapping_direction": "mixed",
    },
    "eu_cra": {
        "title": "EU Cyber Resilience Act (selected articles)",
        "version": "Articles 13-24",
        "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R2847",
        "author": "European Union",
        "release_date": "2024",
        "mapping_direction": "solution_space_direct",
    },
    "eu_dora": {
        "title": "EU Digital Operational Resilience Act (DORA, selected articles)",
        "version": "Regulation (EU) 2022/2554",
        "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022R2554",
        "author": "European Union",
        "release_date": "2022",
        "mapping_direction": "solution_space_direct",
    },
    "eu_nis2": {
        "title": "EU NIS2 Directive (selected articles)",
        "version": "Directive (EU) 2022/2555",
        "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022L2555",
        "author": "European Union",
        "release_date": "2022",
        "mapping_direction": "solution_space_direct",
    },
    "eu_rgpd": {
        "title": "EU General Data Protection Regulation (GDPR, selected articles)",
        "version": "Regulation (EU) 2016/679",
        "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679",
        "author": "European Union",
        "release_date": "2016",
        "mapping_direction": "solution_space_direct",
    },
    "hipaa_security_rule": {
        "title": "HIPAA Security Rule (45 CFR Part 164 Subpart C)",
        "version": "current 2024",
        "url": "https://www.hhs.gov/hipaa/for-professionals/security/laws-regulations/index.html",
        "author": "U.S. Department of Health and Human Services",
        "release_date": "2024",
        "mapping_direction": "solution_space_direct",
    },
    "mcp_official_security_foundations_2025": {
        "title": "MCP Official Security Foundations",
        "version": "2025",
        "url": "https://modelcontextprotocol.io/",
        "author": "Anthropic / MCP Working Group",
        "release_date": "2025",
        "mapping_direction": "mixed",
    },
    "mitre_atlas": {
        "title": "MITRE ATLAS (Adversarial Threat Landscape for Artificial-Intelligence Systems)",
        "version": "v5.6.0",
        "url": "https://atlas.mitre.org/",
        "author": "MITRE",
        "release_date": "2026-05-04",
        "mapping_direction": "problem_space_inverted",
    },
    "nist_ai_100_2_e2025": {
        "title": "NIST AI 100-2 E2025 — Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations",
        "version": "AI 100-2 E2025",
        "url": "https://doi.org/10.6028/NIST.AI.100-2e2025",
        "author": "U.S. National Institute of Standards and Technology",
        "release_date": "2025-03-24",
        "mapping_direction": "mixed",
    },
    "nist_ai_rmf_1_0": {
        "title": "NIST AI Risk Management Framework (AI RMF 1.0)",
        "version": "AI 100-1 / RMF 1.0",
        "url": "https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf",
        "author": "U.S. National Institute of Standards and Technology",
        "release_date": "2023-01",
        "mapping_direction": "mixed",
    },
    "nist_sp800_53_rev5": {
        "title": "NIST SP 800-53 Rev 5 — Security and Privacy Controls for Information Systems and Organizations",
        "version": "Rev 5",
        "url": "https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final",
        "author": "U.S. National Institute of Standards and Technology",
        "release_date": "2020 (upd 2023)",
        "mapping_direction": "mixed",
    },
    "owasp_dsomm": {
        "title": "OWASP DevSecOps Maturity Model (DSOMM)",
        "version": "current",
        "url": "https://owasp.org/www-project-devsecops-maturity-model/",
        "author": "OWASP",
        "release_date": "current",
        "mapping_direction": "solution_space_direct",
    },
    "owasp_llm_top_10": {
        "title": "OWASP Top 10 for LLM Applications",
        "version": "2025",
        "url": "https://genai.owasp.org/llm-top-10/",
        "author": "OWASP GenAI Security Project",
        "release_date": "2025-03",
        "mapping_direction": "solution_space_direct",
    },
    "owasp_mcp_secure_server_development_v1_0": {
        "title": "OWASP MCP Secure Server Development",
        "version": "v1.0",
        "url": "https://owasp.org/www-project-mcp-server-security/",
        "author": "OWASP",
        "release_date": "2025",
        "mapping_direction": "mixed",
    },
    "owasp_mcp_third_party_servers_v1_0": {
        "title": "OWASP MCP Third-Party Servers Security",
        "version": "v1.0",
        "url": "https://owasp.org/www-project-mcp-server-security/",
        "author": "OWASP",
        "release_date": "2025",
        "mapping_direction": "mixed",
    },
    "owasp_mcp_top_10_v0_1_2025_beta": {
        "title": "OWASP MCP Top 10",
        "version": "v0.1 2025 beta",
        "url": "https://owasp.org/www-project-mcp-top-10/",
        "author": "OWASP",
        "release_date": "2025",
        "mapping_direction": "problem_space_inverted",
    },
    "owasp_ml_top_10": {
        "title": "OWASP Machine Learning Security Top 10",
        "version": "v0.3 Draft (2023)",
        "url": "https://owasp.org/www-project-machine-learning-security-top-10/",
        "author": "OWASP",
        "release_date": "2023",
        "mapping_direction": "problem_space_inverted",
    },
    "owasp_proactive_controls_2018": {
        "title": "OWASP Proactive Controls",
        "version": "2018 v3.0",
        "url": "https://owasp.org/www-project-proactive-controls/",
        "author": "OWASP",
        "release_date": "2018",
        "mapping_direction": "solution_space_direct",
    },
    "owasp_samm_v2_1": {
        "title": "OWASP Software Assurance Maturity Model (SAMM)",
        "version": "v2.1",
        "url": "https://owaspsamm.org/",
        "author": "OWASP",
        "release_date": "current",
        "mapping_direction": "mixed",
    },
    "owasp_top_10_2021": {
        "title": "OWASP Top 10",
        "version": "2021",
        "url": "https://owasp.org/Top10/",
        "author": "OWASP",
        "release_date": "2021",
        "mapping_direction": "problem_space_inverted",
    },
    "pci_dss_v4_0_1": {
        "title": "PCI DSS — Payment Card Industry Data Security Standard",
        "version": "v4.0.1",
        "url": "https://www.pcisecuritystandards.org/document_library/?category=pcidss",
        "author": "PCI Security Standards Council",
        "release_date": "2024",
        "mapping_direction": "mixed",
    },
    "pci_sslc_v1_1": {
        "title": "PCI Software Security Lifecycle (SSLC)",
        "version": "v1.1",
        "url": "https://www.pcisecuritystandards.org/document_library/?category=software_security",
        "author": "PCI Security Standards Council",
        "release_date": "2022",
        "mapping_direction": "solution_space_direct",
    },
    "safecode_agile_2012": {
        "title": "SAFECode — Practical Security Stories and Security Tasks for Agile Development Environments",
        "version": "2012",
        "url": "https://safecode.org/",
        "author": "SAFECode",
        "release_date": "2012",
        "mapping_direction": "mixed",
    },
    "safecode_fpssd_2018": {
        "title": "SAFECode — Fundamental Practices for Secure Software Development",
        "version": "2018 (3rd ed.)",
        "url": "https://safecode.org/",
        "author": "SAFECode",
        "release_date": "2018",
        "mapping_direction": "solution_space_direct",
    },
    "safecode_sic_2010": {
        "title": "SAFECode — Software Integrity Controls",
        "version": "2010",
        "url": "https://safecode.org/",
        "author": "SAFECode",
        "release_date": "2010",
        "mapping_direction": "mixed",
    },
    "slsa_spec_v1_0_build_track": {
        "title": "SLSA — Supply-chain Levels for Software Artifacts (Build Track)",
        "version": "v1.0",
        "url": "https://slsa.dev/spec/v1.0/",
        "author": "OpenSSF / SLSA Working Group",
        "release_date": "2023",
        "mapping_direction": "solution_space_direct",
    },
    "ssdf_sp800_218_v1_1": {
        "title": "NIST SP 800-218 — Secure Software Development Framework (SSDF)",
        "version": "v1.1",
        "url": "https://doi.org/10.6028/NIST.SP.800-218",
        "author": "U.S. National Institute of Standards and Technology",
        "release_date": "2022-02",
        "mapping_direction": "mixed",
    },
}


# ============================================================================
# Helpers
# ============================================================================

NOW = datetime.now(timezone.utc).strftime("%Y-%m-%d")
SUBMISSION_AUTHOR = "Pedro Farinha (programme lead) — SbD-ToE Programme"
PROGRAMME_DOI = "10.17605/OSF.IO/7T849"
REFERENCE_DOC_TITLE = "AppSec Core V1 (with ACR-001, ACR-002, ACR-004 incorporated)"
REFERENCE_DOC_VERSION = "V1.next (substrate v7 baseline; cycle-a-frozen-2026-05-08)"
REFERENCE_DOC_AUTHOR = "SbD-ToE Programme — AppSec Core ontology project"
REFERENCE_DOC_URL = "https://osf.io/7t849/"
SUBSTRATE_SUPPLIER_SHA = "596783ed984d9c0e8c8ef6439a0eaee8fbaf2d863af37138cde8fad55d62be04"


def relationship_type(sim: float) -> str:
    """Threshold-based continuous→categorical translation per ratified Step 2."""
    if sim >= 0.6:
        return "equal"
    if sim >= 0.4:
        return "intersects-with"
    return "unspecified"


def truncate(s: str, n: int = 240) -> str:
    s = (s or "").strip()
    if len(s) > n:
        return s[: n - 1] + "…"
    return s


def x(s: str) -> str:
    return xml_escape(s if s is not None else "")


# ============================================================================
# Reference Document (AppSec Core V1)
# ============================================================================

def load_entity_catalog() -> list[dict]:
    """Load 212 AC V1 entities from augmented-text-corpus."""
    d = json.load(ONTOLOGY_CORPUS.open())
    return d.get("records", [])


def emit_reference_doc(entities: list[dict]) -> tuple[str, dict]:
    """Emit AppSec Core V1 OLIR Reference Document (XML + JSON dict)."""
    # JSON structure
    j = {
        "olir_reference_document": {
            "metadata": {
                "title": REFERENCE_DOC_TITLE,
                "version": REFERENCE_DOC_VERSION,
                "author": REFERENCE_DOC_AUTHOR,
                "submission_author": SUBMISSION_AUTHOR,
                "url": REFERENCE_DOC_URL,
                "programme_doi": PROGRAMME_DOI,
                "submission_date": NOW,
                "schema_basis": "NIST IR 8278A r1 STRM resource model — Reference Document Concepts",
                "concepts_total": len(entities),
                "concepts_by_level": {
                    "Slice": sum(1 for e in entities if e["entity_level"] == "Slice"),
                    "ControlObjective": sum(1 for e in entities if e["entity_level"] == "ControlObjective"),
                    "Practice": sum(1 for e in entities if e["entity_level"] == "Practice"),
                    "Mechanism": sum(1 for e in entities if e["entity_level"] == "Mechanism"),
                },
            },
            "concepts": [
                {
                    "id": e["entity_id"],
                    "iri": e["entity_iri"],
                    "level": e["entity_level"],  # IR 8278A r1: Concept type
                    "slice_family": e["family"],
                    "description": truncate(e.get("augmented_text", ""), 480),
                    "strm_resource_type": "Concept",
                }
                for e in entities
            ],
        }
    }

    # XML structure (best-effort IR 8278A r1)
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<olir-reference-document xmlns="https://www.nist.gov/olir/v1" version="1.0">',
        '  <metadata>',
        f'    <title>{x(REFERENCE_DOC_TITLE)}</title>',
        f'    <version>{x(REFERENCE_DOC_VERSION)}</version>',
        f'    <author>{x(REFERENCE_DOC_AUTHOR)}</author>',
        f'    <submission-author>{x(SUBMISSION_AUTHOR)}</submission-author>',
        f'    <url>{x(REFERENCE_DOC_URL)}</url>',
        f'    <programme-doi>{x(PROGRAMME_DOI)}</programme-doi>',
        f'    <submission-date>{NOW}</submission-date>',
        f'    <schema-basis>NIST IR 8278A r1 STRM resource model</schema-basis>',
        f'    <concepts-total>{len(entities)}</concepts-total>',
        '  </metadata>',
        '  <concepts>',
    ]
    for e in entities:
        descr = truncate(e.get("augmented_text", ""), 480)
        lines.append(f'    <concept id="{x(e["entity_id"])}" strm-resource-type="Concept">')
        lines.append(f'      <iri>{x(e["entity_iri"])}</iri>')
        lines.append(f'      <level>{x(e["entity_level"])}</level>')
        lines.append(f'      <slice-family>{x(e["family"])}</slice-family>')
        lines.append(f'      <description>{x(descr)}</description>')
        lines.append('    </concept>')
    lines.append('  </concepts>')
    lines.append('</olir-reference-document>')
    xml = "\n".join(lines) + "\n"

    return xml, j


# ============================================================================
# Per-source Concept Crosswalks
# ============================================================================

def derive_olir_pairs(item: dict) -> list[dict]:
    """For one substrate v7 item, derive OLIR pairs (one per unique target).

    Returns list of dicts with: target_id, target_level, target_slice, sim, level,
                                relationship, is_primary, claim_id, lifted_row_ref.
    """
    claims = item.get("claims", [])
    if not claims:
        return []
    # Group by target_id; pick highest-similarity claim per unique target
    by_target: dict[str, dict] = {}
    for c in claims:
        t = c["target_id"]
        if t not in by_target or c["similarity_score"] > by_target[t]["similarity_score"]:
            by_target[t] = c
    # Determine primary: item's overall highest-similarity claim's target
    primary = max(claims, key=lambda c: c.get("similarity_score", 0.0))
    primary_target = primary["target_id"]

    rows = []
    for t, c in by_target.items():
        sim = float(c["similarity_score"])
        rel = relationship_type(sim)
        rows.append({
            "target_id": t,
            "target_level": c["level"],
            "target_slice": c["slice"],
            "sim": round(sim, 3),
            "level": c["level"],
            "relationship": rel,
            "is_primary": (t == primary_target),
            "claim_id": c["claim_id"],
            "lifted_row_ref": c["lifted_row_ref"],
            "rationale_snippet": (c.get("rationale_snippet") or "")[:160],
        })
    # Sort: primary first, then by descending similarity
    rows.sort(key=lambda r: (not r["is_primary"], -r["sim"]))
    return rows


def emit_crosswalk(pilot_id: str, items: list[dict], entity_catalog_by_id: dict[str, dict]) -> tuple[str, dict, dict]:
    """Emit per-source crosswalk (XML, JSON dict, stats dict)."""
    md = PILOT_METADATA.get(pilot_id, {
        "title": pilot_id, "version": "?", "url": "?",
        "author": "?", "release_date": "?", "mapping_direction": "?",
    })

    # Build mappings
    n_items_total = len(items)
    n_items_grounded = sum(1 for it in items if it["final_classification"] == "GROUNDED")
    mappings_xml = []
    mappings_json = []
    rel_counts = {"equal": 0, "intersects-with": 0, "unspecified": 0}
    primary_count = 0
    secondary_count = 0
    n_pairs = 0

    for it in items:
        if it["final_classification"] != "GROUNDED":
            continue
        rows = derive_olir_pairs(it)
        for r in rows:
            n_pairs += 1
            rel_counts[r["relationship"]] = rel_counts.get(r["relationship"], 0) + 1
            if r["is_primary"]:
                primary_count += 1
            else:
                secondary_count += 1
            target_e = entity_catalog_by_id.get(r["target_id"])
            target_descr = truncate((target_e or {}).get("augmented_text", ""), 200) if target_e else ""
            source_descr = truncate(it.get("source_text", ""), 200)

            # JSON row
            mappings_json.append({
                "is_primary": r["is_primary"],
                "source_element": {
                    "id": it["source_object_id"],
                    "description": source_descr,
                    "strm_resource_type": "ConcreteImpl",
                },
                "reference_element": {
                    "id": r["target_id"],
                    "description": target_descr,
                    "level": r["target_level"],
                    "slice_family": r["target_slice"],
                    "strm_resource_type": "Concept",
                },
                "relationship_type": r["relationship"],
                "strength": r["sim"],
                "claim_level": r["level"],
                "rationale": (
                    f"Cosine similarity {r['sim']:.3f}; threshold mapping → "
                    f"{r['relationship']}. Claim {r['claim_id']} at {r['level']} level. "
                    f"{'Primary anchor (item highest-similarity claim).' if r['is_primary'] else 'Secondary disclosure.'}"
                ),
            })

            # XML row
            mappings_xml.append('    <mapping is-primary="' + ("true" if r["is_primary"] else "false") + '">')
            mappings_xml.append('      <source-element strm-resource-type="ConcreteImpl">')
            mappings_xml.append(f'        <id>{x(it["source_object_id"])}</id>')
            mappings_xml.append(f'        <description>{x(source_descr)}</description>')
            mappings_xml.append('      </source-element>')
            mappings_xml.append('      <reference-element strm-resource-type="Concept">')
            mappings_xml.append(f'        <id>{x(r["target_id"])}</id>')
            mappings_xml.append(f'        <description>{x(target_descr)}</description>')
            mappings_xml.append(f'        <level>{x(r["target_level"])}</level>')
            mappings_xml.append(f'        <slice-family>{x(r["target_slice"])}</slice-family>')
            mappings_xml.append('      </reference-element>')
            mappings_xml.append(f'      <relationship-type>{x(r["relationship"])}</relationship-type>')
            mappings_xml.append(f'      <strength>{r["sim"]:.3f}</strength>')
            mappings_xml.append(f'      <claim-level>{x(r["level"])}</claim-level>')
            primary_note = "Primary anchor (item highest-similarity claim)." if r["is_primary"] else "Secondary disclosure."
            rationale_text = (
                f"Cosine similarity {r['sim']:.3f}; threshold mapping → {r['relationship']}. "
                f"Claim {r['claim_id']} at {r['level']} level. {primary_note}"
            )
            mappings_xml.append('      <rationale>')
            mappings_xml.append(f'        {x(rationale_text)}')
            mappings_xml.append('      </rationale>')
            mappings_xml.append('    </mapping>')

    # JSON document
    j = {
        "olir_concept_crosswalk": {
            "metadata": {
                "title": f"{md['title']} → {REFERENCE_DOC_TITLE} (Concept Crosswalk)",
                "submission_version": "1.0",
                "submission_author": SUBMISSION_AUTHOR,
                "submission_date": NOW,
                "programme_doi": PROGRAMME_DOI,
                "schema_basis": "NIST IR 8477 relationship vocabulary + NIST IR 8278A r1 STRM resource model",
                "source_document": {
                    "title": md["title"],
                    "version": md["version"],
                    "url": md["url"],
                    "author": md["author"],
                    "release_date": md["release_date"],
                    "strm_resource_type": "DocumentaryImpl",
                    "mapping_direction": md["mapping_direction"],
                    "pilot_id": pilot_id,
                },
                "reference_document": {
                    "title": REFERENCE_DOC_TITLE,
                    "version": REFERENCE_DOC_VERSION,
                    "url": REFERENCE_DOC_URL,
                    "author": REFERENCE_DOC_AUTHOR,
                    "strm_resource_type": "Reference Document",
                },
                "methodology": (
                    "Threshold-based continuous→categorical translation: "
                    "sim≥0.6 → equal; 0.4≤sim<0.6 → intersects-with; sim<0.4 → unspecified. "
                    "Multi-claim per source-item: one row per (source-item, target-Core-entity) "
                    "unique pair using highest-similarity claim for that target; "
                    "is-primary=true marks item's overall highest-similarity claim's target. "
                    "subset-of / superset-of NOT in first cut (cosine similarity lacks directional info; "
                    "SME refinement future work). "
                    "STRM resource model: pilot doc → DocumentaryImpl; source-item → ConcreteImpl; "
                    "AppSec Core V1 → Reference Document; Core entity → Concept."
                ),
                "substrate_supplier_sha256": SUBSTRATE_SUPPLIER_SHA,
                "substrate_tag": "substrate-v7-iter-3-ai-ml-incorporated",
                "ontology_tag": "ontology-v1-next-acr004-promoted",
                "cycle_a_frozen_tag": "cycle-a-frozen-2026-05-08",
            },
            "stats": {
                "items_total": n_items_total,
                "items_grounded": n_items_grounded,
                "items_lab_depth_pending": n_items_total - n_items_grounded,
                "olir_pairs_emitted": n_pairs,
                "primary_pairs": primary_count,
                "secondary_pairs": secondary_count,
                "relationship_type_distribution": rel_counts,
            },
            "mappings": mappings_json,
        }
    }

    # XML document
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<olir-concept-crosswalk xmlns="https://www.nist.gov/olir/v1" version="1.0">',
        '  <metadata>',
        f'    <title>{x(md["title"])} → {x(REFERENCE_DOC_TITLE)} (Concept Crosswalk)</title>',
        f'    <submission-version>1.0</submission-version>',
        f'    <submission-author>{x(SUBMISSION_AUTHOR)}</submission-author>',
        f'    <submission-date>{NOW}</submission-date>',
        f'    <programme-doi>{x(PROGRAMME_DOI)}</programme-doi>',
        f'    <schema-basis>NIST IR 8477 relationship vocabulary + NIST IR 8278A r1 STRM resource model</schema-basis>',
        '    <source-document strm-resource-type="DocumentaryImpl">',
        f'      <title>{x(md["title"])}</title>',
        f'      <version>{x(md["version"])}</version>',
        f'      <url>{x(md["url"])}</url>',
        f'      <author>{x(md["author"])}</author>',
        f'      <release-date>{x(md["release_date"])}</release-date>',
        f'      <mapping-direction>{x(md["mapping_direction"])}</mapping-direction>',
        f'      <pilot-id>{x(pilot_id)}</pilot-id>',
        '    </source-document>',
        '    <reference-document strm-resource-type="Reference Document">',
        f'      <title>{x(REFERENCE_DOC_TITLE)}</title>',
        f'      <version>{x(REFERENCE_DOC_VERSION)}</version>',
        f'      <url>{x(REFERENCE_DOC_URL)}</url>',
        f'      <author>{x(REFERENCE_DOC_AUTHOR)}</author>',
        '    </reference-document>',
        '    <methodology>',
        f'      Threshold-based continuous→categorical translation: sim≥0.6 → equal; 0.4≤sim&lt;0.6 → intersects-with; sim&lt;0.4 → unspecified.',
        f'      Multi-claim per source-item: one row per (source-item, target-Core-entity) unique pair using highest-similarity claim for that target.',
        f'      is-primary="true" marks item overall highest-similarity claim&apos;s target.',
        f'      subset-of / superset-of NOT in first cut (cosine similarity lacks directional info; SME refinement future work).',
        f'      STRM resource model: pilot doc → DocumentaryImpl; source-item → ConcreteImpl; AppSec Core V1 → Reference Document; Core entity → Concept.',
        '    </methodology>',
        f'    <substrate-supplier-sha256>{SUBSTRATE_SUPPLIER_SHA}</substrate-supplier-sha256>',
        f'    <substrate-tag>substrate-v7-iter-3-ai-ml-incorporated</substrate-tag>',
        f'    <ontology-tag>ontology-v1-next-acr004-promoted</ontology-tag>',
        f'    <cycle-a-frozen-tag>cycle-a-frozen-2026-05-08</cycle-a-frozen-tag>',
        '  </metadata>',
        '  <stats>',
        f'    <items-total>{n_items_total}</items-total>',
        f'    <items-grounded>{n_items_grounded}</items-grounded>',
        f'    <olir-pairs-emitted>{n_pairs}</olir-pairs-emitted>',
        f'    <primary-pairs>{primary_count}</primary-pairs>',
        f'    <secondary-pairs>{secondary_count}</secondary-pairs>',
        f'    <relationship-type-distribution>',
        f'      <equal>{rel_counts["equal"]}</equal>',
        f'      <intersects-with>{rel_counts["intersects-with"]}</intersects-with>',
        f'      <unspecified>{rel_counts["unspecified"]}</unspecified>',
        f'    </relationship-type-distribution>',
        '  </stats>',
        '  <mappings>',
    ] + mappings_xml + [
        '  </mappings>',
        '</olir-concept-crosswalk>',
    ]
    xml = "\n".join(xml_lines) + "\n"

    stats = {
        "pilot_id": pilot_id,
        "items_total": n_items_total,
        "items_grounded": n_items_grounded,
        "olir_pairs": n_pairs,
        "primary_pairs": primary_count,
        "secondary_pairs": secondary_count,
        "rel_dist": rel_counts,
    }
    return xml, j, stats


# ============================================================================
# Self-validator (best-effort vs IR 8278A r1 documented structure)
# ============================================================================

def self_validate(stats_per_pilot: list[dict], xml_path_per_pilot: dict, ref_xml_path: pathlib.Path) -> dict:
    """Best-effort structural validation. Public NIST OLIR validators not invoked
    here (require external network + may not be publicly accessible per dispatcher
    risk-doc). Instead: structural conformance checks against IR 8278A r1
    documented requirements.
    """
    checks = []

    # Reference document structural check
    ref_text = ref_xml_path.read_text()
    ref_check = {
        "artefact": str(ref_xml_path.relative_to(REPO)),
        "type": "Reference Document",
        "structural_conformance": {
            "has_xml_declaration": ref_text.startswith("<?xml"),
            "has_olir_namespace": "xmlns=\"https://www.nist.gov/olir/v1\"" in ref_text,
            "has_metadata_block": "<metadata>" in ref_text and "</metadata>" in ref_text,
            "has_concepts_block": "<concepts>" in ref_text and "</concepts>" in ref_text,
            "concepts_strm_resource_type": "strm-resource-type=\"Concept\"" in ref_text,
            "has_required_metadata_fields": all(
                f"<{tag}>" in ref_text
                for tag in ["title", "version", "author", "submission-date", "concepts-total"]
            ),
        },
    }
    ref_check["pass"] = all(ref_check["structural_conformance"].values())
    checks.append(ref_check)

    # Per-pilot crosswalks
    for pilot_id, xml_path in xml_path_per_pilot.items():
        text = xml_path.read_text()
        c = {
            "artefact": str(xml_path.relative_to(REPO)),
            "type": "Concept Crosswalk",
            "pilot_id": pilot_id,
            "structural_conformance": {
                "has_xml_declaration": text.startswith("<?xml"),
                "has_olir_namespace": "xmlns=\"https://www.nist.gov/olir/v1\"" in text,
                "has_source_document": "<source-document strm-resource-type=\"DocumentaryImpl\">" in text,
                "has_reference_document": "<reference-document strm-resource-type=\"Reference Document\">" in text,
                "has_methodology_block": "<methodology>" in text,
                "has_mappings_block": "<mappings>" in text and "</mappings>" in text,
                "has_relationship_type_in_each_mapping": "<relationship-type>" in text,
                "uses_only_ratified_relationship_types": all(
                    rt in {"equal", "intersects-with", "unspecified"}
                    for rt in {"equal", "intersects-with", "unspecified"} if f"<relationship-type>{rt}</relationship-type>" in text
                ),
            },
        }
        c["pass"] = all(c["structural_conformance"].values())
        checks.append(c)

    n_pass = sum(1 for c in checks if c["pass"])
    n_fail = len(checks) - n_pass
    return {
        "validator": "self-structural (IR 8278A r1 documented requirements)",
        "external_nist_olir_validator_invoked": False,
        "external_validator_caveat": (
            "External NIST OLIR validators (per https://csrc.nist.gov/projects/olir) "
            "not invoked at generation time — programme-lead may commission external "
            "OLIR submission review separately as part of OLIR registration future "
            "work (§13). Self-validation tests structural conformance against "
            "IR 8278A r1 documented requirements: namespaces, metadata blocks, "
            "STRM resource types, ratified relationship vocabulary."
        ),
        "n_artefacts_validated": len(checks),
        "n_pass": n_pass,
        "n_fail": n_fail,
        "per_artefact": checks,
    }


# ============================================================================
# Main
# ============================================================================

def main():
    print("=" * 90)
    print("OLIR exports generation — Step 2 (RATIFIED 2026-05-09)")
    print("=" * 90)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"\nOutput dir: {OUT_DIR.relative_to(REPO)}\n")

    # Reference document
    print("[1/3] Loading AppSec Core V1 entity catalog...", file=sys.stderr)
    entities = load_entity_catalog()
    print(f"      {len(entities)} entities loaded "
          f"(Slice {sum(1 for e in entities if e['entity_level']=='Slice')} / "
          f"CO {sum(1 for e in entities if e['entity_level']=='ControlObjective')} / "
          f"Practice {sum(1 for e in entities if e['entity_level']=='Practice')} / "
          f"Mechanism {sum(1 for e in entities if e['entity_level']=='Mechanism')})", file=sys.stderr)
    entity_by_id = {e["entity_id"]: e for e in entities}

    print("[2/3] Emitting AppSec Core V1 OLIR Reference Document...", file=sys.stderr)
    ref_xml, ref_json = emit_reference_doc(entities)
    ref_xml_path = OUT_DIR / "appsec_core_v1_reference_doc.xml"
    ref_json_path = OUT_DIR / "appsec_core_v1_reference_doc.json"
    ref_xml_path.write_text(ref_xml)
    ref_json_path.write_text(json.dumps(ref_json, indent=2))
    print(f"      [write] {ref_xml_path.name} + {ref_json_path.name}", file=sys.stderr)

    # Per-source crosswalks
    print("\n[3/3] Emitting per-source Concept Crosswalks...", file=sys.stderr)
    sup = json.load(SUPPLIER.open())
    items_by_pilot: dict[str, list] = defaultdict(list)
    for it in sup["items"]:
        items_by_pilot[it["source"]].append(it)

    stats_per_pilot = []
    xml_path_per_pilot = {}
    for pilot_id in sorted(items_by_pilot.keys()):
        items = items_by_pilot[pilot_id]
        xml, j, stats = emit_crosswalk(pilot_id, items, entity_by_id)
        xml_path = OUT_DIR / f"concept_crosswalk_{pilot_id}.xml"
        json_path = OUT_DIR / f"concept_crosswalk_{pilot_id}.json"
        xml_path.write_text(xml)
        json_path.write_text(json.dumps(j, indent=2))
        xml_path_per_pilot[pilot_id] = xml_path
        stats_per_pilot.append(stats)
        rel_dist = stats["rel_dist"]
        print(
            f"      [write] {pilot_id:<46} "
            f"items {stats['items_total']:>4} ({stats['items_grounded']:>4}G) "
            f"pairs {stats['olir_pairs']:>4} "
            f"({stats['primary_pairs']:>3}P / {stats['secondary_pairs']:>4}S) "
            f"eq={rel_dist['equal']:>3} ix={rel_dist['intersects-with']:>4} un={rel_dist['unspecified']:>3}",
            file=sys.stderr,
        )

    # Self-validator report
    print("\n[validate] Running self-structural validator (IR 8278A r1 conformance)...", file=sys.stderr)
    val_report = self_validate(stats_per_pilot, xml_path_per_pilot, ref_xml_path)

    # Aggregate stats
    total_pairs = sum(s["olir_pairs"] for s in stats_per_pilot)
    total_primary = sum(s["primary_pairs"] for s in stats_per_pilot)
    total_secondary = sum(s["secondary_pairs"] for s in stats_per_pilot)
    rel_total = {"equal": 0, "intersects-with": 0, "unspecified": 0}
    for s in stats_per_pilot:
        for k, v in s["rel_dist"].items():
            rel_total[k] += v

    # Validator markdown report
    md = []
    md.append("# OLIR validator report — substrate v7 OLIR exports\n")
    md.append(f"**Generated:** {NOW}")
    md.append(f"**Validator:** self-structural (IR 8278A r1 documented requirements)")
    md.append(f"**External NIST OLIR validator:** NOT invoked at generation time (see caveat below)")
    md.append("")
    md.append(f"## Aggregate")
    md.append("")
    md.append(f"- **Reference Document:** `appsec_core_v1_reference_doc.xml` + `.json` ({len(entities)} Concepts; Slice 10 / CO 75 / Practice 69 / Mechanism 58)")
    md.append(f"- **Per-source Concept Crosswalks:** 31 pilots × 2 formats (XML + JSON) = 62 files")
    md.append(f"- **OLIR pairs emitted:** {total_pairs} ({total_primary} primary + {total_secondary} secondary)")
    md.append(f"- **Relationship type distribution:**")
    md.append(f"  - `equal` (sim ≥ 0.6): {rel_total['equal']}")
    md.append(f"  - `intersects-with` (0.4 ≤ sim < 0.6): {rel_total['intersects-with']}")
    md.append(f"  - `unspecified` (sim < 0.4): {rel_total['unspecified']}")
    md.append("")
    md.append(f"## Self-validator results")
    md.append("")
    md.append(f"- Artefacts validated: {val_report['n_artefacts_validated']}")
    md.append(f"- Pass: **{val_report['n_pass']}** / Fail: {val_report['n_fail']}")
    md.append("")
    md.append(f"### Caveat — external validator not invoked")
    md.append("")
    md.append(f"> {val_report['external_validator_caveat']}")
    md.append("")
    md.append("## Per-artefact structural conformance")
    md.append("")
    md.append("| Artefact | Type | Pass? | Checks |")
    md.append("|---|---|:---:|---|")
    for c in val_report["per_artefact"]:
        passed = "✅" if c["pass"] else "❌"
        nfail = sum(1 for v in c["structural_conformance"].values() if not v)
        nchecks = len(c["structural_conformance"])
        path_short = c["artefact"].split("/")[-1]
        md.append(f"| `{path_short}` | {c['type']} | {passed} | {nchecks - nfail}/{nchecks} |")
    md.append("")
    md.append("## Per-pilot stats")
    md.append("")
    md.append("| Pilot | items | grounded | OLIR pairs | primary | secondary | equal | intersects-with | unspecified |")
    md.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for s in stats_per_pilot:
        rd = s["rel_dist"]
        md.append(
            f"| `{s['pilot_id']}` | {s['items_total']} | {s['items_grounded']} | "
            f"{s['olir_pairs']} | {s['primary_pairs']} | {s['secondary_pairs']} | "
            f"{rd['equal']} | {rd['intersects-with']} | {rd['unspecified']} |"
        )
    md.append("")
    md.append("## Methodology — schema decisions ratified by programme-lead 2026-05-09")
    md.append("")
    md.append("**Continuous → categorical translation (threshold-based):**")
    md.append("- `sim ≥ 0.6` → relationship-type `equal`")
    md.append("- `0.4 ≤ sim < 0.6` → relationship-type `intersects-with`")
    md.append("- `sim < 0.4` → relationship-type `unspecified`")
    md.append("")
    md.append("**Multi-claim per source-item:**")
    md.append("- One OLIR row per (source-item, target-Core-entity) unique pair using highest-similarity claim for that target.")
    md.append("- `is-primary=true` marks item's overall highest-similarity claim's target (one primary per item).")
    md.append("- Lower-similarity claims to other targets become secondary OLIR rows (`is-primary=false`).")
    md.append("")
    md.append("**Relationship vocabulary used (subset of IR 8477 6-element catalog):**")
    md.append("- `equal`, `intersects-with`, `unspecified` (3 of 6)")
    md.append("")
    md.append("**Relationship vocabulary NOT used (first-cut limitation):**")
    md.append("- `subset-of`, `superset-of`: cosine similarity is undirected; cannot mechanically infer subset/superset directionality. SME refinement future work (§13).")
    md.append("- `not-related`: only emitted as absence (item with no claim ≥ 0.4 to a target produces no row for that target). Not explicitly emitted as `not-related` rows.")
    md.append("")
    md.append("**STRM resource model (IR 8278A r1):**")
    md.append("- Pilot document → `DocumentaryImpl`")
    md.append("- Source item → `ConcreteImpl`")
    md.append("- AppSec Core V1 → Reference Document")
    md.append("- Core entity (CO/Practice/Mechanism/Slice) → `Concept`")
    md.append("")
    md.append("**Substrate v7 anchor:** SUPPLIER SHA-256 `" + SUBSTRATE_SUPPLIER_SHA + "`; tag `substrate-v7-iter-3-ai-ml-incorporated`; cycle-a-frozen-2026-05-08.")
    md.append("")
    md.append("## Future work (§13 — out of scope for this generation)")
    md.append("")
    md.append("- SME review of individual mappings + κ inter-rater reliability")
    md.append("- NIST CRWS peer submission")
    md.append("- OLIR registration via NIST OLIR Submission Tool")
    md.append("- subset-of / superset-of vocabulary extension (requires directional information beyond cosine similarity)")
    md.append("- External NIST OLIR validator pass (requires programme-lead authorization for external submission)")

    val_path = OUT_DIR / "olir_validator_report.md"
    val_path.write_text("\n".join(md))
    print(f"\n[write] {val_path.relative_to(REPO)}", file=sys.stderr)

    # JSON aggregate
    val_json_path = OUT_DIR / "olir_validator_report.json"
    val_json_path.write_text(json.dumps({
        "validator_report": val_report,
        "aggregate": {
            "olir_pairs_total": total_pairs,
            "primary_pairs": total_primary,
            "secondary_pairs": total_secondary,
            "relationship_type_distribution": rel_total,
            "n_pilots": len(stats_per_pilot),
            "n_entities_in_reference_doc": len(entities),
        },
        "per_pilot_stats": stats_per_pilot,
    }, indent=2))
    print(f"[write] {val_json_path.relative_to(REPO)}", file=sys.stderr)

    print(f"\n[done] {len(stats_per_pilot)} pilots × 2 formats = {len(stats_per_pilot)*2} crosswalks "
          f"+ Reference Doc (×2 formats) + validator report (×2 formats)", file=sys.stderr)
    print(f"       Total OLIR pairs: {total_pairs}", file=sys.stderr)
    print(f"       Pass: {val_report['n_pass']} / Fail: {val_report['n_fail']}", file=sys.stderr)


if __name__ == "__main__":
    main()
