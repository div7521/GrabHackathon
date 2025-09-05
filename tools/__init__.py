# Tools package for Project Synapse
# Complete integration of all agentic tools

# Merchant Tools
from .merchant_tools import (
    get_merchant_status, 
    get_nearby_merchants, 
    notify_customer,
    schema_get_merchant_status,
    schema_get_nearby_merchants, 
    schema_notify_customer
)

# Traffic Tools
from .traffic_tools import (
    check_traffic,
    calculate_alternative_route,
    notify_passenger_and_driver,
    schema_check_traffic,
    schema_calculate_alternative_route,
    schema_notify_passenger_and_driver
)

# Customer Tools
from .customer_tools import (
    contact_recipient_via_chat,
    issue_instant_refund,
    schema_contact_recipient_via_chat,
    schema_issue_instant_refund
)

# Driver Tools
from .driver_tools import (
    re_route_driver,
    exonerate_driver,
    schema_re_route_driver,
    schema_exonerate_driver
)

# Mediation Tools
from .mediation_tools import (
    initiate_mediation_flow,
    collect_evidence,
    analyze_evidence,
    schema_initiate_mediation_flow,
    schema_collect_evidence,
    schema_analyze_evidence
)

# Logistics Tools
from .logistics_tools import (
    suggest_safe_drop_off,
    find_nearby_locker,
    log_merchant_packaging_feedback,
    schema_suggest_safe_drop_off,
    schema_find_nearby_locker,
    schema_log_merchant_packaging_feedback
)

# Flight Tools
from .flight_tools import (
    check_flight_status,
    schema_check_flight_status
)

# Dictionary of all available tools and their functions
AVAILABLE_TOOLS = {
    # Merchant Tools
    "get_merchant_status": get_merchant_status,
    "get_nearby_merchants": get_nearby_merchants,
    "notify_customer": notify_customer,
    
    # Traffic Tools
    "check_traffic": check_traffic,
    "calculate_alternative_route": calculate_alternative_route,
    "notify_passenger_and_driver": notify_passenger_and_driver,
    
    # Customer Tools
    "contact_recipient_via_chat": contact_recipient_via_chat,
    "issue_instant_refund": issue_instant_refund,
    
    # Driver Tools
    "re_route_driver": re_route_driver,
    "exonerate_driver": exonerate_driver,
    
    # Mediation Tools
    "initiate_mediation_flow": initiate_mediation_flow,
    "collect_evidence": collect_evidence,
    "analyze_evidence": analyze_evidence,
    
    # Logistics Tools
    "suggest_safe_drop_off": suggest_safe_drop_off,
    "find_nearby_locker": find_nearby_locker,
    "log_merchant_packaging_feedback": log_merchant_packaging_feedback,
    
    # Flight Tools
    "check_flight_status": check_flight_status,
}

# List of all tool schemas for Gemini
TOOL_SCHEMAS = [
    # Merchant Schemas
    schema_get_merchant_status,
    schema_get_nearby_merchants,
    schema_notify_customer,
    
    # Traffic Schemas
    schema_check_traffic,
    schema_calculate_alternative_route,
    schema_notify_passenger_and_driver,
    
    # Customer Schemas
    schema_contact_recipient_via_chat,
    schema_issue_instant_refund,
    
    # Driver Schemas
    schema_re_route_driver,
    schema_exonerate_driver,
    
    # Mediation Schemas
    schema_initiate_mediation_flow,
    schema_collect_evidence,
    schema_analyze_evidence,
    
    # Logistics Schemas
    schema_suggest_safe_drop_off,
    schema_find_nearby_locker,
    schema_log_merchant_packaging_feedback,
    
    # Flight Schemas
    schema_check_flight_status,
]

# Export everything for easy importing
__all__ = [
    'AVAILABLE_TOOLS', 
    'TOOL_SCHEMAS',
    
    # Merchant tools
    'get_merchant_status',
    'get_nearby_merchants', 
    'notify_customer',
    
    # Traffic tools
    'check_traffic',
    'calculate_alternative_route',
    'notify_passenger_and_driver',
    
    # Customer tools
    'contact_recipient_via_chat',
    'issue_instant_refund',
    
    # Driver tools
    're_route_driver',
    'exonerate_driver',
    
    # Mediation tools
    'initiate_mediation_flow',
    'collect_evidence',
    'analyze_evidence',
    
    # Logistics tools
    'suggest_safe_drop_off',
    'find_nearby_locker',
    'log_merchant_packaging_feedback',
    
    # Flight tools
    'check_flight_status',
]