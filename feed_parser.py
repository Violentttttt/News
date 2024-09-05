import feedparser
from bs4 import BeautifulSoup
import requests

# URLs для RSS-фидов
coindesk_url = "https://www.coindesk.com/arc/outboundfeeds/rss/"
cointelegraph_url = "https://cointelegraph.com/rss"

def clean_description(description):
    """
    Очистка HTML-тегов из описания.
    """
    soup = BeautifulSoup(description, 'html.parser')
    return soup.get_text()

def fetch_news():
    """
    Извлечение новостей с различных источников.
    """
    news_items = []

    # Парсинг новостей с Coindesk
    feed_coindesk = feedparser.parse(coindesk_url)
    latest_coindesk = feed_coindesk.entries[0]
    news_items.append({
        "title": latest_coindesk.title,
        "link": latest_coindesk.link,
        "description": latest_coindesk.description,
        "source": "Coindesk"
    })

    # Парсинг новостей с Cointelegraph
    feed_cointelegraph = feedparser.parse(cointelegraph_url)
    latest_cointelegraph = feed_cointelegraph.entries[0]
    cleaned_description = clean_description(latest_cointelegraph.description)
    news_items.append({
        "title": latest_cointelegraph.title,
        "link": latest_cointelegraph.link,
        "description": cleaned_description,
        "source": "Cointelegraph"
    })

    # Парсинг новостей с CryptoPanic
    response = crypto_panic().json()
    if 'results' in response and len(response['results']) > 0:
        latest_post = response['results'][0]
        news_items.append({
            "title": latest_post.get('title', 'No Title'),
            "link": latest_post.get('url', 'No URL'),
            "description": latest_post.get('title', 'No Description'),
            "source": "CryptoPanic"
        })

    return news_items

def crypto_panic():
    """
    Получение данных с CryptoPanic API.
    """
    return requests.get('https://cryptopanic.com/api/v1/posts/?auth_token=41a77784b55b6a34cd7344be46f283283ffc1488&filter=hot')
