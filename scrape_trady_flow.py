import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from telegram import Bot
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = 'https://tradytics.com/trady-flow'

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)

try:
    print("🌐 Navigating to Trady Flow...")
    driver.get(URL)
    time.sleep(30)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    text = soup.get_text()
    matches = re.findall(r'Premium:\s*\$([\d.,]+)M', text)

    found_alert = False
    for match in matches:
        value = float(match.replace(",", ""))
        if value >= 1.0:
            found_alert = True
            message = f"🚨 Option Block Detected!\nPremium: ${value}M"
            Bot(token=BOT_TOKEN).send_message(chat_id=CHAT_ID, text=message)
            print("✅ Sent alert:", message)

    if not found_alert:
        print("🔍 No option block with premium > $1M found.")

except Exception as e:
    print("❌ Error occurred:", e)

finally:
    driver.quit()
