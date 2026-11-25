from flask import Flask, request, jsonify
from llm import chat_with_user
from embedding import search
from dotenv import load_dotenv
import os
import secrets

load_dotenv()

app = Flask(__name__)

@app.before_request
def protect_chat():
    if request.path != "/chat":
        return None

    token = os.getenv("CHAT_API_KEY")

    if not token:
        return jsonify(error="Chat access is not configured."), 503

    provided = request.headers.get("Authorization", "")
    expected = f"Bearer {token}"

    if not secrets.compare_digest(provided, expected):
        return jsonify(error="Unauthorized"), 401

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('user_input')
    response = chat_with_user(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)