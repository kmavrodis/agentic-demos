import streamlit as st
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

def get_inventory_status(product_id: str) -> Dict[str, Any]:
    """
    Retrieves the current inventory status for a given product.
    Returns both quantity and component availability.
    """
    inventory = st.session_state.context['inventory']
    components = st.session_state.context['components']
    products = st.session_state.context['products']
    
    if product_id not in products:
        return {'error': f"Product ID {product_id} not found."}
        
    quantity = inventory.get(product_id, 0)
    components_status = {}
    
    # Check component availability
    for comp_id, needed_qty in products[product_id]['components_needed'].items():
        if comp_id in components:
            components_status[comp_id] = {
                'available': components[comp_id]['available_quantity'],
                'needed_per_unit': needed_qty
            }
    
    return {
        'product_id': product_id,
        'quantity': quantity,
        'components_status': components_status
    }

def get_product_details(product_id: str) -> Dict[str, Any]:
    """
    Fetches comprehensive product details including components and suppliers.
    """
    products = st.session_state.context['products']
    components = st.session_state.context['components']
    
    if product_id not in products:
        return {'error': f"Product ID {product_id} not found."}
    
    product = products[product_id]
    components_info = {}
    
    for comp_id, qty_needed in product['components_needed'].items():
        if comp_id in components:
            comp_data = components[comp_id]
            components_info[comp_id] = {
                'quantity_needed': qty_needed,
                'available_quantity': comp_data['available_quantity'],
                'supplier': comp_data['suppliers']
            }
    
    return {
        'name': product['name'],
        'components': components_info
    }

def update_inventory(product_id: str, quantity_change: int) -> Dict[str, Any]:
    """
    Updates inventory with validation for component availability.
    """
    inventory = st.session_state.context['inventory']
    products = st.session_state.context['products']
    components = st.session_state.context['components']
    
    if product_id not in products:
        return {'error': f"Product ID {product_id} not found."}
    
    current_qty = inventory.get(product_id, 0)
    new_quantity = current_qty + quantity_change
    
    if new_quantity < 0:
        return {'error': 'Resulting inventory cannot be negative.'}
    
    # Check component availability if increasing inventory
    if quantity_change > 0:
        for comp_id, needed_qty in products[product_id]['components_needed'].items():
            total_needed = needed_qty * quantity_change
            if components[comp_id]['available_quantity'] < total_needed:
                return {'error': f'Insufficient components available for {comp_id}'}
            components[comp_id]['available_quantity'] -= total_needed
    
    inventory[product_id] = new_quantity
    return {
        'product_id': product_id,
        'new_quantity': new_quantity,
        'timestamp': datetime.now().isoformat()
    }

def fetch_new_orders() -> List[Dict[str, Any]]:
    """
    Fetches and validates new customer orders.
    """
    orders = st.session_state.context['orders']
    inventory = st.session_state.context['inventory']
    
    validated_orders = []
    for order in orders:
        order_status = {
            'order_id': order['order_id'],
            'product_id': order['product_id'],
            'quantity': order['quantity'],
            'can_fulfill': False,
            'available_quantity': inventory.get(order['product_id'], 0)
        }
        
        if order['product_id'] in inventory:
            order_status['can_fulfill'] = inventory[order['product_id']] >= order['quantity']
        
        validated_orders.append(order_status)
    
    return validated_orders

def allocate_stock(order_id: str, product_id: str, quantity: int) -> Dict[str, Any]:
    """
    Allocates stock for an order with validation and partial allocation support.
    """
    inventory = st.session_state.context['inventory']
    orders = st.session_state.context['orders']
    
    # Validate order exists
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        return {'error': f"Order {order_id} not found."}
    
    if product_id not in inventory:
        return {'error': f"Product {product_id} not found in inventory."}
    
    available = inventory[product_id]
    allocated_quantity = min(available, quantity)
    
    if allocated_quantity > 0:
        inventory[product_id] -= allocated_quantity
        
    return {
        'order_id': order_id,
        'product_id': product_id,
        'allocated_quantity': allocated_quantity,
        'remaining_quantity': quantity - allocated_quantity,
        'status': 'Fully Allocated' if allocated_quantity == quantity else 'Partially Allocated'
    }

def check_available_suppliers() -> Dict[str, List[Dict[str, Any]]]:
    """
    Returns detailed supplier availability information.
    """
    suppliers = st.session_state.context.get('available_suppliers', [])
    components = st.session_state.context['components']
    
    supplier_details = []
    for supplier_id in suppliers:
        supplier_components = [
            {'component_id': comp_id, 'quantity': comp_data['available_quantity']}
            for comp_id, comp_data in components.items()
            if comp_data['suppliers'] == supplier_id
        ]
        supplier_details.append({
            'supplier_id': supplier_id,
            'available_components': supplier_components
        })
    
    return {'suppliers': supplier_details}

def place_purchase_order(supplier_id: str, component_id: str, quantity: int) -> Dict[str, Any]:
    """
    Places and validates a purchase order with improved error handling.
    """
    suppliers = st.session_state.context['available_suppliers']
    components = st.session_state.context['components']
    
    if supplier_id not in suppliers:
        return {'error': f"Invalid supplier ID: {supplier_id}"}
        
    if component_id not in components:
        return {'error': f"Invalid component ID: {component_id}"}
        
    component = components[component_id]
    if component['suppliers'] != supplier_id:
        return {'error': f"Supplier {supplier_id} does not supply component {component_id}"}
        
    if quantity <= 0:
        return {'error': "Quantity must be positive"}
        
    po_number = f"PO_{datetime.now().strftime('%Y%m%d')}_{supplier_id}_{component_id}"
    
    # Update component availability and production capacity
    component['available_quantity'] += quantity
    st.session_state.context['production_capacity']['next_week'] += quantity
    
    return {
        'po_number': po_number,
        'supplier_id': supplier_id,
        'component_id': component_id,
        'quantity': quantity,
        'status': 'Placed',
        'timestamp': datetime.now().isoformat()
    }

