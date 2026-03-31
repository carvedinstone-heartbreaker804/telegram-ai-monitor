import requests


def set_telegram_webhook(bot_token: str, webhook_url: str):
    url = f"https://api.telegram.org/bot{bot_token}/setWebhook"
    response = requests.post(url, json={"url": webhook_url})
    return response.json()


def get_telegram_webhook_info(bot_token: str):
    url = f"https://api.telegram.org/bot{bot_token}/getWebhookInfo"
    response = requests.get(url)
    return response.json()