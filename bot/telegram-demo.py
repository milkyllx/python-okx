from flask import Flask, request
import requests

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = "7561392980:AAFPoY-Y9oq3braE_noH0xnug6azBTGozBQ"
TELEGRAM_CHAT_ID = "-4879047817"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    message = f"🚨 Trading Signal Alert 🚨\n\nSymbol: {data['ticker']}\nPrice: {data['close']}\nCondition: {data['strategy']['order']['action']}"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    requests.post(url, json=payload)
    return "OK", 200

if __name__ == '__main__':
    app.run(port=5000)
