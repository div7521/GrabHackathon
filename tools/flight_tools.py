import time
import json
import random

def check_flight_status(flight_number: str) -> str:
    """Check real-time flight status information for airport trips to assess passenger urgency.

    Args:
        flight_number: Flight identifier (e.g., 'SQ123', 'BA456')

    Returns:
        JSON string containing flight status and passenger impact analysis
    """
    time.sleep(random.uniform(0.1, 0.4))

    if not flight_number:
        return json.dumps({
            "error": "INVALID_FLIGHT_NUMBER",
            "message": "Flight number is required"
        })


    airline_code = "".join([c for c in flight_number if c.isalpha()]).upper()
    flight_num = "".join([c for c in flight_number if c.isdigit()])

    if not airline_code or not flight_num:
        return json.dumps({
            "error": "INVALID_FLIGHT_FORMAT",
            "message": "Flight number must contain both airline code and number (e.g., SQ123)"
        })


    airlines = {
        "SQ": {"name": "Singapore Airlines", "hub": "Changi Airport"},
        "3K": {"name": "Jetstar Asia", "hub": "Changi Airport"},
        "TR": {"name": "Scoot", "hub": "Changi Airport"},
        "BA": {"name": "British Airways", "hub": "Heathrow"},
        "EK": {"name": "Emirates", "hub": "Dubai International"},
        "QF": {"name": "Qantas", "hub": "Sydney"},
        "CX": {"name": "Cathay Pacific", "hub": "Hong Kong"},
        "NH": {"name": "ANA", "hub": "Tokyo Narita"},
        "LH": {"name": "Lufthansa", "hub": "Frankfurt"}
    }

    airline_info = airlines.get(airline_code, {
        "name": f"Airline {airline_code}",
        "hub": "International Airport"
    })


    routes = [
        {"origin": "SIN", "destination": "LHR", "duration_hours": 13.5},
        {"origin": "SIN", "destination": "NRT", "duration_hours": 7.5},
        {"origin": "SIN", "destination": "SYD", "duration_hours": 8.0},
        {"origin": "SIN", "destination": "HKG", "duration_hours": 3.5},
        {"origin": "SIN", "destination": "BKK", "duration_hours": 2.5},
        {"origin": "SIN", "destination": "KUL", "duration_hours": 1.5}
    ]

    route = random.choice(routes)


    base_hour = random.randint(6, 23)
    scheduled_departure = f"2024-01-15T{base_hour:02d}:{random.choice([0, 15, 30, 45]):02d}:00Z"


    arrival_hour = (base_hour + int(route["duration_hours"])) % 24
    arrival_minute = random.choice([0, 15, 30, 45])
    scheduled_arrival = f"2024-01-15T{arrival_hour:02d}:{arrival_minute:02d}:00Z"


    status_options = [
        {"status": "on_time", "delay_minutes": 0, "probability": 0.70},
        {"status": "delayed", "delay_minutes": random.randint(15, 60), "probability": 0.20},
        {"status": "significantly_delayed", "delay_minutes": random.randint(61, 180), "probability": 0.07},
        {"status": "cancelled", "delay_minutes": 0, "probability": 0.02},
        {"status": "boarding", "delay_minutes": random.randint(-5, 10), "probability": 0.01}
    ]

    selected_status = random.choices(
        status_options,
        weights=[s["probability"] for s in status_options]
    )[0]


    gates = ["A", "B", "C", "D"]
    departure_gate = f"{random.choice(gates)}{random.randint(1, 30)}"
    arrival_gate = f"{random.choice(gates)}{random.randint(1, 30)}"


    urgency_level = "high" if selected_status["delay_minutes"] > 60 else "medium" if selected_status["delay_minutes"] > 15 else "low"


    incidents = []
    if selected_status["delay_minutes"] > 30:
        incident_types = ["weather", "technical_issue", "air_traffic", "crew_delay", "airport_congestion"]
        incidents.append({
            "type": random.choice(incident_types),
            "description": f"Flight delayed due to {random.choice(incident_types).replace('_', ' ')}",
            "estimated_resolution": f"{random.randint(30, 120)} minutes"
        })


    rebooking_options = []
    if selected_status["status"] == "cancelled" or selected_status["delay_minutes"] > 180:
        rebooking_options = [
            {
                "flight_number": f"{airline_code}{int(flight_num) + 2}",
                "departure_time": f"2024-01-15T{(base_hour + 4) % 24:02d}:00:00Z",
                "availability": random.choice(["available", "waitlist"]),
                "additional_cost": round(random.uniform(0, 150), 2)
            },
            {
                "flight_number": f"{airline_code}{int(flight_num) + 4}",
                "departure_time": f"2024-01-16T{base_hour:02d}:00:00Z",
                "availability": "available",
                "additional_cost": 0
            }
        ]

    return json.dumps({
        "flight_number": flight_number,
        "airline": airline_info,
        "route": {
            "origin_airport": route["origin"],
            "destination_airport": route["destination"],
            "flight_duration_hours": route["duration_hours"]
        },
        "schedule": {
            "scheduled_departure": scheduled_departure,
            "scheduled_arrival": scheduled_arrival,
            "actual_departure": scheduled_departure if selected_status["delay_minutes"] == 0 else None,
            "actual_arrival": scheduled_arrival if selected_status["delay_minutes"] == 0 else None
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
            "last_updated": "2024-01-15T10:30:00Z"
        },
        "gate_information": {
            "departure_gate": departure_gate,
            "arrival_gate": arrival_gate if selected_status["status"] != "cancelled" else None,
            "terminal": random.choice(["T1", "T2", "T3", "T4"])
        },
        "passenger_impact": {
            "urgency_level": urgency_level,
            "rebooking_required": selected_status["status"] == "cancelled",
            "compensation_eligible": selected_status["delay_minutes"] > 120,
            "connection_risk": "high" if selected_status["delay_minutes"] > 30 else "low"
        },
        "incidents": incidents,
        "rebooking_options": rebooking_options,
        "travel_recommendations": [
            "Monitor flight status regularly",
            "Arrive at airport 2 hours early for international flights",
            "Complete online check-in if available"
        ] + (["Consider rebooking options", "Contact airline customer service"] if selected_status["status"] in ["cancelled", "significantly_delayed"] else []),
        "weather_conditions": {
            "origin": random.choice(["clear", "light_rain", "cloudy", "foggy"]),
            "destination": random.choice(["clear", "light_rain", "cloudy", "windy"]),
            "weather_impact": selected_status["delay_minutes"] > 45 and random.choice([True, False])
        },
        "timestamp": "2024-01-15T10:30:00Z"
    })
