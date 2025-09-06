import random
from config import PARCEL_LOCKERS
from google.genai import types

def suggest_safe_drop_off(delivery_address, package_value, recipient_preferences=None):
    """
    Suggest secure drop-off alternatives when recipient is unavailable,
    considering package value and location safety.
    """

    # Determine area from address (simplified)
    area = "Downtown"  # Default
    if "mall" in delivery_address.lower():
        area = "Mall Area"
    elif "business" in delivery_address.lower() or "office" in delivery_address.lower():
        area = "Business District"

    # Generate drop-off suggestions based on package value
    low_value_options = [
        "Building front desk/concierge",
        "Trusted neighbor (with permission)",
        "Building management office",
        "Secure mailroom"
    ]

    high_value_options = [
        "Building concierge with ID verification",
        "Secure parcel room with access code",
        "Building management with signature required"
    ]

    package_val = float(package_value.replace('$', '')) if isinstance(package_value, str) else float(package_value)
    options = high_value_options if package_val > 50 else low_value_options

    suggestions = f"""
Safe Drop-off Analysis:
- Delivery Address: {delivery_address}
- Package Value: ${package_val}
- Security Level Required: {'High' if package_val > 50 else 'Standard'}
- Area Assessment: {area}

RECOMMENDED DROP-OFF OPTIONS:

"""

    for i, option in enumerate(options, 1):
        security_score = random.randint(7, 10) if package_val > 50 else random.randint(6, 9)
        availability = random.choice(["Available now", "Available 9 AM - 6 PM", "Available 24/7"])

        suggestions += f"{i}. {option}\n"
        suggestions += f"   - Security Score: {security_score}/10\n"
        suggestions += f"   - Availability: {availability}\n"
        suggestions += f"   - Recipient Notification: {'Required' if package_val > 50 else 'Recommended'}\n\n"

    suggestions += "IMPORTANT: All drop-offs require photo confirmation and recipient notification"

    return suggestions

schema_suggest_safe_drop_off = types.FunctionDeclaration(
    name="suggest_safe_drop_off",
    description="Suggests secure drop-off alternatives when the recipient is unavailable, considering package value, location safety, and building amenities.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "delivery_address": types.Schema(
                type=types.Type.STRING,
                description="The delivery address where safe drop-off is needed",
            ),
            "package_value": types.Schema(
                type=types.Type.STRING,
                description="The value of the package (e.g., '$25.00', '$150.00')",
            ),
            "recipient_preferences": types.Schema(
                type=types.Type.STRING,
                description="Any specific preferences mentioned by the recipient",
            ),
        },
        required=["delivery_address", "package_value"],
    ),
)

def find_nearby_locker(location, package_dimensions=None):
    """
    Find secure parcel lockers near the delivery location as an alternative
    delivery point when recipient is unavailable.
    """

    if location not in PARCEL_LOCKERS:
        return f"No parcel lockers found in {location}. Checking nearby areas..."

    lockers = PARCEL_LOCKERS[location]

    locker_results = f"""
Nearby Parcel Locker Search:
- Search Location: {location}
- Available Lockers: {len(lockers)} facilities found
- Search Radius: 2 miles

AVAILABLE LOCKER FACILITIES:

"""

    for i, locker_name in enumerate(lockers, 1):
        # Generate realistic locker details
        distance = round(random.uniform(0.2, 1.8), 1)
        available_sizes = random.sample(["Small", "Medium", "Large", "Extra Large"], random.randint(2, 4))
        hours = random.choice(["24/7", "6 AM - 10 PM", "7 AM - 9 PM"])
        cost = random.choice(["Free", "$1.99", "$2.99", "$0.99"])

        locker_results += f"{i}. {locker_name}\n"
        locker_results += f"   - Distance: {distance} miles\n"
        locker_results += f"   - Available Sizes: {', '.join(available_sizes)}\n"
        locker_results += f"   - Operating Hours: {hours}\n"
        locker_results += f"   - Storage Cost: {cost}\n"
        locker_results += "   - Security: 24/7 monitoring + access code\n"
        locker_results += "   - Pickup Window: 72 hours\n\n"

    # Add package dimension check if provided
    if package_dimensions:
        locker_results += f"Package Dimensions: {package_dimensions}\n"
        locker_results += "Size compatibility verified for all listed lockers\n\n"

    locker_results += """AUTO-SETUP FEATURES:
- Recipient SMS with pickup code
- Location directions and photos
- Pickup reminder notifications
- Automatic refund if not collected"""

    return locker_results

