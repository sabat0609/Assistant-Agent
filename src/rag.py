import json

with open("data/knowledge_base.json") as f:
    kb = json.load(f)

def retrieve_context(query):
    query = query.lower()
    results = []

    for category in kb["categories"]:
        for item in category["items"]:
            if any(word in item.get("question", "").lower() for word in query.split()):
                results.append(item)

    return results[:3]  # top 3 matches
