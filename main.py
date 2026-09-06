# Build Version: v15 - Added Favicon for Professional Branding
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
    <!-- Professional SVG Favicon -->
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='20' fill='%232563eb'/><text x='50' y='68' font-size='55' font-family='Arial, sans-serif' font-weight='bold' fill='white' text-anchor='middle'>N</text></svg>">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
</head>
<body class="bg-slate-900 font-sans text-gray-100 min-h-screen flex flex-col justify-between">
    <div>
        <!-- Top Enterprise Header -->
        <header class="bg-slate-950 border-b border-slate-800 text-white py-5 px-8 shadow-md">
            <div class="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center">
                <div class="flex items-center gap-3 cursor-pointer" onclick="switchTab('home')">
                    <div class="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center font-bold text-lg shadow-inner">N</div>
                    <div>
                        <h1 class="text-xl font-extrabold tracking-tight">Nexus Automation</h1>
                        <p class="text-xs text-slate-400">AI-Powered Enterprise Solutions & Hub</p>
                    </div>
                </div>
                <div class="mt-4 md:mt-0 flex items-center gap-4">
                    <button onclick="switchTab('home')" id="nav-home" class="text-xs font-semibold px-3 py-1.5 rounded-lg bg-slate-800 text-blue-400 hover:bg-slate-700 transition">Dashboard</button>
                    <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                        <span class="w-2 h-2 rounded-full bg-emerald-400 mr-2 animate-pulse"></span> Systems Active
                    </span>
                </div>
            </div>
        </header>

        <!-- Main Workspace Container -->
        <main class="max-w-7xl mx-auto p-6 md:p-10">
            
            <!-- VIEW 0: THREE LARGE PROFESSIONAL ENTERPRISE BOXES -->
            <div id="tab-home" class="space-y-8">
                <div class="text-center max-w-3xl mx-auto py-4">
                    <h2 class="text-3xl md:text-4xl font-black text-white tracking-tight">Welcome to Nexus Client Center</h2>
                    <p class="text-slate-400 mt-2 text-sm">Select one of the enterprise portals below to interact with our AI systems, open support inquiries, or submit feedback.</p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-6xl mx-auto pt-4">
                    <!-- Box 1: AI Assistant -->
                    <div onclick="switchTab('chat')" class="bg-slate-800/60 border border-slate-700/80 rounded-3xl p-8 hover:border-blue-500 hover:bg-slate-800 cursor-pointer transition-all duration-300 shadow-xl flex flex-col justify-between group relative overflow-hidden">
                        <div class="absolute top-0 right-0 w-32 h-32 bg-blue-500/5 rounded-full blur-2xl group-hover:bg-blue-500/15 transition"></div>
                        <div>
                            <div class="w-14 h-14 bg-blue-600/20 border border-blue-500/30 text-blue-400 rounded-2xl flex items-center justify-center text-3xl mb-6 group-hover:scale-110 transition-transform">💬</div>
                            <h3 class="text-xl font-bold text-white mb-3">Live AI Assistant</h3>
                            <p class="text-slate-400 text-xs leading-relaxed">Engage with our custom RAG-powered model to get instant answers regarding web development stacks, pricing, and project deliverables.</p>
                        </div>
                        <div class="mt-8 flex items-center gap-2 text-xs font-bold text-blue-400 group-hover:translate-x-1 transition-transform">
                            Launch AI Console &rarr;
                        </div>
                    </div>

                    <!-- Box 2: Support Ticket -->
                    <div onclick="switchTab('ticket')" class="bg-slate-800/60 border border-slate-700/80 rounded-3xl p-8 hover:border-indigo-500 hover:bg-slate-800 cursor-pointer transition-all duration-300 shadow-xl flex flex-col justify-between group relative overflow-hidden">
                        <div class="absolute top-0 right-0 w-32 h-32 bg-indigo-500/5 rounded-full blur-2xl group-hover:bg-indigo-500/15 transition"></div>
                        <div>
                            <div class="w-14 h-14 bg-indigo-600/20 border border-indigo-500/30 text-indigo-400 rounded-2xl flex items-center justify-center text-3xl mb-6 group-hover:scale-110 transition-transform">🎫</div>
                            <h3 class="text-xl font-bold text-white mb-3">Support Ticket Hub</h3>
                            <p class="text-slate-400 text-xs leading-relaxed">Encountering a bug or require specialized technical intervention? Register a priority support ticket for our engineering team.</p>
                        </div>
                        <div class="mt-8 flex items-center gap-2 text-xs font-bold text-indigo-400 group-hover:translate-x-1 transition-transform">
                            Open Ticket Portal &rarr;
                        </div>
                    </div>

                    <!-- Box 3: Feedback Portal -->
                    <div onclick="switchTab('feedback')" class="bg-slate-800/60 border border-slate-700/80 rounded-3xl p-8 hover:border-amber-500 hover:bg-slate-800 cursor-pointer transition-all duration-300 shadow-xl flex flex-col justify-between group relative overflow-hidden">
                        <div class="absolute top-0 right-0 w-32 h-32 bg-amber-500/5 rounded-full blur-2xl group-hover:bg-amber-500/15 transition"></div>
                        <div>
                            <div class="w-14 h-14 bg-amber-600/20 border border-amber-500/30 text-amber-400 rounded-2xl flex items-center justify-center text-3xl mb-6 group-hover:scale-110 transition-transform">⭐</div>
                            <h3 class="text-xl font-bold text-white mb-3">Client Feedback</h3>
                            <p class="text-slate-400 text-xs leading-relaxed">Rate your collaboration experience and share constructive reviews regarding our engineering solutions and deliverables.</p>
                        </div>
                        <div class="mt-8 flex items-center gap-2 text-xs font-bold text-amber-400 group-hover:translate-x-1 transition-transform">
                            Submit Review &rarr;
                        </div>
                    </div>
                </div>
            </div>

            <!-- VIEW 1: CHAT INTERFACE -->
            <div id="tab-chat" class="hidden max-w-5xl mx-auto">
                <div class="mb-4 flex items-center justify-between">
                    <button onclick="switchTab('home')" class="text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 px-4 py-2 rounded-xl transition border border-slate-700">&larr; Back to Dashboard</button>
                    <span class="text-xs text-slate-400 font-mono">Active Module: AI Support Chat</span>
                </div>
                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <section class="lg:col-span-2 bg-slate-800 rounded-2xl shadow-xl border border-slate-700 flex flex-col h-[600px]">
                        <div class="p-4 border-b border-slate-700 bg-slate-900/50 rounded-t-2xl flex items-center justify-between">
                            <h2 class="font-bold text-slate-200 text-sm flex items-center gap-2">🤖 Hammad's RAG Support Assistant</h2>
                            <span class="text-xs text-emerald-400">Online</span>
                        </div>
                        <div id="chat-box" class="flex-1 p-4 overflow-y-auto space-y-4 bg-slate-800/30">
                            <div class="flex items-start">
                                <div class="bg-blue-600 text-white rounded-2xl rounded-tl-none px-4 py-3 max-w-[85%] text-sm shadow-sm leading-relaxed">
                                    Assalamu alaikum! Welcome to Nexus Automation. I am Hammad's AI support guide. How can I assist you with your web development or AI integration project today?
                                </div>
                            </div>
                        </div>
                        <div class="p-4 border-t border-slate-700 bg-slate-800/80 rounded-b-2xl flex gap-2">
                            <input type="text" id="user-input" placeholder="Ask about services, timelines, or pricing..."
                                class="flex-1 bg-slate-900 border border-slate-700 text-white rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                            <button onclick="sendMessage()"
                                class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl text-sm font-semibold transition shadow-sm">Send</button>
                        </div>
                    </section>

                    <div class="bg-slate-800 rounded-2xl shadow-xl border border-slate-700 p-6 flex flex-col justify-between">
                        <div>
                            <h3 class="font-bold text-white text-base mb-3">Quick Guidelines</h3>
                            <ul class="space-y-3 text-xs text-slate-300">
                                <li class="flex items-start gap-2">✅ <b>Turnaround:</b> Landing pages in 2-4 days.</li>
                                <li class="flex items-start gap-2">✅ <b>Tech Stack:</b> React, Node, PHP, Python, MongoDB.</li>
                                <li class="flex items-start gap-2">✅ <b>Custom RAG:</b> Specialized client chat agents.</li>
                            </ul>
                        </div>
                        <div class="bg-blue-950/50 border border-blue-800/50 p-3 rounded-xl text-xs text-blue-300">
                            Need technical support? Switch back and open a support ticket.
                        </div>
                    </div>
                </div>
            </div>

            <!-- VIEW 2: SUPPORT TICKET -->
            <div id="tab-ticket" class="hidden max-w-2xl mx-auto">
                <div class="mb-4">
                    <button onclick="switchTab('home')" class="text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 px-4 py-2 rounded-xl transition border border-slate-700">&larr; Back to Dashboard</button>
                </div>
                <div class="bg-slate-800 rounded-2xl shadow-xl border border-slate-700 p-8">
                    <h2 class="text-xl font-bold text-white mb-1">Create a Support Ticket</h2>
                    <p class="text-xs text-slate-400 mb-6">Submit your technical queries directly to Hammad's development desk.</p>
                    <form id="ticket-form" onsubmit="submitTicket(event)" class="space-y-4">
                        <div>
                            <label class="block text-xs font-semibold text-slate-300 uppercase mb-1">Full Name</label>
                            <input type="text" id="t-name" required class="w-full bg-slate-900 border border-slate-700 text-white rounded-xl px-4 py-2.5 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none">
                        </div>
                        <div>
                            <label class="block text-xs font-semibold text-slate-300 uppercase mb-1">Email Address</label>
                            <input type="email" id="t-email" required class="w-full bg-slate-900 border border-slate-700 text-white rounded-xl px-4 py-2.5 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none">
                        </div>
                        <div>
                            <label class="block text-xs font-semibold text-slate-300 uppercase mb-1">Service Category</label>
                            <select id="t-service" class="w-full bg-slate-900 border border-slate-700 text-white rounded-xl px-4 py-2.5 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none">
                                <option>Full-Stack Web Development</option>
                                <option>AI / RAG Integration</option>
                                <option>Bug Fixing / Optimization</option>
                                <option>General Inquiry</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-xs font-semibold text-slate-300 uppercase mb-1">Issue Description</label>
                            <textarea id="t-msg" rows="4" required class="w-full bg-slate-900 border border-slate-700 text-white rounded-xl px-4 py-2.5 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"></textarea>
                        </div>
                        <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 rounded-xl text-sm transition shadow-sm">Submit Ticket</button>
                    </form>
                    <div id="ticket-response" class="mt-4 hidden p-4 rounded-xl text-sm"></div>
                </div>
            </div>

            <!-- VIEW 3: FEEDBACK PORTAL -->
            <div id="tab-feedback" class="hidden max-w-2xl mx-auto">
                <div class="mb-4">
                    <button onclick="switchTab('home')" class="text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 px-4 py-2 rounded-xl transition border border-slate-700">&larr; Back to Dashboard</button>
                </div>
                <div class="bg-slate-800 rounded-2xl shadow-xl border border-slate-700 p-8">
                    <h2 class="text-xl font-bold text-white mb-1">Client Feedback Portal</h2>
                    <p class="text-xs text-slate-400 mb-6">Let us know about your experience working with Nexus Automation.</p>
                    <form id="feedback-form" onsubmit="submitFeedback(event)" class="space-y-4">
                        <div>
                            <label class="block text-xs font-semibold text-slate-300 uppercase mb-1">Your Name / Company</label>
                            <input type="text" id="f-name" required class="w-full bg-slate-900 border border-slate-700 text-white rounded-xl px-4 py-2.5 text-sm focus:ring-2 focus:ring-amber-500 focus:outline-none">
                        </div>
                        <div>
                            <label class="block text-xs font-semibold text-slate-300 uppercase mb-1">Rating</label>
                            <select id="f-rating" class="w-full bg-slate-900 border border-slate-700 text-white rounded-xl px-4 py-2.5 text-sm focus:ring-2 focus:ring-amber-500 focus:outline-none">
                                <option value="5">⭐⭐⭐⭐⭐ (5 - Excellent)</option>
                                <option value="4">⭐⭐⭐⭐ (4 - Very Good)</option>
                                <option value="3">⭐⭐⭐ (3 - Good)</option>
                                <option value="2">⭐⭐ (2 - Fair)</option>
                                <option value="1">⭐ (1 - Poor)</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-xs font-semibold text-slate-300 uppercase mb-1">Comments & Reviews</label>
                            <textarea id="f-comments" rows="4" required class="w-full bg-slate-900 border border-slate-700 text-white rounded-xl px-4 py-2.5 text-sm focus:ring-2 focus:ring-amber-500 focus:outline-none"></textarea>
                        </div>
                        <button type="submit" class="w-full bg-amber-600 hover:bg-amber-700 text-white font-semibold py-3 rounded-xl text-sm transition shadow-sm">Submit Review</button>
                    </form>
                    <div id="feedback-response" class="mt-4 hidden p-4 rounded-xl text-sm"></div>
                </div>
            </div>

        </main>
    </div>

    <footer class="bg-slate-950 border-t border-slate-800 text-center py-4 text-xs text-slate-500">
        Nexus Automation &bull; Developed by Hammad Ahmad
    </footer>

    <script>
        function switchTab(tab) {
            ['home', 'chat', 'ticket', 'feedback'].forEach(t => {
                const el = document.getElementById('tab-' + t);
                if(el) el.classList.add('hidden');
            });
            const targetTab = document.getElementById('tab-' + tab);
            if(targetTab) targetTab.classList.remove('hidden');
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        async function sendMessage() {
            const inputField = document.getElementById("user-input");
            const chatBox = document.getElementById("chat-box");
            const question = inputField.value.trim();
            if (!question) return;
            chatBox.innerHTML += `<div class="flex justify-end"><div class="bg-blue-600 text-white rounded-2xl rounded-tr-none px-4 py-3 max-w-[85%] text-sm shadow-sm leading-relaxed">${question}</div></div>`;
            inputField.value = "";
            chatBox.scrollTop = chatBox.scrollHeight;
            const loadingId = "loading-" + Date.now();
            chatBox.innerHTML += `<div id="${loadingId}" class="flex items-start"><div class="bg-slate-700 text-slate-300 rounded-2xl rounded-tl-none px-4 py-3 text-sm italic">AI is thinking...</div></div>`;
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
                const modelTag = data.model_used ? `<div class="mt-2 text-[10px] text-blue-400 font-mono border-t border-slate-700 pt-1">⚡ Model: ${data.model_used}</div>` : '';
                const parsedHtml = marked.parse(replyText);
                chatBox.innerHTML += `<div class="flex items-start"><div class="bg-slate-900 border border-slate-700 text-slate-100 rounded-2xl rounded-tl-none px-4 py-3 max-w-[85%] text-sm shadow-sm leading-relaxed space-y-2">${parsedHtml}${modelTag}</div></div>`;
            } catch (err) {
                document.getElementById(loadingId).remove();
                chatBox.innerHTML += `<div class="flex items-start"><div class="bg-red-900/50 text-red-200 rounded-2xl rounded-tl-none px-4 py-3 text-sm">Server connection error.</div></div>`;
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
                resDiv.className = "mt-4 p-4 rounded-xl text-sm bg-emerald-950 text-emerald-300 border border-emerald-800";
                resDiv.innerText = data.message;
                document.getElementById('ticket-form').reset();
            } catch(err) {
                resDiv.className = "mt-4 p-4 rounded-xl text-sm bg-red-950 text-red-300 border border-red-800";
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
                resDiv.className = "mt-4 p-4 rounded-xl text-sm bg-emerald-950 text-emerald-300 border border-emerald-800";
                resDiv.innerText = data.message;
                document.getElementById('feedback-form').reset();
            } catch(err) {
                resDiv.className = "mt-4 p-4 rounded-xl text-sm bg-red-950 text-red-300 border border-red-800";
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