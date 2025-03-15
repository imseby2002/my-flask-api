import os
from flask import Flask, request, jsonify
import openai
from dotenv import load_dotenv

load_dotenv()  # 加載 .env 檔案

app = Flask(__name__)

# 設定 OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")


# 處理 /ask 路徑的 GET 和 POST 請求
@app.route('/ask', methods=['GET', 'POST'])
def ask():
    if request.method == 'POST':
        # 處理 POST 請求
        data = request.get_json()  # 從請求中獲取 JSON 資料
        question = data.get('question')  # 提取問題

        if question:
            try:
                # 使用 OpenAI API 生成回應
                response = openai.Completion.create(
                    model="gpt-3.5-turbo",  # 可以更換為其他模型，如 gpt-4
                    prompt=question,        # 傳入的問題
                    max_tokens=150          # 設定最大回應字數
                )
                answer = response.choices[0].text.strip()  # 提取並清除回答的空格
                return jsonify({"answer": answer})  # 返回回答
            except Exception as e:
                return jsonify({"error": str(e)}), 500  # 如果發生錯誤，返回錯誤訊息

        else:
            return jsonify({"error": "No question provided"}), 400  # 如果沒有提供問題，返回錯誤訊息

    elif request.method == 'GET':
        # 處理 GET 請求，返回簡單的歡迎信息
        return jsonify({"message": "Welcome to the /ask endpoint! Send a POST request with a 'question' field."})

# 啟動 Flask 應用
if __name__ == "__main__":
    app.run(debug=True)
