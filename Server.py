
from flask import Flask, render_template, jsonify, request, send_from_directory
import os

app = Flask(__name__)

# الصفحة الرئيسية
@app.route('/')
def home():
    return render_template('index.html')

# عشان ملف المانفيست
@app.route('/manifest.json')
def manifest():
    return send_from_directory('.', 'manifest.json')

# عشان service worker
@app.route('/service-worker.js')
def sw():
    return send_from_directory('.', 'service-worker.js')

# دا الويبهوك بتاع الواتساب
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # التحقق
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == "but12345":
            return request.args.get("hub.challenge")
    
    # استقبال الرسائل
    if request.method == 'POST':
        data = request.get_json()
        print("رسالة جات:", data)
        # هنا بعدين بنضيف الرد الذكي
    return "ok", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
