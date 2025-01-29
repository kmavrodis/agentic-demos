# tools.py for Delivery Route Planning
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_order_info",
            "description": "Retrieves high-level order information including destination, priority, and deadline.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "Unique identifier for the order."
                    }
                },
                "required": ["order_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_driver_info",
            "description": "Retrieves information about a driver, including experience and rating.",
            "parameters": {
                "type": "object",
                "properties": {
                    "driver_id": {
                        "type": "string",
                        "description": "Unique identifier for the driver."
                    }
                },
                "required": ["driver_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "plan_optimal_route",
            "description": "Generates an optimal route for a list of given orders, considering constraints like vehicle capacity and deadlines.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of order IDs to include in route planning."
                    },
                    "vehicle_id": {
                        "type": "string",
                        "description": "Unique identifier of the vehicle for this route."
                    }
                },
                "required": ["order_ids", "vehicle_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_order_status",
            "description": "Updates the status of the order (e.g., pending, in_progress, completed).",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "Unique identifier for the order."
                    },
                    "new_status": {
                        "type": "string",
                        "description": "The new status of the order."
                    }
                },
                "required": ["order_id", "new_status"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_high_priority_orders",
            "description": "Fetches a list of orders that are marked as High priority.",
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
            "name": "assign_driver_to_route",
            "description": "Assigns a driver to a route after the route has been planned.",
            "parameters": {
                "type": "object",
                "properties": {
                    "driver_id": {
                        "type": "string",
                        "description": "Unique identifier of the driver."
                    },
                    "route_id": {
                        "type": "string",
                        "description": "Unique identifier for the planned route."
                    }
                },
                "required": ["driver_id", "route_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_schedule_resources",
            "description": "Checks the availability of drivers and vehicles.",
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
            "name": "instructions_complete",
            "description": "Function should be called when we have completed ALL of the instructions."
        }
    }
]