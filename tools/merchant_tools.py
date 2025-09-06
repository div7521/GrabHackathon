import time
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

def get_merchant_status(merchant_id: str) -> str:
    """
    Check the current status and preparation time of a specific merchant.

    Args:
        merchant_id: Unique merchant identifier (e.g., 'restaurant_001')

    Returns:
        JSON string containing merchant status, prep times, alerts, and recommendations
    """
    # Realistic delay for database lookup + kitchen analysis
    time.sleep(random.uniform(0.8, 2.0))

    # Basic validation
    if not merchant_id or not isinstance(merchant_id, str):
        return json.dumps({
            "status": "error",
            "error_code": "INVALID_MERCHANT_ID",
            "message": "Merchant ID is required and must be a valid string",
            "timestamp": datetime.now().isoformat()
        }, indent=2)

    # Simple merchant database
    merchants = {
        "restaurant_001": {"name": "Pizza Palace", "base_prep": 15, "status": "open", "location": "Downtown"},
        "restaurant_002": {"name": "Burger Barn", "base_prep": 25, "status": "open", "location": "Mall Area"},
        "restaurant_003": {"name": "Sushi Spot", "base_prep": 20, "status": "open", "location": "Business District"},
        "restaurant_004": {"name": "Taco Time", "base_prep": 12, "status": "open", "location": "Downtown"},
        "restaurant_005": {"name": "Thai Garden", "base_prep": 18, "status": "busy", "location": "Mall Area"},
    }

    if merchant_id not in merchants:
        return json.dumps({
            "status": "error",
            "error_code": "MERCHANT_NOT_FOUND",
            "message": f"Merchant '{merchant_id}' not found in system",
            "available_merchants": list(merchants.keys()),
            "timestamp": datetime.now().isoformat()
        }, indent=2)

    merchant = merchants[merchant_id]
    current_hour = datetime.now().hour

    # Calculate current prep time with simple time-of-day variation
    base_prep = merchant["base_prep"]
    time_multiplier = 1.0

    # Peak hours increase prep time
    if 11 <= current_hour <= 14 or 18 <= current_hour <= 21:
        time_multiplier = random.uniform(1.2, 1.8)
    elif merchant["status"] == "busy":
        time_multiplier = random.uniform(1.5, 2.2)

    current_prep = int(base_prep * time_multiplier)
    current_prep = max(5, current_prep)  # Minimum 5 minutes

    # Determine alert level
    alert_level = "normal"
    alert_message = "Normal operations"
    if current_prep > 35:
        alert_level = "critical"
        alert_message = "Kitchen overloaded - significant delays"
    elif current_prep > 25:
        alert_level = "warning"
        alert_message = "Higher than normal prep times"

    # Generate recommendations based on status
    recommendations = []
    if current_prep > 30:
        recommendations.extend([
            "Consider suggesting alternative merchants",
            "Proactive customer notification recommended",
            "Re-route drivers to avoid idle time"
        ])
    elif current_prep > 20:
        recommendations.append("Monitor kitchen status closely")

    response_data = {
        "status": "success",
        "merchant_info": {
            "merchant_id": merchant_id,
            "name": merchant["name"],
            "location": merchant["location"],
            "operational_status": merchant["status"]
        },
        "timing": {
            "base_prep_time_minutes": base_prep,
            "current_prep_time_minutes": current_prep,
            "estimated_ready_time": (datetime.now() + timedelta(minutes=current_prep)).isoformat(),
            "last_updated": datetime.now().isoformat()
        },
        "alerts": {
            "level": alert_level,
            "message": alert_message,
            "requires_action": current_prep > 25
        },
        "kitchen_metrics": {
            "active_orders": random.randint(2, 20),
            "kitchen_staff": random.randint(2, 6),
            "capacity_utilization": min(100, int((current_prep / base_prep) * 60))
        },
        "recommendations": recommendations,
        "metadata": {
            "response_time_ms": random.randint(800, 2000),
            "confidence_score": random.uniform(0.85, 0.98)
        }
    }

    return json.dumps(response_data, indent=2)


