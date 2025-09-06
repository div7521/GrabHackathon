import time
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

def suggest_safe_drop_off(package_id: str, current_location: str, recipient_unavailable_reason: str = "not_home",
                         package_value: float = 50.0, security_level: str = "standard") -> str:
    """
    Recommend secure alternative delivery locations when recipients are unavailable.

    Args:
        package_id: Unique package identifier
        current_location: Current delivery location
        recipient_unavailable_reason: Reason recipient is unavailable
        package_value: Estimated value of package for security assessment
        security_level: Required security level ('basic', 'standard', 'high', 'premium')

    Returns:
        JSON string containing secure drop-off location recommendations
    """
    # Realistic delay for location analysis + security assessment
    time.sleep(random.uniform(1.2, 2.8))

    # Basic validation
    if not package_id or not isinstance(package_id, str):
        return json.dumps({
            "status": "error",
            "error_code": "INVALID_PACKAGE_ID",
            "message": "Package ID is required and must be a valid string",
            "timestamp": datetime.now().isoformat()
        }, indent=2)

    if not current_location or not isinstance(current_location, str):
        return json.dumps({
            "status": "error",
            "error_code": "INVALID_LOCATION",
            "message": "Current location is required and must be a valid string",
            "timestamp": datetime.now().isoformat()
        }, indent=2)

    current_time = datetime.now()

    # Determine security requirements based on package value and level
    security_requirements = {
        "basic": {"min_value": 0, "max_value": 25, "requires_id": False, "requires_signature": False},
        "standard": {"min_value": 25, "max_value": 100, "requires_id": False, "requires_signature": True},
        "high": {"min_value": 100, "max_value": 500, "requires_id": True, "requires_signature": True},
        "premium": {"min_value": 500, "max_value": float('inf'), "requires_id": True, "requires_signature": True}
    }

    # Auto-adjust security level based on package value
    if package_value > 500:
        security_level = "premium"
    elif package_value > 100:
        security_level = "high"
    elif package_value > 25:
        security_level = "standard"
    else:
        security_level = "basic"

    # Location-based drop-off options
    location_options = {
        "Downtown": [
            {
                "option_id": "DROPOFF_001",
                "type": "building_concierge",
                "name": "Building Concierge Desk",
                "address": "Main Building Lobby",
                "distance_meters": 50,
                "security_rating": "high",
                "operating_hours": "24/7",
                "requires_id": True,
                "signature_required": True,
                "storage_duration_hours": 72,
                "fee": 0.0,
                "contact_info": "Concierge Desk - Call Building Management"
            },
            {
                "option_id": "DROPOFF_002",
                "type": "neighbor_delivery",
                "name": "Trusted Neighbor (Unit 12-05)",
                "address": "Same building, Unit 12-05",
                "distance_meters": 30,
                "security_rating": "medium",
                "operating_hours": "9 AM - 6 PM",
                "requires_id": False,
                "signature_required": True,
                "storage_duration_hours": 24,
                "fee": 0.0,
                "contact_info": "Neighbor agreed to accept packages"
            },
            {
                "option_id": "DROPOFF_003",
                "type": "retail_pickup",
                "name": "Convenience Store Pickup Point",
                "address": "123 Main Street",
                "distance_meters": 200,
                "security_rating": "standard",
                "operating_hours": "7 AM - 11 PM",
                "requires_id": True,
                "signature_required": True,
                "storage_duration_hours": 168,
                "fee": 2.50,
                "contact_info": "+65-1234-5678"
            }
        ],
        "Mall Area": [
            {
                "option_id": "DROPOFF_004",
                "type": "mall_security",
                "name": "Mall Security Office",
                "address": "Shopping Mall Level B1",
                "distance_meters": 100,
                "security_rating": "high",
                "operating_hours": "10 AM - 10 PM",
                "requires_id": True,
                "signature_required": True,
                "storage_duration_hours": 48,
                "fee": 0.0,
                "contact_info": "Mall Security - Level B1"
            },
            {
                "option_id": "DROPOFF_005",
                "type": "parcel_shop",
                "name": "Parcel Collection Point",
                "address": "Shop Unit #02-15",
                "distance_meters": 150,
                "security_rating": "high",
                "operating_hours": "10 AM - 9 PM",
                "requires_id": True,
                "signature_required": True,
                "storage_duration_hours": 120,
                "fee": 1.50,
                "contact_info": "+65-2345-6789"
            }
        ],
        "Business District": [
            {
                "option_id": "DROPOFF_006",
                "type": "office_reception",
                "name": "Office Building Reception",
                "address": "Corporate Tower Reception",
                "distance_meters": 25,
                "security_rating": "premium",
                "operating_hours": "8 AM - 6 PM",
                "requires_id": True,
                "signature_required": True,
                "storage_duration_hours": 24,
                "fee": 0.0,
                "contact_info": "Reception Desk - Corporate Tower"
            },
            {
                "option_id": "DROPOFF_007",
                "type": "postal_service",
                "name": "Post Office Collection",
                "address": "Central Post Office",
                "distance_meters": 300,
                "security_rating": "premium",
                "operating_hours": "8:30 AM - 5:30 PM",
                "requires_id": True,
                "signature_required": True,
                "storage_duration_hours": 336,
                "fee": 3.00,
                "contact_info": "+65-3456-7890"
            }
        ]
    }

    available_options = location_options.get(current_location, [
        {
            "option_id": "DROPOFF_008",
            "type": "secure_location",
            "name": "Secure Drop Box",
            "address": "Nearby secure location",
            "distance_meters": 100,
            "security_rating": "standard",
            "operating_hours": "24/7",
            "requires_id": False,
            "signature_required": False,
            "storage_duration_hours": 24,
            "fee": 1.00,
            "contact_info": "Self-service secure box"
        }
    ])

    # Filter options based on security requirements and package value
    suitable_options = []
    for option in available_options:
        # Check if security level is adequate
        option_security_adequate = True
        if security_level == "premium" and option["security_rating"] not in ["premium", "high"]:
            option_security_adequate = False
        elif security_level == "high" and option["security_rating"] not in ["premium", "high", "standard"]:
            option_security_adequate = False

        # Check if ID requirement can be met
        id_requirement_met = not security_requirements[security_level]["requires_id"] or option["requires_id"]

        # Check if signature requirement can be met
        signature_requirement_met = not security_requirements[security_level]["requires_signature"] or option["signature_required"]

        if option_security_adequate and id_requirement_met and signature_requirement_met:
            # Calculate suitability score
            security_score = {"basic": 1, "standard": 2, "high": 3, "premium": 4}[option["security_rating"]]
            distance_score = max(1, 5 - (option["distance_meters"] / 100))
            availability_score = 5 if option["operating_hours"] == "24/7" else 3
            fee_score = max(1, 5 - option["fee"])

            overall_score = (security_score + distance_score + availability_score + fee_score) / 4

            option_with_score = option.copy()
            option_with_score["suitability_score"] = round(overall_score, 2)
            option_with_score["estimated_pickup_time"] = {
                "earliest": (current_time + timedelta(hours=1)).isoformat(),
                "latest": (current_time + timedelta(hours=option["storage_duration_hours"])).isoformat(),
                "recommended": (current_time + timedelta(hours=random.randint(2, 12))).isoformat()
            }
            suitable_options.append(option_with_score)

    # Sort by suitability score
    suitable_options.sort(key=lambda x: x["suitability_score"], reverse=True)

    # Generate recipient notification plan
    notification_plan = {
        "notification_required": True,
        "notification_methods": ["sms", "email", "in_app"],
        "message_template": f"Your package {package_id} has been delivered to a secure location due to recipient unavailability",
        "pickup_instructions_included": True,
        "security_code_provided": len(suitable_options) > 0 and suitable_options[0]["requires_id"]
    }

    # Risk assessment
    risk_assessment = {
        "package_value_risk": "low" if package_value < 50 else "medium" if package_value < 200 else "high",
        "location_risk": random.choice(["low", "medium"]),
        "time_sensitivity": recipient_unavailable_reason in ["urgent_travel", "emergency"],
        "weather_considerations": random.choice(["none", "light_rain", "heavy_rain"]),
        "security_recommendations": []
    }

    # Add security recommendations based on risk
    if risk_assessment["package_value_risk"] == "high":
        risk_assessment["security_recommendations"].append("Require photo ID for pickup")
    if risk_assessment["location_risk"] == "medium":
        risk_assessment["security_recommendations"].append("Use only premium security locations")
    if risk_assessment["time_sensitivity"]:
        risk_assessment["security_recommendations"].append("Prioritize 24/7 accessible locations")

    response_data = {
        "status": "success",
        "package_details": {
            "package_id": package_id,
            "current_location": current_location,
            "package_value": package_value,
            "security_level_required": security_level,
            "recipient_unavailable_reason": recipient_unavailable_reason
        },
        "drop_off_options": {
            "total_options_found": len(suitable_options),
            "recommended_option": suitable_options[0] if suitable_options else None,
            "all_options": suitable_options[:5],  # Limit to top 5 options
            "options_filtered_by_security": len(available_options) - len(suitable_options)
        },
        "security_analysis": {
            "minimum_requirements": security_requirements[security_level],
            "risk_assessment": risk_assessment,
            "compliance_verified": True,
            "insurance_coverage": package_value <= 1000  # Coverage up to $1000
        },
        "recipient_communication": notification_plan,
        "logistics": {
            "delivery_attempt_number": random.randint(1, 3),
            "next_delivery_window": (current_time + timedelta(hours=24)).isoformat() if not suitable_options else None,
            "storage_fees_applicable": any(opt["fee"] > 0 for opt in suitable_options),
            "pickup_deadline": (current_time + timedelta(hours=72)).isoformat(),
            "driver_instructions": "Take photo of package at secure location and obtain receipt"
        },
        "success_factors": {
            "location_accessibility": "high" if suitable_options else "limited",
            "security_adequacy": "adequate" if suitable_options else "insufficient",
            "cost_effectiveness": "optimal" if any(opt["fee"] == 0 for opt in suitable_options) else "reasonable",
            "convenience_rating": random.uniform(3.5, 4.8) if suitable_options else 2.0
        },
        "metadata": {
            "processing_time_ms": random.randint(1200, 2800),
            "location_analysis_engine": "secure_drop_finder_v2.3",
            "security_assessment_complete": True,
            "recommendation_confidence": random.uniform(0.85, 0.96) if suitable_options else 0.4
        }
    }

    return json.dumps(response_data, indent=2)


