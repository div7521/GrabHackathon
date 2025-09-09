import time
import json
import random
from typing import Optional

def get_merchant_status(merchant_id: str) -> str:
    """Check the current operational status, preparation time, and alerts for a specific merchant.

    Args:
        merchant_id: Unique merchant identifier

    Returns:
        JSON string containing merchant status and preparation time information
    """
    time.sleep(random.uniform(0.1, 0.3))

    if not merchant_id:
        return json.dumps({
            "error": "INVALID_MERCHANT_ID",
            "message": "Merchant ID is required"
        })


    statuses = ["operational", "busy", "very_busy", "temporarily_closed"]
    status = random.choice(statuses)

    base_prep_time = random.randint(8, 25)
    if status == "busy":
        prep_time = base_prep_time + random.randint(5, 15)
    elif status == "very_busy":
        prep_time = base_prep_time + random.randint(15, 30)
    elif status == "temporarily_closed":
        prep_time = 0
    else:
        prep_time = base_prep_time

    return json.dumps({
        "merchant_id": merchant_id,
        "status": status,
        "preparation_time_minutes": prep_time,
        "capacity_level": random.randint(60, 100) if status != "temporarily_closed" else 0,
        "estimated_ready_time": f"{prep_time} minutes",
        "alerts": {
            "high_demand": status in ["busy", "very_busy"],
            "delays_expected": prep_time > 20
        }
    })

def get_nearby_merchants(location: str, cuisine_type: Optional[str] = None, max_distance: float = 5.0) -> str:
    """Find alternative merchants in the same geographical area that can fulfill similar orders.

    Args:
        location: Geographic area or address
        cuisine_type: Optional cuisine filter
        max_distance: Maximum search radius in kilometers

    Returns:
        JSON string containing list of nearby merchants with availability
    """
    time.sleep(random.uniform(0.2, 0.5))

    if not location:
        return json.dumps({
            "error": "INVALID_LOCATION",
            "message": "Location is required"
        })


    cuisines = ["asian", "italian", "mexican", "american", "indian", "thai", "chinese"]

    merchants = []
    for i in range(random.randint(3, 8)):
        merchant_cuisine = random.choice(cuisines)
        distance = round(random.uniform(0.2, max_distance), 1)
        prep_time = random.randint(10, 35)


        if cuisine_type and cuisine_type.lower() not in merchant_cuisine:
            continue

        merchants.append({
            "merchant_id": f"merchant_{random.randint(1000, 9999)}",
            "name": f"{merchant_cuisine.title()} {random.choice(['Express', 'Kitchen', 'Corner', 'House', 'Palace'])}",
            "cuisine_type": merchant_cuisine,
            "distance_km": distance,
            "preparation_time_minutes": prep_time,
            "rating": round(random.uniform(3.8, 4.9), 1),
            "availability": random.choice(["available", "busy", "very_busy"]),
            "estimated_delivery_time": prep_time + random.randint(15, 25)
        })

    return json.dumps({
        "location": location,
        "search_radius_km": max_distance,
        "cuisine_filter": cuisine_type,
        "total_results": len(merchants),
        "merchants": sorted(merchants, key=lambda x: x["distance_km"])
    })

def notify_customer(customer_id: str, message: str, compensation: Optional[str] = None) -> str:
    """Send proactive notifications to customers about order updates, delays, or compensation.

    Args:
        customer_id: Unique customer identifier
        message: Notification message content
        compensation: Optional compensation offer

    Returns:
        JSON string containing notification delivery status and customer response
    """
    time.sleep(random.uniform(0.1, 0.4))

    if not customer_id or not message:
        return json.dumps({
            "error": "MISSING_REQUIRED_FIELDS",
            "message": "Customer ID and message are required"
        })


    delivery_success = random.choice([True, True, True, False])
    channels = ["push_notification", "sms", "in_app"]
    delivered_channels = random.sample(channels, random.randint(1, 3)) if delivery_success else []

    customer_response = None
    if delivery_success and random.choice([True, False]):
        responses = [
            {"type": "acknowledgment", "message": "OK, thanks for letting me know"},
            {"type": "inquiry", "message": "How much longer will it take?"},
            {"type": "concern", "message": "This is the second delay this week"},
            {"type": "satisfaction", "message": "Appreciate the update"}
        ]
        customer_response = random.choice(responses)

    return json.dumps({
        "notification_id": f"notif_{random.randint(100000, 999999)}",
        "customer_id": customer_id,
        "message_sent": message,
        "compensation_offered": compensation,
        "delivery_status": "delivered" if delivery_success else "failed",
        "channels_used": delivered_channels,
        "customer_response": customer_response,
        "timestamp": "2024-01-15T10:30:00Z"
    })
