# Augmentation format conventions — Archon → Cartographer + Orchestrator (2026-05-03)

**From:** Archon (sbd-toe-ontology, Part A in flight)
**To:** Cartographer (Phase 1a structural lifting, gated on this snippet) + Orchestrator
**Authority:** Decision 0003 Amendment 1 §F (augmentation symmetry principle, ratified 2026-05-03).
**Purpose:** before either side commits its composition rule, lock the format conventions both sides must mirror so SBERT similarity scores in PIPELINE 2 §2.1 compare structurally analogous representations.

This snippet is the binding shared contract. Five conventions, each with rationale + symmetric expectation for the source side.

---

## (1) Separator — `". "` (period + space)

- **Why:** SBERT tokenizers handle sentence boundaries cleanly and periods are well-represented in the encoder's training distribution. Avoids artificial bracket tokens (e.g., `[Practice]`, `<<slice>>`) which would create encoder distribution shift.
- **Ontology side:** fields joined with `". "`; never `"\n"`, `" - "`, `" | "`, or other markup.
- **Source side mirror:** seed text + ascending hierarchy titles joined with `". "` between segments.
- **Clarification 2 (Cartographer Phase 1a final 2026-05-03):** each fragment is **period-stripped** (trailing period(s) + whitespace removed) **before joining**, so a fragment that already ends with `.` does not produce `".. "` at the boundary. Implementation: `strip_trailing_period(s)` applied to each fragment before `". ".join(parts)`. Both sides apply this.

## (2) Label prefixes — none

- **Why:** the augmented text reads as natural prose. The entity-own name is the first token, which lets the encoder's natural lead-phrase attention bias do the level-disambiguating work. Per-level filtering at retrieval time uses the corpus record's `entity_level` field, not an in-text token.
- **Ontology side:** no `[Slice]`, `[CO]`, `[Practice]`, `[Mechanism]` prefixes. The text starts with the entity's own `name`.
- **Source side mirror:** no `[Source]`, `[Domain]`, `[Section]` prefixes either. The text starts with the source seed text. Per-level filtering on the source side, if needed, uses lifted-row metadata fields, not in-text tokens.

## (3) Snake-case enum handling — replace `_` with space, CASING PRESERVED

- **Why:** `validation_and_analysis` is not a token the encoder has seen often; `validation and analysis` is. Replacing the underscore with a space preserves natural-word boundaries and reads as natural prose.
- **Ontology side:** every snake-case enum value (e.g., `practice_family`, `mechanism_family`, `verification_posture`, `meta.scope`, `local_practice_type`) is transformed by `s.replace('_', ' ')` before concatenation.
- **Source side mirror:** any source-internal labels that arrive in snake_case (or PascalCase) get the same `_` → space transform.
- **Clarification 1 (Cartographer Phase 1a final 2026-05-03):** "casing preserved" means the rule does **NOT force lowercase**. `humanise_snake_case("Threat_Modeling") == "Threat Modeling"` (preserve casing after the replace; do not damage proper nouns like "RESTful Web Services", "PCI DSS", "OWASP", "NIST 800-53"). The ontology's snake_case enums are already lowercase, so this is a no-op on the ontology side; the rule is shared with the source side, where preserving proper-noun casing matters.

## (4) Field ordering — most specific → least specific (DESCENDING specificity)

**Convergence at most-specific-first 2026-05-03 (Cartographer Phase 1a final).** During the convention sync, Archon initially proposed most-specific-first; then revised to context-first/seed-last after considering Cartographer's natural-prose argument. Cartographer simultaneously revised to most-specific-first to mirror Archon's original proposal. Both ratified Archon's original principle in Cartographer Phase 1a final composition. Both orderings are roughly equivalent for mean-pooled SBERT; convergence chooses Archon's original.

