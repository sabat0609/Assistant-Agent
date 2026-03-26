import google.generativeai as genai
import os

# 🔑 Set your API key here OR via environment variable
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def ask_llm(prompt):
    response = model.generate_content(prompt)
    return response.text