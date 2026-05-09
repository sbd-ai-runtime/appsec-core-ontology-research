"""Cosine scoring + E2 admissibility + E3 disambiguation per (slice, level).

Per Decision 0003 Amendment 1 §B PIPELINE 2 step 2.1–2.3:
  2.1 Score similarity (cosine) of source-side embedding vs ontology embeddings
      across 10 slices × 3 levels (CO / Practice / Mechanism). Slice-level
      entities (10) are excluded from the candidate pool — they are domain
      groupings, not entity-grounding targets.
  2.2 Apply E2 admissibility threshold per level.
  2.3 Apply E3 disambiguation margin per (slice, level) tuple [B.2].

Both thresholds are calibrated empirically (see calibrate_thresholds.py).
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable

import numpy as np


# Levels we ground claims at (Slice excluded — too coarse, used as domain marker).
TARGET_LEVELS = ("ControlObjective", "Practice", "Mechanism")


@dataclass(frozen=True)
class Candidate:
    score: float
    entity_iri: str
    entity_id: str
    level: str
    slice_family: str  # ACO-XXX

    def to_dict(self) -> dict:
        return {
            "score": float(self.score),
            "entity_iri": self.entity_iri,
            "entity_id": self.entity_id,
            "level": self.level,
            "slice_family": self.slice_family,
        }


@dataclass(frozen=True)
class Claim:
    target_iri: str
    target_id: str
    level: str
    slice_family: str
    similarity_score: float
    disambiguation_margin: float

    def to_dict(self) -> dict:
        return {
            "target_core_entity": self.target_iri,
            "target_id": self.target_id,
            "level": self.level,
            "slice": self.slice_family,
            "similarity_score": float(self.similarity_score),
            "disambiguation_margin": float(self.disambiguation_margin),
        }


def cosine_scores(source_embeddings: np.ndarray, ontology_embeddings: np.ndarray) -> np.ndarray:
    """Compute cosine similarity matrix.

    Both inputs assumed L2-normalized (per Archon manifest + Cartographer encoder),
    so cosine = dot product. Returns (N_source, N_ontology).
    """
    return source_embeddings @ ontology_embeddings.T


def candidates_for_row(
    sims_row: np.ndarray,
    ontology_iris: np.ndarray,
    ontology_levels: np.ndarray,
    ontology_ids: np.ndarray,
    ontology_families: np.ndarray,
    target_levels: Iterable[str] = TARGET_LEVELS,
) -> list[Candidate]:
    """Build full candidate list for one source row, restricted to target levels."""
    cands: list[Candidate] = []
    target_set = set(target_levels)
    for j in range(len(sims_row)):
        lvl = str(ontology_levels[j])
        if lvl not in target_set:
            continue
        cands.append(
            Candidate(
                score=float(sims_row[j]),
                entity_iri=str(ontology_iris[j]),
                entity_id=str(ontology_ids[j]),
                level=lvl,
                slice_family=str(ontology_families[j]),
            )
        )
    cands.sort(key=lambda c: -c.score)
    return cands


def emit_claims(
    candidates: list[Candidate],
    e2_per_level: dict[str, float],
    e3_per_level: dict[str, float],
) -> list[Claim]:
    """Apply E2 admissibility + E3 per-(slice, level) disambiguation.

    Per amendment 1 §B/§4 (B.2 ratified):
      - E2 admissibility per level: candidate.score ≥ E2(level).
      - E3 per (slice, level) tuple: candidate.score - next_best_in_same_(slice,level).score ≥ E3(level).

    Within the same (slice, level) tuple, only the top-1 can be emitted as a claim.
    Across distinct (slice, level) tuples, multiple claims are allowed for one
    source row (per amendment 1: lifted row → multiple claims permitted when
    distinct semantic targets in distinct (slice, level) pass thresholds).

    Returns: list[Claim], sorted by score descending.
    """
    # Group candidates by (slice, level)
    by_tuple: dict[tuple[str, str], list[Candidate]] = {}
    for c in candidates:
        key = (c.slice_family, c.level)
        by_tuple.setdefault(key, []).append(c)

    claims: list[Claim] = []
    for (slice_fam, level), group in by_tuple.items():
        group.sort(key=lambda c: -c.score)
        top = group[0]
        # E2: admissibility on top-1 score.
        e2 = e2_per_level.get(level)
        if e2 is None or top.score < e2:
            continue
        # E3: gap to next-best within same tuple (or against virtual zero if singleton).
        next_score = group[1].score if len(group) >= 2 else 0.0
        margin = top.score - next_score
        e3 = e3_per_level.get(level)
        if e3 is None or margin < e3:
            continue
        claims.append(
            Claim(
                target_iri=top.entity_iri,
                target_id=top.entity_id,
                level=top.level,
                slice_family=top.slice_family,
                similarity_score=top.score,
                disambiguation_margin=margin,
            )
        )
    claims.sort(key=lambda c: -c.similarity_score)
    return claims
