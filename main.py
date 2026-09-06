import os
import traceback
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
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

# Purana line hata kar yeh lagayein:
chroma_client = chromadb.EphemeralClient()
collection = chroma_client.get_or_create_collection(name="nexus_knowledge")

class ChatQuery(BaseModel):
    question: str

@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    # Yahan index.html ka code direct serve ho raha hai
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nexus Automation - AI Support & Ticketing Portal</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
</head>
<body class="bg-gray-50 font-sans text-gray-800">
    <header class="bg-gradient-to-r from-blue-700 to-indigo-800 text-white shadow-md py-6 px-8">
        <div class="max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-center">
            <div>
                <h1 class="text-2xl md:text-3xl font-bold tracking-wide">Nexus Automation | AI Support Hub</h1>
                <p class="text-blue-200 text-sm mt-1">Powered by Hammad Ahmad's RAG AI Assistant • Full-Stack Web & AI Solutions</p>
            </div>
            <div class="mt-4 md:mt-0 bg-blue-900 bg-opacity-50 px-4 py-2 rounded-lg border border-blue-400 text-xs text-blue-100">
                <span class="inline-block w-2 h-2 rounded-full bg-green-400 mr-1 animate-pulse"></span> System Online & Ready
            </div>
        </div>
    </header>
    <main class="max-w-6xl mx-auto p-4 md:p-6 grid grid-cols-1 lg:grid-cols-3 gap-6 mt-4">
        <section class="lg:col-span-2 bg-white rounded-xl shadow-sm border border-gray-200 flex flex-col h-[650px]">
            <div class="p-4 border-b border-gray-100 bg-gray-50 rounded-t-xl flex items-center justify-between">
                <h2 class="font-semibold text-gray-700 flex items-center gap-2">💬 Live AI Assistant</h2>
                <span class="text-xs text-gray-500">Ask about services, pricing, & timelines</span>
            </div>
            <div id="chat-box" class="flex-1 p-4 overflow-y-auto space-y-4 bg-gray-50/50">
                <div class="flex items-start">
                    <div class="bg-blue-600 text-white rounded-2xl rounded-tl-none px-4 py-3 max-w-[85%] text-sm shadow-sm leading-relaxed">
                        Assalamu alaikum! Welcome to Nexus Automation. I am Hammad's AI support guide. How can I assist you with your web development or AI integration project today?
                    </div>
                </div>
            </div>
            <div class="p-4 border-t border-gray-100 bg-white rounded-b-xl flex gap-2">
                <input type="text" id="user-input" placeholder="Type your question here (e.g. services, pricing)..."
                    class="flex-1 border border-gray-300 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                <button onclick="sendMessage()"
                    class="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2.5 rounded-lg text-sm font-medium transition duration-200 shadow-sm">Send</button>
            </div>
        </section>
        <div class="space-y-6">
            <section class="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
                <h2 class="font-bold text-gray-800 text-md mb-1 border-b pb-2">📋 Direct Project Ticket</h2>
                <p class="text-xs text-gray-500 mb-3">Want to hire Hammad? Fill out this form to send a direct notification ticket.</p>
                <form id="ticket-form" onsubmit="submitTicket(event)" class="space-y-3">
                    <div>
                        <label class="block text-xs font-semibold text-gray-600 mb-1">Your Name</label>
                        <input type="text" id="ticket-name" required placeholder="e.g. Ali Khan"
                            class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-gray-600 mb-1">Your Email</label>
                        <input type="email" id="ticket-email" required placeholder="name@example.com"
                            class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-gray-600 mb-1">Project Details</label>
                        <textarea id="ticket-details" required rows="2" placeholder="Describe project or requirements..."
                            class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"></textarea>
                    </div>
                    <button type="submit"
                        class="w-full bg-indigo-600 hover:bg-indigo-700 text-white py-2 rounded-lg text-xs font-medium transition duration-200 shadow-sm">
                        Submit Ticket & Notify
                    </button>
                </form>
                <div id="ticket-status" class="text-xs text-center mt-2 font-medium"></div>
            </section>
        </div>
    </main>
    <script>
        async function sendMessage() {
            const inputField = document.getElementById("user-input");
            const chatBox = document.getElementById("chat-box");
            const question = inputField.value.trim();
            if (!question) return;
            chatBox.innerHTML += `<div class="flex justify-end"><div class="bg-indigo-600 text-white rounded-2xl rounded-tr-none px-4 py-3 max-w-[85%] text-sm shadow-sm leading-relaxed">${question}</div></div>`;
            inputField.value = "";
            chatBox.scrollTop = chatBox.scrollHeight;
            const loadingId = "loading-" + Date.now();
            chatBox.innerHTML += `<div id="${loadingId}" class="flex items-start"><div class="bg-gray-200 text-gray-600 rounded-2xl rounded-tl-none px-4 py-3 text-sm italic">Thinking...</div></div>`;
            chatBox.scrollTop = chatBox.scrollHeight;
            try {
                const response = await fetch("/chat", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ question: question })
                });
                const data = await response.json();
                document.getElementById(loadingId).remove();
                const replyText = data.response || data.detail || "No response received.";
                const parsedHtml = marked.parse(replyText);
                chatBox.innerHTML += `<div class="flex items-start"><div class="bg-white border border-gray-200 text-gray-800 rounded-2xl rounded-tl-none px-4 py-3 max-w-[85%] text-sm shadow-sm leading-relaxed space-y-2">${parsedHtml}</div></div>`;
            } catch (error) {
                document.getElementById(loadingId).remove();
                chatBox.innerHTML += `<div class="flex items-start"><div class="bg-red-100 text-red-700 rounded-2xl rounded-tl-none px-4 py-3 text-sm">Error connecting to server.</div></div>`;
            }
            chatBox.scrollTop = chatBox.scrollHeight;
        }
        document.getElementById("user-input").addEventListener("keypress", function (e) {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>"""
    return html_content

@app.post("/chat")
def chat_with_ai(query: ChatQuery):
    try:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            return {"response": "❌ Error: GROQ_API_KEY is missing in Vercel environment variables."}
        
        client = Groq(api_key=api_key)

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

        system_prompt = (
            "You are a helpful customer support AI for Hammad Ahmad (Nexus Automation).\n"
            "Strictly answer based on the context below. If details are missing, reply: "
            "'Yeh maloomat mere database mein dastiyab nahi hain, barah-e-karam customer support team se contact karein.'\n\n"
            f"Context:\n{context}"
        )

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
        return {"response": f"❌ Server Error: {str(e)}"}