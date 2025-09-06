# Tools package for Project Synapse
# Complete integration of all agentic tools with LangChain compatibility

from langchain_core.tools import StructuredTool

# Merchant Tools
from .merchant_tools import (
    get_merchant_status,
    get_nearby_merchants,
    notify_customer
)

# Traffic Tools
from .traffic_tools import (
    check_traffic,
    calculate_alternative_route,
    notify_passenger_and_driver
)

# Customer Tools
from .customer_tools import (
    contact_recipient_via_chat,
    issue_instant_refund
)

# Driver Tools
from .driver_tools import (
    re_route_driver,
    exonerate_driver
)

# Mediation Tools
from .mediation_tools import (
    initiate_mediation_flow,
    collect_evidence,
    analyze_evidence
)

# Logistics Tools
from .logistic_tools import (
    suggest_safe_drop_off,
    find_nearby_locker,
    log_merchant_packaging_feedback
)

# Flight Tools
from .flight_tools import (
    check_flight_status
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

def get_langchain_tools():
    """Convert all tools to LangChain StructuredTool format"""
    langchain_tools = []

    # Merchant Tools
    langchain_tools.extend([
        StructuredTool.from_function(
            func=get_merchant_status,
            name="get_merchant_status",
            description="Retrieves the current operational status, preparation time, and alerts for a specific merchant/restaurant. Essential for assessing delivery delays and making proactive decisions."
        ),
        StructuredTool.from_function(
            func=get_nearby_merchants,
            name="get_nearby_merchants",
            description="Finds alternative merchants in the same geographical area that can fulfill similar orders. Useful when the primary merchant has delays or issues."
        ),
        StructuredTool.from_function(
            func=notify_customer,
            name="notify_customer",
            description="Sends proactive notifications to customers about order updates, delays, issues, or compensation offers. Essential for maintaining customer satisfaction during disruptions."
        )
    ])

    # Traffic Tools
    langchain_tools.extend([
        StructuredTool.from_function(
            func=check_traffic,
            name="check_traffic",
            description="Checks real-time traffic conditions on a specific route, including delays, incidents, and congestion levels. Critical for delivery time estimation and route planning."
        ),
        StructuredTool.from_function(
            func=calculate_alternative_route,
            name="calculate_alternative_route",
            description="Calculates and compares alternative routes when the primary route has traffic issues, accidents, or delays. Provides time estimates and recommendations."
        ),
        StructuredTool.from_function(
            func=notify_passenger_and_driver,
            name="notify_passenger_and_driver",
            description="Sends synchronized notifications to both passenger and driver about route changes, delays, or important updates. Ensures both parties have the same information."
        )
    ])

    # Customer Tools
    langchain_tools.extend([
        StructuredTool.from_function(
            func=contact_recipient_via_chat,
            name="contact_recipient_via_chat",
            description="Initiates real-time chat communication with the package recipient to resolve delivery issues, get instructions, or coordinate alternative arrangements."
        ),
        StructuredTool.from_function(
            func=issue_instant_refund,
            name="issue_instant_refund",
            description="Processes immediate refunds for service failures, order issues, or customer satisfaction problems. Provides quick resolution and maintains customer loyalty."
        )
    ])

    # Driver Tools
    langchain_tools.extend([
        StructuredTool.from_function(
            func=re_route_driver,
            name="re_route_driver",
            description="Assigns drivers to alternative tasks or short deliveries during wait times to optimize their earning potential and reduce idle time."
        ),
        StructuredTool.from_function(
            func=exonerate_driver,
            name="exonerate_driver",
            description="Clears drivers from fault claims when evidence shows they are not responsible for issues. Protects driver ratings and income."
        )
    ])

    # Mediation Tools
    langchain_tools.extend([
        StructuredTool.from_function(
            func=initiate_mediation_flow,
            name="initiate_mediation_flow",
            description="Starts real-time dispute resolution process between customers and drivers. Opens synchronized interface on both parties' devices for fair conflict resolution."
        ),
        StructuredTool.from_function(
            func=collect_evidence,
            name="collect_evidence",
            description="Guides structured evidence collection during disputes. Prompts both parties to provide photos, descriptions, and answers to relevant questions."
        ),
        StructuredTool.from_function(
            func=analyze_evidence,
            name="analyze_evidence",
            description="AI-powered analysis of collected evidence to determine fault and recommend fair resolutions. Processes photos, testimonies, and context to make objective decisions."
        )
    ])

    # Logistics Tools
    langchain_tools.extend([
        StructuredTool.from_function(
            func=suggest_safe_drop_off,
            name="suggest_safe_drop_off",
            description="Recommends secure alternative delivery locations when recipients are unavailable. Considers package value, security requirements, and convenience."
        ),
        StructuredTool.from_function(
            func=find_nearby_locker,
            name="find_nearby_locker",
            description="Locates secure parcel locker facilities near the delivery address for safe package storage when other drop-off options aren't available."
        ),
        StructuredTool.from_function(
            func=log_merchant_packaging_feedback,
            name="log_merchant_packaging_feedback",
            description="Reports packaging quality issues to merchants with evidence-backed recommendations for improvement. Helps prevent future damage incidents."
        )
    ])

    # Flight Tools
    langchain_tools.extend([
        StructuredTool.from_function(
            func=check_flight_status,
            name="check_flight_status",
            description="Checks real-time flight status information for airport trips. Helps assess passenger urgency and adjust service priorities accordingly."
        )
    ])

    return langchain_tools

# Export everything for easy importing
__all__ = [
    'AVAILABLE_TOOLS',
    'get_langchain_tools',

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
