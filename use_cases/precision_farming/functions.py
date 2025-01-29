# functions.py for Crop Analysis
import streamlit as st
from typing import Dict, Any, List
from datetime import datetime


def get_field_info(field_id: str) -> Dict[str, Any]:
    """
    Retrieves high-level field information including plan and monthly charges.
    """
    fields = st.session_state.context['fields']
    if field_id not in fields:
        return {"error": f"Field ID {field_id} not found."}
    field = fields[field_id]
    return {
        "field_id": field_id,
        "farmer_name": field["farmer_name"],
        "analysis_plan": field["analysis_plan"],
        "monthly_charge": field["monthly_charge"],
        "months_with_service": field["months_with_service"],
        "analysis_score": field.get("analysis_score", 0)
    }


def get_soil_quality(field_id: str) -> Dict[str, Any]:
    """
    Fetches soil quality metrics for a particular field.
    """
    fields = st.session_state.context['fields']
    if field_id not in fields:
        return {"error": f"Field ID {field_id} not found."}
    soil_data = fields[field_id].get("soil_quality", {})
    return {
        "field_id": field_id,
        "pH": soil_data.get("pH", 0),
        "moisture": soil_data.get("moisture", 0),
        "N": soil_data.get("N", 0),
        "P": soil_data.get("P", 0),
        "K": soil_data.get("K", 0)
    }


