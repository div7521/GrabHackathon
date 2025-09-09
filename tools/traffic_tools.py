import time
import json
import random

def check_traffic(route_id: str) -> str:
    """Check real-time traffic conditions on a specific route.

    Args:
        route_id: Unique route identifier

    Returns:
        JSON string containing traffic conditions and delay information
    """
    time.sleep(random.uniform(0.1, 0.3))

    if not route_id:
        return json.dumps({
            "error": "INVALID_ROUTE_ID",
            "message": "Route ID is required"
        })


    traffic_levels = ["light", "moderate", "heavy", "severe"]
    traffic_level = random.choice(traffic_levels)

    if traffic_level == "light":
        delay_minutes = random.randint(0, 5)
    elif traffic_level == "moderate":
        delay_minutes = random.randint(5, 15)
    elif traffic_level == "heavy":
        delay_minutes = random.randint(15, 30)
    else:
        delay_minutes = random.randint(30, 60)


    incidents = []
    if random.choice([True, False, False]):
        incident_types = ["accident", "construction", "road_closure", "weather"]
        incidents.append({
            "type": random.choice(incident_types),
            "location": f"Km {random.randint(1, 20)} on route {route_id}",
            "severity": random.choice(["minor", "moderate", "major"]),
            "estimated_clearance": f"{random.randint(15, 90)} minutes"
        })

    return json.dumps({
        "route_id": route_id,
        "traffic_level": traffic_level,
        "delay_minutes": delay_minutes,
        "average_speed_kmh": random.randint(15, 80),
        "distance_km": round(random.uniform(5.0, 25.0), 1),
        "estimated_travel_time": random.randint(10, 45) + delay_minutes,
        "incidents": incidents,
        "last_updated": "2024-01-15T10:30:00Z",
        "confidence": random.choice(["high", "medium", "low"])
    })

def calculate_alternative_route(route_id: str, destination: str, urgency: str = "normal") -> str:
    """Calculate and compare alternative routes when the primary route has traffic issues.

    Args:
        route_id: The original route with problems
        destination: Destination description
        urgency: Priority level ('low', 'normal', 'high', 'urgent')

    Returns:
        JSON string containing alternative route options with time estimates
    """
    time.sleep(random.uniform(0.2, 0.5))

    if not route_id or not destination:
        return json.dumps({
            "error": "MISSING_REQUIRED_FIELDS",
            "message": "Route ID and destination are required"
        })


    num_alternatives = random.randint(2, 4)
    alternatives = []

    for i in range(num_alternatives):
        base_time = random.randint(15, 50)
        if urgency == "urgent":
            time_factor = 0.8
        elif urgency == "high":
            time_factor = 0.9
        else:
            time_factor = 1.0

        route_time = int(base_time * time_factor)

        alternatives.append({
            "route_id": f"alt_route_{i+1}",
            "description": f"Alternative via {random.choice(['Highway A', 'City Center', 'Bypass Road', 'Express Lane'])}",
            "estimated_time_minutes": route_time,
            "distance_km": round(random.uniform(8.0, 30.0), 1),
            "traffic_level": random.choice(["light", "moderate", "heavy"]),
            "toll_cost": round(random.uniform(0, 12.50), 2) if random.choice([True, False]) else 0.0,
            "road_type": random.choice(["highway", "city_streets", "mixed"]),
            "recommendation_score": random.randint(60, 95)
        })


    alternatives.sort(key=lambda x: x["estimated_time_minutes"])

    return json.dumps({
        "original_route": route_id,
        "destination": destination,
        "urgency_level": urgency,
        "alternatives_found": len(alternatives),
        "recommended_route": alternatives[0]["route_id"] if alternatives else None,
        "alternative_routes": alternatives,
        "calculation_time": "2024-01-15T10:30:00Z"
    })

def notify_passenger_and_driver(passenger_id: str, driver_id: str, message: str) -> str:
    """Send synchronized notifications to both passenger and driver about route changes.

    Args:
        passenger_id: Unique passenger identifier
        driver_id: Unique driver identifier
        message: Update message content

    Returns:
        JSON string containing notification delivery status for both parties
    """
    time.sleep(random.uniform(0.1, 0.4))

    if not passenger_id or not driver_id or not message:
        return json.dumps({
            "error": "MISSING_REQUIRED_FIELDS",
            "message": "Passenger ID, driver ID, and message are required"
        })


    passenger_delivery = random.choice([True, True, False])
    passenger_channels = ["in_app", "sms"] if passenger_delivery else []


    driver_delivery = random.choice([True, True, True, False])
    driver_channels = ["driver_app", "voice_alert"] if driver_delivery else []


    passenger_response = None
    if passenger_delivery and random.choice([True, False]):
        passenger_response = random.choice([
            "Understood, thank you",
            "How much longer?",
            "OK",
            "Thanks for the update"
        ])

    driver_response = None
    if driver_delivery and random.choice([True, False]):
        driver_response = random.choice([
            "Acknowledged",
            "Route updated",
            "Copy that",
            "Understood"
        ])

    return json.dumps({
        "notification_id": f"sync_{random.randint(100000, 999999)}",
        "message_sent": message,
        "passenger_notification": {
            "passenger_id": passenger_id,
            "delivery_status": "delivered" if passenger_delivery else "failed",
            "channels_used": passenger_channels,
            "response": passenger_response
        },
        "driver_notification": {
            "driver_id": driver_id,
            "delivery_status": "delivered" if driver_delivery else "failed",
            "channels_used": driver_channels,
            "response": driver_response
        },
        "synchronization_successful": passenger_delivery and driver_delivery,
        "timestamp": "2024-01-15T10:30:00Z"
    })
