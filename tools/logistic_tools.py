import time
import json
import random

def suggest_safe_drop_off(package_id: str, location: str, reason: str, value: float) -> str:
    """Recommend secure alternative delivery locations when recipients are unavailable.

    Args:
        package_id: Unique package identifier
        location: Current delivery location
        reason: Reason recipient is unavailable
        value: Estimated value of package for security assessment

    Returns:
        JSON string containing secure drop-off location recommendations
    """
    time.sleep(random.uniform(0.1, 0.4))

    if not all([package_id, location, reason]):
        return json.dumps({
            "error": "MISSING_REQUIRED_FIELDS",
            "message": "Package ID, location, and reason are required"
        })

    if value < 0:
        return json.dumps({
            "error": "INVALID_VALUE",
            "message": "Package value must be non-negative"
        })


    if value > 200:
        security_level = "high"
    elif value > 50:
        security_level = "medium"
    else:
        security_level = "standard"


    drop_off_options = []


    base_options = [
        {
            "option_id": f"dropoff_{random.randint(1000, 9999)}",
            "type": "building_concierge",
            "name": "Building Concierge/Reception",
            "address": f"{location} - Main Lobby",
            "distance_meters": random.randint(10, 50),
            "security_rating": "high",
            "operating_hours": "24/7" if random.choice([True, False]) else "8 AM - 8 PM",
            "requires_id": True,
            "storage_duration_hours": 72,
            "fee": 0.0
        },
        {
            "option_id": f"dropoff_{random.randint(1000, 9999)}",
            "type": "neighbor_delivery",
            "name": "Trusted Neighbor",
            "address": f"{location} - Adjacent Unit",
            "distance_meters": random.randint(5, 30),
            "security_rating": "medium",
            "operating_hours": "9 AM - 6 PM",
            "requires_id": False,
            "storage_duration_hours": 24,
            "fee": 0.0
        },
        {
            "option_id": f"dropoff_{random.randint(1000, 9999)}",
            "type": "parcel_shop",
            "name": "Nearby Parcel Collection Point",
            "address": f"500m from {location}",
            "distance_meters": random.randint(300, 800),
            "security_rating": "high",
            "operating_hours": "10 AM - 9 PM",
            "requires_id": True,
            "storage_duration_hours": 168,
            "fee": round(random.uniform(1.50, 3.50), 2)
        }
    ]


    for option in base_options:
        security_adequate = True

        if security_level == "high" and option["security_rating"] not in ["high"]:
            security_adequate = False

        if security_adequate:

            security_score = {"high": 3, "medium": 2, "standard": 1}[option["security_rating"]]
            distance_score = max(1, 4 - (option["distance_meters"] / 200))
            fee_score = max(1, 4 - option["fee"])

            recommendation_score = (security_score + distance_score + fee_score) / 3
            option["recommendation_score"] = round(recommendation_score, 1)

            drop_off_options.append(option)


    drop_off_options.sort(key=lambda x: x["recommendation_score"], reverse=True)


    risk_level = "high" if value > 200 else "medium" if value > 50 else "low"

    return json.dumps({
        "package_id": package_id,
        "current_location": location,
        "recipient_unavailable_reason": reason,
        "package_value": value,
        "security_level_required": security_level,
        "risk_assessment": risk_level,
        "drop_off_options": drop_off_options[:5],
        "recommended_option": drop_off_options[0]["option_id"] if drop_off_options else None,
        "recipient_notification": {
            "notification_required": True,
            "notification_methods": ["sms", "email", "in_app"],
            "pickup_instructions_provided": True
        },
        "insurance_coverage": value <= 1000,
        "timestamp": "2024-01-15T10:30:00Z"
    })

