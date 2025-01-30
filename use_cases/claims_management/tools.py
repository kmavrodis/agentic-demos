# tool definitions for suspicious-claim detection
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "fetch_claim_details",
            "description": "Fetches all details related to a given claim.",
            "parameters": {
                "type": "object",
                "properties": {
                    "claim_id": {
                        "type": "string",
                        "description": "The unique identifier of the claim."}
                },
                "required": ["claim_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_policyholder_info",
            "description": "Retrieves policyholder details by either policyholder ID or name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "policyholder_id": {
                        "type": "string",
                        "description": "Unique ID of the policyholder.",
                        "nullable": True
                    },
                    "policyholder_name": {
                        "type": "string",
                        "description": "Name of the policyholder.",
                        "nullable": True
                    }
                },
                "required": [],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "parse_claim_narrative",
            "description": "Uses advanced LLM logic to parse the claim description and identify suspicious keywords or phrases.",
            "parameters": {
                "type": "object",
                "properties": {
                    "claim_id": {
                        "type": "string",
                        "description": "Claim ID whose narrative is to be checked for suspicious elements."}
                },
                "required": ["claim_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_ml_fraud_scoring",
            "description": "Runs the claim and LLM-generated flags through a fraud model to produce a fraud score.",
            "parameters": {
                "type": "object",
                "properties": {
                    "claim_id": {
                        "type": "string",
                        "description": "Claim ID to run through the fraud model."}
                },
                "required": ["claim_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "flag_claim_for_investigation",
            "description": "Flags a claim for manual review based on suspicious findings.",
            "parameters": {
                "type": "object",
                "properties": {
                    "claim_id": {
                        "type": "string",
                        "description": "The ID of the claim to flag."},
                    "reason": {
                        "type": "string",
                        "description": "Reason or summary of why the claim is being flagged."}
                },
                "required": ["claim_id", "reason"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_claim_status",
            "description": "Updates the status of a claim (e.g., from Open to Under Investigation or Closed).",
            "parameters": {
                "type": "object",
                "properties": {
                    "claim_id": {
                        "type": "string",
                        "description": "The claim ID to update."},
                    "new_status": {
                        "type": "string",
                        "description": "The new status of the claim.",
                        "enum": ["Open", "Under Investigation", "Closed"]}
                },
                "required": ["claim_id", "new_status"],
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
