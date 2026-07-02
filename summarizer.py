from groq import Groq
from dotenv import load_dotenv
import os

# ==========================================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================================

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ==========================================================
# AI SUMMARY FUNCTION
# ==========================================================

def generate_summary(text):

    prompt = f"""
You are an AI Cyber Security and Compliance Expert.

Analyze the uploaded document carefully.

Generate a professional report using the following format.

--------------------------------------------------

## 1. Document Summary
Give a short summary of the document in 3-5 lines.

## 2. Sensitive Information Detected
List all sensitive information found.

## 3. Compliance Risks
Mention possible compliance risks such as:
- GDPR
- Data Privacy
- Confidential Information
- Personal Data Exposure

If none are found, mention "No major compliance risks detected."

## 4. Security Risks
Mention possible security concerns.

## 5. Recommendations
Provide 5 practical recommendations to improve document security.

Keep the response professional, concise and well formatted.

--------------------------------------------------

Document:
{text[:2500]}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception:
        return "⚠️ AI Summary is temporarily unavailable because the Groq API limit has been reached. Please try again later."