import os
import requests
import xml.etree.ElementTree as ET

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

# 準備多個備用的 RSSHub 公共節點，只要有一個成功就能運作
RSS_URLS = [
    "https://rsshub.rssforever.com/twitter/user/Wuthering_Waves",
    "https://rss.artie.id/twitter/user/Wuthering_Waves",
    "https://nitter.privacydev.net/Wuthering_Waves/rss"
]

def check_and_post():
    if not DISCORD_WEBHOOK_URL:
        print("未找到 Discord Webhook URL 密鑰。")
        return

    success = False
    for url in RSS_URLS:
        try:
            print(f"嘗試連線至: {url}")
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=8)
            
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
                        success = True
                        break
                    else:
                        print(f"Discord 發送失敗，狀態碼：{discord_res.status_code}")
            else:
                print(f"節點回應異常，狀態碼：{response.status_code}")
        except Exception as e:
            print(f"此節點連線失敗：{e}")
            continue

    if not success:
        print("所有備用 RSS 節點目前皆無法連線，將等待下一次排程再試。")

if __name__ == "__main__":
    check_and_post()