def schedule_production_run(product_id: str, quantity: int, time_frame: str) -> Dict[str, Any]:
    """
    Schedules production with component and capacity validation.
    """
    capacity = st.session_state.context['production_capacity']
    products = st.session_state.context['products']
    components = st.session_state.context['components']
    
    if time_frame not in capacity:
        return {'error': f"Invalid time frame: {time_frame}"}
        
    if product_id not in products:
        return {'error': f"Invalid product ID: {product_id}"}
        
    if capacity[time_frame] < quantity:
        return {'error': f"Insufficient production capacity for {time_frame}"}
    
    # Validate component availability
    for comp_id, needed_qty in products[product_id]['components_needed'].items():
        total_needed = needed_qty * quantity
        if components[comp_id]['available_quantity'] < total_needed:
            return {'error': f"Insufficient quantity of component {comp_id}"}
            
        components[comp_id]['available_quantity'] -= total_needed
    
    # Update capacity and inventory
    capacity[time_frame] -= quantity
    if time_frame == 'immediate':
        st.session_state.context['inventory'][product_id] = \
            st.session_state.context['inventory'].get(product_id, 0) + quantity
    
    return {
        'production_id': f"PROD_{datetime.now().strftime('%Y%m%d')}_{product_id}",
        'product_id': product_id,
        'quantity': quantity,
        'time_frame': time_frame,
        'status': 'Scheduled'
    }

def calculate_shipping_options(destination: str, weight: float, dimensions: Dict[str, float]) -> Dict[str, Any]:
    """
    Calculates shipping options with validation and sorting.
    """
    shipping_options = st.session_state.context['shipping_options']
    
    if destination not in shipping_options:
        return {'error': f"No shipping options available for destination {destination}"}
    
    options = shipping_options[destination]
    
    # Sort options by cost and delivery time
    sorted_options = sorted(options, key=lambda x: (x['cost'], x['estimated_days']))
    
    return {
        'destination': destination,
        'options': sorted_options,
        'recommended': sorted_options[0] if sorted_options else None
    }

def book_shipment(order_id: str, carrier_id: str, service_level: str) -> Dict[str, Any]:
    """
    Books shipment with improved validation and tracking.
    """
    orders = st.session_state.context['orders']
    order = next((o for o in orders if o['order_id'] == order_id), None)
    
    if not order:
        return {'error': f"Order {order_id} not found"}
        
    shipping_options = st.session_state.context['shipping_options'][order['destination']]
    valid_option = next((opt for opt in shipping_options 
                        if opt['carrier_id'] == carrier_id 
                        and opt['service_level'] == service_level), None)
    
    if not valid_option:
        return {'error': f"Invalid carrier or service level for destination {order['destination']}"}
    
    tracking_number = f"TRACK_{datetime.now().strftime('%Y%m%d')}_{order_id}"
    
    return {
        'order_id': order_id,
        'tracking_number': tracking_number,
        'carrier_id': carrier_id,
        'service_level': service_level,
        'estimated_delivery': valid_option['estimated_days'],
        'status': 'Booked',
        'timestamp': datetime.now().isoformat()
    }

def send_order_update(customer_id: str, order_id: str, message: str) -> Dict[str, Any]:
    """
    Sends order updates with customer validation.
    """
    customers = st.session_state.context['customers']
    orders = st.session_state.context['orders']
    
    if customer_id not in customers:
        return {'error': f"Customer {customer_id} not found"}
        
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        return {'error': f"Order {order_id} not found"}
        
    if order.get('customer_id') != customer_id:
        return {'error': "Order does not belong to this customer"}
    
    return {
        'customer_id': customer_id,
        'order_id': order_id,
        'message': message,
        'timestamp': datetime.now().isoformat(),
        'status': 'sent'
    }

# Function mapping is necessary for the Streamlit app to recognize the functions
FUNCTION_MAPPING = {
    'get_inventory_status': get_inventory_status,
    'get_product_details': get_product_details,
    'update_inventory': update_inventory,
    'fetch_new_orders': fetch_new_orders,
    'allocate_stock': allocate_stock,
    'check_available_suppliers': check_available_suppliers,
    'place_purchase_order': place_purchase_order,
    'schedule_production_run': schedule_production_run,
    'calculate_shipping_options': calculate_shipping_options,
    'book_shipment': book_shipment,
    'send_order_update': send_order_update
}

# Sample scenarios are necessary definitions of tasks that can be performed using the functions and sample data (if ID is needed it needs to be present in Sample Data)
SAMPLE_SCENARIOS = [
    "Can we fulfill the current order ORD3001 from ElectroWorld completely from our inventory? If not, what's our shortfall?",
    "What shipping options are available for delivering to ElectroWorld in Los Angeles and which one is the fastest?",
    "Do we have enough COMP_X200 components and production capacity to manufacture the remaining units needed for order ORD3001?"
]