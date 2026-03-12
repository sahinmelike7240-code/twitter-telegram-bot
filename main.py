import feedparser
import requests
import time
import re
import os

# --- AYARLAR ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
feed_url = "https://rss.app/feeds/X411D152Had8CdC6.xml"
CHECK_INTERVAL = 120 

last_link = ""

def send_to_telegram(message, image_url=None):
    try:
        # Mesajın içine direkt linki koyacağımız için HTML modunu basit tutuyoruz
        if image_url:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
            payload = {
                "chat_id": CHANNEL_ID,
                "photo": image_url,
                "caption": message
            }
        else:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            payload = {
                "chat_id": CHANNEL_ID,
                "text": message,
                "disable_web_page_preview": False
            }
        
        response = requests.post(url, data=payload)
        return response.status_code == 200
    except Exception as e:
        print(f"Mesaj hatasi: {e}")

print("Bot baslatildi...")

while True:
    try:
        feed = feedparser.parse(feed_url)
        
        if feed.entries:
            tweet = feed.entries[0]
            current_link = tweet.link
            
            if current_link != last_link:
                # Metni al
                raw_text = tweet.get('summary', tweet.get('description', ''))
                
                # 1. Gereksiz RSS eklerini temizle (Tarih ve Kullanıcı adı)
                if "—" in raw_text:
                    raw_text = raw_text.split("—")[0].strip()
                
                # 2. Satır aralıklarını (Enter) düzelt
                clean_text = raw_text.replace('<br />', '\n').replace('<br>', '\n').replace('</p>', '\n').replace('<p>', '')
                
                # 3. HTML etiketlerini temizle
                clean_text = re.sub(r'<[^>]+>', '', clean_text)
                
                # Mesaj Formatı: Önce metin, sonra direkt link
                tweet_text = clean_text.strip()
                message = f"{tweet_text}\n\n{current_link}"
                
                # Görsel kontrolü
                image_url = None
                if 'media_content' in tweet:
                    image_url = tweet.media_content[0]['url']
                elif 'links' in tweet:
                    for l in tweet.links:
                        if 'image' in l.get('type', ''):
                            image_url = l.get('href')
                
                # Telegram'a gönder
                if send_to_telegram(message, image_url):
                    last_link = current_link
                    print(f"Paylasildi: {current_link}")
        
    except Exception as e:
        print(f"Hata: {e}")
    
    time.sleep(CHECK_INTERVAL)
