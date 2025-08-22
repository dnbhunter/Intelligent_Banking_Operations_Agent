import json
import os

import httpx
import plotly.express as px
import streamlit as st


st.set_page_config(page_title="Banking Ops Dashboard", layout="wide")
st.title("🏦 Intelligent Banking Operations Agent")

API_BASE = os.getenv("DASHBOARD_API_BASE", "http://localhost:8000/api/v1")


tab1, tab2, tab3 = st.tabs(["Fraud Triage", "Credit Triage", "Analytics"])

with tab1:
	st.subheader("Fraud Triage")
	col1, col2 = st.columns(2)
	with col1:
		amount = st.number_input("Amount", min_value=0.0, value=120.0, step=10.0)
		currency = st.text_input("Currency", value="USD")
		merchant = st.text_input("Merchant", value="Test Merchant")
		mcc = st.text_input("MCC", value="7995")
	with col2:
		geo = st.text_input("Geo", value="US-NY")
		device_id = st.text_input("Device ID", value="dev-123")
		account_id = st.text_input("Account ID", value="acct-001")
		channel = st.text_input("Channel", value="ecommerce")

	if st.button("Run Fraud Triage"):
		payload = {
			"account_id": account_id,
			"amount": amount,
			"currency": currency,
			"merchant": merchant,
			"mcc": mcc,
			"geo": geo,
			"device_id": device_id,
			"channel": channel,
		}
		with httpx.Client(timeout=10.0) as client:
			resp = client.post(f"{API_BASE}/fraud/triage", json=payload)
			data = resp.json()
		st.json(data)

with tab2:
	st.subheader("Credit Triage")
	col1, col2 = st.columns(2)
	with col1:
		income = st.number_input("Monthly Income", min_value=0.0, value=4000.0, step=100.0)
		liabilities = st.number_input("Monthly Liabilities", min_value=0.0, value=1200.0, step=50.0)
	with col2:
		delinquency_flags = st.multiselect("Delinquency Flags", ["late_payment_30d", "late_payment_60d", "charged_off"])
		requested_limit = st.number_input("Requested Limit", min_value=0.0, value=1500.0, step=100.0)

	if st.button("Run Credit Triage"):
		payload = {
			"applicant_id": "app-001",
			"income": income,
			"liabilities": liabilities,
			"delinquency_flags": delinquency_flags,
			"requested_limit": requested_limit,
		}
		with httpx.Client(timeout=10.0) as client:
			resp = client.post(f"{API_BASE}/credit/triage", json=payload)
			data = resp.json()
		st.json(data)

with tab3:
	st.subheader("Analytics KPIs")
	with httpx.Client(timeout=10.0) as client:
		resp = client.get(f"{API_BASE}/analytics/kpis")
		kpis = resp.json()
	st.json(kpis)


