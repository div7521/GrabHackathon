import random
from google.genai import types

def contact_recipient_via_chat(recipient_id, message, message_type="automated"):
    """
    Contact the recipient through in-app chat with automated prompts
    for delivery instructions when they're unavailable.
    """

    # Simulate different recipient response scenarios
    response_scenarios = [
        {
            "status": "responded",
            "response": "Please leave with building concierge at front desk",
            "response_time": "2 minutes"
        },
        {
            "status": "responded",
            "response": "I'm in a meeting until 3 PM, can you deliver after that?",
            "response_time": "5 minutes"
        },
        {
            "status": "responded",
            "response": "Leave it with my neighbor in apartment 4B",
            "response_time": "1 minute"
        },
        {
            "status": "no_response",
            "response": None,
            "response_time": None
        }
    ]

    scenario = random.choice(response_scenarios)

    chat_result = f"""
Chat Contact Attempt:
- Recipient ID: {recipient_id}
- Message Sent: {message}
- Message Type: {message_type}
- Delivery Status: Message delivered
- Read Receipt: Message read
- Response Status: {scenario['status']}
"""

    if scenario['status'] == "responded":
        chat_result += f"- Recipient Response: \"{scenario['response']}\"\n"
        chat_result += f"- Response Time: {scenario['response_time']}\n"
        chat_result += "- Next Action: Follow recipient instructions"
    else:
        chat_result += "- Recipient Response: No response after 10 minutes\n"
        chat_result += "- Next Action: Consider alternative delivery options"

    return chat_result.strip()

schema_contact_recipient_via_chat = types.FunctionDeclaration(
    name="contact_recipient_via_chat",
    description="Contacts the package recipient through in-app chat when they're unavailable for delivery. Sends automated prompts asking for delivery instructions.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "recipient_id": types.Schema(
                type=types.Type.STRING,
                description="The unique identifier of the package recipient",
            ),
            "message": types.Schema(
                type=types.Type.STRING,
                description="The message to send to the recipient asking for delivery instructions",
            ),
            "message_type": types.Schema(
                type=types.Type.STRING,
                description="Type of message (automated, urgent, standard)",
            ),
        },
        required=["recipient_id", "message"],
    ),
)

def issue_instant_refund(customer_id, order_id, refund_amount, refund_reason):
    """
    Process an immediate refund for customer due to delivery issues,
    damaged items, or service failures.
    """

    refund_methods = ["original_payment_method", "grab_wallet", "grab_credits"]
    selected_method = random.choice(refund_methods)

    transaction_id = f"REF_{random.randint(100000, 999999)}"
    processing_time = random.choice(["Instant", "2-3 business days", "24-48 hours"])

    refund_result = f"""
Instant Refund Processed:
- Customer ID: {customer_id}
- Order ID: {order_id}
- Refund Amount: ${refund_amount}
- Reason: {refund_reason}
- Transaction ID: {transaction_id}
- Refund Method: {selected_method}
- Processing Time: {processing_time}
- Status: APPROVED & PROCESSED
- Customer Notification: SMS and push notification sent
- Accounting: Automatically logged for reconciliation
"""

    # Add additional details based on refund reason
    if "damage" in refund_reason.lower():
        refund_result += "\n- Quality Assurance: Merchant feedback report generated"
        refund_result += "\n- Photo Evidence: Stored for merchant review"

    if "delay" in refund_reason.lower():
        refund_result += "\n- Compensation: Additional $2 service credit applied"
        refund_result += "\n- Driver Impact: No penalty applied to driver"

    return refund_result

schema_issue_instant_refund = types.FunctionDeclaration(
    name="issue_instant_refund",
    description="Processes an immediate refund to the customer for delivery issues, damaged items, or service failures. Handles payment processing and notifications automatically.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "customer_id": types.Schema(
                type=types.Type.STRING,
                description="The unique identifier of the customer receiving the refund",
            ),
            "order_id": types.Schema(
                type=types.Type.STRING,
                description="The order ID associated with the refund",
            ),
            "refund_amount": types.Schema(
                type=types.Type.STRING,
                description="The refund amount (e.g., '15.50', '8.99')",
            ),
            "refund_reason": types.Schema(
                type=types.Type.STRING,
                description="Reason for the refund (e.g., 'damaged packaging', 'excessive delay', 'wrong order')",
            ),
        },
        required=["customer_id", "order_id", "refund_amount", "refund_reason"],
    ),
)
