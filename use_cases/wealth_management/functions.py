import streamlit as st
from typing import Dict, Any, List
from datetime import datetime

def get_portfolio_overview(portfolio_id: str) -> Dict[str, Any]:
    portfolios = st.session_state.context['portfolios']
    market_data = st.session_state.context['market_data']

    portfolio = next((p for p in portfolios if p['portfolio_id'] == portfolio_id), None)
    if not portfolio:
        return {"error": f"Portfolio {portfolio_id} not found.", "success": False}

    total_value = 0.0
    holdings_details = []

    for holding in portfolio['holdings']:
        symbol = holding['symbol']
        shares = holding['shares']
        avg_cost = holding['avg_cost']
        if symbol in market_data:
            current_price = market_data[symbol]['price']
            holding_value = current_price * shares
            total_value += holding_value
            holdings_details.append({
                "symbol": symbol,
                "shares": shares,
                "avg_cost": avg_cost,
                "current_price": current_price,
                "holding_value": holding_value
            })
        else:
            holdings_details.append({
                "symbol": symbol,
                "shares": shares,
                "avg_cost": avg_cost,
                "error": "Market data not found"
            })

    return {
        "success": True,
        "portfolio_id": portfolio_id,
        "total_value": total_value,
        "holdings": holdings_details
    }

def analyze_security(symbol: str) -> Dict[str, Any]:
    market_data = st.session_state.context['market_data']
    if symbol not in market_data:
        return {"error": f"Symbol {symbol} not found.", "success": False}

    data = market_data[symbol]
    return {
        "success": True,
        "symbol": symbol,
        "price": data['price'],
        "volume": data['volume']
    }

def suggest_optimizations(portfolio_id: str) -> Dict[str, Any]:
    portfolios = st.session_state.context['portfolios']
    users = st.session_state.context['users']

    portfolio = next((p for p in portfolios if p['portfolio_id'] == portfolio_id), None)
    if not portfolio:
        return {"error": f"Portfolio {portfolio_id} not found.", "success": False}

    user = users.get(portfolio['owner_id'])
    if not user:
        return {"error": f"Owner for portfolio {portfolio_id} not found.", "success": False}

    risk_tolerance = user['preferences'].get('risk_tolerance', 'medium')
    # Fake logic: Suggest adding TSLA for high risk, adding more GOOGL for medium, etc.
    suggestions = []

    if risk_tolerance == 'high':
        suggestions.append("Consider adding more TSLA due to potential growth.")
    elif risk_tolerance == 'medium':
        suggestions.append("Consider gradually increasing positions in stable tech stocks.")
    else:
        suggestions.append("Consider more balanced ETFs to minimize volatility.")

    return {
        "success": True,
        "portfolio_id": portfolio_id,
        "risk_tolerance": risk_tolerance,
        "recommended_actions": suggestions
    }

def fetch_latest_news() -> Dict[str, Any]:
    market_news = st.session_state.context['market_news']
    return {
        "success": True,
        "latest_news": market_news
    }

def update_market_data(symbol: str, new_price: float) -> Dict[str, Any]:
    market_data = st.session_state.context['market_data']
    if symbol not in market_data:
        return {"error": f"Symbol {symbol} not found.", "success": False}

    market_data[symbol]['price'] = new_price
    return {
        "success": True,
        "symbol": symbol,
        "new_price": new_price,
        "timestamp": datetime.now().isoformat()
    }

def place_trade(portfolio_id: str, symbol: str, shares: int) -> Dict[str, Any]:
    portfolios = st.session_state.context['portfolios']
    market_data = st.session_state.context['market_data']
    portfolio = next((p for p in portfolios if p['portfolio_id'] == portfolio_id), None)

    if not portfolio:
        return {"error": f"Portfolio {portfolio_id} not found.", "success": False}
    if symbol not in market_data:
        return {"error": f"Symbol {symbol} not found.", "success": False}

    current_holding = next((h for h in portfolio['holdings'] if h['symbol'] == symbol), None)
    # Buy or Sell
    if shares > 0:
        # Buying
        if current_holding:
            # Adjust average cost (simplified calculation)
            total_shares_before = current_holding['shares']
            total_cost_before = total_shares_before * current_holding['avg_cost']
            total_new_cost = shares * market_data[symbol]['price']
            new_avg_cost = (total_cost_before + total_new_cost) / (total_shares_before + shares)
            current_holding['shares'] += shares
            current_holding['avg_cost'] = new_avg_cost
        else:
            portfolio['holdings'].append({
                "symbol": symbol,
                "shares": shares,
                "avg_cost": market_data[symbol]['price']
            })
    else:
        # Selling (shares is negative)
        if not current_holding or current_holding['shares'] < abs(shares):
            return {"error": "Not enough shares to sell.", "success": False}
        current_holding['shares'] += shares  # shares is negative
        if current_holding['shares'] == 0:
            portfolio['holdings'].remove(current_holding)

    return {
        "success": True,
        "portfolio_id": portfolio_id,
        "symbol": symbol,
        "shares_traded": shares,
        "timestamp": datetime.now().isoformat()
    }

FUNCTION_MAPPING = {
    'get_portfolio_overview': get_portfolio_overview,
    'analyze_security': analyze_security,
    'suggest_optimizations': suggest_optimizations,
    'fetch_latest_news': fetch_latest_news,
    'update_market_data': update_market_data,
    'place_trade': place_trade
}

SAMPLE_SCENARIOS = [
    "What is the total value of portfolio PORT1001?",
    "Please provide the latest market news headlines.",
    "Suggest potential changes to portfolio PORT1002, given Bob's high risk tolerance.",
    "Place a trade to buy 10 shares of AAPL in portfolio PORT1001.",
    "Update the price of TSLA to 680.0 and see the new portfolio PORT1001 value"
]
