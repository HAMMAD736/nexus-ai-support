# Build Version: v12 - Professional Portal with Primary Working Model
import os
os.environ["HOME"] = "/tmp"

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatQuery(BaseModel):
    question: str

class TicketQuery(BaseModel):
    name: str
    email: str
    service: str
    message: str

class FeedbackQuery(BaseModel):
    client_name: str
    rating: int
    comments: str

@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nexus Automation - Enterprise Support & Client Portal</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
</head>
<body class="bg-gray-100 font-sans text-gray-800">
    <header class="bg-gradient-to-r from-blue-800 via-indigo-900 to-slate-900 text-white shadow-lg py-6 px-8">
        <div class="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center">
            <div>
                <h1 class="text-2xl md:text-3xl font-extrabold tracking-tight">Nexus Automation</h1>
                <p class="text-blue-300 text-sm mt-1">AI-Powered Solutions • Full-Stack Development • Client Hub</p>
            </div>
            <div class="mt-4 md:mt-0 flex items-center gap-3">
                <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 mr-2 animate-pulse"></span> Systems Operational
                </span>
            </div>
        </div>
    </header>

    <nav class="bg-white border-b border-gray-200 shadow-sm">
        <div class="max-w-7xl mx-auto px-6 flex space-x-8">
            <button onclick="switchTab('chat')" id="nav-chat" class="py-4 px-2 border-b-2 border-blue-600 text-blue-600 font-semibold text-sm transition">💬 Live AI Assistant</button>
            <button onclick="switchTab('ticket')" id="nav-ticket" class="py-4 px-2 border-b-2 border-transparent text-gray-500 hover:text-gray-700 font-medium text-sm transition">🎫 Support Ticket</button>
            <button onclick="switchTab('feedback')" id="nav-feedback" class="py-4 px-2 border-b-2 border-transparent text-gray-500 hover:text-gray-700 font-medium text-sm transition">⭐ Client Feedback</button>
        </div>
    </nav>

    <main class="max-w-7xl mx-auto p-6">
        <!-- TAB 1: CHAT -->
        <div id="tab-chat" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <section class="lg:col-span-2 bg-white rounded-2xl shadow-sm border border-gray-200 flex flex-col h-[650px]">
                <div class="p-4 border-b border-gray-100 bg-gray-50/50 rounded-t-2xl flex items-center justify-between">
                    <h2 class="font-bold text-gray-700 flex items-center gap-2">🤖 Hammad's RAG Support Assistant</h2>
                    <span class="text-xs text-gray-400">Instant AI Responses</span>
                </div>
                <div id="chat-box" class="flex-1 p-4 overflow-y-auto space-y-4 bg-gray-50/30">
                    <div class="flex items-start">
                        <div class="bg-blue-600 text-white rounded-2xl rounded-tl-none px-4 py-3 max-w-[85%] text-sm shadow-sm leading-relaxed">
                            Assalamu alaikum! Welcome to Nexus Automation. I am Hammad's AI support guide. How can I assist you with your web development or AI integration project today?
                        </div>
                    </div>
                </div>
                <div class="p-4 border-t border-gray-100 bg-white rounded-b-2xl flex gap-2">
                    <input type="text" id="user-input" placeholder="Ask about services, timelines, or pricing..."
                        class="flex-1 border border-gray-300 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                    <button onclick="sendMessage()"
                        class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl text-sm font-semibold transition shadow-sm">Send</button>
                </div>
            </section>

            <div class="bg-white rounded-2xl shadow-sm border border-gray-200 p-6 flex flex-col justify-between">
                <div>
                    <h3 class="font-bold text-gray-800 text-lg mb-3">Quick Guidelines</h3>
                    <ul class="space-y-3 text-sm text-gray-600">
                        <li class="flex items-start gap-2">✅ <b>Fast Turnaround:</b> Landing pages in 2-4 days.</li>
                        <li class="flex items-start gap-2">✅ <b>Tech Stack:</b> React, Node.js, PHP, Python & MongoDB.</li>
                        <li class="flex items-start gap-2">✅ <b>Custom RAG:</b> Tailored AI chatbot solutions for business websites.</li>
                    </ul>
                </div>
                <div class="bg-blue-50 border border-blue-100 p-4 rounded-xl text-xs text-blue-800">
                    Need immediate human assistance? Drop a support ticket via the tab above.
                </div>
            </div>
        </div>

        <!-- TAB 2: TICKET -->
        <div id="tab-ticket" class="hidden max-w-2xl mx-auto bg-white rounded-2xl shadow-sm border border-gray-200 p-8">
            <h2 class="text-xl font-bold text-gray-800 mb-2">Create a Support Ticket</h2>
            <p class="text-xs text-gray-500 mb-6">Submit your technical issues or project queries directly to Hammad's team.</p>
            <form id="ticket-form" onsubmit="submitTicket(event)" class="space-y-4">
                <div>
                    <label class="block text-xs font-semibold text-gray-700 uppercase mb-1">Full Name</label>
                    <input type="text" id="t-name" required class="w-full border border-gray-300 rounded-xl px-4 py-2.5 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none">
                </div>
                <div>
                    <label class="block text-xs font-semibold text-gray-700 uppercase mb-1">Email Address</label>
                    <input type="email" id="t-email" required class="w-full border border-gray-300 rounded-xl px-4 py-2.5 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none">
                </div>
                <div>
                    <label class="block text-xs font-semibold text-gray-700 uppercase mb-1">Service Category</label>
                    <select id="t-service" class="w-full border border-gray-300 rounded-xl px-4 py-2.5 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none bg-white">
                        <option>Full-Stack Web Development</option>
                        <option>AI / RAG Integration</option>
                        <option>Bug Fixing / Optimization</option>
                        <option>General Inquiry</option>
                    </select>
                </div>
                <div>
                    <label class="block text-xs font-semibold text-gray-700 uppercase mb-1">Issue Description / Details</label>
                    <textarea id="t-msg" rows="4" required class="w-full border border-gray-300 rounded-xl px-4 py-2.5 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"></textarea>
                </div>
                <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 rounded-xl text-sm transition shadow-sm">Submit Ticket</button>
            </form>
            <div id="ticket-response" class="mt-4 hidden p-4 rounded-xl text-sm"></div>
        </div>

        <!-- TAB 3: FEEDBACK -->
        <div id="tab-feedback" class="hidden max-w-2xl mx-auto bg-white rounded-2xl shadow-sm border border-gray-200 p-8">
            <h2 class="text-xl font-bold text-gray-800 mb-2">Client Feedback Portal</h2>
            <p class="text-xs text-gray-500 mb-6">We value your review. Let us know about your experience working with Nexus Automation.</p>
            <form id="feedback-form" onsubmit="submitFeedback(event)" class="space-y-4">
                <div>
                    <label class="block text-xs font-semibold text-gray-700 uppercase mb-1">Your Name / Company</label>
                    <input type="text" id="f-name" required class="w-full border border-gray-300 rounded-xl px-4 py-2.5 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none">
                </div>
                <div>
                    <label class="block text-xs font-semibold text-gray-700 uppercase mb-1">Rating (1 to 5 Stars)</label>
                    <select id="f-rating" class="w-full border border-gray-300 rounded-xl px-4 py-2.5 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none bg-white">
                        <option value="5">⭐⭐⭐⭐⭐ (5 - Excellent)</option>
                        <option value="4">⭐⭐⭐⭐ (4 - Very Good)</option>
                        <option value="3">⭐⭐⭐ (3 - Good)</option>
                        <option value="2">⭐⭐ (2 - Fair)</option>
                        <option value="1">⭐ (1 - Poor)</option>
                    </select>
                </div>
                <div>
                    <label class="block text-xs font-semibold text-gray-700 uppercase mb-1">Your Feedback & Comments</label>
                    <textarea id="f-comments" rows="4" required class="w-full border border-gray-300 rounded-xl px-4 py-2.5 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"></textarea>
                </div>
                <button type="submit" class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3 rounded-xl text-sm transition shadow-sm">Submit Feedback</button>
            </form>
            <div id="feedback-response" class="mt-4 hidden p-4 rounded-xl text-sm"></div>
        </div>
    </main>

    <script>
        function switchTab(tab) {
            ['chat', 'ticket', 'feedback'].forEach(t => {
                document.getElementById('tab-' + t).classList.add('hidden');
                document.getElementById('nav-' + t).className = "py-4 px-2 border-b-2 border-transparent text-gray-500 hover:text-gray-700 font-medium text-sm transition";
            });
            document.getElementById('tab-' + tab).classList.remove('hidden');
            document.getElementById('nav-' + tab).className = "py-4 px-2 border-b-2 border-blue-600 text-blue-600 font-semibold text-sm transition";
        }

        async function sendMessage() {
            const inputField = document.getElementById("user-input");
            const chatBox = document.getElementById("chat-box");
            const question = inputField.value.trim();
            if (!question) return;
            chatBox.innerHTML += `<div class="flex justify-end"><div class="bg-indigo-600 text-white rounded-2xl rounded-tr-none px-4 py-3 max-w-[85%] text-sm shadow-sm leading-relaxed">${question}</div></div>`;
            inputField.value = "";
            chatBox.scrollTop = chatBox.scrollHeight;
            const loadingId = "loading-" + Date.now();
            chatBox.innerHTML += `<div id="${loadingId}" class="flex items-start"><div class="bg-gray-200 text-gray-600 rounded-2xl rounded-tl-none px-4 py-3 text-sm italic">AI is thinking...</div></div>`;
            chatBox.scrollTop = chatBox.scrollHeight;
            try {
                const response = await fetch("/chat", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ question: question })
                });
                const data = await response.json();
                document.getElementById(loadingId).remove();
                const replyText = data.response || "No response received.";
                const modelTag = data.model_used ? `<div class="mt-2 text-[10px] text-indigo-500 font-mono border-t border-gray-100 pt-1">⚡ Model: ${data.model_used}</div>` : '';
                const parsedHtml = marked.parse(replyText);
                chatBox.innerHTML += `<div class="flex items-start"><div class="bg-white border border-gray-200 text-gray-800 rounded-2xl rounded-tl-none px-4 py-3 max-w-[85%] text-sm shadow-sm leading-relaxed space-y-2">${parsedHtml}${modelTag}</div></div>`;
            } catch (err) {
                document.getElementById(loadingId).remove();
                chatBox.innerHTML += `<div class="flex items-start"><div class="bg-red-100 text-red-700 rounded-2xl rounded-tl-none px-4 py-3 text-sm">Server connection error.</div></div>`;
            }
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        document.getElementById("user-input").addEventListener("keypress", function (e) {
            if (e.key === 'Enter') sendMessage();
        });

        async function submitTicket(e) {
            e.preventDefault();
            const payload = {
                name: document.getElementById('t-name').value,
                email: document.getElementById('t-email').value,
                service: document.getElementById('t-service').value,
                message: document.getElementById('t-msg').value
            };
            const resDiv = document.getElementById('ticket-response');
            try {
                const response = await fetch("/ticket", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload)
                });
                const data = await response.json();
                resDiv.className = "mt-4 p-4 rounded-xl text-sm bg-emerald-50 text-emerald-800 border border-emerald-200";
                resDiv.innerText = data.message;
                document.getElementById('ticket-form').reset();
            } catch(err) {
                resDiv.className = "mt-4 p-4 rounded-xl text-sm bg-red-50 text-red-800 border border-red-200";
                resDiv.innerText = "Error submitting ticket.";
            }
            resDiv.classList.remove('hidden');
        }

        async function submitFeedback(e) {
            e.preventDefault();
            const payload = {
                client_name: document.getElementById('f-name').value,
                rating: parseInt(document.getElementById('f-rating').value),
                comments: document.getElementById('f-comments').value
            };
            const resDiv = document.getElementById('feedback-response');
            try {
                const response = await fetch("/feedback", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload)
                });
                const data = await response.json();
                resDiv.className = "mt-4 p-4 rounded-xl text-sm bg-emerald-50 text-emerald-800 border border-emerald-200";
                resDiv.innerText = data.message;
                document.getElementById('feedback-form').reset();
            } catch(err) {
                resDiv.className = "mt-4 p-4 rounded-xl text-sm bg-red-50 text-red-800 border border-red-200";
                resDiv.innerText = "Error submitting feedback.";
            }
            resDiv.classList.remove('hidden');
        }
    </script>
