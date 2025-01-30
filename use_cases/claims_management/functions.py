# functions.py - Implementation for suspicious-claim detection use case
import streamlit as st
from typing import Dict, Any, List, Optional
from datetime import datetime


def fetch_claim_details(claim_id: str) -> Dict[str, Any]:
    """
    Fetches all details related to a given claim.
    """
    claims = st.session_state.context['claims']
    claim = next((c for c in claims if c['claim_id'] == claim_id), None)
    if not claim:
        return {"error": f"Claim {claim_id} not found."}
    return {"claim": claim}


def get_policyholder_info(policyholder_id: Optional[str] = None, policyholder_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieves policyholder details using either ID or name.
    """
    policyholders = st.session_state.context['policyholders']

    # If an ID is provided, look it up.
    if policyholder_id:
        if policyholder_id not in policyholders:
            return {"error": f"Policyholder ID {policyholder_id} not found."}
        return {"policyholder_id": policyholder_id, "info": policyholders[policyholder_id]}

    # Otherwise, if a name is provided, search for a matching record.
    if policyholder_name:
        for pid, data in policyholders.items():
            if data.get('name') == policyholder_name:
                return {"policyholder_id": pid, "info": data}
        return {"error": f"No policyholder found with name {policyholder_name}."}

    return {"error": "No policyholder_id or policyholder_name provided."}


def parse_claim_narrative(claim_id: str) -> Dict[str, Any]:
    """
    Uses advanced LLM logic to parse the claim description and identify suspicious keywords.
    """
    claims = st.session_state.context['claims']
    analysis_rules = st.session_state.context['analysis_rules']
    claim = next((c for c in claims if c['claim_id'] == claim_id), None)

    if not claim:
        return {"error": f"Claim {claim_id} not found."}

    description = claim.get('description', "")
    words = description.lower().split()
    suspicious_flags = []

    # Check if claim amount exceeds threshold.
    if claim.get('claim_amount', 0) > analysis_rules['threshold_amount']:
        suspicious_flags.append({
            "flag_type": "HighAmount",
            "flag_description": "Claim amount exceeds threshold."})

    # Check if claim type is in high-risk.
    if claim.get('claim_type') in analysis_rules['high_risk_claim_types']:
        suspicious_flags.append({
            "flag_type": "HighRiskType",
            "flag_description": f"Claim type {claim['claim_type']} is high-risk."})

    # Check suspicious keywords.
    for kw in analysis_rules['sentiment_keywords']:
        if kw.lower() in words:
            suspicious_flags.append({
                "flag_type": "KeywordMatch",
                "flag_description": f"Suspicious keyword '{kw}' found in narrative."})

    return {"claim_id": claim_id, "suspicious_flags": suspicious_flags}


def run_ml_fraud_scoring(claim_id: str) -> Dict[str, Any]:
    """
    Runs the claim data and suspicious flags through a simple fraud model to produce a fraud score.
    """
    claims = st.session_state.context['claims']
    ml_model = st.session_state.context['ml_fraud_model']
    suspicions = st.session_state.context['suspicions']

    claim = next((c for c in claims if c['claim_id'] == claim_id), None)
    if not claim:
        return {"error": f"Claim {claim_id} not found."}

    # Retrieve any suspicious flags that may have been computed.
    suspicious_record = next((s for s in suspicions if s['claim_id'] == claim_id), None)
    suspicious_flags_count = len(suspicious_record['suspicious_flags']) if suspicious_record else 0

    # Simple scoring: 0.4 * (amount / threshold_amount) + 0.3 * (risky type) + 0.3 * (# of suspicious flags)
    # For demonstration only.
    raw_score = 0.0

    # Factor in claim amount
    raw_score += 0.4 * (claim.get('claim_amount', 0) / (ml_model['features'].count('claim_amount') * 10000))

    # Factor in claim type risk
    if 'claim_type' in ml_model['features']:
        if claim.get('claim_type', "") in st.session_state.context['analysis_rules']['high_risk_claim_types']:
            raw_score += 0.3

    # Factor in suspicious flags
    if 'suspicious_flags_count' in ml_model['features']:
        raw_score += 0.3 * suspicious_flags_count

    fraud_score = round(min(raw_score, 1.0), 2)
    is_fraudulent = True if fraud_score >= ml_model['fraud_threshold'] else False

    return {
        "claim_id": claim_id,
        "fraud_score": fraud_score,
        "is_fraudulent": is_fraudulent
    }


def flag_claim_for_investigation(claim_id: str, reason: str) -> Dict[str, Any]:
    """
    Flags a claim for manual review.
    """
    claims = st.session_state.context['claims']
    claim = next((c for c in claims if c['claim_id'] == claim_id), None)

    if not claim:
        return {"error": f"Claim {claim_id} not found."}

    claim['status'] = "Under Investigation"
    return {
        "claim_id": claim_id,
        "flagged": True,
        "reason": reason,
        "timestamp": datetime.now().isoformat()
    }


def update_claim_status(claim_id: str, new_status: str) -> Dict[str, Any]:
    """
    Updates the status of a claim.
    """
    claims = st.session_state.context['claims']
    claim = next((c for c in claims if c['claim_id'] == claim_id), None)

    if not claim:
        return {"error": f"Claim {claim_id} not found."}

    claim['status'] = new_status
    return {
        "claim_id": claim_id,
        "new_status": new_status,
        "timestamp": datetime.now().isoformat()
    }

FUNCTION_MAPPING = {
    'fetch_claim_details': fetch_claim_details,
    'get_policyholder_info': get_policyholder_info,
    'parse_claim_narrative': parse_claim_narrative,
    'run_ml_fraud_scoring': run_ml_fraud_scoring,
    'flag_claim_for_investigation': flag_claim_for_investigation,
    'update_claim_status': update_claim_status
}

SAMPLE_SCENARIOS= ["Determine if CLAIM001 has any suspicious elements in the narrative. If so, generate suspicious flags and evaluate if it should be sent for further ML fraud scoring.",
    "Retrieve policyholder information for ID POLICY002 to understand their claims history and verify if they have been flagged before.",
    "Run the ML fraud model on CLAIM002 and if the fraud score exceeds the threshold, flag it for manual investigation."
  ]