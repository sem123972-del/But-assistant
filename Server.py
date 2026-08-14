from flask import Flask, render_template_string, request, jsonify
import requests
import os

app = Flask(__name__)
API_KEY = os.environ.get("GROQ_API_KEY")
API_URL = "https://api.groq.com/openai/v1/chat/completions"

HTML = """<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>المساعد الذكي BTU</title><style>body{font-family:'Segoe UI',sans-serif;background:#f0f2f5;margin:0}.header{background:#004d40;color:white;padding:15px;text-align:center}input{width:70%;padding:12px;font-size:16px;border:2px solid #004d40;border-radius:8px}button{width:25%;padding:12px;font-size:16px;background:#004d40;color:#fff;border:none;border-radius:8px}#ans{margin-top:20px;padding:15px;background:#e8f5e9;border-right:4px solid #004d40;border-radius:8px;white-space:pre-wrap}</style></head><body><div class="header"><h1>المساعد الذكي - جامعة البطانة BTU</h1></div><div style="max-width:700px;margin:20px auto;padding:20px"><input id="q" placeholder="اسأل عن اي شي في الجامعة..."><button onclick="ask()">بحث</button><div id="ans">مرحبا! انا المساعد بالذكاء الاصطناعي</div></div><script>async function ask(){let q=document.getElementById('q').value;if(!q)return;document.getElementById('ans').innerText='جاري التفكير...';let res=await fetch('/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({q})});let data=await res.json();document.getElementById('ans').innerText=data.answer;}</script></body></html>"""

def get_answer(question):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": f"انت المساعد الرسمي لجامعة البطانة BTU. رد باللهجة السودانية وباسلوب رسمي. السؤال: {question}"}]}
    r = requests.post(API_URL, headers=headers, json=payload, timeout=60)
    return r.json()["choices"][0]["message"]["content"]

@app.route("/")
def home(): return render_template_string(HTML)
@app.route("/ask", methods=["POST"])
def ask(): return jsonify({"answer": get_answer(request.get_json().get("q",""))})

if __name__ == "__main__": app.run(host="0.0.0.0", port=5000)
