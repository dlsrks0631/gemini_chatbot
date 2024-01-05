from flask import Flask, render_template, request
import os
import google.generativeai as genai

app = Flask(__name__)

apikey = os.getenv("API_KEY")

genai.configure(api_key=apikey)

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

def format_chat_history(history):
    formatted_history = []
    for message in history:
        text = message.parts[0].text
        role = message.role
        formatted_message = f'{role}: {text}'
        formatted_history.append(formatted_message)
    return formatted_history



@app.route('/')
def index():
    chat_history = format_chat_history(chat.history)
    return render_template("index.html", chat_history=chat_history)

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.form['user_input']
    response = chat.send_message(user_message)
    chat_history = format_chat_history(chat.history)
    return render_template('index.html', chat_history=chat_history, user_input=user_message, bot_response=f'model: {response.text}')

# 채팅 초기화
@app.route('/reset')
def reset():
    global chat
    chat = model.start_chat(history=[])
    return render_template('index.html', chat_history=[])

if __name__ == '__main__':
    app.run(port=1111, debug=True)

