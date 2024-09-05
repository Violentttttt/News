import requests

bot_token = '7333169074:AAGB9iqwvj0W9YL0Cv3tGiAwiOg4LZgtHJk'
channel_id = '-1002216802741'


def send_news_to_channel(message):

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    data = {
        'chat_id': channel_id,
        'text': message + "\n\n#violent\n<b><a href='https://t.me/crypto_tidings_ai'>👉Violent's News. Subscribe</a></b>",
        'parse_mode': 'HTML',
        'disable_web_page_preview': True
    }

    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("Новость успешно отправлена в канал!")
    else:
        print(f"Ошибка при отправке новости: {response.status_code}, {response.text}")





