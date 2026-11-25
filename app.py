from flask import Flask, request, jsonify
from llm import chat_with_user
from embedding import search
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

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