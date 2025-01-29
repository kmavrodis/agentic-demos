# Tool definitions for Churn Prediction (Telecom)
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_customer_info",
            "description": "Retrieves high-level customer information including plan details.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "Unique identifier for the customer."
                    }
                },
                "required": ["customer_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_customer_usage",
            "description": "Fetches usage statistics for a particular customer (minutes, data usage, etc.).",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "Unique identifier of the customer."
                    }
                },
                "required": ["customer_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_customer_info",
            "description": "Updates the customer's information such as plan, usage, or churn score.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "Unique identifier for the customer."
                    },
                    "updates": {
                        "type": "object",
                        "description": "Key-value pairs of customer fields to update.",
                        "additionalProperties": True
                    }
                },
                "required": ["customer_id", "updates"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_risky_customers",
            "description": "Fetches a list of customers who have high churn scores based on the model threshold.",
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
            "name": "predict_churn",
            "description": "Runs the churn model on a specific customer to calculate or update their churn score.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "Unique identifier for the customer."
                    }
                },
                "required": ["customer_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "propose_retention_action",
            "description": "Suggests a retention offer or action for a high-churn-risk customer.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "Unique identifier for the customer."
                    }
                },
                "required": ["customer_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "apply_retention_offer",
            "description": "Applies a specific retention offer to a customer's account.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "Unique identifier of the customer."
                    },
                    "offer_id": {
                        "type": "string",
                        "description": "Unique identifier of the retention offer to apply."
                    }
                },
                "required": ["customer_id", "offer_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_retention_resources",
            "description": "Checks the availability of resources for retention tasks (agents, callback slots, etc.).",
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
            "name": "schedule_follow_up",
            "description": "Schedules a follow-up call or message for a high-risk customer.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "Unique customer ID."
                    },
                    "follow_up_type": {
                        "type": "string",
                        "description": "Type of follow-up, e.g. phone, email, text.",
                        "enum": ["phone", "email", "text"]
                    }
                },
                "required": ["customer_id", "follow_up_type"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_customer_survey",
            "description": "Generates a post-retention-offer survey for the customer.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "Unique identifier of the customer."
                    }
                },
                "required": ["customer_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "gather_survey_results",
            "description": "Gathers survey responses and updates customer satisfaction metrics.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "Unique identifier of the customer."
                    },
                    "survey_responses": {
                        "type": "object",
                        "description": "Key-value pairs representing questions and responses.",
                        "additionalProperties": True
                    }
                },
                "required": ["customer_id", "survey_responses"],
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
