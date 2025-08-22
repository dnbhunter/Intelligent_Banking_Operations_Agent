from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AnomalyResult:
	score: float
	method: str


def zscore_to_anomaly(z: float) -> AnomalyResult:
	# Map z-score to [0,1] anomaly score via logistic-like squashing
	# Emphasize high z values while keeping smooth gradient
	s = 1.0 / (1.0 + pow(2.718281828, -0.9 * (abs(z) - 2.0)))
	return AnomalyResult(score=max(0.0, min(1.0, s)), method="zscore")


