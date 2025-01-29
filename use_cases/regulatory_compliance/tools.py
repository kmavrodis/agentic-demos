# Tool definitions for AI-driven mortgage, fraud detection, and AML monitoring.
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "check_credit_risk",
            "description": "Evaluates the mortgage applicant's credit risk by analyzing the credit score and basic application details.",
            "parameters": {
                "type": "object",
                "properties": {
                    "application_id": {
                        "type": "string",
                        "description": "The ID of the mortgage application to evaluate."
                    }
                },
                "required": ["application_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "assess_income_stability",
            "description": "Checks the consistency of reported income against known tax records, either through customer ID or name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_identifier": {
                        "type": "string",
                        "description": "The unique customer ID or full name of the customer."
                    }
                },
                "required": ["customer_identifier"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "evaluate_property_value",
            "description": "Retrieves the property value for a given address to check loan-to-value ratios.",
            "parameters": {
                "type": "object",
                "properties": {
                    "property_address": {
                        "type": "string",
                        "description": "The address of the property being purchased or refinanced."
                    }
                },
                "required": ["property_address"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "underwrite_mortgage",
            "description": "Completes a mortgage underwriting decision based on credit score, income stability, and property value.",
            "parameters": {
                "type": "object",
                "properties": {
                    "application_id": {
                        "type": "string",
                        "description": "The ID of the mortgage application to underwrite."
                    }
                },
                "required": ["application_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "detect_fraud",
            "description": "Analyzes mortgage application data for inconsistencies (income vs. tax records) that indicate potential fraud.",
            "parameters": {
                "type": "object",
                "properties": {
                    "application_id": {
                        "type": "string",
                        "description": "ID of the mortgage application to evaluate for fraud."
                    }
                },
                "required": ["application_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_aml_check",
            "description": "Reviews high-value transactions against AML thresholds and flags any potential money laundering.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_identifier": {
                        "type": "string",
                        "description": "Unique customer ID or name of the customer who performed the transaction."
                    },
                    "transaction_id": {
                        "type": "string",
                        "description": "ID of the transaction to evaluate."
                    }
                },
                "required": ["customer_identifier", "transaction_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_compliance_notice",
            "description": "Sends a compliance-related notification for a flagged transaction or mortgage application.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_identifier": {
                        "type": "string",
                        "description": "The unique ID or name of the customer."
                    },
                    "reference_id": {
                        "type": "string",
                        "description": "The mortgage application ID or transaction ID being referenced."
                    },
                    "message": {
                        "type": "string",
                        "description": "The content of the notice being sent."
                    }
                },
                "required": ["customer_identifier", "reference_id", "message"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "instructions_complete",
            "description": "Function should be called when we have completed ALL of the instructions."
        }
    }
]
