TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_portfolio_overview",
            "description": "Returns the overall value and composition of a portfolio.",
            "parameters": {
                "type": "object",
                "properties": {
                    "portfolio_id": {
                        "type": "string",
                        "description": "The unique identifier of the portfolio to analyze."
                    }
                },
                "required": ["portfolio_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_security",
            "description": "Provides insight into a specific security, including current price and volume.",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "The ticker symbol of the security."
                    }
                },
                "required": ["symbol"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "suggest_optimizations",
            "description": "Suggests potential changes to a portfolio to improve returns or reduce risk.",
            "parameters": {
                "type": "object",
                "properties": {
                    "portfolio_id": {
                        "type": "string",
                        "description": "The ID of the portfolio to optimize."
                    }
                },
                "required": ["portfolio_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_latest_news",
            "description": "Fetches the latest dummy market news items.",
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
            "name": "update_market_data",
            "description": "Updates the real-time price of a particular security.",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "The ticker symbol of the security."
                    },
                    "new_price": {
                        "type": "number",
                        "description": "The new price of the security."
                    }
                },
                "required": ["symbol","new_price"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "place_trade",
            "description": "Places a trade to buy or sell shares of a security.",
            "parameters": {
                "type": "object",
                "properties": {
                    "portfolio_id": {
                        "type": "string",
                        "description": "The portfolio ID to place the trade in."
                    },
                    "symbol": {
                        "type": "string",
                        "description": "The ticker symbol to trade."
                    },
                    "shares": {
                        "type": "integer",
                        "description": "The number of shares to buy (positive) or sell (negative)."
                    }
                },
                "required": ["portfolio_id","symbol","shares"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "instructions_complete",
            "description": "Function should be called when we have completed ALL instructions."
        }
    }
]
