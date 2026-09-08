import os
import requests
import xml.etree.ElementTree as ET

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

# 改用穩定的 Nitter RSS 來源來追蹤《鳴潮》英文官方帳號
TWITTER_RSS_URL = "https://nitter.privacydev.net/Wuthering_Waves/rss"

def check_and_post():
    if not DISCORD_WEBHOOK_URL:
        print("未找到 Discord Webhook URL 密鑰。")
        return

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(TWITTER_RSS_URL, headers=headers, timeout=10)
        
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            item = root.find(".//item")
            if item is not None:
                title = item.find("title").text if item.find("title") is not None else "無標題"
                link = item.find("link").text if item.find("link") is not None else ""
                
                message = f"📢 **《鳴潮》官方 Twitter 更新：**\n{title}\n🔗 {link}"
                
                payload = {"content": message}
                discord_res = requests.post(DISCORD_WEBHOOK_URL, json=payload)
                
                if discord_res.status_code == 204:
                    print("成功發送最新貼文到 Discord！")
                else:
                    print(f"發送失敗，錯誤碼：{discord_res.status_code}")
        else:
            print(f"無法讀取 RSS，狀態碼：{response.status_code}")
    except Exception as e:
        print(f"發生錯誤：{e}")

if __name__ == "__main__":
    check_and_post()
