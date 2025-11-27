import os
import google.generativeai as genai
from dotenv import load_dotenv
from utils import setup_logger

logger = setup_logger()
load_dotenv()
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
model = genai.GenerativeModel(model_name="gemma-3n-e4b-it")


def answer_query(context: str, question: str) -> str:
    prompt = f"""
You are a professional, friendly, and knowledgeable website assistant.

You will be shown the content of a website. Your job is to act like a real human assistant or customer support agent who knows everything about the website — its purpose, features, services, and offerings.

Even if some information is missing, never say it's not provided or unclear. Always provide a helpful, complete, and user-friendly response using your best understanding from the page's tone, structure, and context.

You should respond as if you're chatting directly with a visitor to the website, answering their questions clearly, conversationally, and accurately.

Keep responses direct, helpful, and supportive — avoid robotic or technical language.

---

Website content:
{context}

---

Visitor's question:
{question}

---

Your response (speak like a helpful website agent):
"""
    try:
        logger.info("[LLM] Sending prompt to Gemini")
        response = model.generate_content(prompt)
        logger.info("[LLM] Response received")
        return response.text.strip()
    except Exception as e:
        logger.error(f"[LLM ERROR] {e}")
        return f"Bot Error: {str(e)}"
