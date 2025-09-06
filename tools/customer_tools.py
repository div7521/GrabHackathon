import time
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

def contact_recipient_via_chat(recipient_id: str, message: str, delivery_context: str = "package_delivery",
                              urgency: str = "normal", timeout_minutes: int = 10) -> str:
    """
    Initiate real-time chat communication with package recipient to resolve delivery issues.

    Args:
        recipient_id: Unique recipient identifier
        message: Initial chat message content
        delivery_context: Context of delivery ('package_delivery', 'food_delivery', 'document_delivery')
        urgency: Message urgency level ('low', 'normal', 'high', 'urgent')
        timeout_minutes: How long to wait for recipient response

    Returns:
        JSON string containing chat initiation status and recipient response
    """
    # Realistic delay for chat system initialization + message delivery
    time.sleep(random.uniform(0.4, 1.5))

    # Basic validation
    if not recipient_id or not isinstance(recipient_id, str):
        return json.dumps({
            "status": "error",
            "error_code": "INVALID_RECIPIENT_ID",
            "message": "Recipient ID is required and must be a valid string",
            "timestamp": datetime.now().isoformat()
        }, indent=2)

    if not message or len(message.strip()) < 3:
        return json.dumps({
            "status": "error",
            "error_code": "INVALID_MESSAGE",
            "message": "Message content must be at least 3 characters long",
            "timestamp": datetime.now().isoformat()
        }, indent=2)

    current_time = datetime.now()
    chat_session_id = f"CHAT_{random.randint(100000, 999999)}"

    # Simulate recipient availability based on time of day and urgency
    current_hour = current_time.hour
    availability_score = 0.8  # Base availability

    # Time-based availability adjustments
    if 9 <= current_hour <= 17:  # Business hours
        availability_score = 0.85
    elif 18 <= current_hour <= 22:  # Evening
        availability_score = 0.75
    elif 22 <= current_hour or current_hour <= 7:  # Late night/early morning
        availability_score = 0.3

    # Urgency adjustments
    if urgency == "urgent":
        availability_score = min(1.0, availability_score + 0.2)
    elif urgency == "high":
        availability_score = min(1.0, availability_score + 0.1)

    # Determine if recipient responds
    recipient_responds = random.random() < availability_score

    # Chat delivery status
    chat_delivery = {
        "message_delivered": True,
        "delivery_time_ms": random.randint(200, 800),
        "delivery_channel": random.choice(["sms", "in_app", "push_notification"]),
        "read_receipt": random.choice([True, True, False]) if recipient_responds else False,
        "read_time": (current_time + timedelta(seconds=random.randint(10, 120))).isoformat() if recipient_responds and random.choice([True, False]) else None
    }

    # Generate recipient response if they respond
    recipient_response = None
    if recipient_responds:
        response_time_minutes = random.randint(1, min(timeout_minutes, 8))

        # Different response scenarios based on delivery context
        response_scenarios = {
            "package_delivery": [
                {"response": "I'm not home right now, can you leave it with the building manager?", "intent": "alternative_dropoff"},
                {"response": "I'll be home in 20 minutes, can you wait?", "intent": "delay_request"},
                {"response": "Please leave it at the door, it's safe here", "intent": "door_delivery"},
                {"response": "Can you deliver tomorrow instead? I'm traveling", "intent": "reschedule"},
                {"response": "I'm here now, where are you?", "intent": "immediate_delivery"}
            ],
            "food_delivery": [
                {"response": "I'm in the lobby, come down", "intent": "location_update"},
                {"response": "Please call when you arrive", "intent": "communication_preference"},
                {"response": "Leave it with security, they know me", "intent": "alternative_dropoff"},
                {"response": "I'm running 5 minutes late", "intent": "delay_request"}
            ],
            "document_delivery": [
                {"response": "I need to see ID verification first", "intent": "security_check"},
                {"response": "Please deliver to reception desk", "intent": "alternative_dropoff"},
                {"response": "I'm in meeting room 5B on 3rd floor", "intent": "location_update"}
            ]
        }

        scenario_responses = response_scenarios.get(delivery_context, response_scenarios["package_delivery"])
        selected_response = random.choice(scenario_responses)

        recipient_response = {
            "responded": True,
            "response_time_minutes": response_time_minutes,
            "response_text": selected_response["response"],
            "intent_detected": selected_response["intent"],
            "response_timestamp": (current_time + timedelta(minutes=response_time_minutes)).isoformat(),
            "sentiment": random.choice(["positive", "neutral", "cooperative", "concerned"]),
            "follow_up_needed": selected_response["intent"] in ["delay_request", "reschedule", "security_check"]
        }
    else:
        recipient_response = {
            "responded": False,
            "timeout_reached": True,
            "timeout_duration_minutes": timeout_minutes,
            "last_seen": random.choice([
                "2 hours ago",
                "30 minutes ago",
                "1 day ago",
                "unknown"
            ])
        }

    # Generate next steps based on response
    recommended_actions = []
    if recipient_response.get("responded"):
        intent = recipient_response.get("intent_detected")
        if intent == "alternative_dropoff":
            recommended_actions.extend([
                "Verify alternative drop-off location security",
                "Take photo confirmation of delivery"
            ])
        elif intent == "delay_request":
            recommended_actions.extend([
                "Confirm new delivery timeframe",
                "Update customer and dispatch on delay"
            ])
        elif intent == "reschedule":
            recommended_actions.extend([
                "Initiate rescheduling process",
                "Return package to facility"
            ])
        elif intent == "immediate_delivery":
            recommended_actions.append("Proceed with immediate delivery")
    else:
        recommended_actions.extend([
            "Try alternative contact methods",
            "Consider safe drop-off options",
            "Contact dispatch for guidance"
        ])

    response_data = {
        "status": "success",
        "chat_session": {
            "session_id": chat_session_id,
            "recipient_id": recipient_id,
            "initiated_timestamp": current_time.isoformat(),
            "delivery_context": delivery_context,
            "urgency_level": urgency
        },
        "initial_message": {
            "content": message,
            "character_count": len(message),
            "delivery_status": chat_delivery
        },
        "recipient_response": recipient_response,
        "availability_analysis": {
            "estimated_availability": round(availability_score * 100, 1),
            "factors_considered": ["time_of_day", "urgency_level", "historical_patterns"],
            "time_of_day_factor": current_hour,
            "optimal_contact_time": "9:00-17:00" if current_hour < 9 or current_hour > 22 else "current_time"
        },
        "recommended_actions": recommended_actions,
        "escalation": {
            "required": not recipient_response.get("responded", False) and urgency in ["high", "urgent"],
            "next_steps": ["Try phone call", "Contact emergency contact"] if not recipient_response.get("responded", False) and urgency == "urgent" else [],
            "timeout_policy": f"Auto-escalate after {timeout_minutes} minutes without response"
        },
        "metadata": {
            "processing_time_ms": random.randint(400, 1500),
            "chat_platform": "unified_messaging_v2",
            "success_rate_estimate": round(availability_score * 100, 1)
        }
    }

    return json.dumps(response_data, indent=2)