def get_nearby_merchants(location: str, cuisine_type: Optional[str] = None, max_distance_km: float = 5.0) -> str:
    """
    Find alternative merchants in the same area that can fulfill similar orders.

    Args:
        location: Geographic area (e.g., 'Downtown', 'Mall Area')
        cuisine_type: Optional cuisine filter (e.g., 'pizza', 'burger', 'asian')
        max_distance_km: Maximum search radius in kilometers

    Returns:
        JSON string containing list of alternative merchants with detailed information
    """
    # Realistic delay for geolocation query + database search
    time.sleep(random.uniform(1.0, 2.5))

    # Basic validation
    if not location or not isinstance(location, str):
        return json.dumps({
            "status": "error",
            "error_code": "INVALID_LOCATION",
            "message": "Location parameter is required and must be a non-empty string",
            "timestamp": datetime.now().isoformat()
        }, indent=2)

    # Location-based merchant mapping
    location_merchants = {
        "Downtown": [
            {"id": "restaurant_001", "name": "Pizza Palace", "prep": 15, "distance": 0.8, "cuisines": ["pizza", "italian"]},
            {"id": "restaurant_004", "name": "Taco Time", "prep": 12, "distance": 1.2, "cuisines": ["mexican", "latin"]},
            {"id": "restaurant_006", "name": "Noodle House", "prep": 18, "distance": 2.1, "cuisines": ["chinese", "asian"]}
        ],
        "Mall Area": [
            {"id": "restaurant_002", "name": "Burger Barn", "prep": 25, "distance": 0.5, "cuisines": ["burger", "american"]},
            {"id": "restaurant_005", "name": "Thai Garden", "prep": 18, "distance": 1.8, "cuisines": ["thai", "asian"]},
            {"id": "restaurant_007", "name": "Cafe Corner", "prep": 10, "distance": 1.5, "cuisines": ["coffee", "sandwiches"]}
        ],
        "Business District": [
            {"id": "restaurant_003", "name": "Sushi Spot", "prep": 20, "distance": 0.6, "cuisines": ["sushi", "japanese", "asian"]},
            {"id": "restaurant_008", "name": "Express Bites", "prep": 8, "distance": 1.0, "cuisines": ["fast food", "american"]},
            {"id": "restaurant_009", "name": "Healthy Bowl", "prep": 14, "distance": 2.3, "cuisines": ["healthy", "salads"]}
        ]
    }

    if location not in location_merchants:
        return json.dumps({
            "status": "error",
            "error_code": "LOCATION_NOT_FOUND",
            "message": f"No merchants found in location '{location}'",
            "available_locations": list(location_merchants.keys()),
            "timestamp": datetime.now().isoformat()
        }, indent=2)

    merchants = location_merchants[location]
    alternatives = []

    current_time = datetime.now()
    current_hour = current_time.hour

    for merchant in merchants:
        # Apply time-of-day variation
        base_prep = merchant["prep"]
        time_multiplier = 1.0

        if 11 <= current_hour <= 14 or 18 <= current_hour <= 21:
            time_multiplier = random.uniform(1.1, 1.6)

        current_prep = int(base_prep * time_multiplier)
        distance = merchant["distance"]

        # Filter by distance
        if distance > max_distance_km:
            continue

        # Filter by cuisine if specified
        cuisine_match = not cuisine_type or any(cuisine_type.lower() in cuisine.lower() for cuisine in merchant["cuisines"])
        if cuisine_type and not cuisine_match:
            continue

        # Calculate availability score
        prep_score = max(0, 100 - (current_prep * 2))
        distance_score = max(0, 100 - (distance * 15))
        overall_score = (prep_score + distance_score) / 2

        merchant_info = {
            "merchant_id": merchant["id"],
            "name": merchant["name"],
            "distance_km": distance,
            "prep_time_minutes": current_prep,
            "estimated_ready_time": (current_time + timedelta(minutes=current_prep)).isoformat(),
            "cuisines": merchant["cuisines"],
            "availability_score": round(overall_score, 1),
            "capacity_status": "high" if current_prep < 20 else "medium" if current_prep < 30 else "low",
            "estimated_delivery_time": current_prep + random.randint(15, 30),
            "rating": round(random.uniform(4.2, 4.8), 1)
        }
        alternatives.append(merchant_info)

    # Sort by availability score
    alternatives.sort(key=lambda x: x["availability_score"], reverse=True)

    response_data = {
        "status": "success",
        "search_criteria": {
            "location": location,
            "cuisine_type": cuisine_type,
            "max_distance_km": max_distance_km,
            "search_timestamp": datetime.now().isoformat()
        },
        "results": {
            "total_found": len(alternatives),
            "alternatives": alternatives[:8],  # Limit to top 8
            "has_more_results": len(alternatives) > 8
        },
        "recommendations": {
            "best_option": alternatives[0]["merchant_id"] if alternatives else None,
            "fastest_prep": min(alternatives, key=lambda x: x["prep_time_minutes"])["merchant_id"] if alternatives else None,
            "closest_distance": min(alternatives, key=lambda x: x["distance_km"])["merchant_id"] if alternatives else None
        },
        "metadata": {
            "query_time_ms": random.randint(1000, 2500),
            "data_sources": ["merchant_db", "location_service"]
        }
    }

    return json.dumps(response_data, indent=2)


