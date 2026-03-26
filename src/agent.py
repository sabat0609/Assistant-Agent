from src.llm import ask_llm
from src.memory import add_message, get_history
from src.rag import retrieve_context
from src.escalation import should_escalate


def classify_intent(query):
    prompt = f"""
Classify the intent of this query:
"{query}"

Categories:
- account
- shipping
- returns
- billing
- technical
- general

Only return one word.
"""
    try:
        return ask_llm(prompt).strip().lower()
    except:
        return "general"


def format_knowledge(context):
    """Convert KB results into readable text"""
    formatted = ""

    for item in context:
        formatted += f"\nQ: {item.get('question', '')}\n"

        if "answer" in item:
            formatted += f"A: {item['answer']}\n"

        if "steps" in item:
            formatted += "Steps:\n"
            for i, step in enumerate(item["steps"], 1):
                formatted += f"{i}. {step}\n"

        if "details" in item:
            formatted += "Details:\n"
            for d in item["details"]:
                formatted += f"- {d}\n"

    return formatted


def generate_response(query, context, history):
    formatted_context = format_knowledge(context)

    prompt = f"""
You are a professional customer support agent for Aura Electronics.

STRICT RULES:
- Always acknowledge the customer's concern first
- Be empathetic and professional
- Use numbered steps for troubleshooting
- Use bullet points for policies
- Keep response under 200 words
- Ask ONLY ONE question if clarification is needed
- If unsure, say you are not sure

Conversation history:
{history}

Knowledge base:
{formatted_context}

User query:
{query}

Generate a helpful response.
"""
    try:
        return ask_llm(prompt)
    except:
        return "I'm sorry, I'm having trouble responding right now. Let me escalate this for you."


def agent(query):
    # store user message
    add_message("user", query)

    # 🚨 STEP 1: Escalation check (CRITICAL RULE)
    if should_escalate(query):
        return {
            "status": "escalated",
            "message": "I've escalated your case to a specialist. They will contact you shortly.",
            "reason": "critical_trigger"
        }

    # STEP 2: Intent classification
    intent = classify_intent(query)

    # STEP 3: Retrieve knowledge
    context = retrieve_context(query)

    # STEP 4: Generate response
    response = generate_response(query, context, get_history())

    # STEP 5: Confidence (simplified for stability)
    confidence = 0.85

    # store assistant response
    add_message("assistant", response)

    return {
        "status": "resolved",
        "intent": intent,
        "confidence": confidence,
        "response": response
    }
