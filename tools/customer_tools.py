import time
import json
import random

def contact_recipient_via_chat(recipient_id: str, message: str) -> str:
    """Initiate real-time chat communication with the package recipient to resolve delivery issues.

    Args:
        recipient_id: Unique recipient identifier
        message: Initial chat message content

    Returns:
        JSON string containing chat initiation status and recipient response
    """
    time.sleep(random.uniform(0.1, 0.4))

    if not recipient_id or not message:
        return json.dumps({
            "error": "MISSING_REQUIRED_FIELDS",
            "message": "Recipient ID and message are required"
        })

    chat_delivered = random.choice([True, True, True, False])

    recipient_response = None
    response_time_minutes = None

    if chat_delivered:
        recipient_available = random.choice([True, True, False])

        if recipient_available:
            response_time_minutes = random.randint(1, 10)
            responses = [
                {"text": "I'm not home right now, can you leave it with the neighbor?", "intent": "alternative_delivery"},
                {"text": "I'll be there in 15 minutes, please wait", "intent": "delay_request"},
                {"text": "Please leave it at the door", "intent": "safe_delivery"},
                {"text": "Can you deliver tomorrow instead?", "intent": "reschedule"},
                {"text": "I'm here now, where are you?", "intent": "immediate_delivery"}
            ]
            recipient_response = random.choice(responses)

    return json.dumps({
        "chat_session_id": f"chat_{random.randint(100000, 999999)}",
        "recipient_id": recipient_id,
        "message_sent": message,
        "delivery_status": "delivered" if chat_delivered else "failed",
        "recipient_response": recipient_response,
        "response_time_minutes": response_time_minutes,
        "chat_active": chat_delivered and recipient_response is not None,
        "recommended_actions": [
            "Verify delivery location" if recipient_response and recipient_response["intent"] == "alternative_delivery" else None,
            "Wait for recipient" if recipient_response and recipient_response["intent"] == "delay_request" else None,
            "Take photo confirmation" if recipient_response and recipient_response["intent"] == "safe_delivery" else None,
            "Schedule redelivery" if recipient_response and recipient_response["intent"] == "reschedule" else None,
            "Proceed with delivery" if recipient_response and recipient_response["intent"] == "immediate_delivery" else None
        ],
        "timestamp": "2024-01-15T10:30:00Z"
    })

def issue_instant_refund(customer_id: str, order_id: str, amount: float, reason: str) -> str:
    """Process immediate refunds for service failures, order issues, or customer satisfaction problems.

    Args:
        customer_id: Unique customer identifier
        order_id: Order or transaction identifier
        amount: Amount to refund in local currency
        reason: Reason for the refund

    Returns:
        JSON string containing refund processing status and transaction details
    """
    time.sleep(random.uniform(0.2, 0.6))

    if not all([customer_id, order_id, amount, reason]):
        return json.dumps({
            "error": "MISSING_REQUIRED_FIELDS",
            "message": "Customer ID, order ID, amount, and reason are required"
        })

    if amount <= 0:
        return json.dumps({
            "error": "INVALID_AMOUNT",
            "message": "Refund amount must be greater than zero"
        })

    if amount > 500:
        return json.dumps({
            "error": "AMOUNT_EXCEEDS_LIMIT",
            "message": "Refunds over $500 require manager approval",
            "recommended_action": "escalate_to_supervisor"
        })

    processing_success = random.choice([True, True, True, False])

    if not processing_success:
        return json.dumps({
            "status": "failed",
            "refund_id": f"ref_failed_{random.randint(100000, 999999)}",
            "customer_id": customer_id,
            "order_id": order_id,
            "failure_reason": random.choice([
                "Payment method expired",
                "Insufficient account information",
                "Bank processing error",
                "Daily refund limit exceeded"
            ]),
            "alternative_options": [
                "Issue service credit",
                "Process manual refund",
                "Contact customer for updated payment method"
            ],
            "retry_available": True
        })

    payment_methods = [
        {"method": "credit_card", "processing_time": "1-3 business days"},
        {"method": "digital_wallet", "processing_time": "instant"},
        {"method": "bank_transfer", "processing_time": "3-5 business days"},
        {"method": "service_credit", "processing_time": "instant"}
    ]

    payment_method = random.choice(payment_methods)
    processing_fee = 0.0 if payment_method["method"] == "service_credit" else round(min(amount * 0.029, 2.50), 2)
    final_amount = round(amount - processing_fee, 2)

    return json.dumps({
        "status": "success",
        "refund_id": f"ref_{random.randint(100000, 999999)}",
        "transaction_id": f"txn_{random.randint(100000000, 999999999)}",
        "customer_id": customer_id,
        "order_id": order_id,
        "refund_details": {
            "original_amount": amount,
            "processing_fee": processing_fee,
            "final_refund_amount": final_amount,
            "currency": "USD",
            "payment_method": payment_method["method"],
            "processing_time": payment_method["processing_time"]
        },
        "reason": reason,
        "processing_status": "approved_and_processing",
        "estimated_completion": payment_method["processing_time"],
        "customer_notification": {
            "email_sent": True,
            "sms_sent": amount > 50,
            "confirmation_code": f"CONF_{random.randint(100000, 999999)}"
        },
        "timestamp": "2024-01-15T10:30:00Z"
    })