def notify_customer(customer_id: str, message: str, compensation: Optional[str] = None,
                   notification_type: str = "proactive_update", priority: str = "normal") -> str:
    """
    Send proactive notifications to customers about order updates, delays, or issues.

    Args:
        customer_id: Unique customer identifier
        message: Notification message content
        compensation: Optional compensation offer (e.g., '$5 voucher', '20% discount')
        notification_type: Type of notification ('proactive_update', 'delay_alert', 'compensation')
        priority: Message priority ('low', 'normal', 'high', 'urgent')

    Returns:
        JSON string containing notification delivery status and customer response
    """
    # Realistic delay for multi-channel notification delivery
    time.sleep(random.uniform(0.3, 1.2))

    # Basic validation
    if not customer_id or not isinstance(customer_id, str):
        return json.dumps({
            "status": "error",
            "error_code": "INVALID_CUSTOMER_ID",
            "message": "Customer ID is required and must be a valid string",
            "timestamp": datetime.now().isoformat()
        }, indent=2)

    if not message or len(message.strip()) < 3:
        return json.dumps({
            "status": "error",
            "error_code": "INVALID_MESSAGE",
            "message": "Message content must be at least 3 characters long",
            "timestamp": datetime.now().isoformat()
        }, indent=2)

    # Simulate multi-channel delivery
    delivery_success_rate = 0.9 if priority in ["high", "urgent"] else 0.75
    channels_delivered = []

    # Always try in-app notification
    channels_delivered.append({
        "channel": "in_app",
        "delivered": True,
        "delivery_time_ms": random.randint(50, 200)
    })

    # Try push notification
    if random.random() < delivery_success_rate:
        channels_delivered.append({
            "channel": "push_notification",
            "delivered": True,
            "delivery_time_ms": random.randint(200, 1500)
        })

    # Try SMS for high/urgent priority
    if priority in ["high", "urgent"] and random.random() < 0.8:
        channels_delivered.append({
            "channel": "sms",
            "delivered": True,
            "delivery_time_ms": random.randint(500, 3000)
        })

    # Simulate customer response
    response_scenarios = [
        {"responded": True, "response": "Thanks for the update", "sentiment": "neutral"},
        {"responded": True, "response": "Okay, I'll wait", "sentiment": "positive"},
        {"responded": True, "response": "Can you suggest alternatives?", "sentiment": "concerned"},
        {"responded": False, "response": None, "sentiment": None}
    ]

    customer_response = random.choice(response_scenarios)

    # Handle compensation if offered
    compensation_status = None
    if compensation:
        compensation_status = {
            "offered": True,
            "type": compensation,
            "accepted": random.choice([True, True, False]),  # 67% acceptance rate
            "estimated_value": random.uniform(3.0, 12.0)
        }

    response_data = {
        "status": "success",
        "notification_id": f"NOTIF_{random.randint(100000, 999999)}",
        "customer_info": {
            "customer_id": customer_id,
            "preferred_channels": ["in_app", "push_notification"]
        },
        "message_details": {
            "content": message,
            "type": notification_type,
            "priority": priority,
            "character_count": len(message),
            "sent_timestamp": datetime.now().isoformat()
        },
        "delivery_status": {
            "overall_success": len(channels_delivered) > 0,
            "channels_delivered": channels_delivered,
            "primary_channel": "in_app",
            "total_channels_attempted": len(channels_delivered)
        },
        "customer_response": customer_response,
        "compensation": compensation_status,
        "follow_up": {
            "required": customer_response.get("response") and "alternative" in customer_response.get("response", "").lower(),
            "escalation_needed": priority == "urgent" and len(channels_delivered) == 0
        },
        "metadata": {
            "processing_time_ms": random.randint(300, 1200),
            "delivery_success_rate": len([ch for ch in channels_delivered if ch["delivered"]]) / max(1, len(channels_delivered))
        }
    }

    return json.dumps(response_data, indent=2)
