import random
from config import TRAFFIC_CONDITIONS, ALTERNATIVE_ROUTES
from google.genai import types

def check_traffic(route_id):
    """
    Check current traffic conditions on a specific route.
    Returns traffic status, delays, and any incidents.
    """
    if route_id not in TRAFFIC_CONDITIONS:
        return f"Error: Route '{route_id}' not found in traffic system"

    traffic_data = TRAFFIC_CONDITIONS[route_id]

    # Add some real-time variability
    current_delay = traffic_data["delay_minutes"] + random.randint(-5, 10)
    current_delay = max(0, current_delay)  # Can't have negative delay

    traffic_report = f"""
Traffic Status Report:
- Route ID: {route_id}
- Current Status: {traffic_data['status'].upper()}
- Expected Delay: {current_delay} minutes
- Conditions: {traffic_data['description']}
- Last Updated: {random.choice(['2 minutes ago', '5 minutes ago', '1 minute ago'])}
- Congestion Level: {_get_congestion_level(current_delay)}
- Recommendation: {_get_route_recommendation(current_delay)}
"""

    return traffic_report.strip()

def _get_congestion_level(delay_minutes):
    """Helper function to categorize congestion level"""
    if delay_minutes == 0:
        return "Clear"
    elif delay_minutes <= 10:
        return "Light"
    elif delay_minutes <= 20:
        return "Moderate"
    else:
        return "Heavy"

def _get_route_recommendation(delay_minutes):
    """Helper function to provide route recommendations"""
    if delay_minutes == 0:
        return "Proceed as planned"
    elif delay_minutes <= 15:
        return "Consider alternative if time-sensitive"
    else:
        return "STRONGLY RECOMMEND alternative route"

schema_check_traffic = types.FunctionDeclaration(
    name="check_traffic",
    description="Checks real-time traffic conditions on a specific route, including delays, incidents, and congestion levels. Critical for delivery time estimation and route planning.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "route_id": types.Schema(
                type=types.Type.STRING,
                description="The unique identifier of the route to check (e.g., 'route_001', 'route_002')",
            ),
        },
        required=["route_id"],
    ),
)

def calculate_alternative_route(current_route_id, destination):
    """
    Calculate alternative routes when the primary route has issues.
    Returns alternative options with time estimates.
    """
    if current_route_id not in ALTERNATIVE_ROUTES:
        return f"Error: No alternative routes available for '{current_route_id}'"

    alternatives = ALTERNATIVE_ROUTES[current_route_id]

    route_options = f"Alternative Route Analysis for {destination}:\n"
    route_options += f"Original Route: {current_route_id} (experiencing delays)\n\n"

    for i, alt_route in enumerate(alternatives, 1):
        # Get traffic data for alternative route
        if alt_route in TRAFFIC_CONDITIONS:
            traffic_data = TRAFFIC_CONDITIONS[alt_route]
            estimated_delay = traffic_data["delay_minutes"] + random.randint(-3, 7)
            estimated_delay = max(0, estimated_delay)
        else:
            estimated_delay = random.randint(0, 15)

        # Calculate estimated total time (base time + delay)
        base_time = random.randint(20, 45)  # Simulated base travel time
        total_time = base_time + estimated_delay

        route_options += f"Option {i}: {alt_route}\n"
        route_options += f"  - Base Travel Time: {base_time} minutes\n"
        route_options += f"  - Current Delay: {estimated_delay} minutes\n"
        route_options += f"  - Total Estimated Time: {total_time} minutes\n"
        route_options += f"  - Status: {_get_congestion_level(estimated_delay)}\n"
        route_options += f"  - Recommendation: {_get_route_recommendation(estimated_delay)}\n\n"

    # Find the best alternative
    best_route = min(alternatives, key=lambda r: TRAFFIC_CONDITIONS.get(r, {}).get("delay_minutes", 10))
    route_options += f"RECOMMENDED: {best_route} (fastest alternative)"

    return route_options

schema_calculate_alternative_route = types.FunctionDeclaration(
    name="calculate_alternative_route",
    description="Calculates and compares alternative routes when the primary route has traffic issues, accidents, or delays. Provides time estimates and recommendations.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "current_route_id": types.Schema(
                type=types.Type.STRING,
                description="The current route that has issues (e.g., 'route_002')",
            ),
            "destination": types.Schema(
                type=types.Type.STRING,
                description="The destination address or location name",
            ),
        },
        required=["current_route_id", "destination"],
    ),
)

def notify_passenger_and_driver(passenger_id, driver_id, message, new_route=None, updated_eta=None):
    """
    Send synchronized notifications to both passenger and driver about route changes,
    delays, or other important updates.
    """
    notification_details = f"""
Synchronized Notification Sent:
- Passenger ID: {passenger_id}
- Driver ID: {driver_id}
- Message: {message}
- Timestamp: {random.choice(['Now', '30 seconds ago', '1 minute ago'])}
"""

    if new_route:
        notification_details += f"- New Route: {new_route}\n"

    if updated_eta:
        notification_details += f"- Updated ETA: {updated_eta}\n"

    notification_details += """
Delivery Status:
- Passenger: Notification received and acknowledged
- Driver: Notification received, route updated in GPS
- System: Both parties synchronized
"""

    return notification_details.strip()

schema_notify_passenger_and_driver = types.FunctionDeclaration(
    name="notify_passenger_and_driver",
    description="Sends synchronized notifications to both passenger and driver about route changes, delays, or important updates. Ensures both parties have the same information.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "passenger_id": types.Schema(
                type=types.Type.STRING,
                description="The unique identifier of the passenger",
            ),
            "driver_id": types.Schema(
                type=types.Type.STRING,
                description="The unique identifier of the driver",
            ),
            "message": types.Schema(
                type=types.Type.STRING,
                description="The message to send to both parties",
            ),
            "new_route": types.Schema(
                type=types.Type.STRING,
                description="Optional new route information if route was changed",
            ),
            "updated_eta": types.Schema(
                type=types.Type.STRING,
                description="Optional updated estimated time of arrival",
            ),
        },
        required=["passenger_id", "driver_id", "message"],
    ),
)
