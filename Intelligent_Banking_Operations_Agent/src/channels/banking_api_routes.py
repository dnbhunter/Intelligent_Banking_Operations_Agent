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
	return {
		"alert_score": result.alert_score,
		"decision": result.decision,
		"rationale": result.rationale,
		"policy_citations": result.policy_citations,
		"features": result.features,
		"risk_band": result.risk_band,
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


