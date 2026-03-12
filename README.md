import requests
import time

BOT_TOKEN = "TELEGRAM_BOT_TOKEN"
CHANNEL_ID = "@kanaladi"
TWITTER_USERNAME = "kullaniciadi"

last_tweet_id = None

def get_latest_tweet():
    url = f"https://api.rsshub.app/twitter/user/{TWITTER_USERNAME}"
    r = requests.get(url)
    return r.text

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHANNEL_ID,
        "text": message
    }
    requests.post(url, data=data)

while True:
    tweet = get_latest_tweet()
    send_telegram(tweet)
    time.sleep(300)
