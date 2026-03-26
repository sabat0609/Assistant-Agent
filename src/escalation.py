ESCALATION_KEYWORDS = [
    "fraud", "unauthorized", "lawsuit", "lawyer",
    "injury", "fire", "damage", "abuse", "threat",
    "speak to manager", "human agent"
]

def should_escalate(query):
    query = query.lower()
    return any(word in query for word in ESCALATION_KEYWORDS)
