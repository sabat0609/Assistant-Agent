import google.generativeai as genai
import os

# 🔑 Set your API key here OR via environment variable
genai.configure(api_key=os.getenv("AIzaSyBlrtA8VqH-s0n97HQdgKBfH_jiBpZYYbo"))

model = genai.GenerativeModel("gemini-1.5-flash")

def ask_llm(prompt):
    response = model.generate_content(prompt)
    return response.text