def find_nearby_locker(delivery_address: str, max_distance_km: float = 2.0,
                      package_size: str = "medium", accessibility_required: bool = False) -> str:
    """
    Locate secure parcel locker facilities near delivery address for safe package storage.

    Args:
        delivery_address: Target delivery address or area
        max_distance_km: Maximum search radius in kilometers
        package_size: Package size category ('small', 'medium', 'large', 'extra_large')
        accessibility_required: Whether wheelchair accessibility is required

    Returns:
        JSON string containing nearby locker locations with availability and booking details
    """
    # Realistic delay for location services + availability check
    time.sleep(random.uniform(0.8, 2.2))

    # Basic validation
    if not delivery_address or not isinstance(delivery_address, str):
        return json.dumps({
            "status": "error",
            "error_code": "INVALID_ADDRESS",
            "message": "Delivery address is required and must be a valid string",
            "timestamp": datetime.now().isoformat()
        }, indent=2)

    if not isinstance(max_distance_km, (int, float)) or max_distance_km <= 0:
        return json.dumps({
            "status": "error",
            "error_code": "INVALID_DISTANCE",
            "message": "Maximum distance must be a positive number",
            "timestamp": datetime.now().isoformat()
        }, indent=2)

    current_time = datetime.now()

    # Package size requirements
    size_requirements = {
        "small": {"max_dimensions": "30x20x15 cm", "max_weight_kg": 2, "locker_size": "S"},
        "medium": {"max_dimensions": "40x30x25 cm", "max_weight_kg": 5, "locker_size": "M"},
        "large": {"max_dimensions": "60x40x40 cm", "max_weight_kg": 10, "locker_size": "L"},
        "extra_large": {"max_dimensions": "80x60x50 cm", "max_weight_kg": 20, "locker_size": "XL"}
    }

    # Locker network database
    locker_locations = [
        {
            "locker_id": "LOC_001",
            "network": "ParcelPod",
            "name": "Downtown Hub Lockers",
            "address": "123 Main Street, Downtown",
            "coordinates": {"lat": 1.2966, "lng": 103.8520},
            "distance_km": round(random.uniform(0.2, 2.0), 1),
            "operating_hours": "24/7",
            "accessibility": "wheelchair_accessible",
            "locker_sizes": {"S": 15, "M": 20, "L": 10, "XL": 5},
            "availability": {
                "S": random.randint(8, 15),
                "M": random.randint(12, 20),
                "L": random.randint(5, 10),
                "XL": random.randint(2, 5)
            },
            "pricing": {"S": 2.50, "M": 3.50, "L": 5.00, "XL": 7.50},
            "max_storage_days": 7,
            "security_features": ["CCTV", "secure_access", "temperature_controlled"],
            "payment_methods": ["credit_card", "digital_wallet", "cash"]
        },
        {
            "locker_id": "LOC_002",
            "network": "SecureBox",
            "name": "Mall Collection Point",
            "address": "Shopping Center Level B1",
            "coordinates": {"lat": 1.3021, "lng": 103.8634},
            "distance_km": round(random.uniform(0.5, 2.0), 1),
            "operating_hours": "10 AM - 10 PM",
            "accessibility": "stairs_only",
            "locker_sizes": {"S": 25, "M": 30, "L": 15, "XL": 8},
            "availability": {
                "S": random.randint(15, 25),
                "M": random.randint(20, 30),
                "L": random.randint(8, 15),
                "XL": random.randint(4, 8)
            },
            "pricing": {"S": 2.00, "M": 3.00, "L": 4.50, "XL": 6.50},
            "max_storage_days": 5,
            "security_features": ["CCTV", "secure_access", "alarm_system"],
            "payment_methods": ["credit_card", "digital_wallet"]
        },
        {
            "locker_id": "LOC_003",
            "network": "QuickCollect",
            "name": "Business District Express",
            "address": "456 Corporate Avenue",
            "coordinates": {"lat": 1.2845, "lng": 103.8455},
            "distance_km": round(random.uniform(0.3, 1.8), 1),
            "operating_hours": "6 AM - 11 PM",
            "accessibility": "wheelchair_accessible",
            "locker_sizes": {"S": 20, "M": 25, "L": 12, "XL": 6},
            "availability": {
                "S": random.randint(10, 20),
                "M": random.randint(15, 25),
                "L": random.randint(6, 12),
                "XL": random.randint(3, 6)
            },
            "pricing": {"S": 3.00, "M": 4.00, "L": 5.50, "XL": 8.00},
            "max_storage_days": 10,
            "security_features": ["CCTV", "secure_access", "biometric_lock", "24h_monitoring"],
            "payment_methods": ["credit_card", "digital_wallet", "corporate_account"]
        },
        {
            "locker_id": "LOC_004",
            "network": "ParcelPod",
            "name": "Residential Hub",
            "address": "789 Residential Road",
            "coordinates": {"lat": 1.3156, "lng": 103.8712},
            "distance_km": round(random.uniform(1.0, 2.5), 1),
            "operating_hours": "24/7",
            "accessibility": "wheelchair_accessible",
            "locker_sizes": {"S": 18, "M": 22, "L": 8, "XL": 4},
            "availability": {
                "S": random.randint(12, 18),
                "M": random.randint(16, 22),
                "L": random.randint(4, 8),
                "XL": random.randint(2, 4)
            },
            "pricing": {"S": 2.25, "M": 3.25, "L": 4.75, "XL": 7.00},
            "max_storage_days": 7,
            "security_features": ["CCTV", "secure_access", "mobile_alerts"],
            "payment_methods": ["credit_card", "digital_wallet", "subscription"]
        }
    ]

    # Filter by distance
    nearby_lockers = [locker for locker in locker_locations if locker["distance_km"] <= max_distance_km]

    # Filter by accessibility if required
    if accessibility_required:
        nearby_lockers = [locker for locker in nearby_lockers if locker["accessibility"] == "wheelchair_accessible"]

    # Filter by package size availability
    required_size = size_requirements[package_size]["locker_size"]
    available_lockers = []

    for locker in nearby_lockers:
        if required_size in locker["locker_sizes"] and locker["availability"][required_size] > 0:
            # Calculate convenience score
            distance_score = max(0, 5 - locker["distance_km"])
            availability_score = min(5, locker["availability"][required_size] / 5)
            price_score = max(0, 5 - (locker["pricing"][required_size] / 2))
            hours_score = 5 if locker["operating_hours"] == "24/7" else 3
            security_score = min(5, len(locker["security_features"]))

            convenience_score = (distance_score + availability_score + price_score + hours_score + security_score) / 5

            locker_info = locker.copy()
            locker_info.update({
                "convenience_score": round(convenience_score, 2),
                "recommended_size": required_size,
                "rental_cost": locker["pricing"][required_size],
                "available_units": locker["availability"][required_size],
                "booking_ref": f"BOOK_{random.randint(100000, 999999)}",
                "estimated_pickup_by": (current_time + timedelta(days=locker["max_storage_days"])).isoformat(),
                "directions_available": True,
                "real_time_availability": True
            })
            available_lockers.append(locker_info)

    # Sort by convenience score
    available_lockers.sort(key=lambda x: x["convenience_score"], reverse=True)

    # Generate booking instructions
    booking_process = {
        "steps": [
            "Select preferred locker location",
            "Choose locker size and rental duration",
            "Complete payment through app",
            "Receive unique access code via SMS",
            "Driver delivers package to locker",
            "Pickup package using access code"
        ],
        "estimated_setup_time": "2-3 minutes",
        "payment_required_upfront": True,
        "refund_policy": "Full refund if package not delivered within 2 hours",
        "customer_support": "+65-1800-LOCKER"
    }

    # Network coverage analysis
    network_analysis = {
        "networks_available": list(set(locker["network"] for locker in available_lockers)),
        "total_locations_in_area": len(nearby_lockers),
        "locations_with_availability": len(available_lockers),
        "average_distance_km": round(sum(locker["distance_km"] for locker in available_lockers) / len(available_lockers), 2) if available_lockers else 0,
        "price_range": {
            "min": min(locker["rental_cost"] for locker in available_lockers) if available_lockers else 0,
            "max": max(locker["rental_cost"] for locker in available_lockers) if available_lockers else 0,
            "average": round(sum(locker["rental_cost"] for locker in available_lockers) / len(available_lockers), 2) if available_lockers else 0
        }
    }

    response_data = {
        "status": "success",
        "search_parameters": {
            "delivery_address": delivery_address,
            "max_distance_km": max_distance_km,
            "package_size": package_size,
            "package_requirements": size_requirements[package_size],
            "accessibility_required": accessibility_required,
            "search_timestamp": current_time.isoformat()
        },
        "locker_options": {
            "total_found": len(available_lockers),
            "recommended_locker": available_lockers[0] if available_lockers else None,
            "all_locations": available_lockers[:8],  # Limit to top 8
            "has_more_locations": len(available_lockers) > 8
        },
        "network_coverage": network_analysis,
        "booking_process": booking_process,
        "service_benefits": {
            "24_7_access": any(locker["operating_hours"] == "24/7" for locker in available_lockers),
            "security_guaranteed": True,
            "contactless_pickup": True,
            "extended_storage": max((locker["max_storage_days"] for locker in available_lockers), default=0),
            "weather_protection": True,
            "theft_protection": "fully_insured"
        },
        "delivery_integration": {
            "driver_notification_automatic": True,
            "customer_pickup_alerts": True,
            "real_time_status_updates": True,
            "photo_confirmation": True,
            "gps_tracking_to_locker": True
        },
        "alternative_recommendations": [
            "Increase search radius if no lockers found",
            "Consider smaller package size category",
            "Check availability during off-peak hours",
            "Use multiple smaller lockers for large items"
        ] if not available_lockers else [],
        "metadata": {
            "processing_time_ms": random.randint(800, 2200),
            "location_service_version": "locker_finder_v2.7",
            "real_time_availability": True,
            "data_freshness_minutes": random.randint(1, 5)
        }
    }

    return json.dumps(response_data, indent=2)


