from flask import Flask, request
import tweepy

# Twitter API credentials
API_KEY = "your_api_key"
API_SECRET = "your_api_key_secret"
ACCESS_TOKEN = "your_access_token"
ACCESS_TOKEN_SECRET = "your_access_token_secret"

# Authenticate with Twitter
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
twitter_api = tweepy.API(auth)

# Flask app to receive TradingView Webhook
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    # Construct the tweet message
    tweet = f"🚨 Trading Signal Alert 🚨\n\nSymbol: {data['symbol']}\nPrice: {data['price']}\nAction: {data['action']}"

    # Send the tweet
    try:
        twitter_api.update_status(tweet)
        return "Tweet sent successfully!", 200
    except Exception as e:
        return f"Failed to send tweet: {e}", 500


if __name__ == '__main__':
    app.run(port=5000)
