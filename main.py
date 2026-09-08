import os
import requests

# 讀取我們待會在 GitHub 設定的秘密金鑰
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

def check_and_post():
    # 這裡未來會串接 Twitter 抓取邏輯，目前先以發送測試訊息為主
    message = "【系統測試】機器人運作正常！準備開始監控 Twitter 更新。"
    
    if DISCORD_WEBHOOK_URL:
        payload = {"content": message}
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        if response.status_code == 204:
            print("成功發送到 Discord！")
        else:
            print(f"發送失敗，錯誤碼: {response.status_code}")
    else:
        print("未找到 Discord Webhook URL 變數。")

if __name__ == "__main__":
    check_and_post()