def find_nearby_locker(address: str, max_distance: float, package_size: str) -> str:
    """Locate secure parcel locker facilities near the delivery address for safe package storage.

    Args:
        address: Target delivery address or area
        max_distance: Maximum search radius in kilometers
        package_size: Package size category ('small', 'medium', 'large', 'extra_large')

    Returns:
        JSON string containing nearby locker locations with availability and booking details
    """
    time.sleep(random.uniform(0.1, 0.3))

    if not all([address, package_size]):
        return json.dumps({
            "error": "MISSING_REQUIRED_FIELDS",
            "message": "Address and package size are required"
        })

    if max_distance <= 0:
        return json.dumps({
            "error": "INVALID_DISTANCE",
            "message": "Maximum distance must be greater than zero"
        })


    size_specs = {
        "small": {"max_dimensions": "30x20x15 cm", "locker_type": "S"},
        "medium": {"max_dimensions": "40x30x25 cm", "locker_type": "M"},
        "large": {"max_dimensions": "60x40x40 cm", "locker_type": "L"},
        "extra_large": {"max_dimensions": "80x60x50 cm", "locker_type": "XL"}
    }

    if package_size not in size_specs:
        return json.dumps({
            "error": "INVALID_PACKAGE_SIZE",
            "message": f"Package size must be one of: {list(size_specs.keys())}"
        })

    required_locker_type = size_specs[package_size]["locker_type"]


    locker_networks = ["SecureBox", "ParcelHub", "PickupPoint", "LockerNet"]
    nearby_lockers = []

    num_lockers = random.randint(2, 6)
    for i in range(num_lockers):
        distance = round(random.uniform(0.2, max_distance), 1)
        network = random.choice(locker_networks)


        total_lockers = {"S": 20, "M": 15, "L": 10, "XL": 5}
        available_lockers = {
            size: random.randint(0, total_lockers[size])
            for size in total_lockers
        }


        if available_lockers[required_locker_type] == 0:
            continue

        locker_info = {
            "locker_id": f"LOC_{random.randint(1000, 9999)}",
            "network": network,
            "name": f"{network} Station {chr(65 + i)}",
            "address": f"{random.randint(100, 999)} {random.choice(['Main St', 'Oak Ave', 'Park Rd', 'Center Blvd'])}",
            "distance_km": distance,
            "operating_hours": random.choice(["24/7", "6 AM - 11 PM", "8 AM - 10 PM"]),
            "locker_availability": {
                "total_units": total_lockers,
                "available_units": available_lockers,
                "required_size_available": available_lockers[required_locker_type]
            },
            "pricing": {
                "S": 2.50,
                "M": 3.50,
                "L": 5.00,
                "XL": 7.50
            },
            "rental_cost": {
                "S": 2.50,
                "M": 3.50,
                "L": 5.00,
                "XL": 7.50
            }[required_locker_type],
            "max_storage_days": random.choice([5, 7, 10]),
            "security_features": ["CCTV", "secure_access", "climate_controlled"],
            "accessibility": random.choice(["wheelchair_accessible", "stairs_only"]),
            "payment_methods": ["credit_card", "digital_wallet"]
        }


        distance_score = max(0, 5 - distance)
        availability_score = min(5, available_lockers[required_locker_type])
        price_score = max(0, 5 - (locker_info["rental_cost"] / 2))
        hours_score = 5 if locker_info["operating_hours"] == "24/7" else 3

        locker_info["convenience_score"] = round(
            (distance_score + availability_score + price_score + hours_score) / 4, 1
        )

        nearby_lockers.append(locker_info)


    nearby_lockers.sort(key=lambda x: x["convenience_score"], reverse=True)

    if not nearby_lockers:
        return json.dumps({
            "status": "no_lockers_found",
            "address": address,
            "search_radius_km": max_distance,
            "package_size": package_size,
            "message": "No suitable lockers found within search radius",
            "suggestions": [
                "Increase search radius",
                "Consider smaller package size",
                "Try again later for availability updates"
            ]
        })

    return json.dumps({
        "search_parameters": {
            "address": address,
            "max_distance_km": max_distance,
            "package_size": package_size,
            "required_locker_type": required_locker_type,
            "package_dimensions": size_specs[package_size]["max_dimensions"]
        },
        "results": {
            "total_lockers_found": len(nearby_lockers),
            "lockers_with_availability": len(nearby_lockers),
            "recommended_locker": nearby_lockers[0]["locker_id"] if nearby_lockers else None,
            "locker_options": nearby_lockers[:5]
        },
        "booking_process": {
            "steps": [
                "Select preferred locker location",
                "Choose rental duration",
                "Complete payment",
                "Receive access code via SMS",
                "Package delivery to locker",
                "Pickup using access code"
            ],
            "estimated_setup_time": "2-3 minutes",
            "customer_support": "+65-1800-LOCKER"
        },
        "service_benefits": {
            "24_7_access": any(loc["operating_hours"] == "24/7" for loc in nearby_lockers),
            "secure_storage": True,
            "contactless_pickup": True,
            "weather_protection": True,
            "extended_storage": max((loc["max_storage_days"] for loc in nearby_lockers), default=0)
        },
        "timestamp": "2024-01-15T10:30:00Z"
    })