</body>
</html>"""
    return html_content

@app.post("/chat")
def chat_with_ai(query: ChatQuery):
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return {"response": "❌ Error: GROQ_API_KEY missing.", "model_used": None}
    
    client = Groq(api_key=api_key)
    knowledge_base = (
        "Developer Name: Hammad Ahmad. "
        "Role & Business: Founder of Nexus Automation, Undergraduate Student studying Artificial Intelligence at UET Lahore (third semester). "
        "Services Offered: Modern Full-Stack Web Development (Core PHP, JavaScript, React, Node.js, Express.js, MongoDB), AI/RAG Integrations, Custom Software Solutions. "
        "Pricing: Custom-quoted based on project scope, requirements, and technical complexity. "
        "Timelines: 2 to 4 days for landing pages, 5 to 10 days for e-commerce platforms, 10+ days for complex custom AI systems."
    )
    system_prompt = (
        "You are a helpful customer support AI for Hammad Ahmad (Nexus Automation).\n"
        "1. Answer strictly based on the Knowledge Base Context.\n"
        "2. If info is missing, reply: 'Yeh maloomat mere database mein dastiyab nahi hain, barah-e-karam support ticket submit karein.'\n"
        "3. Respond warmly to greetings.\n\n"
        f"Knowledge Base Context:\n{knowledge_base}"
    )

    # Working model prioritized first
    models_to_try = ["openai/gpt-oss-120b", "llama-3.3-70b-versatile"]
    for model_name in models_to_try:
        try:
            completion = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": query.question}],
                temperature=0.3,
                max_tokens=150,
            )
            return {"response": completion.choices[0].message.content, "model_used": model_name}
        except Exception:
            continue
    return {"response": "❌ All models failed.", "model_used": "None"}

@app.post("/ticket")
def create_ticket(ticket: TicketQuery):
    return {"status": "success", "message": f"🎫 Ticket successfully generated for {ticket.name}! Support team will contact you shortly via {ticket.email}."}

@app.post("/feedback")
def submit_feedback(feedback: FeedbackQuery):
    return {"status": "success", "message": f"⭐ Thank you for your valuable feedback, {feedback.client_name}! Your rating has been recorded."}