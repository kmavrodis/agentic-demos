# functions.py for Product Recommendation
import streamlit as st
from typing import Dict, Any, List
from datetime import datetime

def get_customer_info(customer_id: str) -> Dict[str, Any]:
    '''
    Retrieves high-level customer information including membership plan.
    '''
    customers = st.session_state.context['customers']
    if customer_id not in customers:
        return {'error': f'Customer ID {customer_id} not found.'}
    cust = customers[customer_id]
    return {
        'customer_id': customer_id,
        'customer_name': cust['customer_name'],
        'membership_plan': cust['membership_plan'],
        'monthly_subscription_fee': cust['monthly_subscription_fee'],
        'months_with_service': cust['months_with_service'],
        'recommendation_score': cust.get('recommendation_score', 0)
    }

def get_product_info(product_id: str) -> Dict[str, Any]:
    '''
    Fetches product information for a given product.
    '''
    products = st.session_state.context['products']
    if product_id not in products:
        return {'error': f'Product ID {product_id} not found.'}
    prod = products[product_id]
    return {
        'product_id': product_id,
        'product_name': prod['product_name'],
        'brand': prod['brand'],
        'category': prod['category'],
        'price': prod['price'],
        'rating': prod['rating']
    }

def update_customer_info(customer_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    '''
    Updates the customer's information.
    '''
    customers = st.session_state.context['customers']
    if customer_id not in customers:
        return {'error': f'Customer ID {customer_id} not found.'}
    for key, value in updates.items():
        customers[customer_id][key] = value
    return {
        'customer_id': customer_id,
        'updated_fields': updates,
        'timestamp': datetime.now().isoformat()
    }

def fetch_high_value_customers() -> List[Dict[str, Any]]:
    '''
    Fetches customers with recommendation_score above the global recommendation threshold.
    '''
    customers = st.session_state.context['customers']
    threshold = st.session_state.context['recommendation_model'].get('recommendation_threshold', 0.6)
    results = []
    for cid, data in customers.items():
        score = data.get('recommendation_score', 0)
        if score >= threshold:
            results.append({
                'customer_id': cid,
                'recommendation_score': score
            })
    return results

def run_recommendation_model(customer_id: str) -> Dict[str, Any]:
    '''
    Recalculates a recommendation_score for the customer.
    '''
    customers = st.session_state.context['customers']
    if customer_id not in customers:
        return {'error': f'Customer ID {customer_id} not found.'}
    preferences = customers[customer_id].get('preferences', {})
    purchased = customers[customer_id].get('purchased_products', [])

    # Simple heuristic for demonstration
    brand_factor = len(preferences.get('preferred_brands', [])) * 0.1
    category_factor = len(preferences.get('preferred_categories', [])) * 0.2
    purchase_factor = len(purchased) * 0.05

    base_score = brand_factor + category_factor + purchase_factor
    recommendation_score = min(base_score, 1.0)
    customers[customer_id]['recommendation_score'] = recommendation_score

    return {
        'customer_id': customer_id,
        'recommendation_score': recommendation_score,
        'timestamp': datetime.now().isoformat()
    }

def propose_product_recommendation(customer_id: str) -> Dict[str, Any]:
    '''
    Suggests product recommendations for the customer.
    '''
    customers = st.session_state.context['customers']
    recommendations = st.session_state.context['recommendations']

    if customer_id not in customers:
        return {'error': f'Customer ID {customer_id} not found.'}

    recommendation_score = customers[customer_id].get('recommendation_score', 0)
    eligible_recs = []

    for rec in recommendations:
        if 'recommendation_score>0.8' in rec['eligibility_criteria'] and recommendation_score > 0.8:
            eligible_recs.append(rec)
        elif 'recommendation_score>0.5' in rec['eligibility_criteria'] and recommendation_score > 0.5:
            eligible_recs.append(rec)

    if not eligible_recs:
        return {
            'customer_id': customer_id,
            'suggested_recommendations': [],
            'message': 'No special recommendations at this time.'
        }

    return {
        'customer_id': customer_id,
        'suggested_recommendations': eligible_recs,
        'message': 'Recommendations suggested based on recommendation_score.'
    }

def apply_recommendation(customer_id: str, recommendation_id: str) -> Dict[str, Any]:
    '''
    Applies a specific recommendation for a customer.
    '''
    customers = st.session_state.context['customers']
    recommendations = st.session_state.context['recommendations']

    if customer_id not in customers:
        return {'error': f'Customer ID {customer_id} not found.'}

    rec = next((r for r in recommendations if r['recommendation_id'] == recommendation_id), None)
    if not rec:
        return {'error': f'Recommendation {recommendation_id} not found.'}

    customers[customer_id]['active_recommendation'] = recommendation_id

    return {
        'customer_id': customer_id,
        'recommendation_id': recommendation_id,
        'status': 'Recommendation applied',
        'timestamp': datetime.now().isoformat()
    }

def check_support_resources() -> Dict[str, Any]:
    '''
    Checks availability of support resources (agents, tickets).
    '''
    resources = st.session_state.context['support_resources']
    return {
        'available_agents': resources['available_agents'],
        'support_tickets': resources['support_tickets'],
        'timestamp': datetime.now().isoformat()
    }

def schedule_support_call(customer_id: str, call_type: str) -> Dict[str, Any]:
    '''
    Schedules a support call.
    '''
    customers = st.session_state.context['customers']
    resources = st.session_state.context['support_resources']

    if customer_id not in customers:
        return {'error': f'Customer ID {customer_id} not found.'}

    if call_type == 'emergency' and resources['available_agents'] <= 0:
        return {'error': 'No available agents for emergency calls.'}

    if call_type == 'emergency':
        resources['available_agents'] -= 1
    else:
        resources['support_tickets'] -= 1

    return {
        'customer_id': customer_id,
        'call_type': call_type,
        'status': 'Call scheduled',
        'timestamp': datetime.now().isoformat()
    }

def generate_customer_survey(customer_id: str) -> Dict[str, Any]:
    '''
    Generates a simple survey for the customer.
    '''
    customers = st.session_state.context['customers']
    if customer_id not in customers:
        return {'error': f'Customer ID {customer_id} not found.'}

    survey_questions = [
        'How satisfied are you with our recommendation service?',
        'Were our recommended products relevant to your needs?',
        'Any additional feedback to improve our services?'
    ]

    return {
        'customer_id': customer_id,
        'survey_questions': survey_questions,
        'timestamp': datetime.now().isoformat()
    }

def gather_survey_feedback(customer_id: str, survey_responses: Dict[str, Any]) -> Dict[str, Any]:
    '''
    Processes the survey responses and updates the customer record.
    '''
    customers = st.session_state.context['customers']
    if customer_id not in customers:
        return {'error': f'Customer ID {customer_id} not found.'}

    customers[customer_id]['survey_responses'] = survey_responses

    return {
        'customer_id': customer_id,
        'status': 'Survey results recorded',
        'timestamp': datetime.now().isoformat()
    }

FUNCTION_MAPPING = {
    'get_customer_info': get_customer_info,
    'get_product_info': get_product_info,
    'update_customer_info': update_customer_info,
    'fetch_high_value_customers': fetch_high_value_customers,
    'run_recommendation_model': run_recommendation_model,
    'propose_product_recommendation': propose_product_recommendation,
    'apply_recommendation': apply_recommendation,
    'check_support_resources': check_support_resources,
    'schedule_support_call': schedule_support_call,
    'generate_customer_survey': generate_customer_survey,
    'gather_survey_feedback': gather_survey_feedback
}

SAMPLE_SCENARIOS = [
    'A marketing agent wants to identify customers with a recommendation_score above 0.6 and offer them a discount on new kitchen appliances.',
    "The user wants to upgrade the membership plan for CUST002 from 'Silver' to 'Gold' and then recalculate the recommendation_score."
]
