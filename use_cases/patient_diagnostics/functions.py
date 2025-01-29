import streamlit as st
from typing import Dict, Any, List
from datetime import datetime

# Retrieve a patient's full medical history
def get_patient_history(patient_id: str) -> Dict[str, Any]:
    patients = st.session_state.context['patients']
    if patient_id not in patients:
        return {"error": f"Patient {patient_id} not found."}
    return {
        "patient_id": patient_id,
        "medical_history": patients[patient_id].get("medical_history", []),
        "current_medications": patients[patient_id].get("current_medications", []),
        "symptoms_reported": patients[patient_id].get("symptoms_reported", [])
    }

# Record a symptom for a particular patient
def record_symptom(patient_id: str, symptom: str, severity: str) -> Dict[str, Any]:
    patients = st.session_state.context['patients']
    if patient_id not in patients:
        return {"error": f"Patient {patient_id} not found."}
    new_symptom = {
        "symptom": symptom,
        "reported_date": datetime.now().strftime("%Y-%m-%d"),
        "severity": severity
    }
    patients[patient_id].setdefault("symptoms_reported", []).append(new_symptom)
    return {
        "patient_id": patient_id,
        "symptom_recorded": True,
        "timestamp": datetime.now().isoformat()
    }

# Add a new diagnosis for a patient
def add_diagnosis(patient_id: str, diagnosis: str, date: str, treating_doctor: str) -> Dict[str, Any]:
    patients = st.session_state.context['patients']
    if patient_id not in patients:
        return {"error": f"Patient {patient_id} not found."}
    diagnosis_entry = {
        "diagnosis": diagnosis,
        "date": date,
        "treating_doctor": treating_doctor
    }
    patients[patient_id].setdefault("medical_history", []).append(diagnosis_entry)
    return {
        "patient_id": patient_id,
        "diagnosis_added": True,
        "timestamp": datetime.now().isoformat()
    }

# Compile a timeline of patient events
def compile_timeline(patient_id: str) -> Dict[str, Any]:
    patients = st.session_state.context['patients']
    lab_tests = st.session_state.context['lab_tests']
    if patient_id not in patients:
        return {"error": f"Patient {patient_id} not found."}
    history = patients[patient_id].get("medical_history", [])
    symptoms = patients[patient_id].get("symptoms_reported", [])
    patient_tests = [test for test in lab_tests if test.get("patient_id") == patient_id]
    # Combine events into a single list
    events = []
    for dx in history:
        events.append({
            "type": "diagnosis",
            "diagnosis": dx["diagnosis"],
            "date": dx["date"],
            "treating_doctor": dx["treating_doctor"]
        })
    for s in symptoms:
        events.append({
            "type": "symptom",
            "symptom": s["symptom"],
            "date": s["reported_date"],
            "severity": s["severity"]
        })
    for t in patient_tests:
        events.append({
            "type": "lab_test",
            "test_id": t["test_id"],
            "test_type": t["test_type"],
            "date": t["date_conducted"],
            "results_summary": t.get("results_summary", "")
        })
    # Sort events by date
    def date_key(e):
        return e.get("date", "9999-12-31")
    events.sort(key=date_key)
    return {
        "patient_id": patient_id,
        "timeline": events
    }

# Retrieve lab test results
def get_lab_test_results(test_id: str) -> Dict[str, Any]:
    lab_tests = st.session_state.context['lab_tests']
    test = next((t for t in lab_tests if t["test_id"] == test_id), None)
    if not test:
        return {"error": f"Lab test {test_id} not found."}
    return {
        "test_id": test_id,
        "patient_id": test.get("patient_id"),
        "test_type": test.get("test_type"),
        "date_conducted": test.get("date_conducted"),
        "results_summary": test.get("results_summary", "")
    }

# Schedule a new lab test for a patient
def schedule_lab_test(patient_id: str, test_type: str, date_conducted: str) -> Dict[str, Any]:
    patients = st.session_state.context['patients']
    if patient_id not in patients:
        return {"error": f"Patient {patient_id} not found."}
    lab_tests = st.session_state.context['lab_tests']
    new_test_id = f"LT_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    new_test = {
        "test_id": new_test_id,
        "patient_id": patient_id,
        "test_type": test_type,
        "date_conducted": date_conducted,
        "results_summary": "Pending"
    }
    lab_tests.append(new_test)
    return {
        "test_id": new_test_id,
        "scheduled": True,
        "timestamp": datetime.now().isoformat()
    }

# Send an update message to a patient
def send_patient_update(patient_id: str, message: str) -> Dict[str, Any]:
    patients = st.session_state.context['patients']
    if patient_id not in patients:
        return {"error": f"Patient {patient_id} not found."}
    return {
        "patient_id": patient_id,
        "message_sent": True,
        "message": message,
        "timestamp": datetime.now().isoformat()
    }

FUNCTION_MAPPING = {
    "get_patient_history": get_patient_history,
    "record_symptom": record_symptom,
    "add_diagnosis": add_diagnosis,
    "compile_timeline": compile_timeline,
    "get_lab_test_results": get_lab_test_results,
    "schedule_lab_test": schedule_lab_test,
    "send_patient_update": send_patient_update
}

SAMPLE_SCENARIOS = [
    "Show me the complete medical history for patient PAT001.",
    "Record that patient PAT002 has a headache with mild severity.",
    "Add an oncology diagnosis for patient PAT001 dated 2023-09-10, treated by DR1003.",
    "Build a complete timeline of events for patient PAT001.",
    "Retrieve the results of lab test LT3001.",
    "Schedule a new Blood Panel test for patient PAT002 on 2023-10-01.",
    "Send an update message to patient PAT001 regarding their recent test results."
]
