# Tool definitions for Crop Analysis
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_field_info",
            "description": "Retrieves high-level field information including plan details.",
            "parameters": {
                "type": "object",
                "properties": {
                    "field_id": {
                        "type": "string",
                        "description": "Unique identifier for the field."
                    }
                },
                "required": ["field_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_soil_quality",
            "description": "Fetches soil quality metrics (pH, moisture, nutrients) for a field.",
            "parameters": {
                "type": "object",
                "properties": {
                    "field_id": {
                        "type": "string",
                        "description": "Unique identifier of the field."
                    }
                },
                "required": ["field_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_field_info",
            "description": "Updates the field's information such as plan, soil metrics, or analysis score.",
            "parameters": {
                "type": "object",
                "properties": {
                    "field_id": {
                        "type": "string",
                        "description": "Unique identifier for the field."
                    },
                    "updates": {
                        "type": "object",
                        "description": "Key-value pairs of field attributes to update.",
                        "additionalProperties": True
                    }
                },
                "required": ["field_id", "updates"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_high_risk_fields",
            "description": "Fetches a list of fields that have high analysis scores based on the model threshold.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "predict_analysis_score",
            "description": "Runs the analysis model on a specific field to calculate or update the analysis score.",
            "parameters": {
                "type": "object",
                "properties": {
                    "field_id": {
                        "type": "string",
                        "description": "Unique identifier for the field."
                    }
                },
                "required": ["field_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "propose_recommendation",
            "description": "Suggests a recommendation or action for a field with high analysis score.",
            "parameters": {
                "type": "object",
                "properties": {
                    "field_id": {
                        "type": "string",
                        "description": "Unique identifier for the field."
                    }
                },
                "required": ["field_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "apply_recommendation",
            "description": "Applies a specific recommendation to a field.",
            "parameters": {
                "type": "object",
                "properties": {
                    "field_id": {
                        "type": "string",
                        "description": "Unique identifier of the field."
                    },
                    "recommendation_id": {
                        "type": "string",
                        "description": "Unique identifier of the recommendation to apply."
                    }
                },
                "required": ["field_id", "recommendation_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_support_resources",
            "description": "Checks the availability of resources for field visits or analysis support.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "schedule_field_visit",
            "description": "Schedules a field visit for high-risk or high-priority fields.",
            "parameters": {
                "type": "object",
                "properties": {
                    "field_id": {
                        "type": "string",
                        "description": "Unique field ID."
                    },
                    "visit_type": {
                        "type": "string",
                        "description": "Type of visit, e.g. routine, emergency.",
                        "enum": ["routine", "emergency"]
                    }
                },
                "required": ["field_id", "visit_type"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_field_survey",
            "description": "Generates a post-recommendation survey for the field.",
            "parameters": {
                "type": "object",
                "properties": {
                    "field_id": {
                        "type": "string",
                        "description": "Unique identifier of the field."
                    }
                },
                "required": ["field_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "gather_survey_results",
            "description": "Gathers survey responses and updates overall field satisfaction metrics.",
            "parameters": {
                "type": "object",
                "properties": {
                    "field_id": {
                        "type": "string",
                        "description": "Unique identifier of the field."
                    },
                    "survey_responses": {
                        "type": "object",
                        "description": "Key-value pairs representing survey questions and responses.",
                        "additionalProperties": True
                    }
                },
                "required": ["field_id", "survey_responses"],
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
