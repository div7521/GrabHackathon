import random
from google.genai import types

def initiate_mediation_flow(order_id, driver_id, customer_id, dispute_type):
    """
    Start a real-time mediation session between driver and customer
    for at-the-door disputes, creating a synchronized resolution interface.
    """

    session_id = f"MED_{random.randint(100000, 999999)}"

    mediation_setup = f"""
Real-Time Mediation Session Initiated:
- Session ID: {session_id}
- Order ID: {order_id}
- Driver ID: {driver_id}
- Customer ID: {customer_id}
- Dispute Type: {dispute_type}
- Session Status: 🟢 ACTIVE
- Interface: ✅ Synchronized on both devices
- Order Completion: ⏸️ PAUSED until resolution

Mediation Interface Features:
- Real-time chat between parties
- Photo/video evidence upload
- Guided questionnaire system
- AI-assisted resolution suggestions
- Instant compensation processing
- Automated documentation

Session Controls:
- Maximum Duration: 15 minutes
- Auto-escalation: If unresolved after 10 minutes
- Emergency Support: Available via panic button
- Session Recording: ✅ Enabled for quality assurance

Next Step: Proceed to evidence collection phase
"""

    return mediation_setup

schema_initiate_mediation_flow = types.FunctionDeclaration(
    name="initiate_mediation_flow",
    description="Initiates a real-time mediation session between driver and customer for at-the-door disputes. Creates synchronized interface on both devices to resolve conflicts immediately.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "order_id": types.Schema(
                type=types.Type.STRING,
                description="The order ID where the dispute occurred",
            ),
            "driver_id": types.Schema(
                type=types.Type.STRING,
                description="The driver involved in the dispute",
            ),
            "customer_id": types.Schema(
                type=types.Type.STRING,
                description="The customer involved in the dispute",
            ),
            "dispute_type": types.Schema(
                type=types.Type.STRING,
                description="Type of dispute (e.g., 'damaged_packaging', 'missing_items', 'delivery_condition')",
            ),
        },
        required=["order_id", "driver_id", "customer_id", "dispute_type"],
    ),
)

def collect_evidence(session_id, evidence_type, party_type):
    """
    Guide both driver and customer through structured evidence collection
    with photos, questionnaires, and relevant documentation.
    """

    # Simulate evidence collection results
    evidence_scenarios = {
        "driver": {
            "photos_taken": random.randint(2, 5),
            "questionnaire_completed": True,
            "response_time": f"{random.randint(1, 4)} minutes",
            "compliance": random.choice(["fully_compliant", "partially_compliant"])
        },
        "customer": {
            "photos_taken": random.randint(1, 4),
            "questionnaire_completed": True,
            "response_time": f"{random.randint(1, 6)} minutes",
            "compliance": random.choice(["fully_compliant", "partially_compliant"])
        }
    }

    party_data = evidence_scenarios.get(party_type, evidence_scenarios["customer"])

    evidence_result = f"""
Evidence Collection Results:
- Session ID: {session_id}
- Evidence Type: {evidence_type}
- Collecting Party: {party_type.title()}
- Photos Submitted: {party_data['photos_taken']} images
- Photo Quality: ✅ All images clear and relevant
- Questionnaire Status: {'✅ Completed' if party_data['questionnaire_completed'] else '❌ Incomplete'}
- Response Time: {party_data['response_time']}
- Compliance Level: {party_data['compliance'].replace('_', ' ').title()}

Evidence Details Collected:
"""

    if evidence_type == "damaged_packaging":
        evidence_result += """- Package condition upon handover: Documented
- Seal integrity status: Photographed
- Damage location and extent: Mapped
- Handling process verification: Recorded"""

    elif evidence_type == "missing_items":
        evidence_result += """- Package weight verification: Recorded
- Merchant packaging process: Documented
- Delivery bag inspection: Photographed
- Item checklist comparison: Completed"""

    else:
        evidence_result += """- General delivery condition: Documented
- Environmental factors: Recorded
- Process adherence: Verified
- Timeline verification: Logged"""

    evidence_result += """

Evidence Status: ✅ Successfully collected and stored
Next Step: Ready for automated analysis
"""

    return evidence_result

schema_collect_evidence = types.FunctionDeclaration(
    name="collect_evidence",
    description="Guides both driver and customer through structured evidence collection using photos, questionnaires, and documentation. Essential for fair dispute resolution.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "session_id": types.Schema(
                type=types.Type.STRING,
                description="The mediation session ID where evidence is being collected",
            ),
            "evidence_type": types.Schema(
                type=types.Type.STRING,
                description="Type of evidence being collected (e.g., 'damaged_packaging', 'missing_items', 'delivery_condition')",
            ),
            "party_type": types.Schema(
                type=types.Type.STRING,
                description="Which party is providing evidence ('driver' or 'customer')",
            ),
        },
        required=["session_id", "evidence_type", "party_type"],
    ),
)

def analyze_evidence(session_id, collected_evidence_summary):
    """
    AI-powered analysis of collected evidence to determine fault
    and recommend fair resolution for all parties involved.
    """

    # Simulate AI analysis results
    analysis_outcomes = [
        {
            "fault_determination": "merchant_fault",
            "confidence": "94%",
            "key_factors": ["Bag seal was intact", "Damage occurred pre-delivery", "Driver followed protocol"],
            "recommended_action": "Full customer refund + driver exoneration"
        },
        {
            "fault_determination": "no_fault_incident",
            "confidence": "87%",
            "key_factors": ["External factors", "Reasonable handling", "Unavoidable circumstances"],
            "recommended_action": "Partial customer compensation + driver protection"
        },
        {
            "fault_determination": "shared_responsibility",
            "confidence": "76%",
            "key_factors": ["Mixed evidence", "Multiple contributing factors"],
            "recommended_action": "Split compensation + education for both parties"
        }
    ]

    analysis = random.choice(analysis_outcomes)

    analysis_result = f"""
AI Evidence Analysis Complete:
- Session ID: {session_id}
- Evidence Reviewed: {collected_evidence_summary}
- Analysis Confidence: {analysis['confidence']}
- Processing Time: {random.randint(15, 45)} seconds

🎯 FAULT DETERMINATION: {analysis['fault_determination'].replace('_', ' ').upper()}

Key Contributing Factors:
"""

    for i, factor in enumerate(analysis['key_factors'], 1):
        analysis_result += f"{i}. {factor}\n"

    analysis_result += f"""
📋 RECOMMENDED RESOLUTION:
{analysis['recommended_action']}

Resolution Breakdown:
- Customer Impact: Fair compensation based on evidence
- Driver Impact: Protection from unfair penalties
- Merchant Impact: Feedback for process improvement
- System Learning: Case added to ML training dataset

Status: ✅ Ready for automated resolution execution
"""

    return analysis_result

schema_analyze_evidence = types.FunctionDeclaration(
    name="analyze_evidence",
    description="AI-powered analysis of collected dispute evidence to determine fault and recommend fair resolutions. Uses machine learning to ensure objective decision-making.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "session_id": types.Schema(
                type=types.Type.STRING,
                description="The mediation session ID being analyzed",
            ),
            "collected_evidence_summary": types.Schema(
                type=types.Type.STRING,
                description="Summary of all evidence collected from both parties",
            ),
        },
        required=["session_id", "collected_evidence_summary"],
    ),
)
