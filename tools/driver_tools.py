import random


def re_route_driver(driver_id, current_order_id, new_task_type, estimated_time):
    """
    Reassign a driver to a different task while waiting for delayed orders,
    optimizing their time and earnings potential.
    """

    new_tasks = [
        {"task": "nearby_short_delivery", "earnings": "$4.50", "location": "0.3 miles away"},
        {"task": "food_pickup_only", "earnings": "$3.20", "location": "0.5 miles away"},
        {"task": "package_delivery", "earnings": "$5.80", "location": "0.8 miles away"},
        {"task": "return_to_merchant_area", "earnings": "$2.00", "location": "merchant zone"}
    ]

    selected_task = random.choice(new_tasks)
    task_id = f"TASK_{random.randint(1000, 9999)}"

    reroute_result = f"""
Driver Re-routing Executed:
- Driver ID: {driver_id}
- Original Order: {current_order_id} (on hold)
- New Task Type: {new_task_type}
- Task ID: {task_id}
- Task Details: {selected_task['task']}
- Additional Earnings: {selected_task['earnings']}
- Distance to New Task: {selected_task['location']}
- Estimated Completion Time: {estimated_time} minutes
- Return Time to Original Order: +{int(estimated_time) + random.randint(5, 15)} minutes
- Driver Status: Accepted new assignment
- GPS Navigation: Updated with new route
- Earnings Impact: Optimized (no idle time loss)
"""

    return reroute_result



def exonerate_driver(driver_id, incident_id, evidence_summary):
    """
    Clear a driver of fault when evidence shows they were not responsible
    for delivery issues, protecting their rating and earnings.
    """

    case_number = f"EXO_{random.randint(10000, 99999)}"

    exoneration_result = f"""
Driver Exoneration Processed:
- Driver ID: {driver_id}
- Incident ID: {incident_id}
- Case Number: {case_number}
- Evidence Reviewed: {evidence_summary}
- Decision: DRIVER EXONERATED
- Fault Assignment: Merchant/External factors
- Rating Impact: No negative rating applied
- Earnings Impact: Full payment maintained
- Record Update: Incident marked as "No Driver Fault"
- Driver Notification: Informed of exoneration
- Appeal Status: Resolved - No further action needed

Driver Protection Measures Applied:
- Performance metrics: Unaffected
- Account standing: Maintained
- Future order eligibility: Unimpacted
- Incident learning: Added to training database
"""

    return exoneration_result
