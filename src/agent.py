from src.escalation import should_escalate

def agent(query):
    add_message("user", query)

    # 🚨 escalation check FIRST (important rule)
    if should_escalate(query):
        return {
            "status": "escalated",
            "message": "I've escalated your case to a specialist. They will contact you shortly.",
            "reason": "critical_trigger"
        }

    intent = classify_intent(query)
    context = retrieve_context(query)

    response = generate_response(query, context, get_history())

    confidence = 0.8  # keep simple for now

    add_message("assistant", response)

    return {
        "status": "resolved",
        "intent": intent,
        "confidence": confidence,
        "response": response
    }
