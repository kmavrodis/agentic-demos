# tools.py for Product Recommendation
TOOLS = [
    {
        'type': 'function',
        'function': {
            'name': 'get_customer_info',
            'description': 'Retrieves high-level customer information including membership plan.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'customer_id': {
                        'type': 'string',
                        'description': 'Unique identifier for the customer.'
                    }
                },
                'required': ['customer_id'],
                'additionalProperties': False
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_product_info',
            'description': 'Fetches product information such as brand, price, and category.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'product_id': {
                        'type': 'string',
                        'description': 'Unique identifier for the product.'
                    }
                },
                'required': ['product_id'],
                'additionalProperties': False
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'update_customer_info',
            'description': 'Updates information for a given customer, e.g. membership plan or recommendation score.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'customer_id': {
                        'type': 'string',
                        'description': 'Unique identifier for the customer.'
                    },
                    'updates': {
                        'type': 'object',
                        'description': 'Key-value pairs of customer attributes to update.',
                        'additionalProperties': True
                    }
                },
                'required': ['customer_id', 'updates'],
                'additionalProperties': False
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'fetch_high_value_customers',
            'description': 'Returns a list of customers who have recommendation_score above the threshold.',
            'parameters': {
                'type': 'object',
                'properties': {},
                'required': [],
                'additionalProperties': False
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'run_recommendation_model',
            'description': 'Runs the recommendation model on a specific customer to update their recommendation_score.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'customer_id': {
                        'type': 'string',
                        'description': 'Unique identifier for the customer.'
                    }
                },
                'required': ['customer_id'],
                'additionalProperties': False
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'propose_product_recommendation',
            'description': 'Suggests product recommendations for a customer based on their recommendation_score.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'customer_id': {
                        'type': 'string',
                        'description': 'Unique identifier for the customer.'
                    }
                },
                'required': ['customer_id'],
                'additionalProperties': False
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'apply_recommendation',
            'description': 'Applies a specific recommendation to a customer account.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'customer_id': {
                        'type': 'string',
                        'description': 'Unique identifier of the customer.'
                    },
                    'recommendation_id': {
                        'type': 'string',
                        'description': 'Unique identifier of the recommendation to apply.'
                    }
                },
                'required': ['customer_id', 'recommendation_id'],
                'additionalProperties': False
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'check_support_resources',
            'description': 'Checks the availability of resources for support or inquiries.',
            'parameters': {
                'type': 'object',
                'properties': {},
                'required': [],
                'additionalProperties': False
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'schedule_support_call',
            'description': 'Schedules a support call for high-value or high-priority customers.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'customer_id': {
                        'type': 'string',
                        'description': 'Unique customer ID.'
                    },
                    'call_type': {
                        'type': 'string',
                        'description': 'Type of call, e.g. routine, emergency.',
                        'enum': ['routine', 'emergency']
                    }
                },
                'required': ['customer_id', 'call_type'],
                'additionalProperties': False
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'generate_customer_survey',
            'description': 'Generates a post-recommendation survey for the customer.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'customer_id': {
                        'type': 'string',
                        'description': 'Unique identifier of the customer.'
                    }
                },
                'required': ['customer_id'],
                'additionalProperties': False
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'gather_survey_feedback',
            'description': 'Gathers survey responses and updates overall customer satisfaction metrics.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'customer_id': {
                        'type': 'string',
                        'description': 'Unique identifier of the customer.'
                    },
                    'survey_responses': {
                        'type': 'object',
                        'description': 'Key-value pairs representing survey questions and responses.',
                        'additionalProperties': True
                    }
                },
                'required': ['customer_id', 'survey_responses'],
                'additionalProperties': False
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'instructions_complete',
            'description': 'Function should be called when we have completed ALL of the instructions.'
        }
    }
]
