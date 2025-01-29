# Tool definitions for the specialized medical use case.
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_patient_history",
            "description": "Retrieves a comprehensive medical history for a given patient, including diagnoses, treatments, medications, and reported symptoms.",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_id": {
                        "type": "string",
                        "description": "The unique identifier for the patient whose history is needed."
                    }
                },
                "required": ["patient_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "record_symptom",
            "description": "Records a new symptom for a specified patient, capturing severity and date.",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_id": {
                        "type": "string",
                        "description": "The unique identifier for the patient reporting the symptom."
                    },
                    "symptom": {
                        "type": "string",
                        "description": "The symptom being reported."
                    },
                    "severity": {
                        "type": "string",
                        "description": "Severity level (e.g., mild, moderate, severe)."
                    }
                },
                "required": ["patient_id", "symptom", "severity"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_diagnosis",
            "description": "Adds a new diagnosis entry for a patient, including date of diagnosis and treating doctor.",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_id": {
                        "type": "string",
                        "description": "The unique identifier for the patient."
                    },
                    "diagnosis": {
                        "type": "string",
                        "description": "The name of the diagnosis."
                    },
                    "date": {
                        "type": "string",
                        "description": "The date of the diagnosis in YYYY-MM-DD format."
                    },
                    "treating_doctor": {
                        "type": "string",
                        "description": "The identifier of the treating doctor."
                    }
                },
                "required": ["patient_id", "diagnosis", "date", "treating_doctor"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "compile_timeline",
            "description": "Builds a chronological timeline of a patient's medical events (diagnoses, symptoms, and lab tests).",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_id": {
                        "type": "string",
                        "description": "The unique identifier for the patient whose timeline is requested."
                    }
                },
                "required": ["patient_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_lab_test_results",
            "description": "Retrieves lab test results for a given test ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "test_id": {
                        "type": "string",
                        "description": "The unique identifier for the lab test."
                    }
                },
                "required": ["test_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "schedule_lab_test",
            "description": "Creates a new lab test entry for a patient.",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_id": {
                        "type": "string",
                        "description": "The unique identifier for the patient requiring the lab test."
                    },
                    "test_type": {
                        "type": "string",
                        "description": "The type of test (e.g., Blood Panel, MRI, X-Ray)."
                    },
                    "date_conducted": {
                        "type": "string",
                        "description": "The date on which the test is scheduled or took place in YYYY-MM-DD format."
                    }
                },
                "required": ["patient_id", "test_type", "date_conducted"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_patient_update",
            "description": "Sends a message update to the patient, confirming new diagnoses or test results.",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_id": {
                        "type": "string",
                        "description": "The unique identifier for the patient."
                    },
                    "message": {
                        "type": "string",
                        "description": "The content of the message to the patient."
                    }
                },
                "required": ["patient_id", "message"],
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
