import random
from config import MERCHANTS_DATABASE, NEARBY_MERCHANTS
from google.genai import types

def get_merchant_status(merchant_id):
    """
    Check the current status and preparation time of a specific merchant.
    Returns merchant operational status, current prep time, and any alerts.
    """
    if merchant_id not in MERCHANTS_DATABASE:
        return f"Error: Merchant '{merchant_id}' not found in system"

    merchant = MERCHANTS_DATABASE[merchant_id]

    # Simulate some variability in prep times
    base_prep = merchant["prep_time"]
    current_prep = base_prep + random.randint(-5, 15)  # Add some realistic variation

    status_message = f"""
Merchant Status Report:
- Merchant ID: {merchant_id}
- Name: {merchant['name']}
- Location: {merchant['location']}
- Current Status: {merchant['status']}
- Base Prep Time: {base_prep} minutes
- Current Prep Time: {current_prep} minutes
- System Alert: {'HIGH DELAY' if current_prep > 30 else 'NORMAL OPERATIONS'}
"""

    return status_message.strip()

schema_get_merchant_status = types.FunctionDeclaration(
    name="get_merchant_status",
    description="Retrieves the current operational status, preparation time, and alerts for a specific merchant/restaurant. Essential for assessing delivery delays and making proactive decisions.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "merchant_id": types.Schema(
                type=types.Type.STRING,
                description="The unique identifier of the merchant (e.g., 'restaurant_001', 'restaurant_002')",
            ),
        },
        required=["merchant_id"],
    ),
)

def get_nearby_merchants(location, cuisine_type=None):
    """
    Find alternative merchants in the same area that can fulfill similar orders.
    Helps suggest alternatives when primary merchant has issues.
    """
    if location not in NEARBY_MERCHANTS:
        return f"Error: No merchants found in location '{location}'"

    nearby_merchant_ids = NEARBY_MERCHANTS[location]
    alternatives = []

    for merchant_id in nearby_merchant_ids:
        merchant = MERCHANTS_DATABASE[merchant_id]
        prep_time = merchant["prep_time"] + random.randint(-3, 10)

        alternatives.append({
            "merchant_id": merchant_id,
            "name": merchant["name"],
            "prep_time": prep_time,
            "status": merchant["status"],
            "availability": "Available" if merchant["status"] == "open" else "Limited"
        })

    # Sort by prep time (fastest first)
    alternatives.sort(key=lambda x: x["prep_time"])

    result = f"Alternative Merchants in {location}:\n"
    for i, alt in enumerate(alternatives, 1):
        result += f"{i}. {alt['name']} (ID: {alt['merchant_id']})\n"
        result += f"   - Prep Time: {alt['prep_time']} minutes\n"
        result += f"   - Status: {alt['status']}\n"
        result += f"   - Availability: {alt['availability']}\n\n"

    return result.strip()

schema_get_nearby_merchants = types.FunctionDeclaration(
    name="get_nearby_merchants",
    description="Finds alternative merchants in the same geographical area that can fulfill similar orders. Useful when the primary merchant has delays or issues.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "location": types.Schema(
                type=types.Type.STRING,
                description="The geographical area to search for merchants (e.g., 'Downtown', 'Mall Area', 'Business District')",
            ),
            "cuisine_type": types.Schema(
                type=types.Type.STRING,
                description="Optional filter for specific cuisine type (e.g., 'pizza', 'burger', 'sushi')",
            ),
        },
        required=["location"],
    ),
)

def notify_customer(customer_id, message, compensation=None):
    """
    Send proactive notifications to customers about order status, delays, or issues.
    Can include compensation offers when appropriate.
    """
    notification_sent = f"""
Customer Notification Sent:
- Customer ID: {customer_id}
- Message: {message}
- Timestamp: {random.choice(['10:30 AM', '2:45 PM', '6:20 PM', '8:15 PM'])}
- Delivery Method: Push Notification + SMS
"""

    if compensation:
        notification_sent += f"- Compensation Offered: {compensation}\n"
        notification_sent += "- Customer Response Required: Accept/Decline compensation\n"

    notification_sent += "- Status: Successfully Delivered"

    return notification_sent

schema_notify_customer = types.FunctionDeclaration(
    name="notify_customer",
    description="Sends proactive notifications to customers about order updates, delays, issues, or compensation offers. Essential for maintaining customer satisfaction during disruptions.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "customer_id": types.Schema(
                type=types.Type.STRING,
                description="The unique identifier of the customer to notify",
            ),
            "message": types.Schema(
                type=types.Type.STRING,
                description="The message content to send to the customer",
            ),
            "compensation": types.Schema(
                type=types.Type.STRING,
                description="Optional compensation offer (e.g., '$5 voucher', '20% discount on next order')",
            ),
        },
        required=["customer_id", "message"],
    ),
)
