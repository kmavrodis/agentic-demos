# functions.py for Delivery Route Planning
import streamlit as st
from typing import Dict, Any, List
from datetime import datetime


def get_order_info(order_id: str) -> Dict[str, Any]:
    '''Retrieves high-level order information including destination, priority, and deadline.'''
    orders = st.session_state.context['orders']
    if order_id not in orders:
        return {"error": f"Order ID {order_id} not found."}
    order = orders[order_id]
    return {
        "order_id": order_id,
        "destination": order["destination"],
        "priority": order["priority"],
        "deadline": order["deadline"],
        "status": order.get("status", "unknown")
    }


def get_driver_info(driver_id: str) -> Dict[str, Any]:
    '''Retrieves information about a driver, including experience and rating.'''
    drivers = st.session_state.context['drivers']
    if driver_id not in drivers:
        return {"error": f"Driver ID {driver_id} not found."}
    driver = drivers[driver_id]
    return {
        "driver_id": driver_id,
        "name": driver["name"],
        "license_type": driver["license_type"],
        "years_experience": driver["years_experience"],
        "rating": driver["rating"]
    }


def plan_optimal_route(order_ids: List[str], vehicle_id: str) -> Dict[str, Any]:
    '''Generates an optimal route for a list of given orders, considering constraints like vehicle capacity and deadlines.'''
    orders = st.session_state.context['orders']
    fleet = st.session_state.context['fleet']
    if vehicle_id not in fleet:
        return {"error": f"Vehicle ID {vehicle_id} not found."}

    # Validate orders
    unavailable_orders = [oid for oid in order_ids if oid not in orders]
    if len(unavailable_orders) > 0:
        return {"error": f"One or more orders not found: {unavailable_orders}"}

    # Very simplified route planning mock
    # We just return them in the same order for demonstration
    route_plan = [
        {
            "stop_number": idx + 1,
            "order_id": oid,
            "destination": orders[oid]["destination"]
        } for idx, oid in enumerate(order_ids)
    ]
    route_id = f"ROUTE-{int(datetime.now().timestamp())}"
    return {
        "route_id": route_id,
        "vehicle_id": vehicle_id,
        "planned_stops": route_plan,
        "timestamp": datetime.now().isoformat()
    }


def update_order_status(order_id: str, new_status: str) -> Dict[str, Any]:
    '''Updates the status of the order (e.g., pending, in_progress, completed).'''
    orders = st.session_state.context['orders']
    if order_id not in orders:
        return {"error": f"Order ID {order_id} not found."}
    orders[order_id]["status"] = new_status
    return {
        "order_id": order_id,
        "new_status": new_status,
        "timestamp": datetime.now().isoformat()
    }


def fetch_high_priority_orders() -> List[Dict[str, Any]]:
    '''Fetches a list of orders that are marked as High priority.'''
    orders = st.session_state.context['orders']
    results = []
    for oid, data in orders.items():
        if data.get('priority', '').lower() == 'high':
            results.append({
                "order_id": oid,
                "destination": data.get("destination"),
                "deadline": data.get("deadline"),
                "status": data.get("status", "unknown")
            })
    return results


def assign_driver_to_route(driver_id: str, route_id: str) -> Dict[str, Any]:
    '''Assigns a driver to a route after the route has been planned.'''
    drivers = st.session_state.context['drivers']
    if driver_id not in drivers:
        return {"error": f"Driver ID {driver_id} not found."}

    # For this demo, we record the assignment in session_state.
    assigned_routes = st.session_state.context.get('assigned_routes', {})
    assigned_routes[route_id] = driver_id
    st.session_state.context['assigned_routes'] = assigned_routes

    return {
        "driver_id": driver_id,
        "route_id": route_id,
        "status": "Route assignment completed",
        "timestamp": datetime.now().isoformat()
    }


def check_schedule_resources() -> Dict[str, Any]:
    '''Checks the availability of drivers and vehicles.'''
    resources = st.session_state.context['schedule_resources']
    return {
        "available_drivers": resources["available_drivers"],
        "available_vehicles": resources["available_vehicles"],
        "timestamp": datetime.now().isoformat()
    }

# The final function to indicate instructions complete

FUNCTION_MAPPING = {
    'get_order_info': get_order_info,
    'get_driver_info': get_driver_info,
    'plan_optimal_route': plan_optimal_route,
    'update_order_status': update_order_status,
    'fetch_high_priority_orders': fetch_high_priority_orders,
    'assign_driver_to_route': assign_driver_to_route,
    'check_schedule_resources': check_schedule_resources
}

SAMPLE_SCENARIOS = [
    "An operations manager wants to identify all high-priority orders and plan an optimal route for them.",
    "A driver with ID DRV2002 needs to be assigned to a newly created route with ID ROUTE-1696791111.",
    "The company wants to mark an order as completed once it is delivered.",
    "An agent checks how many vehicles and drivers are still available to schedule more deliveries."
]
