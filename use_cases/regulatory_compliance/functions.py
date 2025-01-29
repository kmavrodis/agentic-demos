import streamlit as st
from typing import Dict, Any, List, Optional
from datetime import datetime

# The following functions manage mortgage applications, income checks, 
# property valuations, fraud detection, and AML compliance.


def check_credit_risk(application_id: str) -> Dict[str, Any]:
    """
    Evaluates the mortgage applicant's credit risk by analyzing their credit score.
    Returns a risk rating such as "LOW", "MEDIUM", or "HIGH".
    """
    data = st.session_state.context
    apps = data['mortgage_applications']

    application = next((app for app in apps if app['application_id'] == application_id), None)
    if not application:
        return {"error": f"Application {application_id} not found.", "success": False}

    credit_score = application.get('credit_score', 0)
    if credit_score >= 750:
        risk = "LOW"
    elif credit_score >= 650:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    return {
        "application_id": application_id,
        "credit_score": credit_score,
        "risk": risk,
        "success": True
    }


def assess_income_stability(customer_identifier: str) -> Dict[str, Any]:
    """
    Compares customer's reported income with tax records to assess consistency.
    Accepts either a customer ID (e.g., "CUST101") or a customer's name.
    """
    data = st.session_state.context
    customers = data['customers']

    # Attempt to find by ID or by name
    found_customer = None
    if customer_identifier in customers:
        found_customer = customers[customer_identifier]
        cust_key = customer_identifier
    else:
        # Search by name
        for cid, info in customers.items():
            if info['name'].lower() == customer_identifier.lower():
                found_customer = info
                cust_key = cid
                break

    if not found_customer:
        return {"error": f"Customer {customer_identifier} not found.", "success": False}

    reported = found_customer.get('income_reported', 0)
    tax_records = found_customer.get('tax_records', 0)
    variance = abs(reported - tax_records)
    threshold = data['compliance_rules']['income_vs_tax_variance_threshold']

    stable = True if variance <= threshold else False

    return {
        "customer_id": cust_key,
        "income_reported": reported,
        "tax_records": tax_records,
        "variance": variance,
        "stable": stable,
        "success": True
    }


def evaluate_property_value(property_address: str) -> Dict[str, Any]:
    """
    Retrieves the property value from the data store.
    """
    data = st.session_state.context
    prop_values = data['property_values']

    if property_address not in prop_values:
        return {"error": f"Property address {property_address} not found.", "success": False}

    return {
        "property_address": property_address,
        "value": prop_values[property_address],
        "success": True
    }


def underwrite_mortgage(application_id: str) -> Dict[str, Any]:
    """
    Completes a mortgage underwriting decision based on risk, income stability, and property value.
    """
    data = st.session_state.context
    apps = data['mortgage_applications']
    application = next((app for app in apps if app['application_id'] == application_id), None)

    if not application:
        return {"error": f"Application {application_id} not found.", "success": False}

    # Suppose we've already computed risk, income stability, and property value.
    # For demonstration, we'll do a simple check:
    credit_score = application.get('credit_score', 0)
    if credit_score < 600:
        application['status'] = 'denied'
        return {"application_id": application_id, "decision": "DENIED", "reason": "Credit score too low", "success": True}

    # If property value < loan amount, deny
    property_value = application.get('property_value', 0)
    loan_amount = application.get('loan_amount', 0)
    if loan_amount > property_value:
        application['status'] = 'denied'
        return {"application_id": application_id, "decision": "DENIED", "reason": "Loan exceeds property value", "success": True}

    # If all checks pass, approve
    application['status'] = 'approved'
    return {
        "application_id": application_id,
        "decision": "APPROVED",
        "success": True
    }


def detect_fraud(application_id: str) -> Dict[str, Any]:
    """
    Examines application data for income vs. tax inconsistencies.
    """
    data = st.session_state.context
    apps = data['mortgage_applications']
    customers = data['customers']

    application = next((app for app in apps if app['application_id'] == application_id), None)
    if not application:
        return {"error": f"Application {application_id} not found.", "success": False}

    applicant_id = application.get('applicant_id')
    if applicant_id not in customers:
        return {"error": "Applicant not found.", "success": False}

    cust_data = customers[applicant_id]
    reported = cust_data.get('income_reported', 0)
    tax = cust_data.get('tax_records', 0)
    variance = abs(reported - tax)
    threshold = data['compliance_rules']['income_vs_tax_variance_threshold']

    flagged = True if variance > threshold else False

    return {
        "application_id": application_id,
        "flagged": flagged,
        "variance": variance,
        "success": True
    }


def run_aml_check(customer_identifier: str, transaction_id: str) -> Dict[str, Any]:
    """
    Checks if the customer's transaction exceeds AML threshold.
    """
    data = st.session_state.context
    aml_threshold = data['compliance_rules']['aml_threshold']
    customers = data['customers']

    # Attempt to find by ID or by name
    found_customer_key = None
    found_customer = None
    for k, cdata in customers.items():
        if k == customer_identifier or cdata['name'].lower() == customer_identifier.lower():
            found_customer = cdata
            found_customer_key = k
            break

    if not found_customer:
        return {"error": f"Customer {customer_identifier} not found.", "success": False}

    transactions = found_customer.get('transactions', [])
    txn = next((t for t in transactions if t['transaction_id'] == transaction_id), None)
    if not txn:
        return {"error": f"Transaction {transaction_id} not found.", "success": False}

    amount = txn.get('amount', 0)
    flagged = True if amount > aml_threshold else False

    return {
        "customer_id": found_customer_key,
        "transaction_id": transaction_id,
        "amount": amount,
        "aml_threshold": aml_threshold,
        "flagged": flagged,
        "success": True
    }


def send_compliance_notice(customer_identifier: str, reference_id: str, message: str) -> Dict[str, Any]:
    """
    Sends a compliance notice to the specified customer about the given reference (e.g., a transaction or application ID).
    """
    data = st.session_state.context
    customers = data['customers']

    # Attempt to find by ID or by name
    found_customer_key = None
    found_customer = None
    for k, cdata in customers.items():
        if k == customer_identifier or cdata['name'].lower() == customer_identifier.lower():
            found_customer = cdata
            found_customer_key = k
            break

    if not found_customer:
        return {"error": f"Customer {customer_identifier} not found.", "success": False}

    timestamp = datetime.now().isoformat()

    return {
        "customer_id": found_customer_key,
        "reference_id": reference_id,
        "message": message,
        "timestamp": timestamp,
        "success": True
    }

# Function mapping for the Streamlit app
FUNCTION_MAPPING = {
    'check_credit_risk': check_credit_risk,
    'assess_income_stability': assess_income_stability,
    'evaluate_property_value': evaluate_property_value,
    'underwrite_mortgage': underwrite_mortgage,
    'detect_fraud': detect_fraud,
    'run_aml_check': run_aml_check,
    'send_compliance_notice': send_compliance_notice
}

# Sample scenarios demonstrating possible interactions
SAMPLE_SCENARIOS = [
    "1. Evaluate the credit risk for mortgage application APP1001.",
    "2. Check income stability for customer 'John Doe'.",
    "3. Detect potential fraud for mortgage application APP1002.",
    "4. Run an AML check for transaction TXN1001 belonging to CUST101.",
    "5. Underwrite mortgage for application APP1001 and finalize approval.",
    "6. Send a compliance notice about the potential AML flag on transaction TXN1001."
]
