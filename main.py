import datetime
import os
import smtplib
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import chromadb
from groq import Groq

app = FastAPI(title="Nexus Automation AI Support")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

chroma_client = chromadb.EphemeralClient()
collection = chroma_client.get_or_create_collection(
    name="support_knowledge_base"
)


class DocumentInput(BaseModel):
    doc_id: str
    text: str
    metadata: dict = {}


class ChatQuery(BaseModel):
    question: str


class TicketInput(BaseModel):
    client_name: str
    client_email: str
    project_details: str


class FeedbackInput(BaseModel):
    client_name: str
    client_email: str
    rating: str
    feedback_message: str


@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "<h3>Frontend index.html not found!</h3>"


@app.post("/add-document")
def add_document(data: DocumentInput):
    try:
        collection.upsert(
            ids=[data.doc_id], documents=[data.text], metadatas=[data.metadata]
        )
        return {"status": "success", "message": f"Document {data.doc_id} added."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat")
def chat_with_ai(query: ChatQuery):
    try:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise HTTPException(
                status_code=500, detail="GROQ_API_KEY environment variable is missing on Vercel!"
            )
        
        client = Groq(api_key=api_key)

        count = collection.count()
        if count == 0:
            collection.upsert(
                ids=["hammad_profile_modern"],
                documents=[
                    "Developer Name: Hammad Ahmad (Founder of Nexus Automation, AI "
                    "Undergraduate at UET Lahore). Core Expertise: Modern "
                    "Full-Stack Web Development, AI/RAG Integrations, and Custom "
                    "Software Solutions. Services and Tech Stack: AI & RAG "
                    "Applications (intelligent customer support bots, LLM "
                    "integrations via Hugging Face and Groq, retrieval-augmented "
                    "systems using FastAPI, ChromaDB, and Python); Full-Stack "
                    "Web Development (dynamic web apps, e-commerce platforms, "
                    "school portals, and verification systems using React, "
                    "Node.js, Express.js, MongoDB, Core PHP, MySQL, and "
                    "JavaScript); Modern DevOps & Deployment (containerizing apps "
                    "using Docker Desktop and deploying on Vercel and "
                    "InfinityFree); Systems & Security (robust code/scripts in "
                    "C++ and Python, and web vulnerability testing). Project "
                    "Delivery Timelines: Landing pages & basic features take 2 to "
                    "4 days; Medium web apps & e-commerce stores take 5 to 10 "
                    "days; Advanced custom systems & AI integrations take 10+ "
                    "days depending on project scope. Pricing & Quotation: "
                    "Custom-quoted based on project scope, complexity, and "
                    "features. Client Inquiry & Ticketing Policy: If a client "
                    "wants to hire, place an order, or discuss a project, "
                    "collect their Name, Email, and Project Details, generate a "
                    "support ticket, and notify Hammad instantly."
                ],
                metadatas=[{"category": "profile"}],
            )

        all_docs = collection.get()
        retrieved_docs = all_docs.get("documents", [])
        context = "\n\n".join(retrieved_docs) if retrieved_docs else "No context."

      system_prompt = (
            "You are a helpful, polite, professional, and welcoming customer support "
            "AI for Hammad Ahmad (Founder of Nexus Automation, UET Lahore).\n\n"
            "IMPORTANT GUIDELINES & GUARDRAILS:\n"
            "1. Strict Context Adherence: Answer questions strictly based on the provided Knowledge Base Context below. "
            "If a user's question is related to Hammad's business, services, or web/AI development, but the exact details "
            "are NOT present in the database context, do NOT make up facts. Instead, reply with: "
            "'Yeh maloomat mere database mein dastiyab nahi hain, barah-e-karam project ticket fill kar ke ya hamari customer support team se contact karein.'\n"
            "2. Casual & Polite Greetings: Respond warmly to greetings like 'salam', 'hello', or general well-being queries.\n"
            "3. Formatting: Never use markdown tables. Always use clean bullet points and short paragraphs.\n\n"
            f"Knowledge Base Context:\n{context}"
        )

        model_id = "llama-3.3-70b-versatile"

        chat_completion = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query.question},
            ],
            temperature=0.3,
            max_tokens=150,
        )

        answer = chat_completion.choices[0].message.content

        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] User: {query.question} | AI: {answer}\n"
            with open("/tmp/chat_logs.txt", "a", encoding="utf-8") as f:
                f.write(log_entry + "-" * 50 + "\n")
        except Exception:
            pass

        return {
            "response": answer,
            "retrieved_context": retrieved_docs,
            "active_model": model_id,
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/create-ticket")
def create_support_ticket(ticket: TicketInput):
    try:
        sender_email = os.environ.get("SENDER_EMAIL")
        sender_password = os.environ.get("SENDER_PASSWORD")
        receiver_email = os.environ.get("RECEIVER_EMAIL", sender_email)

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = f"🚨 New Project Ticket from {ticket.client_name}"

        body = (
            f"A new client has submitted a support ticket!\n\nClient Name: "
            f"{ticket.client_name}\nClient Email: {ticket.client_email}\nProject "
            f"Details / Message:\n{ticket.project_details}\n\nPlease contact them back."
        )
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        return {
            "status": "success",
            "message": "Ticket successfully created and email notification sent to Hammad!",
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/submit-feedback")
def submit_feedback(feedback: FeedbackInput):
    try:
        sender_email = os.environ.get("SENDER_EMAIL")
        sender_password = os.environ.get("SENDER_PASSWORD")
        receiver_email = os.environ.get("RECEIVER_EMAIL", sender_email)

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = f"⭐ New Client Feedback from {feedback.client_name} ({feedback.rating})"

        body = (
            f"You have received a new feedback submission!\n\nClient Name: "
            f"{feedback.client_name}\nClient Email: {feedback.client_email}\nRating: "
            f"{feedback.rating}\nFeedback Message:\n{feedback.feedback_message}"
        )
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        return {
            "status": "success",
            "message": "Feedback submitted successfully and emailed to Hammad!",
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)