def update_field_info(field_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Updates the field's information such as plan or analysis score.
    """
    fields = st.session_state.context['fields']
    if field_id not in fields:
        return {"error": f"Field ID {field_id} not found."}
    for key, value in updates.items():
        fields[field_id][key] = value
    return {
        "field_id": field_id,
        "updated_fields": updates,
        "timestamp": datetime.now().isoformat()
    }


def fetch_high_risk_fields() -> List[Dict[str, Any]]:
    """
    Fetches a list of fields that have high analysis score based on the global threshold.
    """
    fields = st.session_state.context['fields']
    threshold = st.session_state.context['analysis_model'].get('analysis_threshold', 0.7)
    results = []
    for fid, data in fields.items():
        score = data.get('analysis_score', 0)
        if score >= threshold:
            results.append({
                "field_id": fid,
                "analysis_score": score
            })
    return results


def predict_analysis_score(field_id: str) -> Dict[str, Any]:
    """
    Runs the analysis model on a specific field to calculate a fresh analysis score.
    """
    fields = st.session_state.context['fields']
    if field_id not in fields:
        return {"error": f"Field ID {field_id} not found."}

    # Placeholder heuristic for demonstration
    soil = fields[field_id].get("soil_quality", {})
    crop_health = fields[field_id].get("crop_health", {})
    moisture_factor = soil.get("moisture", 0) / 10.0
    disease_factor = crop_health.get("disease_incidents", 0) * 0.1

    base_score = moisture_factor + disease_factor
    # Clip at 1.0 for demonstration
    analysis_score = min(base_score, 1.0)
    fields[field_id]["analysis_score"] = analysis_score

    return {
        "field_id": field_id,
        "analysis_score": analysis_score,
        "timestamp": datetime.now().isoformat()
    }


def propose_recommendation(field_id: str) -> Dict[str, Any]:
    """
    Suggests a recommendation or action for a high-analysis-score field.
    """
    fields = st.session_state.context['fields']
    recommendations = st.session_state.context['recommendations']

    if field_id not in fields:
        return {"error": f"Field ID {field_id} not found."}

    analysis_score = fields[field_id].get("analysis_score", 0)
    eligible_recs = []

    for rec in recommendations:
        if "analysis_score>0.8" in rec["eligibility_criteria"] and analysis_score > 0.8:
            eligible_recs.append(rec)
        elif "analysis_score>0.5" in rec["eligibility_criteria"] and analysis_score > 0.5:
            eligible_recs.append(rec)

    if not eligible_recs:
        return {
            "field_id": field_id,
            "suggested_recommendations": [],
            "message": "No special recommendations at this time."
        }

    return {
        "field_id": field_id,
        "suggested_recommendations": eligible_recs,
        "message": "Recommendations suggested based on analysis score."
    }


def apply_recommendation(field_id: str, recommendation_id: str) -> Dict[str, Any]:
    """
    Applies a specific recommendation to a field.
    """
    fields = st.session_state.context['fields']
    recommendations = st.session_state.context['recommendations']

    if field_id not in fields:
        return {"error": f"Field ID {field_id} not found."}

    rec = next((r for r in recommendations if r['recommendation_id'] == recommendation_id), None)
    if not rec:
        return {"error": f"Recommendation {recommendation_id} not found."}

    fields[field_id]["active_recommendation"] = recommendation_id

    return {
        "field_id": field_id,
        "recommendation_id": recommendation_id,
        "status": "Recommendation applied",
        "timestamp": datetime.now().isoformat()
    }


def check_support_resources() -> Dict[str, Any]:
    """
    Checks availability of retention resources (agents, field visit slots).
    """
    resources = st.session_state.context['support_resources']
    return {
        "available_agents": resources["available_agents"],
        "field_visit_slots": resources["field_visit_slots"],
        "timestamp": datetime.now().isoformat()
    }


def schedule_field_visit(field_id: str, visit_type: str) -> Dict[str, Any]:
    """
    Schedules a field visit.
    """
    fields = st.session_state.context['fields']
    resources = st.session_state.context['support_resources']

    if field_id not in fields:
        return {"error": f"Field ID {field_id} not found."}

    if visit_type == "emergency" and resources["available_agents"] <= 0:
        return {"error": "No available agents for emergency visits."}

    # Decrement resources if it's an emergency visit
    if visit_type == "emergency":
        resources["available_agents"] -= 1
    else:
        resources["field_visit_slots"] -= 1

    return {
        "field_id": field_id,
        "visit_type": visit_type,
        "status": "Visit scheduled",
        "timestamp": datetime.now().isoformat()
    }


def generate_field_survey(field_id: str) -> Dict[str, Any]:
    """
    Generates a simple survey for the field owner.
    """
    fields = st.session_state.context['fields']
    if field_id not in fields:
        return {"error": f"Field ID {field_id} not found."}

    survey_questions = [
        "How satisfied are you with our monitoring services?",
        "Have you noticed improvements in crop health?",
        "Any additional feedback to improve our services?"
    ]

    return {
        "field_id": field_id,
        "survey_questions": survey_questions,
        "timestamp": datetime.now().isoformat()
    }


def gather_survey_results(field_id: str, survey_responses: Dict[str, Any]) -> Dict[str, Any]:
    """
    Processes the survey responses and updates the field record.
    """
    fields = st.session_state.context['fields']
    if field_id not in fields:
        return {"error": f"Field ID {field_id} not found."}

    fields[field_id]["survey_responses"] = survey_responses

    return {
        "field_id": field_id,
        "status": "Survey results recorded",
        "timestamp": datetime.now().isoformat()
    }

FUNCTION_MAPPING = {
    'get_field_info': get_field_info,
    'get_soil_quality': get_soil_quality,
    'update_field_info': update_field_info,
    'fetch_high_risk_fields': fetch_high_risk_fields,
    'predict_analysis_score': predict_analysis_score,
    'propose_recommendation': propose_recommendation,
    'apply_recommendation': apply_recommendation,
    'check_support_resources': check_support_resources,
    'schedule_field_visit': schedule_field_visit,
    'generate_field_survey': generate_field_survey,
    'gather_survey_results': gather_survey_results
}

SAMPLE_SCENARIOS = [
    "An agronomist wants to identify fields with an analysis_score above 0.7 and apply nitrogen fertilizer if suitable.",
    "The farmer for FIELD002 requests an upgrade from 'Basic Soil Monitoring' to 'Soil & Weather Monitoring,' and we want to recalculate analysis_score."
    ]
