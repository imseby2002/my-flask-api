import os
from flask import Flask, request, jsonify
import openai
from dotenv import load_dotenv

load_dotenv()  # 加載 .env 檔案

app = Flask(__name__)

# 設定 OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/ask", methods=["POST"])
def ask_openai():
    data = request.json
    user_question = data.get("question", "")

    if not user_question:
        return jsonify({"error": "請提供問題"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_question}]
        )
        return jsonify({"answer": response["choices"][0]["message"]["content"]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