- **Why:** entity-own surface as anchor; descending detail outward. Both sides anchor on their own specific surface and decay outward to context.
- **Ontology side:** entity-own name first → entity-own prose fields (statement / description / scope / current_goal) → derived/aggregated parent context (Mechanism's `supports_practices` aggregation) → enum qualifiers (family / type / verification_posture) at the tail.
- **Source side mirror:** seed text first, then ascending hierarchy titles in **specific-to-general** order (immediate parent before grandparent).

## (5) Truncation policy — none at corpus level; encoder enforces token cap

- **Why:** preserve the full augmented text in the corpus JSON for human inspection and any future re-encoding with a longer-context model. Let the encoder enforce its own cap.
- **Ontology side:** `augmented-text-corpus.json` records the full string; no truncation. Encoder's token cap (256 for `all-MiniLM-L6-v2`, 384 for `mpnet-base-v2`) handled inside the encode call. Mechanism's augmented text is the longest level in the ontology corpus (median ≈ 55 words ≈ 75 tokens; max ≈ 110 tokens worst-case), well under any cap.
- **Source side mirror:** record the full `contextualised_text` in the lifted-row JSONL. Encoder applies the same cap. If a source-side seed + hierarchy chain would exceed the cap, flag in the lifted-row's diagnostics — do not pre-truncate at composition time.

---

## Worked examples — both sides

### Ontology side (Archon, ratified)

**Slice (ASC-07 / ACO-IVF) — most-specific-first ordering:**
```
AppSec Core Slice Contract. input validation safe parsing and controlled failure. Consolidated contract for the seventh AppSec core slice. … Stabilize a seventh reusable AppSec domain slice on a technical semantic surface centered on input validation, safe parsing and controlled failure before opening an eighth slice or broadening secure-development semantics prematurely
```

**ControlObjective (ACO-IVF-002):**
```
Schema, Type And Allowlist Discipline. Constrain structured payloads and enumerated parameters through explicit schema, type and allowlist semantics rather than permissive parsing or blacklist-only defenses. Only explicitly accepted shapes and values are processed, and malformed structured inputs fail deterministically. schema and allowlist controls are explicit
```

**Practice (ACP-IVF-002):**
```
Schema And Allowlist Enforcement. Constrain structured payloads and accepted values through explicit schema, type and allowlist checks. validation and analysis. schema enforcement
```

**Mechanism (ACM-IVF-003) — name + aggregated supports_practices descriptions + note + family + type:**
```
Schema And Contract Validators. Validate external inputs and malformed messages at entry points before processing continues. Constrain structured payloads and accepted values through explicit schema, type and allowlist checks. Re-validate data before internal business use, persistence or downstream propagation instead of trusting it by arrival. Schema and payload-validation semantics are strong in the requirement and evidence surfaces, but are not yet cleanly materialized in the current semantic mechanism catalog. validation and analysis. schema validator
```

### Source side (Cartographer mirror — illustrative; final form is Cartographer's call)

**Lifted row from a hypothetical NIST Family / Control / Enhancement chain:**
```
<seed text of the enhancement>. <immediate parent control title>. <family title>
```

**Lifted row from a CWE entry:**
```
<CWE description>. <category title>. <view title>
```

In both cases: most-specific text first, ascending titles after, separated by `". "`, no prefixes, snake_case normalized to spaces if present.

---

## What this snippet does NOT cover

- **Embedding model + version pinning** — Archon's call (preliminary: `all-MiniLM-L6-v2` if cached locally; will document final choice + HF revision SHA + library versions in `embeddings-manifest.json`). Cartographer mirrors the model + commit + library version exactly when running the source-side embed in PIPELINE 2 §2.1.
- **Threshold values E2 (admissibility) and E3 (disambiguation margin)** — Cartographer's calibration cohort (SSDF + CIS + SAMM + CWE per Amendment 1 §A E2 calibration); not Archon's territory.
- **Source-side flattener internals** — per-source decomposers, multiplicity heuristics, hierarchy parsing (Cartographer Pipeline 1 §1.1–1.5).

---

## Acceptance for moving forward

- Cartographer reads, confirms or proposes amendment within the symmetry constraint.
- If amended, both sides re-coordinate before either commits.
- If accepted as-is, both sides commit composition rules in parallel:
  - Ontology side: `formal/appsec_core/08-embeddings/augmentation-rule.yaml` (Archon Part A).
  - Source side: per-source flattener configs + the §1.3 `contextualised_text` composition routine (Cartographer Phase 1a).

Mirror of this snippet at `/Volumes/G-DRIVE/Shared/sbd-ai-runtime/handover/em-curso/2026-05-03-archon-format-conventions-snippet.md`.
