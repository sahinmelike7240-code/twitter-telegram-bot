import feedparser
import requests
import time
import re
import os

# --- AYARLAR (Railway'deki Variables kısmından çekilir) ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
# RSS.app linkini buraya direkt sabitliyoruz
feed_url = "https://rss.app/feeds/X411D152Had8CdC6.xml"
CHECK_INTERVAL = 120 # 2 dakikada bir kontrol eder

last_link = ""

def send_to_telegram(message, image_url=None):
    try:
        if image_url:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
            payload = {
                "chat_id": CHANNEL_ID,
                "photo": image_url,
                "caption": message,
                "parse_mode": "HTML"
            }
        else:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            payload = {
                "chat_id": CHANNEL_ID,
                "text": message,
                "parse_mode": "HTML",
                "disable_web_page_preview": False
            }
        
        response = requests.post(url, data=payload)
        print(f"Telegram Yanıtı: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"Mesaj gonderilirken hata olustu: {e}")

print("Bot baslatildi...")

while True:
    try:
        feed = feedparser.parse(feed_url)
        
        if feed.entries:
            tweet = feed.entries[0]
            current_link = tweet.link
            
            # Eğer yeni bir tweet ise
            if current_link != last_link:
                # Metni al
                raw_text = tweet.get('summary', tweet.get('description', ''))
                
                # 1. RSS'in sonuna eklediği tarih ve kullanıcı adını temizle
                # Genellikle "— CryptoELITES (@...)" şeklinde ekler, oradan kesiyoruz.
                if "—" in raw_text:
                    raw_text = raw_text.split("—")[0].strip()
                
                # 2. Satır aralıklarını (Enter) korumak için <br> etiketlerini düzenle
                clean_text = raw_text.replace('<br />', '\n').replace('<br>', '\n')
                # 3. Kalan HTML etiketlerini temizle
                clean_text = re.sub(r'<[^>]+>', '', clean_text)
                
                # Mesajı oluştur (Twitter'daki gibi tertemiz)
                message = f"{clean_text.strip()}\n\n<a href='{current_link}