def log_merchant_packaging_feedback(merchant_id: str, incident_id: str, packaging_issue_type: str,
                                   evidence_photos: int = 0, severity: str = "medium",
                                   improvement_suggestions: Optional[List[str]] = None) -> str:
    """
    Report packaging quality issues to merchants with evidence-backed recommendations for improvement.

    Args:
        merchant_id: Unique merchant identifier
        incident_id: Related incident or order identifier
        packaging_issue_type: Type of packaging problem
        evidence_photos: Number of evidence photos available
        severity: Issue severity level ('low', 'medium', 'high', 'critical')
        improvement_suggestions: List of specific improvement recommendations

    Returns:
        JSON string containing feedback logging status and merchant communication details
    """
    # Realistic delay for evidence processing + merchant system integration
    time.sleep(random.uniform(1.5, 3.2))

    # Basic validation
    if not merchant_id or not isinstance(merchant_id, str):
        return json.dumps({
            "status": "error",
            "error_code": "INVALID_MERCHANT_ID",
            "message": "Merchant ID is required and must be a valid string",
            "timestamp": datetime.now().isoformat()
        }, indent=2)

    if not incident_id or not isinstance(incident_id, str):
        return json.dumps({
            "status": "error",
            "error_code": "INVALID_INCIDENT_ID",
            "message": "Incident ID is required and must be a valid string",
            "timestamp": datetime.now().isoformat()
        }, indent=2)

    current_time = datetime.now()
    feedback_id = f"FEEDBACK_{random.randint(100000, 999999)}"

    # Packaging issue categorization
    issue_categories = {
        "insufficient_protection": {
            "description": "Items not adequately protected during transport",
            "common_causes": ["thin_packaging", "no_bubble_wrap", "loose_fitting"],
            "business_impact": "medium",
            "customer_impact": "high"
        },
        "poor_sealing": {
            "description": "Package seals inadequate or failed during delivery",
            "common_causes": ["weak_tape", "improper_closure", "overfilled_container"],
            "business_impact": "high",
            "customer_impact": "high"
        },
        "wrong_container_size": {
            "description": "Container size inappropriate for contents",
            "common_causes": ["oversized_packaging", "undersized_container", "irregular_items"],
            "business_impact": "low",
            "customer_impact": "medium"
        },
        "fragile_handling_ignored": {
            "description": "Fragile items not packaged with appropriate care",
            "common_causes": ["no_fragile_marking", "insufficient_cushioning", "stacking_damage"],
            "business_impact": "high",
            "customer_impact": "critical"
        },
        "liquid_spillage": {
            "description": "Liquid items improperly contained causing spillage",
            "common_causes": ["loose_caps", "no_double_bagging", "container_failure"],
            "business_impact": "critical",
            "customer_impact": "critical"
        },
        "temperature_sensitive": {
            "description": "Temperature-sensitive items inadequately packaged",
            "common_causes": ["no_insulation", "wrong_cooling_packs", "delayed_preparation"],
            "business_impact": "medium",
            "customer_impact": "high"
        }
    }

    issue_details = issue_categories.get(packaging_issue_type, {
        "description": "General packaging quality issue",
        "common_causes": ["packaging_standards"],
        "business_impact": "medium",
        "customer_impact": "medium"
    })

    # Generate evidence assessment
    evidence_assessment = {
        "photos_provided": evidence_photos,
        "evidence_quality": "excellent" if evidence_photos >= 3 else "good" if evidence_photos >= 2 else "fair" if evidence_photos >= 1 else "insufficient",
        "documentation_complete": evidence_photos >= 2 and improvement_suggestions is not None,
        "actionable_insights": evidence_photos >= 1,
        "evidence_strength": min(1.0, evidence_photos * 0.33 + (0.2 if improvement_suggestions else 0))
    }

    # Merchant profile and history lookup
    merchant_profile = {
        "merchant_id": merchant_id,
        "merchant_name": f"Restaurant_{merchant_id[-3:]}",
        "category": random.choice(["fast_food", "restaurant", "cafe", "bakery", "grocery"]),
        "packaging_history": {
            "previous_incidents": random.randint(0, 8),
            "last_incident_date": (current_time - timedelta(days=random.randint(10, 90))).isoformat() if random.choice([True, False]) else None,
            "improvement_trend": random.choice(["improving", "stable", "declining"]),
            "packaging_score": round(random.uniform(3.2, 4.8), 1)
        },
        "communication_preferences": {
            "preferred_language": random.choice(["english", "mandarin", "malay"]),
            "contact_method": random.choice(["email", "merchant_app", "phone"]),
            "feedback_receptivity": random.choice(["high", "medium", "low"])
        }
    }

    # Generate improvement recommendations if not provided
    if improvement_suggestions is None:
        suggestion_database = {
            "insufficient_protection": [
                "Use additional bubble wrap or cushioning material",
                "Switch to thicker packaging containers",
                "Add protective corners for fragile items",
                "Use proper void fill to prevent movement"
            ],
            "poor_sealing": [
                "Use higher quality packaging tape",
                "Ensure proper closure technique",
                "Double-seal high-value items",
                "Train staff on proper sealing procedures"
            ],
            "wrong_container_size": [
                "Use appropriately sized containers for items",
                "Avoid excessive packaging for small items",
                "Ensure containers can properly accommodate contents",
                "Consider custom packaging for irregular items"
            ],
            "fragile_handling_ignored": [
                "Clearly mark fragile items with warning labels",
                "Use specialized fragile item packaging",
                "Add extra cushioning for breakable goods",
                "Train packaging staff on fragile item handling"
            ],
            "liquid_spillage": [
                "Double-bag all liquid items",
                "Use leak-proof containers",
                "Secure all caps and lids properly",
                "Add absorbent material for liquid orders"
            ],
            "temperature_sensitive": [
                "Use appropriate insulation for hot/cold items",
                "Include proper cooling packs for cold items",
                "Package temperature-sensitive items last",
                "Clearly label temperature requirements"
            ]
        }

        improvement_suggestions = suggestion_database.get(packaging_issue_type, [
            "Review current packaging standards",
            "Implement quality control checks",
            "Train staff on proper packaging techniques"
        ])

    # Impact assessment
    impact_assessment = {
        "customer_impact": {
            "satisfaction_score_change": -random.uniform(0.2, 0.8) if severity in ["high", "critical"] else -random.uniform(0.1, 0.3),
            "refund_likelihood": 0.8 if severity == "critical" else 0.5 if severity == "high" else 0.2,
            "reorder_probability": random.uniform(0.3, 0.7) if severity in ["low", "medium"] else random.uniform(0.1, 0.4),
            "review_impact": random.choice(["negative_review_likely", "neutral", "positive_if_resolved"])
        },
        "business_impact": {
            "estimated_cost": round(random.uniform(5, 50) if severity == "critical" else random.uniform(2, 25), 2),
            "brand_reputation": issue_details["business_impact"],
            "operational_disruption": severity,
            "improvement_potential": "high" if evidence_assessment["evidence_strength"] > 0.6 else "medium"
        },
        "frequency_analysis": {
            "similar_incidents_last_30_days": merchant_profile["packaging_history"]["previous_incidents"],
            "trend_pattern": merchant_profile["packaging_history"]["improvement_trend"],
            "recurring_issue": merchant_profile["packaging_history"]["previous_incidents"] > 3
        }
    }

    # Merchant communication plan
    communication_plan = {
        "immediate_notification": {
            "method": merchant_profile["communication_preferences"]["contact_method"],
            "urgency": "high" if severity in ["high", "critical"] else "normal",
            "language": merchant_profile["communication_preferences"]["preferred_language"],
            "expected_response_time": "2 hours" if severity == "critical" else "24 hours"
        },
        "feedback_delivery": {
            "include_photos": evidence_photos > 0,
            "include_customer_impact": True,
            "include_improvement_plan": True,
            "follow_up_required": severity in ["high", "critical"] or merchant_profile["packaging_history"]["previous_incidents"] > 2,
            "training_recommended": severity in ["medium", "high", "critical"]
        },
        "escalation_path": {
            "manager_notification": severity == "critical",
            "account_review_triggered": merchant_profile["packaging_history"]["previous_incidents"] > 5,
            "quality_audit_scheduled": severity == "critical" and merchant_profile["packaging_history"]["improvement_trend"] == "declining"
        }
    }

    # Generate action plan
    action_plan = {
        "immediate_actions": [
            "Notify merchant of packaging issue",
            "Document incident in merchant profile",
            "Process customer compensation if applicable"
        ],
        "short_term_actions": [
            "Merchant acknowledgment and response",
            "Implementation of suggested improvements",
            "Staff training if recommended"
        ],
        "monitoring_plan": {
            "follow_up_period_days": 30 if severity in ["high", "critical"] else 14,
            "quality_checks_increased": severity in ["high", "critical"],
            "performance_tracking": True,
            "success_metrics": [
                "Reduced packaging incidents",
                "Improved customer satisfaction",
                "Higher packaging quality scores"
            ]
        }
    }

    # System learning and improvement
    system_improvements = {
        "pattern_recognition": {
            "similar_merchants_analyzed": random.randint(5, 20),
            "common_issues_identified": len(improvement_suggestions) > 2,
            "best_practices_shared": True,
            "training_materials_updated": severity in ["high", "critical"]
        },
        "prevention_measures": [
            "Enhanced merchant onboarding training",
            "Regular packaging quality audits",
            "Improved packaging guidelines",
            "Incentive programs for quality improvement"
        ],
        "data_insights": {
            "packaging_trend_analysis": "improving_industry_wide",
            "seasonal_factors": random.choice([True, False]),
            "category_specific_insights": issue_details["common_causes"]
        }
    }

    response_data = {
        "status": "success",
        "feedback_details": {
            "feedback_id": feedback_id,
            "merchant_id": merchant_id,
            "incident_id": incident_id,
            "issue_type": packaging_issue_type,
            "severity_level": severity,
            "logged_timestamp": current_time.isoformat(),
            "processing_priority": "high" if severity == "critical" else "normal"
        },
        "issue_analysis": {
            "issue_description": issue_details["description"],
            "root_causes": issue_details["common_causes"],
            "business_impact_level": issue_details["business_impact"],
            "customer_impact_level": issue_details["customer_impact"],
            "recurrence_likelihood": "high" if merchant_profile["packaging_history"]["previous_incidents"] > 3 else "low"
        },
        "evidence_evaluation": evidence_assessment,
        "merchant_profile": merchant_profile,
        "impact_assessment": impact_assessment,
        "improvement_recommendations": {
            "suggested_actions": improvement_suggestions,
            "implementation_priority": severity,
            "estimated_implementation_time": "1-2 weeks" if severity in ["low", "medium"] else "immediate",
            "cost_estimate": round(random.uniform(50, 500), 2),
            "roi_projection": "high" if evidence_assessment["evidence_strength"] > 0.7 else "medium"
        },
        "communication_plan": communication_plan,
        "action_plan": action_plan,
        "system_improvements": system_improvements,
        "compliance_tracking": {
            "food_safety_relevant": merchant_profile["category"] in ["restaurant", "fast_food", "bakery"],
            "quality_standards_updated": True,
            "regulatory_reporting": severity == "critical",
            "audit_trail_created": True,
            "retention_period_months": 24
        },
        "success_measurement": {
            "kpi_tracking": [
                "packaging_incident_reduction",
                "customer_satisfaction_improvement",
                "merchant_compliance_rate",
                "repeat_incident_prevention"
            ],
            "benchmark_comparison": {
                "industry_average": random.uniform(3.5, 4.2),
                "merchant_current": merchant_profile["packaging_history"]["packaging_score"],
                "target_improvement": 0.3
            },
            "review_schedule": (current_time + timedelta(days=30)).isoformat()
        },
        "metadata": {
            "processing_time_ms": random.randint(1500, 3200),
            "feedback_system_version": "merchant_quality_tracker_v2.5",
            "ai_analysis_confidence": round(evidence_assessment["evidence_strength"], 3),
            "merchant_notification_sent": True
        }
    }

    return json.dumps(response_data, indent=2)
