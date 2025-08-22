from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.credit_risk.affordability_calculator import compute_dti
from src.credit_risk.scorecard import calculate_scorecard
from src.credit_risk.policy_engine import apply_minimums

@dataclass
class CreditTriageOutput:
	score: float
	decision: str
	rationale: str
	policy_citations: list[str]
	key_factors: list[str]


class CreditRiskAgent:
	"""Simple scorecard-like credit triage.

	This is a minimal placeholder; full logic will be in credit_risk modules.
	"""

	def triage(self, *, income: float, liabilities: float, delinquency_flags: list[str] | None, requested_limit: float | None) -> CreditTriageOutput:
		dti = compute_dti(income, liabilities)
		delinquencies = len(delinquency_flags or [])
		requested_limit_ratio = (requested_limit / income) if (requested_limit and income > 0) else None
		sc = calculate_scorecard(dti=dti, delinquencies=delinquencies, requested_limit_ratio=requested_limit_ratio)
		policy = apply_minimums(score=sc.score, dti=dti)
		decision = "approve" if sc.score >= 0.75 else ("review" if sc.score >= 0.5 else "decline")
		if policy.override and decision == "approve":
			decision = "review"
		rationale = "Scorecard banding with affordability; policy gating applied."
		key_factors = sc.contributors or ["no adverse factors"]
		if policy.override and policy.reason:
			key_factors.append(policy.reason)
		return CreditTriageOutput(
			score=sc.score,
			decision=decision,
			rationale=rationale,
			policy_citations=[],
			key_factors=key_factors,
		)


