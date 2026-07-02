from groq import Groq
from dotenv import load_dotenv
import os

from rag_engine import RAGEngine

# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ==========================================================
# Initialize RAG Engine
# ==========================================================



# ==========================================================
# RAG Question Answering
# ==========================================================

def ask_question(rag, question):

   

    # Retrieve relevant chunks
    relevant_chunks = rag.search(question)

    context = "\n\n".join(relevant_chunks)

    prompt = f"""
You are an AI Document Assistant.

Answer ONLY using the given context.

Rules:

1. Do NOT make up information.
2. If the answer is not available, say:
"The document does not contain this information."

Context:
{context}

Question:
{question}

Answer:
"""

    try:

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "system",
                    "content": "You answer questions only from the provided context."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.1,
            max_tokens=250

        )

        return response.choices[0].message.content.strip()

    except Exception as e:

        return f"""⚠️ Unable to generate answer.

Reason:
{str(e)}

Possible Solutions:
• Groq daily token limit reached.
• Wait a few minutes and try again.
• Or use a new Groq API key.
"""