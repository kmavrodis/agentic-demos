# Tool definitions for OpenAI
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_inventory_status",
            "description": "Retrieves the current inventory status for a given product including component availability.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string",
                        "description": "The unique identifier for the product.",
                        "enum": ["X100", "X200", "X300"]
                    }
                },
                "required": ["product_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_product_details",
            "description": "Fetches comprehensive product details including components, suppliers, and availability information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string",
                        "description": "The unique identifier of the product."
                    }
                },
                "required": ["product_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_inventory",
            "description": "Updates inventory with validation for component availability and quantity constraints.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string",
                        "description": "The unique identifier for the product."
                    },
                    "quantity_change": {
                        "type": "integer",
                        "description": "The amount to adjust the inventory by (positive or negative)."
                    }
                },
                "required": ["product_id", "quantity_change"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_new_orders",
            "description": "Fetches and validates new customer orders, including fulfillment possibility assessment.",
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
            "name": "allocate_stock",
            "description": "Allocates stock for an order with support for partial allocation and detailed status reporting.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The unique identifier of the customer order."
                    },
                    "product_id": {
                        "type": "string",
                        "description": "The unique identifier of the product."
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "The quantity of the product to allocate."
                    }
                },
                "required": ["order_id", "product_id", "quantity"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_available_suppliers",
            "description": "Returns detailed supplier availability information including component quantities.",
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
            "name": "get_supplier_info",
            "description": "Retrieves detailed supplier information including available components and quantities.",
            "parameters": {
                "type": "object",
                "properties": {
                    "supplier_id": {
                        "type": "string",
                        "description": "The unique identifier of the supplier."
                    }
                },
                "required": ["supplier_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "place_purchase_order",
            "description": "Places a validated purchase order with comprehensive component and supplier checking.",
            "parameters": {
                "type": "object",
                "properties": {
                    "supplier_id": {
                        "type": "string",
                        "description": "The unique identifier of the supplier."
                    },
                    "component_id": {
                        "type": "string",
                        "description": "The unique identifier of the component."
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "The quantity of the component to order."
                    }
                },
                "required": ["supplier_id", "component_id", "quantity"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_production_capacity",
            "description": "Checks available production capacity with component availability validation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "time_frame": {
                        "type": "string",
                        "description": "The time frame to check.",
                        "enum": ["immediate", "next_week"]
                    }
                },
                "required": ["time_frame"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "schedule_production_run",
            "description": "Schedules production with comprehensive component and capacity validation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string",
                        "description": "The unique identifier of the product."
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "The quantity of the product to produce."
                    },
                    "time_frame": {
                        "type": "string",
                        "description": "The time frame for production scheduling.",
                        "enum": ["immediate", "next_week"]
                    }
                },
                "required": ["product_id", "quantity", "time_frame"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_shipping_options",
            "description": "Calculates optimized shipping options with cost and time-based sorting.",
            "parameters": {
                "type": "object",
                "properties": {
                    "destination": {
                        "type": "string",
                        "description": "The shipping destination address."
                    },
                    "weight": {
                        "type": "number",
                        "description": "The weight of the package in kilograms."
                    },
                    "dimensions": {
                        "type": "object",
                        "description": "The dimensions of the package.",
                        "properties": {
                            "length": {"type": "number", "description": "Length in centimeters"},
                            "width": {"type": "number", "description": "Width in centimeters"},
                            "height": {"type": "number", "description": "Height in centimeters"}
                        },
                        "required": ["length", "width", "height"]
                    }
                },
                "required": ["destination", "weight", "dimensions"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "book_shipment",
            "description": "Books validated shipments with tracking and delivery estimation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The unique identifier of the customer order."
                    },
                    "carrier_id": {
                        "type": "string",
                        "description": "The unique identifier of the shipping carrier."
                    },
                    "service_level": {
                        "type": "string",
                        "description": "The shipping service level.",
                        "enum": ["Standard", "Express"]
                    }
                },
                "required": ["order_id", "carrier_id", "service_level"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_order_update",
            "description": "Sends validated order updates with customer verification.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "The unique identifier of the customer."
                    },
                    "order_id": {
                        "type": "string",
                        "description": "The unique identifier of the order."
                    },
                    "message": {
                        "type": "string",
                        "description": "The message content to send to the customer."
                    }
                },
                "required": ["customer_id", "order_id", "message"],
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