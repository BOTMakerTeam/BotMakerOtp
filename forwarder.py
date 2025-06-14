from bs4 import BeautifulSoup
import requests
import time
import config

last_messages = set()

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": config.CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        res = requests.post(url, data=payload)
        if res.status_code == 200:
            print("[TG] ✅ Sent.")
        else:
            print(f"[TG] ❌ Failed: {res.text}")
    except Exception as e:
        print(f"[TG] ❌ Telegram Error: {e}")

def extract_sms(driver):
    global last_messages
    driver.get(config.SMS_URL)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    headers = soup.find_all('th')

    number_idx = service_idx = sms_idx = None
    for idx, th in enumerate(headers):
        hdr = th.get('aria-label','').lower()
        if 'number' in hdr:
            number_idx = idx
        elif 'cli' in hdr:
            service_idx = idx
        elif 'sms' in hdr:
            sms_idx = idx

    if None in (number_idx, service_idx, sms_idx):
        print("[ERR] Missing required columns.")
        return

    rows = soup.find_all('tr')
    for row in rows[1:]:
        cols = row.find_all('td')
        if len(cols) > max(number_idx, service_idx, sms_idx):
            number = cols[number_idx].get_text(strip=True)
            service = cols[service_idx].get_text(strip=True)
            sms = cols[sms_idx].get_text(strip=True)
            message = f"*New OTP:*\nNumber: `{number}`\nService: `{service}`\nMessage: `{sms}`"
            if message not in last_messages:
                send_to_telegram(message)
                last_messages.add(message)
                if len(last_messages) > 50:
                    last_messages = set(list(last_messages)[-50:])