def log_merchant_packaging_feedback(merchant_id: str, incident_id: str, issue_type: str) -> str:
    """Report packaging quality issues to merchants with evidence-backed recommendations.

    Args:
        merchant_id: Unique merchant identifier
        incident_id: Related incident or order identifier
        issue_type: Type of packaging problem

    Returns:
        JSON string containing feedback logging status and merchant communication details
    """
    time.sleep(random.uniform(0.2, 0.5))

    if not all([merchant_id, incident_id, issue_type]):
        return json.dumps({
            "error": "MISSING_REQUIRED_FIELDS",
            "message": "Merchant ID, incident ID, and issue type are required"
        })

    feedback_id = f"feedback_{random.randint(100000, 999999)}"


    issue_categories = {
        "insufficient_protection": {
            "severity": "medium",
            "description": "Items inadequately protected during transport",
            "business_impact": "customer_complaints",
            "suggested_improvements": [
                "Use additional bubble wrap or cushioning",
                "Switch to thicker packaging containers",
                "Add protective corners for fragile items"
            ]
        },
        "poor_sealing": {
            "severity": "high",
            "description": "Package seals failed during delivery",
            "business_impact": "item_damage",
            "suggested_improvements": [
                "Use higher quality packaging tape",
                "Ensure proper closure technique",
                "Double-seal high-value items"
            ]
        },
        "wrong_container_size": {
            "severity": "low",
            "description": "Container size inappropriate for contents",
            "business_impact": "cost_inefficiency",
            "suggested_improvements": [
                "Use appropriately sized containers",
                "Avoid excessive packaging for small items",
                "Consider custom packaging for irregular items"
            ]
        },
        "liquid_spillage": {
            "severity": "critical",
            "description": "Liquid items improperly contained causing spillage",
            "business_impact": "health_safety",
            "suggested_improvements": [
                "Double-bag all liquid items",
                "Use leak-proof containers",
                "Secure all caps and lids properly"
            ]
        },
        "temperature_sensitive": {
            "severity": "high",
            "description": "Temperature-sensitive items inadequately packaged",
            "business_impact": "food_safety",
            "suggested_improvements": [
                "Use appropriate insulation for hot/cold items",
                "Include proper cooling packs",
                "Package temperature-sensitive items last"
            ]
        }
    }

    issue_details = issue_categories.get(issue_type, {
        "severity": "medium",
        "description": "General packaging quality issue",
        "business_impact": "customer_experience",
        "suggested_improvements": [
            "Review current packaging standards",
            "Implement quality control checks"
        ]
    })


    merchant_profile = {
        "merchant_id": merchant_id,
        "merchant_category": random.choice(["restaurant", "grocery", "pharmacy", "retail"]),
        "packaging_history": {
            "previous_incidents": random.randint(0, 5),
            "last_incident_date": "2024-01-10T14:30:00Z" if random.choice([True, False]) else None,
            "packaging_score": round(random.uniform(3.5, 4.8), 1),
            "improvement_trend": random.choice(["improving", "stable", "declining"])
        }
    }


    communication_priority = "high" if issue_details["severity"] in ["high", "critical"] else "normal"

    notification_plan = {
        "merchant_notification": {
            "priority": communication_priority,
            "delivery_method": "merchant_app",
            "expected_response_time": "2 hours" if communication_priority == "high" else "24 hours",
            "language": "english",
            "include_photos": True,
            "include_improvement_suggestions": True
        },
        "follow_up_required": issue_details["severity"] in ["high", "critical"],
        "training_recommended": merchant_profile["packaging_history"]["previous_incidents"] > 2
    }


    impact_assessment = {
        "customer_impact": {
            "satisfaction_effect": "negative" if issue_details["severity"] in ["high", "critical"] else "minor",
            "reorder_likelihood": random.uniform(0.3, 0.8),
            "compensation_required": issue_details["severity"] in ["high", "critical"]
        },
        "business_impact": {
            "cost_estimate": round(random.uniform(5, 50), 2),
            "reputation_risk": issue_details["business_impact"],
            "operational_disruption": issue_details["severity"]
        },
        "frequency_analysis": {
            "similar_incidents_30_days": merchant_profile["packaging_history"]["previous_incidents"],
            "trend": merchant_profile["packaging_history"]["improvement_trend"],
            "recurring_issue": merchant_profile["packaging_history"]["previous_incidents"] > 3
        }
    }

    return json.dumps({
        "status": "feedback_logged",
        "feedback_id": feedback_id,
        "merchant_id": merchant_id,
        "incident_id": incident_id,
        "issue_analysis": {
            "issue_type": issue_type,
            "severity": issue_details["severity"],
            "description": issue_details["description"],
            "business_impact_category": issue_details["business_impact"],
            "improvement_suggestions": issue_details["suggested_improvements"]
        },
        "merchant_profile": merchant_profile,
        "impact_assessment": impact_assessment,
        "communication_plan": notification_plan,
        "action_items": [
            "Merchant notification sent",
            "Issue documented in merchant profile",
            "Improvement suggestions provided",
            "Follow-up scheduled" if notification_plan["follow_up_required"] else None,
            "Training recommended" if notification_plan["training_recommended"] else None
        ],
        "monitoring": {
            "follow_up_period_days": 30 if issue_details["severity"] in ["high", "critical"] else 14,
            "quality_checks_increased": issue_details["severity"] in ["high", "critical"],
            "success_metrics": [
                "Reduced packaging incidents",
                "Improved customer satisfaction",
                "Higher packaging quality scores"
            ]
        },
        "compliance": {
            "food_safety_relevant": issue_type in ["liquid_spillage", "temperature_sensitive"],
            "documentation_complete": True,
            "audit_trail_created": True,
            "retention_period_months": 12
        },
        "timestamp": "2024-01-15T10:30:00Z"
    })
