from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel

from src.agents.fraud_triage_agent import FraudTriageAgent
from src.fraud_detection.feature_engineering import HistoricalTxn
from src.agents.credit_risk_agent import CreditRiskAgent
from src.agents.langgraph_workflow import TriageOrchestrator

router = APIRouter(tags=["banking"])


class TransactionInput(BaseModel):
	account_id: str
	amount: float
	currency: str | None = "USD"
	merchant: str | None = None
	mcc: str | None = None
	geo: str | None = None
	device_id: str | None = None
	channel: str | None = None
	timestamp: str | None = None


class ApplicationInput(BaseModel):
	applicant_id: str
	income: float
	liabilities: float
	delinquency_flags: list[str] | None = []
	requested_limit: float | None = None


@router.post("/fraud/triage")
async def fraud_triage(input_txn: TransactionInput):
	# For demo: use empty history and run the agent
	agent = FraudTriageAgent()
	result = agent.triage(
		amount=input_txn.amount,
		mcc=input_txn.mcc,
		geo=input_txn.geo,
		device_id=input_txn.device_id,
		history=[],
		now=datetime.utcnow(),
	)

	# Build human-friendly explanations and summary
	features = getattr(result, "features", {}) or {}
	explanations: list[str] = []
	if features.get("amount_zscore", 0.0) >= 3.5:
		explanations.append(f"Transaction amount is {features['amount_zscore']:.1f}σ above the account's average")
	if features.get("geo_novelty", 0.0) >= 1.0:
		explanations.append("Transaction originates from a new or high-risk geographical location")
	if features.get("device_novelty", 0.0) >= 1.0:
		explanations.append("Device ID has not been seen on this account before")
	if features.get("high_risk_mcc", 0.0) >= 1.0 and input_txn.mcc:
		explanations.append(f"Merchant Category ({input_txn.mcc}) is flagged as high-risk")
	if features.get("velocity_1h_count", 0.0) >= 5:
		explanations.append("High transaction velocity in the last 1 hour")

	# Always include rule hits (if any) to preserve transparency
	for hit in getattr(result, "rule_hits", []) or []:
		if hit not in explanations:
			explanations.append(hit)

	risk_score = round(float(getattr(result, "alert_score", 0.0)) * 100)
	risk_band = getattr(result, "risk_band", "low")
	risk_label = risk_band.capitalize()
	decision_human = "Manual review recommended" if risk_band in {"medium", "high"} else "Approve"
	summary = f"{risk_label} Risk ({risk_score}/100): {decision_human}."
	return {
		"alert_score": result.alert_score,
		"decision": result.decision,
		"rationale": result.rationale,
		"policy_citations": result.policy_citations,
		"features": features,
		"risk_band": result.risk_band,
		"explanations": explanations,
		"summary": summary,
	}


@router.post("/credit/triage")
async def credit_triage(input_app: ApplicationInput):
	agent = CreditRiskAgent()
	res = agent.triage(
		income=input_app.income,
		liabilities=input_app.liabilities,
		delinquency_flags=input_app.delinquency_flags,
		requested_limit=input_app.requested_limit,
	)
	return {
		"score": res.score,
		"decision": res.decision,
		"rationale": res.rationale,
		"policy_citations": res.policy_citations,
		"key_factors": res.key_factors,
	}


@router.get("/analytics/kpis")
async def analytics_kpis():
	return {
		"precision": None,
		"recall": None,
		"alert_volumes": 0,
		"sla_ms": None,
		"band_distribution": {"low": 0, "medium": 0, "high": 0},
	}


class TriageInput(BaseModel):
	payload: dict


@router.post("/triage")
async def unified_triage(body: TriageInput):
	orchestrator = TriageOrchestrator()
	result = orchestrator.invoke(body.payload)
	return result


