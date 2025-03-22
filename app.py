import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai
from dotenv import load_dotenv

# 載入 .env 環境變數
load_dotenv()

# 初始化 Flask 應用程式
app = Flask(__name__)

# 加入 CORS 支援，防止前端 fetch 請求被瀏覽器阻擋
CORS(app)

# 設定 OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# 根路由：提供首頁 HTML 頁面
@app.route('/')
def index():
    return render_template('index.html')  # 渲染 index.html 頁面

# 聊天功能的端點，接收前端傳來的 POST 請求
@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()  # 取得前端傳來的 JSON 資料
    question = data.get('question')  # 取出問題

    if question:  # 如果有提供問題
        try:
            # 使用 ChatCompletion 來呼叫 OpenAI GPT-3.5-Turbo 模型
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # 可以替換成 gpt-4
                messages=[{"role": "user", "content": question}],
                max_tokens=150
            )
            # 取得回應的答案並回傳
            answer = response['choices'][0]['message']['content'].strip()
            return jsonify({'answer': answer})
        except Exception as e:
            # 如果發生錯誤，回傳錯誤訊息
            return jsonify({'error': str(e)}), 500
    else:
        # 如果沒有提供問題，回傳錯誤
        return jsonify({'error': "No question provided"}), 400

# 啟動 Flask 應用程式
if __name__ == "__main__":
    app.run(debug=True)
