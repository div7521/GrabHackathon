import time
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

def check_traffic(route_id: str, include_incidents: bool = True, historical_comparison: bool = False) -> str:
    """
    Check real-time traffic conditions on a specific route.

    Args:
        route_id: Unique route identifier (e.g., 'route_001')
        include_incidents: Whether to include detailed incident information
        historical_comparison: Whether to include historical traffic patterns

    Returns:
        JSON string containing comprehensive traffic analysis
    """
    # Realistic delay for traffic API call + processing
    time.sleep(random.uniform(1.5, 3.5))

    # Basic validation
    if not route_id or not isinstance(route_id, str):
        return json.dumps({
            "status": "error",
            "error_code": "INVALID_ROUTE_ID",
            "message": "Route ID is required and must be a valid string",
            "timestamp": datetime.now().isoformat()
        }, indent=2)

    # Traffic conditions database
    traffic_conditions = {
        "route_001": {"base_delay": 5, "status": "light", "description": "Downtown to Airport"},
        "route_002": {"base_delay": 25, "status": "heavy", "description": "Cross-city via Highway"},
        "route_003": {"base_delay": 12, "status": "moderate", "description": "Mall Area to Business District"},
        "route_004": {"base_delay": 8, "status": "light", "description": "Residential Loop"},
        "route_005": {"base_delay": 18, "status": "moderate", "description": "Industrial Zone Route"}
    }

    if route_id not in traffic_conditions:
        return json.dumps({
            "status": "error",
            "error_code": "ROUTE_NOT_FOUND",
            "message": f"Route '{route_id}' not found in traffic monitoring system",
            "available_routes": list(traffic_conditions.keys()),
            "timestamp": datetime.now().isoformat()
        }, indent=2)

    route_data = traffic_conditions[route_id]
    current_time = datetime.now()
    current_hour = current_time.hour

    # Apply time-of-day traffic patterns
    base_delay = route_data["base_delay"]
    time_multiplier = 1.0

    # Rush hour adjustments
    if 7 <= current_hour <= 9 or 17 <= current_hour <= 19:
        time_multiplier = random.uniform(1.5, 2.2)
    elif 11 <= current_hour <= 14:  # Lunch time
        time_multiplier = random.uniform(1.2, 1.6)
    elif 22 <= current_hour or current_hour <= 5:  # Late night/early morning
        time_multiplier = random.uniform(0.5, 0.8)

    current_delay = int(base_delay * time_multiplier)

    # Generate incidents if requested
    incidents = []
    incident_delay = 0
    if include_incidents and random.random() < 0.3:  # 30% chance of incident
        incident_types = [
            {"type": "accident", "severity": "minor", "delay": random.randint(5, 15)},
            {"type": "accident", "severity": "major", "delay": random.randint(15, 40)},
            {"type": "construction", "severity": "moderate", "delay": random.randint(8, 20)},
            {"type": "road_closure", "severity": "major", "delay": random.randint(25, 60)},
            {"type": "weather", "severity": "minor", "delay": random.randint(3, 10)}
        ]

        incident = random.choice(incident_types)
        incident_delay = incident["delay"]
        incidents.append({
            "type": incident["type"],
            "severity": incident["severity"],
            "location": f"Km {random.randint(2, 15)} on {route_data['description']}",
            "delay_minutes": incident_delay,
            "reported_at": (current_time - timedelta(minutes=random.randint(5, 45))).isoformat(),
            "estimated_clearance": (current_time + timedelta(minutes=random.randint(10, 90))).isoformat()
        })

    total_delay = current_delay + incident_delay

    # Determine traffic level
    if total_delay <= 10:
        traffic_level = "light"
        traffic_color = "green"
    elif total_delay <= 25:
        traffic_level = "moderate"
        traffic_color = "yellow"
    else:
        traffic_level = "heavy"
        traffic_color = "red"

    # Historical comparison if requested
    historical_data = None
    if historical_comparison:
        historical_data = {
            "average_delay_this_hour": base_delay + random.randint(-3, 8),
            "average_delay_this_day": base_delay + random.randint(-5, 10),
            "comparison": "above_average" if total_delay > base_delay * 1.3 else "below_average" if total_delay < base_delay * 0.7 else "typical"
        }

    response_data = {
        "status": "success",
        "route_info": {
            "route_id": route_id,
            "description": route_data["description"],
            "distance_km": random.uniform(8.5, 35.2),
            "base_travel_time_minutes": random.randint(15, 45)
        },
        "traffic_conditions": {
            "current_delay_minutes": total_delay,
            "traffic_level": traffic_level,
            "traffic_color": traffic_color,
            "congestion_percentage": min(100, int((total_delay / 60) * 100)),
            "average_speed_kmh": max(10, random.randint(25, 80) - total_delay)
        },
        "incidents": incidents if include_incidents else [],
        "timing": {
            "estimated_travel_time": random.randint(15, 45) + total_delay,
            "estimated_arrival": (current_time + timedelta(minutes=random.randint(15, 45) + total_delay)).isoformat(),
            "last_updated": current_time.isoformat()
        },
        "recommendations": [
            "Consider alternative route" if total_delay > 20 else "Route conditions acceptable",
            "Allow extra time" if total_delay > 15 else "Normal travel time expected"
        ],
        "historical_data": historical_data,
        "metadata": {
            "response_time_ms": random.randint(1500, 3500),
            "data_freshness_minutes": random.randint(1, 5),
            "confidence_score": random.uniform(0.82, 0.96)
        }
    }

    return json.dumps(response_data, indent=2)


