import requests
from django.conf import settings

def send_telegram_message(chat_id: str, message: str) -> bool:
    """
    Отправляет сообщение в Telegram
    """
    bot_token = settings.TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Error sending telegram message: {e}")
        return False 