schema_find_nearby_locker = types.FunctionDeclaration(
    name="find_nearby_locker",
    description="Locates secure parcel lockers near the delivery address as alternative delivery points when recipients are unavailable. Provides details on capacity, security, and costs.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "location": types.Schema(
                type=types.Type.STRING,
                description="The area to search for parcel lockers (e.g., 'Downtown', 'Mall Area', 'Business District')",
            ),
            "package_dimensions": types.Schema(
                type=types.Type.STRING,
                description="Optional package dimensions to check locker compatibility (e.g., '12x8x4 inches')",
            ),
        },
        required=["location"],
    ),
)

def log_merchant_packaging_feedback(merchant_id, incident_id, feedback_type, evidence_details):
    """
    Send evidence-backed feedback to merchants about packaging issues
    to help them improve their processes and reduce future problems.
    """

    feedback_id = f"FB_{random.randint(10000, 99999)}"

    feedback_categories = {
        "packaging_inadequate": {
            "severity": "High",
            "action_required": "Immediate packaging review",
            "training_needed": "Yes"
        },
        "seal_issues": {
            "severity": "Medium",
            "action_required": "Seal quality improvement",
            "training_needed": "Recommended"
        },
        "fragile_handling": {
            "severity": "High",
            "action_required": "Fragile item protocol review",
            "training_needed": "Yes"
        },
        "general_improvement": {
            "severity": "Low",
            "action_required": "Process optimization",
            "training_needed": "Optional"
        }
    }

    category_info = feedback_categories.get(feedback_type, feedback_categories["general_improvement"])

    feedback_report = f"""
Merchant Feedback Report Generated:
- Feedback ID: {feedback_id}
- Merchant ID: {merchant_id}
- Incident Reference: {incident_id}
- Feedback Type: {feedback_type}
- Severity Level: {category_info['severity']}
- Evidence Attached: Photos and incident details included

FEEDBACK SUMMARY:
{evidence_details}

RECOMMENDED ACTIONS:
- Primary Action: {category_info['action_required']}
- Staff Training: {category_info['training_needed']}
- Follow-up Required: {'Yes' if category_info['severity'] == 'High' else 'Optional'}
- Implementation Timeline: {'Within 7 days' if category_info['severity'] == 'High' else 'Within 30 days'}

MERCHANT IMPACT:
- Quality Score Impact: {'Moderate decrease' if category_info['severity'] == 'High' else 'Minor adjustment'}
- Monitoring Period: 30 days increased oversight
- Support Offered: Best practices guide sent
- Training Resources: Available in merchant portal

Delivery Method: Sent to merchant dashboard + email notification
Response Expected: Within 48 hours for high severity issues
"""

    return feedback_report

schema_log_merchant_packaging_feedback = types.FunctionDeclaration(
    name="log_merchant_packaging_feedback",
    description="Sends evidence-backed feedback to merchants about packaging issues, helping them improve processes and reduce future delivery problems. Includes severity assessment and recommended actions.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "merchant_id": types.Schema(
                type=types.Type.STRING,
                description="The merchant ID that needs to receive feedback",
            ),
            "incident_id": types.Schema(
                type=types.Type.STRING,
                description="The incident or dispute ID that generated this feedback",
            ),
            "feedback_type": types.Schema(
                type=types.Type.STRING,
                description="Type of packaging issue (e.g., 'packaging_inadequate', 'seal_issues', 'fragile_handling')",
            ),
            "evidence_details": types.Schema(
                type=types.Type.STRING,
                description="Detailed description of the evidence and specific packaging problems observed",
            ),
        },
        required=["merchant_id", "incident_id", "feedback_type", "evidence_details"],
    ),
)
