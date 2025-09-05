# Configuration settings for Project Synapse
MAX_CHARS = 10000

# Tool response limits
TOOL_RESPONSE_LIMIT = 500

# Simulated data for tools
MERCHANTS_DATABASE = {
    "restaurant_001": {"name": "Pizza Palace", "prep_time": 15, "status": "open", "location": "Downtown"},
    "restaurant_002": {"name": "Burger Barn", "prep_time": 40, "status": "overloaded", "location": "Mall Area"},
    "restaurant_003": {"name": "Sushi Spot", "prep_time": 20, "status": "open", "location": "Business District"},
    "restaurant_004": {"name": "Taco Time", "prep_time": 12, "status": "open", "location": "Downtown"},
}

NEARBY_MERCHANTS = {
    "Downtown": ["restaurant_001", "restaurant_004"],
    "Mall Area": ["restaurant_002"],
    "Business District": ["restaurant_003"],
}

TRAFFIC_CONDITIONS = {
    "route_001": {"status": "clear", "delay_minutes": 0, "description": "No issues"},
    "route_002": {"status": "heavy", "delay_minutes": 25, "description": "Major accident on Highway 1"},
    "route_003": {"status": "moderate", "delay_minutes": 10, "description": "Construction work"},
}

ALTERNATIVE_ROUTES = {
    "route_002": ["route_001", "route_003"],  # If route_002 has issues, suggest these
    "route_001": ["route_003"],
    "route_003": ["route_001"],
}

PARCEL_LOCKERS = {
    "Downtown": ["Locker_Hub_A", "SecureBox_Station_1"],
    "Mall Area": ["Mall_Locker_Central", "PickupPoint_B"],
    "Business District": ["Corporate_Lockers", "Express_Hub_C"],
}