def calculate_alternative_route(primary_route_id: str, destination: str, urgency: str = "normal", vehicle_type: str = "car") -> str:
    """
    Calculate and compare alternative routes when primary route has issues.

    Args:
        primary_route_id: The original route with problems
        destination: Destination description for context
        urgency: Priority level ('low', 'normal', 'high', 'urgent')
        vehicle_type: Vehicle type for route optimization

    Returns:
        JSON string containing alternative route options with comparisons
    """
    # Realistic delay for route calculation + optimization
    time.sleep(random.uniform(2.0, 4.5))

    # Basic validation
    if not primary_route_id or not isinstance(primary_route_id, str):
        return json.dumps({
            "status": "error",
            "error_code": "INVALID_ROUTE_ID",
            "message": "Primary route ID is required",
            "timestamp": datetime.now().isoformat()
        }, indent=2)

    if not destination or not isinstance(destination, str):
        return json.dumps({
            "status": "error",
            "error_code": "INVALID_DESTINATION",
            "message": "Destination is required and must be a valid string",
            "timestamp": datetime.now().isoformat()
        }, indent=2)

    # Route alternatives database
    route_alternatives = {
        "route_001": ["route_003", "route_004"],
        "route_002": ["route_001", "route_005"],
        "route_003": ["route_001", "route_004"],
        "route_004": ["route_001", "route_003"],
        "route_005": ["route_002", "route_003"]
    }

    if primary_route_id not in route_alternatives:
        return json.dumps({
            "status": "error",
            "error_code": "NO_ALTERNATIVES_FOUND",
            "message": f"No alternative routes available for {primary_route_id}",
            "timestamp": datetime.now().isoformat()
        }, indent=2)

    alternative_route_ids = route_alternatives[primary_route_id]
    current_time = datetime.now()

    # Generate alternative route options
    alternatives = []
    for alt_route_id in alternative_route_ids:
        # Base route characteristics
        base_time = random.randint(20, 50)
        base_distance = random.uniform(10.5, 40.2)

        # Apply urgency adjustments
        if urgency == "urgent":
            time_penalty = random.randint(0, 5)  # Prioritize time
            distance_penalty = random.randint(0, 10)  # Less concern for distance
        elif urgency == "high":
            time_penalty = random.randint(0, 8)
            distance_penalty = random.randint(0, 6)
        else:
            time_penalty = random.randint(0, 12)
            distance_penalty = random.randint(0, 8)

        estimated_time = base_time + time_penalty
        estimated_distance = base_distance + (distance_penalty * 0.5)

        # Vehicle type adjustments
        if vehicle_type == "motorcycle":
            estimated_time = int(estimated_time * 0.8)  # Faster through traffic
        elif vehicle_type == "truck":
            estimated_time = int(estimated_time * 1.3)  # Slower, restricted routes

        # Traffic conditions for alternative
        traffic_delay = random.randint(2, 18)
        total_time = estimated_time + traffic_delay

        # Calculate route quality score
        time_score = max(0, 100 - (total_time * 1.5))
        distance_score = max(0, 100 - (estimated_distance * 2))
        traffic_score = max(0, 100 - (traffic_delay * 4))
        overall_score = (time_score + distance_score + traffic_score) / 3

        alternative = {
            "route_id": alt_route_id,
            "route_name": f"Alternative Route {alt_route_id[-1]}",
            "estimated_time_minutes": total_time,
            "estimated_distance_km": round(estimated_distance, 1),
            "traffic_delay_minutes": traffic_delay,
            "traffic_conditions": "light" if traffic_delay < 8 else "moderate" if traffic_delay < 15 else "heavy",
            "route_type": random.choice(["highway", "city_streets", "mixed"]),
            "toll_cost": random.uniform(0, 8.5) if random.random() < 0.4 else 0.0,
            "fuel_estimate": round(estimated_distance * random.uniform(0.08, 0.12), 2),
            "difficulty": random.choice(["easy", "moderate", "complex"]),
            "overall_score": round(overall_score, 1),
            "estimated_arrival": (current_time + timedelta(minutes=total_time)).isoformat()
        }
        alternatives.append(alternative)

    # Sort alternatives by overall score (best first)
    alternatives.sort(key=lambda x: x["overall_score"], reverse=True)

    # Find best options for different criteria
    fastest_route = min(alternatives, key=lambda x: x["estimated_time_minutes"])
    shortest_route = min(alternatives, key=lambda x: x["estimated_distance_km"])
    cheapest_route = min(alternatives, key=lambda x: x.get("toll_cost", 0))

    response_data = {
        "status": "success",
        "original_route": {
            "route_id": primary_route_id,
            "issues_detected": True,
            "estimated_delay": random.randint(20, 60)
        },
        "search_criteria": {
            "destination": destination,
            "urgency": urgency,
            "vehicle_type": vehicle_type,
            "search_timestamp": current_time.isoformat()
        },
        "alternatives": alternatives,
        "recommendations": {
            "best_overall": alternatives[0]["route_id"] if alternatives else None,
            "fastest_route": fastest_route["route_id"],
            "shortest_route": shortest_route["route_id"],
            "most_economical": cheapest_route["route_id"]
        },
        "summary": {
            "total_alternatives": len(alternatives),
            "average_time_savings": round(sum(60 - alt["estimated_time_minutes"] for alt in alternatives) / len(alternatives), 1) if alternatives else 0,
            "best_time_savings": 60 - alternatives[0]["estimated_time_minutes"] if alternatives else 0
        },
        "metadata": {
            "calculation_time_ms": random.randint(2000, 4500),
            "algorithm_version": "v2.1",
            "data_sources": ["traffic_api", "route_optimizer", "historical_patterns"]
        }
    }

    return json.dumps(response_data, indent=2)


