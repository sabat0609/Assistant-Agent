def load_knowledge():
    with open("data/knowledge.txt", "r") as f:
        return f.read()

knowledge = load_knowledge()

def retrieve_context(query):
    query = query.lower()

    if "refund" in query:
        return "Refunds are processed within 5-7 business days."
    elif "return" in query:
        return "Products can be returned within 30 days."
    elif "shipping" in query:
        return "Shipping takes 3-5 business days."
    elif "technical" in query or "not working" in query:
        return "Try restarting the device. If issue persists, contact support."

    return "No relevant information found."