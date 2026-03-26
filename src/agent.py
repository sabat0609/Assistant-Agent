from src.llm import ask_llm
from src.memory import add_message, get_history
from src.rag import retrieve_context

def classify_intent(query):
    prompt = f"""
    Classify the intent of this query:
    "{query}"

    Categories:
    - refund
    - return
    - shipping
    - technical
    - general

    Only return one word.
    """
    return ask_llm(prompt).strip()


def generate_response(query, context, history):
    prompt = f"""
    You are a polite and helpful customer support agent.

    Conversation history:
    {history}

    Knowledge base:
    {context}

    User query:
    {query}

    Answer clearly and professionally.
    If unsure, say you are not sure.
    """
    return ask_llm(prompt)


def check_confidence(response):
    prompt = f"""
    Rate confidence of this response from 0 to 1:
    "{response}"

    Only return a number.
    """
    try:
        score = float(ask_llm(prompt))
        return score
    except:
        return 0.5


def agent(query):
    # store user message
    add_message("user", query)

    # classify intent
    intent = classify_intent(query)

    # retrieve knowledge
    context = retrieve_context(query)

    # generate response
    response = generate_response(query, context, get_history())

    # confidence check
    confidence = check_confidence(response)

    # escalation logic
    if confidence < 0.4:
        return {
            "status": "escalated",
            "message": "Escalating to human agent.",
            "context": get_history()
        }

    # store assistant response
    add_message("assistant", response)

    return {
        "status": "resolved",
        "intent": intent,
        "confidence": confidence,
        "response": response
    }