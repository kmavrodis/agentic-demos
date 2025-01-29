# functions.py for Churn Prediction in Telecom
import streamlit as st
from typing import Dict, Any, List
from datetime import datetime


def get_customer_info(customer_id: str) -> Dict[str, Any]:
    """
    Retrieves high-level customer information including plan and monthly charges.
    """
    customers = st.session_state.context['customers']
    if customer_id not in customers:
        return {"error": f"Customer ID {customer_id} not found."}
    customer = customers[customer_id]
    return {
        "customer_id": customer_id,
        "name": customer["name"],
        "plan": customer["plan"],
        "monthly_charge": customer["monthly_charge"],
        "months_with_company": customer["months_with_company"],
        "churn_score": customer.get("churn_score", 0)
    }


def get_customer_usage(customer_id: str) -> Dict[str, Any]:
    """
    Fetches usage statistics for a particular customer (minutes, data usage, etc.).
    """
    customers = st.session_state.context['customers']
    if customer_id not in customers:
        return {"error": f"Customer ID {customer_id} not found."}
    usage = customers[customer_id].get("usage", {})
    return {
        "customer_id": customer_id,
        "minutes_used": usage.get("minutes_used", 0),
        "data_gb_used": usage.get("data_gb_used", 0)
    }


def update_customer_info(customer_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Updates the customer's information such as plan or churn score.
    """
    customers = st.session_state.context['customers']
    if customer_id not in customers:
        return {"error": f"Customer ID {customer_id} not found."}
    for key, value in updates.items():
        customers[customer_id][key] = value
    return {
        "customer_id": customer_id,
        "updated_fields": updates,
        "timestamp": datetime.now().isoformat()
    }


def fetch_risky_customers() -> List[Dict[str, Any]]:
    """
    Fetches a list of customers who have high churn scores based on the global threshold.
    """
    customers = st.session_state.context['customers']
    threshold = st.session_state.context['churn_model'].get('churn_threshold', 0.7)
    results = []
    for cid, data in customers.items():
        score = data.get('churn_score', 0)
        if score >= threshold:
            results.append({
                "customer_id": cid,
                "churn_score": score
            })
    return results


def predict_churn(customer_id: str) -> Dict[str, Any]:
    """
    Runs the churn model on a specific customer to calculate a fresh churn score.
    In this demo, we'll just simulate a nominal churn score update.
    """
    customers = st.session_state.context['customers']
    if customer_id not in customers:
        return {"error": f"Customer ID {customer_id} not found."}

    # Placeholder logic: simple heuristic combining usage and support calls.
    usage = customers[customer_id].get("usage", {})
    support_calls = customers[customer_id].get("support_calls", 0)
    base_score = (usage.get("data_gb_used", 0) / 10.0) + (support_calls * 0.05)

    # Clip at 1.0 for demonstration, or can apply sophisticated model.
    churn_score = min(base_score, 1.0)
    customers[customer_id]["churn_score"] = churn_score

    return {
        "customer_id": customer_id,
        "churn_score": churn_score,
        "timestamp": datetime.now().isoformat()
    }


def propose_retention_action(customer_id: str) -> Dict[str, Any]:
    """
    Suggests a retention offer or action for a high-churn-risk customer.
    """
    customers = st.session_state.context['customers']
    retention_offers = st.session_state.context['retention_offers']

    if customer_id not in customers:
        return {"error": f"Customer ID {customer_id} not found."}

    churn_score = customers[customer_id].get("churn_score", 0)
    eligible_offers = []

    for offer in retention_offers:
        # parse the eligibility_criteria in a basic way
        if "churn_score>0.8" in offer["eligibility_criteria"] and churn_score > 0.8:
            eligible_offers.append(offer)
        elif "churn_score>0.5" in offer["eligibility_criteria"] and churn_score > 0.5:
            eligible_offers.append(offer)

    if not eligible_offers:
        return {
            "customer_id": customer_id,
            "suggested_offers": [],
            "message": "No special offers suggested at this time."
        }

    return {
        "customer_id": customer_id,
        "suggested_offers": eligible_offers,
        "message": "Retention offers suggested based on churn score."
    }


def apply_retention_offer(customer_id: str, offer_id: str) -> Dict[str, Any]:
    """
    Applies a specific retention offer to a customer's account.
    """
    customers = st.session_state.context['customers']
    retention_offers = st.session_state.context['retention_offers']

    if customer_id not in customers:
        return {"error": f"Customer ID {customer_id} not found."}

    offer = next((o for o in retention_offers if o['offer_id'] == offer_id), None)
    if not offer:
        return {"error": f"Offer {offer_id} not found."}

    # For demonstration purposes, just record it.
    customers[customer_id]["active_offer"] = offer_id

    return {
        "customer_id": customer_id,
        "offer_id": offer_id,
        "status": "Offer applied",
        "timestamp": datetime.now().isoformat()
    }


def check_retention_resources() -> Dict[str, Any]:
    """
    Checks availability of retention resources (support agents, callback slots).
    """
    resources = st.session_state.context['support_resources']
    return {
        "available_agents": resources["available_agents"],
        "callback_slots": resources["callback_slots"],
        "timestamp": datetime.now().isoformat()
    }


def schedule_follow_up(customer_id: str, follow_up_type: str) -> Dict[str, Any]:
    """
    Schedules a follow-up call or message.
    """
    customers = st.session_state.context['customers']
    resources = st.session_state.context['support_resources']

    if customer_id not in customers:
        return {"error": f"Customer ID {customer_id} not found."}
    if resources["available_agents"] <= 0 and follow_up_type == "phone":
        return {"error": "No available agents for phone follow-ups."}

    # Decrement resources if it's a phone call.
    if follow_up_type == "phone":
        resources["available_agents"] -= 1
    else:
        resources["callback_slots"] -= 1

    return {
        "customer_id": customer_id,
        "follow_up_type": follow_up_type,
        "status": "Follow-up scheduled",
        "timestamp": datetime.now().isoformat()
    }


def generate_customer_survey(customer_id: str) -> Dict[str, Any]:
    """
    Generates a simple survey for the customer.
    """
    customers = st.session_state.context['customers']
    if customer_id not in customers:
        return {"error": f"Customer ID {customer_id} not found."}

    # Just a sample survey.
    survey_questions = [
        "How satisfied are you with our service?",
        "Would you recommend us to a friend?",
        "Any feedback to improve our service?"
    ]

    return {
        "customer_id": customer_id,
        "survey_questions": survey_questions,
        "timestamp": datetime.now().isoformat()
    }


def gather_survey_results(customer_id: str, survey_responses: Dict[str, Any]) -> Dict[str, Any]:
    """
    Processes the survey responses and updates the customer's record.
    """
    customers = st.session_state.context['customers']
    if customer_id not in customers:
        return {"error": f"Customer ID {customer_id} not found."}

    # Store the responses.
    customers[customer_id]["survey_responses"] = survey_responses

    return {
        "customer_id": customer_id,
        "status": "Survey results recorded",
        "timestamp": datetime.now().isoformat()
    }

# The final function to indicate instructions complete

FUNCTION_MAPPING = {
    'get_customer_info': get_customer_info,
    'get_customer_usage': get_customer_usage,
    'update_customer_info': update_customer_info,
    'fetch_risky_customers': fetch_risky_customers,
    'predict_churn': predict_churn,
    'propose_retention_action': propose_retention_action,
    'apply_retention_offer': apply_retention_offer,
    'check_retention_resources': check_retention_resources,
    'schedule_follow_up': schedule_follow_up,
    'generate_customer_survey': generate_customer_survey,
    'gather_survey_results': gather_survey_results
}


SAMPLE_SCENARIOS = ["A marketing manager wants to quickly find customers whose churn score exceeds a certain threshold and automatically generate appropriate retention offers for them.",
                    "Customer CUST1002 calls i order to switch from the “Standard Plan” to the “Premium Data Plan.” The company wants to update their record and recalculate the churn score to see if the risk has changed.", 
                    "An agent identifies that high-risk customers are eligible for a free device upgrade (Offer ID: OFF1002). The agent wants to apply this offer to the customers accounts."]