def issue_instant_refund(customer_id: str, order_id: str, refund_amount: float, refund_reason: str,
                        refund_type: str = "full", approval_required: bool = False) -> str:
    """
    Process immediate refund for service failures or customer satisfaction issues.

    Args:
        customer_id: Unique customer identifier
        order_id: Order or transaction identifier
        refund_amount: Amount to refund in local currency
        refund_reason: Reason for the refund
        refund_type: Type of refund ('full', 'partial', 'service_credit', 'voucher')
        approval_required: Whether manager approval is needed for this refund

    Returns:
        JSON string containing refund processing status and transaction details
    """
    # Realistic delay for payment processing + verification
    time.sleep(random.uniform(0.8, 2.5))

    # Basic validation
    if not customer_id or not isinstance(customer_id, str):
        return json.dumps({
            "status": "error",
            "error_code": "INVALID_CUSTOMER_ID",
            "message": "Customer ID is required and must be a valid string",
            "timestamp": datetime.now().isoformat()
        }, indent=2)

    if not order_id or not isinstance(order_id, str):
        return json.dumps({
            "status": "error",
            "error_code": "INVALID_ORDER_ID",
            "message": "Order ID is required and must be a valid string",
            "timestamp": datetime.now().isoformat()
        }, indent=2)

    if not isinstance(refund_amount, (int, float)) or refund_amount <= 0:
        return json.dumps({
            "status": "error",
            "error_code": "INVALID_REFUND_AMOUNT",
            "message": "Refund amount must be a positive number",
            "timestamp": datetime.now().isoformat()
        }, indent=2)

    if refund_amount > 500 and not approval_required:
        return json.dumps({
            "status": "error",
            "error_code": "APPROVAL_REQUIRED",
            "message": f"Refunds over $500 require manager approval. Amount: ${refund_amount}",
            "recommended_action": "Request manager approval or reduce refund amount",
            "timestamp": datetime.now().isoformat()
        }, indent=2)

    current_time = datetime.now()
    refund_id = f"REF_{random.randint(100000, 999999)}"
    transaction_id = f"TXN_{random.randint(100000000, 999999999)}"

    # Simulate payment method detection and processing time
    payment_methods = [
        {"type": "credit_card", "processing_time": "1-3 business days", "success_rate": 0.98},
        {"type": "debit_card", "processing_time": "1-2 business days", "success_rate": 0.96},
        {"type": "digital_wallet", "processing_time": "instant", "success_rate": 0.99},
        {"type": "bank_transfer", "processing_time": "3-5 business days", "success_rate": 0.94},
        {"type": "service_credit", "processing_time": "instant", "success_rate": 1.0}
    ]

    original_payment_method = random.choice(payment_methods)

    # Determine processing success
    processing_successful = random.random() < original_payment_method["success_rate"]

    if not processing_successful:
        return json.dumps({
            "status": "failed",
            "error_code": "PROCESSING_FAILED",
            "refund_id": refund_id,
            "failure_reason": random.choice([
                "Payment method no longer valid",
                "Insufficient account information",
                "Bank processing error",
                "Daily limit exceeded"
            ]),
            "alternative_options": [
                "Issue service credit instead",
                "Process manual check",
                "Contact customer for alternative payment method"
            ],
            "retry_available": True,
            "customer_notification_sent": True,
            "timestamp": current_time.isoformat()
        }, indent=2)

    # Calculate processing fees and final amount
    processing_fee = 0.0
    if refund_type == "service_credit":
        # No processing fee for service credits
        processing_fee = 0.0
        final_refund_amount = refund_amount
    else:
        # Small processing fee for monetary refunds
        processing_fee = round(min(refund_amount * 0.025, 2.50), 2)
        final_refund_amount = round(refund_amount - processing_fee, 2)

    # Determine refund timeline based on payment method
    if original_payment_method["type"] == "service_credit" or refund_type == "service_credit":
        expected_availability = "immediately"
        estimated_completion = current_time.isoformat()
    elif original_payment_method["type"] == "digital_wallet":
        expected_availability = "within 2 hours"
        estimated_completion = (current_time + timedelta(hours=2)).isoformat()
    else:
        processing_days = {
            "credit_card": random.randint(1, 3),
            "debit_card": random.randint(1, 2),
            "bank_transfer": random.randint(3, 5)
        }
        days_to_complete = processing_days.get(original_payment_method["type"], 2)
        expected_availability = f"{days_to_complete} business days"
        estimated_completion = (current_time + timedelta(days=days_to_complete)).isoformat()

    # Generate customer communication
    customer_notification = {
        "notification_sent": True,
        "notification_channels": ["email", "in_app", "sms"] if refund_amount > 50 else ["email", "in_app"],
        "confirmation_code": f"CONF_{random.randint(100000, 999999)}",
        "message_preview": f"Your ${final_refund_amount} refund for order {order_id} is being processed. Expected availability: {expected_availability}."
    }

    # Risk assessment for audit trail
    risk_factors = {
        "amount_threshold": "low" if refund_amount < 50 else "medium" if refund_amount < 200 else "high",
        "frequency_check": random.choice(["normal", "elevated", "high"]),  # Based on customer history
        "reason_category": "operational" if "delay" in refund_reason.lower() or "late" in refund_reason.lower() else "quality",
        "approval_bypassed": not approval_required and refund_amount > 100
    }

    response_data = {
        "status": "success",
        "refund_details": {
            "refund_id": refund_id,
            "transaction_id": transaction_id,
            "customer_id": customer_id,
            "order_id": order_id,
            "original_amount": refund_amount,
            "processing_fee": processing_fee,
            "final_refund_amount": final_refund_amount,
            "refund_type": refund_type,
            "currency": "USD"
        },
        "processing_info": {
            "status": "approved_and_processing",
            "initiated_timestamp": current_time.isoformat(),
            "estimated_completion": estimated_completion,
            "expected_availability": expected_availability,
            "payment_method": original_payment_method["type"],
            "processing_priority": "high" if refund_amount > 200 or approval_required else "normal"
        },
        "reason_details": {
            "primary_reason": refund_reason,
            "category": risk_factors["reason_category"],
            "resolution_type": refund_type,
            "customer_satisfaction_impact": random.choice(["positive", "very_positive"])
        },
        "customer_communication": customer_notification,
        "compliance": {
            "audit_trail_created": True,
            "manager_approval": approval_required,
            "risk_assessment": risk_factors,
            "regulatory_compliance": "PCI_DSS_compliant",
            "retention_period_days": 2555  # 7 years
        },
        "follow_up": {
            "customer_feedback_requested": refund_amount > 75,
            "satisfaction_survey_scheduled": (current_time + timedelta(days=3)).isoformat() if refund_amount > 75 else None,
            "review_required": risk_factors["frequency_check"] == "high" or refund_amount > 300
        },
        "system_impact": {
            "inventory_adjustment": refund_type == "full" and "food" in order_id.lower(),
            "merchant_notification": "food" in order_id.lower() or "restaurant" in refund_reason.lower(),
            "driver_impact_check": "delivery" in refund_reason.lower()
        },
        "metadata": {
            "processing_time_ms": random.randint(800, 2500),
            "refund_engine_version": "v3.1",
            "success_rate": original_payment_method["success_rate"],
            "geographic_region": "default"
        }
    }

    return json.dumps(response_data, indent=2)
