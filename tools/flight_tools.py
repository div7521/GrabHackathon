import random
from datetime import datetime, timedelta
from google.generativeai import types

def check_flight_status(flight_number, airline=None, departure_airport=None):
    """
    Check real-time flight status to help coordinate urgent deliveries
    to passengers heading to the airport.
    """
    
    # Simulate realistic flight scenarios
    flight_scenarios = [
        {
            "status": "On Time",
            "departure_delay": 0,
            "gate": f"A{random.randint(1, 30)}",
            "boarding_status": "Not Started",
            "estimated_boarding": "45 minutes"
        },
        {
            "status": "Delayed", 
            "departure_delay": random.randint(15, 90),
            "gate": f"B{random.randint(1, 25)}",
            "boarding_status": "Delayed",
            "estimated_boarding": "TBD"
        },
        {
            "status": "Boarding",
            "departure_delay": random.randint(-5, 10),
            "gate": f"C{random.randint(1, 20)}",
            "boarding_status": "Now Boarding", 
            "estimated_boarding": "In Progress"
        },
        {
            "status": "Final Call",
            "departure_delay": 0,
            "gate": f"A{random.randint(1, 30)}",
            "boarding_status": "Final Call",
            "estimated_boarding": "Closing Soon"
        }
    ]
    
    scenario = random.choice(flight_scenarios)
    
    # Calculate times
    now = datetime.now()
    scheduled_departure = now + timedelta(minutes=random.randint(30, 180))
    actual_departure = scheduled_departure + timedelta(minutes=scenario['departure_delay'])
    
    flight_info = f"""
Flight Status Report:
- Flight Number: {flight_number}
- Airline: {airline or 'Unknown Airline'}
- Departure Airport: {departure_airport or 'Unknown Airport'}
- Current Status: {scenario['status']}
- Gate: {scenario['gate']}

⏰ TIMING DETAILS:
- Scheduled Departure: {scheduled_departure.strftime('%I:%M %p')}
- Actual Departure: {actual_departure.strftime('%I:%M %p')}
- Delay: {scenario['departure_delay']} minutes
- Boarding Status: {scenario['boarding_status']}
- Estimated Boarding: {scenario['estimated_boarding']}

🚨 PASSENGER URGENCY ASSESSMENT:
"""
    
    if scenario['status'] == "On Time":
        flight_info += "- Urgency Level: MODERATE - Standard delivery timeline acceptable"
        flight_info += "\n- Recommendation: Proceed with normal delivery"
    elif scenario['status'] == "Delayed":
        flight_info += f"- Urgency Level: LOW - Flight delayed {scenario['departure_delay']} minutes"
        flight_info += "\n- Recommendation: Extra time available for delivery"
    elif scenario['status'] == "Boarding":
        flight_info += "- Urgency Level: HIGH - Passenger needs to be at gate NOW"
        flight_info += "\n- Recommendation: URGENT delivery required"
    else:  # Final Call
        flight_info += "- Urgency Level: CRITICAL - Flight boarding is closing"
        flight_info += "\n- Recommendation: EMERGENCY delivery protocols"
    
    flight_info += f"""

📍 DELIVERY COORDINATION:
- Airport Arrival Recommended: {(actual_departure - timedelta(minutes=90)).strftime('%I:%M %p')}
- Traffic Buffer Time: 30 minutes recommended
- Drop-off Location: Departure terminal curbside
"""
    
    return flight_info

schema_check_flight_status = types.FunctionDeclaration(
    name="check_flight_status",
    description="Checks real-time flight status to coordinate urgent deliveries to passengers heading to airport. Provides departure times, delays, and urgency assessment.",
    parameters={
        "type": "object",
        "properties": {
            "flight_number": {
                "type": "string",
                "description": "The flight number to check (e.g., 'AA123', 'SQ456')",
            },
            "airline": {
                "type": "string",
                "description": "The airline name (optional, for verification)",
            },
            "departure_airport": {
                "type": "string",
                "description": "The departure airport code or name (optional)",
            },
        },
        "required": ["flight_number"],
    },
)