def notify_passenger_and_driver(passenger_id: str, driver_id: str, message: str,
                               update_type: str = "route_change", include_eta: bool = True) -> str:
    """
    Send synchronized notifications to both passenger and driver about route changes or updates.

    Args:
        passenger_id: Unique passenger identifier
        driver_id: Unique driver identifier
        message: Update message content
        update_type: Type of update ('route_change', 'delay_alert', 'eta_update')
        include_eta: Whether to include ETA information

    Returns:
        JSON string containing synchronized notification delivery status
    """
    # Realistic delay for coordinated multi-party notification
    time.sleep(random.uniform(0.5, 1.8))

    # Basic validation
    if not passenger_id or not isinstance(passenger_id, str):
        return json.dumps({
            "status": "error",
            "error_code": "INVALID_PASSENGER_ID",
            "message": "Passenger ID is required and must be a valid string",
            "timestamp": datetime.now().isoformat()
        }, indent=2)

    if not driver_id or not isinstance(driver_id, str):
        return json.dumps({
            "status": "error",
            "error_code": "INVALID_DRIVER_ID",
            "message": "Driver ID is required and must be a valid string",
            "timestamp": datetime.now().isoformat()
        }, indent=2)

    if not message or len(message.strip()) < 3:
        return json.dumps({
            "status": "error",
            "error_code": "INVALID_MESSAGE",
            "message": "Message content must be at least 3 characters long",
            "timestamp": datetime.now().isoformat()
        }, indent=2)

    current_time = datetime.now()

    # Generate ETA information if requested
    eta_info = None
    if include_eta:
        eta_minutes = random.randint(8, 45)
        eta_info = {
            "estimated_arrival": (current_time + timedelta(minutes=eta_minutes)).isoformat(),
            "estimated_time_minutes": eta_minutes,
            "confidence_level": random.choice(["high", "medium", "low"])
        }

    # Simulate notification delivery to passenger
    passenger_delivery = {
        "passenger_id": passenger_id,
        "channels_attempted": ["in_app", "push_notification"],
        "delivery_status": {
            "in_app": {
                "delivered": True,
                "delivery_time_ms": random.randint(100, 400)
            },
            "push_notification": {
                "delivered": random.choice([True, True, False]),  # 67% success
                "delivery_time_ms": random.randint(200, 1200)
            }
        },
        "passenger_response": random.choice([
            {"acknowledged": True, "response_time_seconds": random.randint(15, 180)},
            {"acknowledged": False, "response_time_seconds": None}
        ])
    }

    # Simulate notification delivery to driver
    driver_delivery = {
        "driver_id": driver_id,
        "channels_attempted": ["driver_app", "voice_alert"],
        "delivery_status": {
            "driver_app": {
                "delivered": True,
                "delivery_time_ms": random.randint(80, 300)
            },
            "voice_alert": {
                "delivered": random.choice([True, False]),  # 50% have audio on
                "delivery_time_ms": random.randint(500, 2000)
            }
        },
        "driver_response": random.choice([
            {"acknowledged": True, "response_time_seconds": random.randint(5, 60)},
            {"acknowledged": False, "response_time_seconds": None}
        ])
    }

    # Check synchronization success
    passenger_delivered = any(status["delivered"] for status in passenger_delivery["delivery_status"].values())
    driver_delivered = any(status["delivered"] for status in driver_delivery["delivery_status"].values())
    synchronization_successful = passenger_delivered and driver_delivered

    response_data = {
        "status": "success",
        "notification_id": f"SYNC_{random.randint(100000, 999999)}",
        "message_details": {
            "content": message,
            "update_type": update_type,
            "character_count": len(message),
            "sent_timestamp": current_time.isoformat()
        },
        "eta_information": eta_info,
        "passenger_notification": passenger_delivery,
        "driver_notification": driver_delivery,
        "synchronization": {
            "successful": synchronization_successful,
            "both_parties_notified": passenger_delivered and driver_delivered,
            "delivery_time_difference_ms": abs(
                min(status.get("delivery_time_ms", 0) for status in passenger_delivery["delivery_status"].values()) -
                min(status.get("delivery_time_ms", 0) for status in driver_delivery["delivery_status"].values())
            )
        },
        "follow_up": {
            "retry_needed": not synchronization_successful,
            "escalation_required": not (passenger_delivered or driver_delivered),
            "next_check_scheduled": (current_time + timedelta(minutes=5)).isoformat() if not synchronization_successful else None
        },
        "analytics": {
            "passenger_engagement": "high" if passenger_delivery["passenger_response"]["acknowledged"] else "low",
            "driver_engagement": "high" if driver_delivery["driver_response"]["acknowledged"] else "low",
            "overall_success_rate": (int(passenger_delivered) + int(driver_delivered)) / 2
        },
        "metadata": {
            "processing_time_ms": random.randint(500, 1800),
            "coordination_complexity": "synchronized_delivery",
            "notification_priority": "high" if update_type == "route_change" else "normal"
        }
    }

    return json.dumps(response_data, indent=2)
