from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from time import perf_counter

from src.fraud_detection.feature_engineering import HistoricalTxn, build_features
from src.fraud_detection.rule_engine import evaluate_rules
from src.fraud_detection.anomaly_detector import choose_anomaly_score
from src.fraud_detection.fraud_config import get_config


@dataclass
class FraudTriageOutput:
	alert_score: float
	decision: str
	rationale: str
	policy_citations: list[str]
	features: dict[str, Any]
	risk_band: str
	rule_hits: list[str]


class FraudTriageAgent:
	"""Fraud triage combining explainable rules and anomaly scoring.

	This is a minimal, deterministic version without LLM rationales yet.
	"""

	def triage(self, *, amount: float, mcc: str | None, geo: str | None, device_id: str | None, history: list[HistoricalTxn], now: datetime | None = None) -> FraudTriageOutput:
		now = now or datetime.utcnow()
		started = perf_counter()
		features = build_features(amount, now, mcc, geo, device_id, history)
		rule_score, rule_hits = evaluate_rules(features)

		cfg = get_config()
		anom = choose_anomaly_score(features, preferred_method=cfg.anomaly_method)
		anomaly_score = float(anom.score)
		alert_score = max(0.0, min(1.0, 0.6 * rule_score + 0.4 * anomaly_score))

		if alert_score >= cfg.thresholds.high_band_threshold:
			decision = "alert-high"
			risk_band = "high"
		elif alert_score >= cfg.thresholds.medium_band_threshold:
			decision = "alert-medium"
			risk_band = "medium"
		else:
			decision = "allow"
			risk_band = "low"

		reasons = ", ".join(rule_hits) if rule_hits else "no significant rule triggers"
		rationale = f"Combined rules and anomaly analysis; reasons: {reasons}."
		_ = perf_counter() - started  # latency available to caller via API, not stored here
		return FraudTriageOutput(
			alert_score=alert_score,
			decision=decision,
			rationale=rationale,
			policy_citations=[],
			features=features,
			risk_band=risk_band,
			rule_hits=rule_hits,
		)


