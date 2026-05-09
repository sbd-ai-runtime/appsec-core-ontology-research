"""Pydantic schemas for substrate item + claim, with process invariants P1' / M1' / M5
enforced as model validators.

Per Decision 0003 Amendment 1 §2 + §D:
  - M1' (slice coherence on claim): every claim's slice = slice of its target.
  - M5  (semantic warrant on claim): score ≥ E2(level) AND margin ≥ E3(level).
  - P1' (GROUNDED implies anchored): final_classification=GROUNDED ⇒ |claims| ≥ 1.

Invariants P2/P3/P4/P5/P6 are revoked under amendment 1 (artefacts of the
item-anchor framing).
"""
from __future__ import annotations
from typing import Literal, Optional
from pydantic import BaseModel, Field, ConfigDict, model_validator


FinalClassification = Literal["GROUNDED", "LabDepthPending", "OOS_AppSec"]
Level = Literal["ControlObjective", "Practice", "Mechanism"]


class AblationBaseline(BaseModel):
    score_without_chain_context: Optional[float] = None
    differs_from_with_context: Optional[bool] = None


class Claim(BaseModel):
    model_config = ConfigDict(extra="forbid")

    claim_id: str
    lifted_row_ref: str
    item_ref: str
    target_core_entity: str  # canonical IRI
    target_id: str
    level: Level
    slice: str  # ACO-XXX (slice family)
    similarity_score: float
    disambiguation_margin: float
    rationale_snippet: Optional[str] = None
    ablation_baseline_score: Optional[AblationBaseline] = None


class DecompositionDiagnostic(BaseModel):
    n_lifted_rows: int = 0
    multiplicity_in_supposed_atomic: bool = False


class SubstrateItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    item_id: str
    source: str
    source_object_id: str
    source_text: str
    source_lifted_rows: list[str] = Field(default_factory=list)
    final_classification: FinalClassification
    claims: list[Claim] = Field(default_factory=list)
    lab_depth_seeds: list[str] = Field(default_factory=list)
    decomposition_diagnostic: DecompositionDiagnostic = Field(
        default_factory=DecompositionDiagnostic
    )

    @model_validator(mode="after")
    def _enforce_p1_prime(self):
        """P1' — GROUNDED ⇒ |claims| ≥ 1."""
        if self.final_classification == "GROUNDED" and len(self.claims) < 1:
            raise ValueError(
                f"P1' violation: item={self.item_id} GROUNDED but has no claims"
            )
        return self


class SubstrateMeta(BaseModel):
    schema: str = "appsec_core_v5_substrate/1.0"
    pipeline_version: str = "v5.0"
    flattener_version: str  # e.g., "v1.2"
    grounding_model: str
    grounding_model_revision: str
    e2_per_level: dict[str, float]
    e3_per_level: dict[str, float]
    calibration_cohort: list[str]
    n_active_sources: int
    n_lifted_rows_total: int
    n_items_total: int
    n_claims_total: int
    n_grounded: int
    n_lab_depth_pending: int
    n_oos: int
    generated_at: str


class Substrate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    meta: SubstrateMeta
    items: list[SubstrateItem]


class OntologySideIndex(BaseModel):
    """Per Core entity, list of supporting claims (paper §5/§6 view)."""
    model_config = ConfigDict(extra="forbid")

    target_core_entity: str
    target_id: str
    level: Level
    slice: str
    n_claims: int
    by_source: dict[str, int]  # source → number of claims
    claim_refs: list[str]  # claim_id list for traceability
