import requests
import asyncio
from pyppeteer import launch
from fake_useragent import UserAgent
import random
import time
from datetime import datetime

adsterra_link = "https://www.profitableratecpm.com/sguz63ia7?key=dcf4558d982249ca87919995d5e5d402"

def get_proxy():
    try:
        res = requests.get("https://www.proxy-list.download/api/v1/get?type=http&country=US")
        proxy_list = res.text.strip().split("\r\n")
        return random.choice(proxy_list)
    except Exception as e:
        print("[!] Proxy fetch error:", e)
        return None

def get_today_limit():
    day = (datetime.now() - datetime(2024, 6, 1)).days + 1
    if day <= 2:
        return 150
    elif day <= 4:
        return 250
    else:
        return 300

async def click_link(proxy):
    try:
        browser = await launch({
            'headless': True,
            'args': [
                f'--proxy-server=http://{proxy}',
                '--no-sandbox',
                '--disable-setuid-sandbox'
            ]
        })

        page = await browser.newPage()
        ua = UserAgent().random
        await page.setUserAgent(ua)

        await page.goto(adsterra_link, timeout=60000)
        print(f"[✓] Clicked via {proxy}")
        await asyncio.sleep(random.randint(7, 12))
        await browser.close()
        return True

    except Exception as e:
        print("[X] Error in browser:", e)
        return False

def start_clicks():
    limit = get_today_limit()
    for i in range(limit):
        proxy = get_proxy()
        if not proxy:
            print("[!] Skipping... No proxy found")
            continue
        print(f"\n➡️ Click {i+1}/{limit} | Using Proxy: {proxy}")
        try:
            success = asyncio.get_event_loop().run_until_complete(click_link(proxy))
            if not success:
                print("[!] Retrying with new proxy...")
                continue
            time.sleep(random.randint(10, 25))
        except Exception as e:
            print("[!] Global Error:", e)

if __name__ == "__main__":
    start_clicks()
