import os
import traceback
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import chromadb
from groq import Groq

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ephemeral ChromaDB client (Serverless safe)
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="nexus_knowledge")

class ChatQuery(BaseModel):
    question: str

@app.post("/chat")
def chat_with_ai(query: ChatQuery):
    debug_steps = []
    try:
        # Step 1: Check API Key
        debug_steps.append("Checking GROQ_API_KEY...")
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            return {"response": "❌ DEBUG ERROR: GROQ_API_KEY environment variable missing on Vercel!"}
        
        # Step 2: Initialize Groq Client
        debug_steps.append("Initializing Groq client...")
        client = Groq(api_key=api_key)

        # Step 3: Check / Populate ChromaDB
        debug_steps.append("Checking ChromaDB collection...")
        if collection.count() == 0:
            collection.upsert(
                ids=["hammad_profile_modern"],
                documents=[
                    "Developer Name: Hammad Ahmad (Founder of Nexus Automation, AI Undergraduate at UET Lahore). "
                    "Services: Modern Full-Stack Web Development, AI/RAG Integrations, Custom Software Solutions. "
                    "Pricing: Custom-quoted based on scope and complexity. "
                    "Timelines: 2 to 4 days for landing pages, 5 to 10 days for e-commerce, 10+ days for custom AI systems."
                ],
                metadatas=[{"category": "profile"}],
            )

        all_docs = collection.get()
        retrieved_docs = all_docs.get("documents", [])
        context = "\n\n".join(retrieved_docs) if retrieved_docs else "No context."
        debug_steps.append("ChromaDB context loaded successfully.")

        # Step 4: System Prompt & Guardrail
        system_prompt = (
            "You are a helpful customer support AI for Hammad Ahmad (Nexus Automation).\n"
            "Strictly answer based on the context below. If details are missing, reply: "
            "'Yeh maloomat mere database mein dastiyab nahi hain, barah-e-karam customer support team se contact karein.'\n\n"
            f"Context:\n{context}"
        )

        # Step 5: Groq API Call
        debug_steps.append("Calling Groq API (llama-3.3-70b-versatile)...")
        chat_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query.question},
            ],
            temperature=0.3,
            max_tokens=150,
        )

        answer = chat_completion.choices[0].message.content
        return {"response": answer}

    except Exception as e:
        error_trace = traceback.format_exc()
        print(error_trace)
        # Yeh frontend par exact step bata dega kahan fail hua
        last_step = debug_steps[-1] if debug_steps else "Initialization"
        return {"response": f"❌ Error at [{last_step}]: {str(e)}"}