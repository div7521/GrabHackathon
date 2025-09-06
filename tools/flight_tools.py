import time
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

def check_flight_status(flight_number: str, departure_date: str = None,
                       include_connections: bool = True, passenger_context: str = "airport_trip") -> str:
    """
    Check real-time flight status information for airport trips to assess passenger urgency.

    Args:
        flight_number: Flight identifier (e.g., 'SQ123', 'BA456')
        departure_date: Flight departure date (YYYY-MM-DD format, defaults to today)
        include_connections: Whether to check connecting flight information
        passenger_context: Context of request ('airport_trip', 'pickup_planning', 'delay_assessment')

    Returns:
        JSON string containing comprehensive flight status and passenger impact analysis
    """
    # Realistic delay for airline API calls + data processing
    time.sleep(random.uniform(1.2, 3.5))

    # Basic validation
    if not flight_number or not isinstance(flight_number, str):
        return json.dumps({
            "status": "error",
            "error_code": "INVALID_FLIGHT_NUMBER",
            "message": "Flight number is required and must be a valid string",
            "timestamp": datetime.now().isoformat()
        }, indent=2)

    # Parse departure date
    if departure_date:
        try:
            target_date = datetime.strptime(departure_date, "%Y-%m-%d").date()
        except ValueError:
            return json.dumps({
                "status": "error",
                "error_code": "INVALID_DATE_FORMAT",
                "message": "Date must be in YYYY-MM-DD format",
                "timestamp": datetime.now().isoformat()
            }, indent=2)
    else:
        target_date = datetime.now().date()

    current_time = datetime.now()
    query_id = f"FLIGHT_{random.randint(100000, 999999)}"

    # Flight database simulation
    airline_codes = {
        "SQ": {"name": "Singapore Airlines", "hub": "Changi Airport", "reliability": 0.92},
        "3K": {"name": "Jetstar Asia", "hub": "Changi Airport", "reliability": 0.85},
        "TR": {"name": "Scoot", "hub": "Changi Airport", "reliability": 0.88},
        "BA": {"name": "British Airways", "hub": "Heathrow", "reliability": 0.89},
        "EK": {"name": "Emirates", "hub": "Dubai International", "reliability": 0.91},
        "QF": {"name": "Qantas", "hub": "Sydney", "reliability": 0.90},
        "CX": {"name": "Cathay Pacific", "hub": "Hong Kong", "reliability": 0.87},
        "TG": {"name": "Thai Airways", "hub": "Bangkok", "reliability": 0.84},
        "NH": {"name": "ANA", "hub": "Tokyo Narita", "reliability": 0.93},
        "LH": {"name": "Lufthansa", "hub": "Frankfurt", "reliability": 0.89}
    }

    # Extract airline code from flight number
    airline_code = "".join([c for c in flight_number if c.isalpha()]).upper()
    flight_num = "".join([c for c in flight_number if c.isdigit()])

    if airline_code not in airline_codes:
        # Generic airline for unknown codes
        airline_info = {"name": f"Airline {airline_code}", "hub": "Unknown", "reliability": 0.85}
    else:
        airline_info = airline_codes[airline_code]

    # Generate flight routes based on airline
    route_options = {
        "SQ": [
            {"origin": "SIN", "destination": "LHR", "duration_hours": 13.5, "aircraft": "A380"},
            {"origin": "SIN", "destination": "NRT", "duration_hours": 7.5, "aircraft": "A350"},
            {"origin": "SIN", "destination": "SYD", "duration_hours": 8.0, "aircraft": "B777"},
            {"origin": "SIN", "destination": "LAX", "duration_hours": 17.5, "aircraft": "A350"}
        ],
        "3K": [
            {"origin": "SIN", "destination": "BKK", "duration_hours": 2.5, "aircraft": "A320"},
            {"origin": "SIN", "destination": "KUL", "duration_hours": 1.5, "aircraft": "A320"},
            {"origin": "SIN", "destination": "CGK", "duration_hours": 1.8, "aircraft": "A321"}
        ],
        "default": [
            {"origin": "SIN", "destination": "KUL", "duration_hours": 1.5, "aircraft": "B737"},
            {"origin": "SIN", "destination": "BKK", "duration_hours": 2.5, "aircraft": "A320"},
            {"origin": "SIN", "destination": "HKG", "duration_hours": 3.5, "aircraft": "A330"}
        ]
    }

    flight_route = random.choice(route_options.get(airline_code, route_options["default"]))

    # Generate flight schedule
    scheduled_departure = datetime.combine(target_date, datetime.min.time().replace(
        hour=random.randint(6, 23),
        minute=random.choice([0, 15, 30, 45])
    ))

    scheduled_arrival = scheduled_departure + timedelta(hours=flight_route["duration_hours"])

    # Generate flight status scenarios
    status_scenarios = [
        {"status": "on_time", "delay_minutes": 0, "probability": 0.65},
        {"status": "delayed", "delay_minutes": random.randint(15, 60), "probability": 0.25},
        {"status": "significantly_delayed", "delay_minutes": random.randint(61, 180), "probability": 0.07},
        {"status": "cancelled", "delay_minutes": 0, "probability": 0.02},
        {"status": "boarding", "delay_minutes": random.randint(-10, 10), "probability": 0.01}
    ]

    # Weight by airline reliability
    reliability_factor = airline_info["reliability"]
    adjusted_scenarios = []
    for scenario in status_scenarios:
        if scenario["status"] == "on_time":
            adjusted_prob = scenario["probability"] * reliability_factor * 1.2
        elif scenario["status"] in ["delayed", "significantly_delayed"]:
            adjusted_prob = scenario["probability"] * (2 - reliability_factor)
        else:
            adjusted_prob = scenario["probability"]
        adjusted_scenarios.append({**scenario, "probability": adjusted_prob})

    # Normalize probabilities
    total_prob = sum(s["probability"] for s in adjusted_scenarios)
    for scenario in adjusted_scenarios:
        scenario["probability"] /= total_prob

    # Select flight status
    selected_status = random.choices(
        adjusted_scenarios,
        weights=[s["probability"] for s in adjusted_scenarios]
    )[0]

    # Calculate actual times
    actual_departure = scheduled_departure + timedelta(minutes=selected_status["delay_minutes"])
    actual_arrival = scheduled_arrival + timedelta(minutes=selected_status["delay_minutes"])

    # Generate gate and terminal information
    terminal_gates = {
        "SIN": {"terminals": ["T1", "T2", "T3", "T4"], "gates": ["A", "B", "C", "D"]},
        "LHR": {"terminals": ["T2", "T3", "T5"], "gates": ["A", "B", "C"]},
        "NRT": {"terminals": ["T1", "T2"], "gates": ["A", "B", "C"]},
        "default": {"terminals": ["T1", "T2"], "gates": ["A", "B"]}
    }

    origin_info = terminal_gates.get(flight_route["origin"], terminal_gates["default"])
    destination_info = terminal_gates.get(flight_route["destination"], terminal_gates["default"])

    departure_gate = f"{random.choice(origin_info['gates'])}{random.randint(1, 30)}"
    departure_terminal = random.choice(origin_info["terminals"])
    arrival_gate = f"{random.choice(destination_info['gates'])}{random.randint(1, 30)}"
    arrival_terminal = random.choice(destination_info["terminals"])

    # Passenger impact assessment
    passenger_impact = {
        "urgency_level": "high" if selected_status["delay_minutes"] > 60 else "medium" if selected_status["delay_minutes"] > 15 else "low",
        "rebooking_options": [],
        "compensation_eligible": selected_status["delay_minutes"] > 120 or selected_status["status"] == "cancelled",
        "connection_risk": "high" if include_connections and selected_status["delay_minutes"] > 30 else "low"
    }

    # Generate rebooking options for cancelled/severely delayed flights
    if selected_status["status"] == "cancelled" or selected_status["delay_minutes"] > 180:
        passenger_impact["rebooking_options"] = [
            {
                "flight_number": f"{airline_code}{int(flight_num) + 2}",
                "departure_time": (scheduled_departure + timedelta(hours=random.randint(2, 8))).isoformat(),
                "availability": random.choice(["available", "waitlist", "full"]),
                "additional_cost": random.uniform(0, 200) if random.choice([True, False]) else 0
            },
            {
                "flight_number": f"{airline_code}{int(flight_num) + 4}",
                "departure_time": (scheduled_departure + timedelta(hours=random.randint(6, 24))).isoformat(),
                "availability": "available",
                "additional_cost": 0
            }
        ]

    # Connection flight analysis if requested
    connection_analysis = None
    if include_connections and selected_status["delay_minutes"] > 0:
        connection_analysis = {
            "connections_at_risk": random.randint(0, 2),
            "minimum_connection_time": random.randint(45, 120),
            "alternative_connections": [
                {
                    "flight_number": f"{random.choice(list(airline_codes.keys()))}{random.randint(100, 999)}",
                    "departure_time": (actual_arrival + timedelta(hours=random.randint(2, 6))).isoformat(),
                    "destination": random.choice(["NYC", "LON", "PAR", "FRA", "DXB"])
                }
            ] if selected_status["delay_minutes"] > 60 else [],
            "rebooking_assistance": selected_status["delay_minutes"] > 60
        }

    # Weather and operational factors
    operational_factors = {
        "weather_conditions": {
            "origin": random.choice(["clear", "light_rain", "heavy_rain", "thunderstorms", "fog"]),
            "destination": random.choice(["clear", "light_rain", "cloudy", "windy"]),
            "weather_delay_factor": random.choice([True, False]) and selected_status["delay_minutes"] > 30
        },
        "air_traffic": {
            "congestion_level": random.choice(["normal", "moderate", "heavy"]),
            "runway_availability": random.choice(["full", "limited", "single_runway"]),
            "atc_delays": selected_status["delay_minutes"] > 45 and random.choice([True, False])
        },
        "aircraft_status": {
            "maintenance_delay": selected_status["delay_minutes"] > 90 and random.choice([True, False]),
            "crew_change_required": selected_status["delay_minutes"] > 120 and random.choice([True, False]),
            "fuel_delays": random.choice([True, False]) and selected_status["delay_minutes"] > 30
        }
    }

    # Baggage and check-in information
    service_info = {
        "check_in": {
            "online_available": True,
            "counter_opens": (scheduled_departure - timedelta(hours=3)).isoformat(),
            "counter_closes": (scheduled_departure - timedelta(minutes=45)).isoformat(),
            "baggage_drop_deadline": (scheduled_departure - timedelta(minutes=45)).isoformat()
        },
        "baggage": {
            "tracking_available": True,
            "transfer_time": random.randint(30, 90) if include_connections else 0,
            "delayed_baggage_risk": "high" if selected_status["delay_minutes"] > 60 else "low"
        },
        "passenger_services": {
            "lounge_access": airline_code in ["SQ", "BA", "EK", "QF"],
            "meal_service": flight_route["duration_hours"] > 2,
            "wifi_available": random.choice([True, True, False]),  # 67% have wifi
            "entertainment": flight_route["duration_hours"] > 3
        }
    }

    # Travel context analysis
    context_analysis = {
        "airport_trip_impact": {
            "recommended_departure_time": (actual_departure - timedelta(hours=2.5)).isoformat(),
            "traffic_buffer_needed": random.randint(30, 60),
            "alternative_transport_suggested": selected_status["delay_minutes"] > 120,
            "check_in_urgency": "high" if selected_status["delay_minutes"] < -30 else "normal"
        },
        "pickup_coordination": {
            "pickup_time_adjustment": selected_status["delay_minutes"],
            "notification_urgency": "immediate" if abs(selected_status["delay_minutes"]) > 30 else "normal",
            "driver_rebooking_needed": selected_status["delay_minutes"] > 60,
            "cost_implications": round(selected_status["delay_minutes"] * 0.5, 2) if selected_status["delay_minutes"] > 0 else 0
        }
    }

    response_data = {
        "status": "success",
        "query_info": {
            "query_id": query_id,
            "flight_number": flight_number,
            "departure_date": target_date.isoformat(),
            "passenger_context": passenger_context,
            "queried_timestamp": current_time.isoformat()
        },
        "flight_details": {
            "airline": {
                "code": airline_code,
                "name": airline_info["name"],
                "hub_airport": airline_info["hub"],
                "reliability_score": airline_info["reliability"]
            },
            "route": {
                "origin_airport": flight_route["origin"],
                "destination_airport": flight_route["destination"],
                "flight_distance": f"~{int(flight_route['duration_hours'] * 800)} km",
                "aircraft_type": flight_route["aircraft"]
            },
            "schedule": {
                "scheduled_departure": scheduled_departure.isoformat(),
                "scheduled_arrival": scheduled_arrival.isoformat(),
                "actual_departure": actual_departure.isoformat() if selected_status["status"] != "cancelled" else None,
                "actual_arrival": actual_arrival.isoformat() if selected_status["status"] != "cancelled" else None,
                "flight_duration_hours": flight_route["duration_hours"]
            }
        },
        "current_status": {
            "status": selected_status["status"],
            "delay_minutes": selected_status["delay_minutes"],
            "status_description": {
                "on_time": "Flight is operating on schedule",
                "delayed": f"Flight delayed by {selected_status['delay_minutes']} minutes",
                "significantly_delayed": f"Major delay of {selected_status['delay_minutes']} minutes",
                "cancelled": "Flight has been cancelled",
                "boarding": "Flight is currently boarding"
            }.get(selected_status["status"], "Status unknown"),
            "last_updated": (current_time - timedelta(minutes=random.randint(1, 15))).isoformat(),
            "next_update_expected": (current_time + timedelta(minutes=random.randint(15, 45))).isoformat()
        },
        "airport_information": {
            "departure": {
                "terminal": departure_terminal,
                "gate": departure_gate,
                "gate_assigned": selected_status["status"] not in ["cancelled"],
                "security_wait_time": f"{random.randint(10, 45)} minutes"
            },
            "arrival": {
                "terminal": arrival_terminal,
                "gate": arrival_gate if selected_status["status"] != "cancelled" else None,
                "baggage_carousel": random.randint(1, 12) if selected_status["status"] != "cancelled" else None,
                "customs_wait_time": f"{random.randint(5, 30)} minutes"
            }
        },
        "passenger_impact": passenger_impact,
        "connection_analysis": connection_analysis,
        "operational_factors": operational_factors,
        "service_information": service_info,
        "travel_context": context_analysis,
        "recommendations": {
            "passenger_actions": [
                "Monitor flight status regularly",
                "Arrive at airport 2.5 hours early for international flights",
                "Complete online check-in if available"
            ] + (["Consider rebooking options", "Contact airline customer service"] if selected_status["status"] in ["cancelled", "significantly_delayed"] else []),
            "driver_coordination": [
                f"Adjust pickup time by {selected_status['delay_minutes']} minutes" if selected_status['delay_minutes'] != 0 else "Maintain scheduled pickup time",
                "Monitor flight status for further updates",
                "Consider alternative transport if delay exceeds 2 hours"
            ] if passenger_context in ["pickup_planning", "airport_trip"] else []
        },
        "alternative_options": {
            "earlier_flights": [
                {
                    "flight_number": f"{airline_code}{int(flight_num) - 2}",
                    "departure_time": (scheduled_departure - timedelta(hours=random.randint(2, 6))).isoformat(),
                    "availability": random.choice(["available", "waitlist", "full"])
                }
            ] if selected_status["delay_minutes"] > 60 else [],
            "other_airlines": [
                {
                    "airline": random.choice([k for k in airline_codes.keys() if k != airline_code]),
                    "estimated_departure": (scheduled_departure + timedelta(hours=random.randint(1, 4))).isoformat(),
                    "price_difference": random.uniform(-50, 200)
                }
            ] if selected_status["status"] == "cancelled" else []
        },
        "metadata": {
            "processing_time_ms": random.randint(1200, 3500),
            "data_sources": ["airline_api", "airport_systems", "traffic_control"],
            "confidence_score": random.uniform(0.85, 0.98),
            "real_time_accuracy": "high",
            "last_system_update": (current_time - timedelta(minutes=random.randint(1, 10))).isoformat()
        }
    }

    return json.dumps(response_data, indent=2)
