from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine

from ai_comment import ai_comment
from ask import ask
from bot import send_news
from database import Post, Segment
from feed_parser import fetch_news
from prompts import get_rate, add_comment
from send import send_news_to_channel

database_path = 'postgresql+psycopg2://postgres:12385279@127.0.0.1:5432/news'
engine = create_engine(database_path, pool_pre_ping=True)
session = Session(bind=engine)

available_ratings = list(
    range(1, 10))
used_ratings = set()


def update_available_ratings(rating):
    """
    Обновление списка доступных рейтингов.
    """
    global available_ratings, used_ratings
    if rating in available_ratings:
        available_ratings.remove(rating)
        used_ratings.add(rating)
    else:
        print(f"Рейтинг {rating} уже использован или недоступен.")


def reset_ratings():
    global available_ratings, used_ratings
    available_ratings = list(range(1, 10))
    used_ratings = set()


def save_post(title, url, description, rate, source):
    """
    Сохранение новости в базу данных.
    """
    post = Post(
        title=title,
        url=url,
        description=description,
        rate=rate,
        source=source
    )
    session.add(post)
    session.commit()
    add_post_to_segment(session, post)


def add_post_to_segment(session, post):
    segment = session.query(Segment).order_by(Segment.id.desc()).first()
    if not segment or segment.is_fully_filled():
        segment = Segment()
        session.add(segment)

    segment.add_post(post, session)
    session.commit()



def get_highest_rated_post():
    """
    Получение поста с наивысшим рейтингом из последнего сегмента.
    """
    segment = session.query(Segment).order_by(Segment.id.desc()).first()  # Получаем последний сегмент

    if not segment:
        print("Сегмент не найден")
        return None

    # Получаем список всех постов в сегменте
    post_ids = [getattr(segment, f'post_with_rate_{i}') for i in range(1, 10) if getattr(segment, f'post_with_rate_{i}') is not None]

    if not post_ids:
        print("Нет постов в сегменте")
        return None

    # Находим пост с максимальным рейтингом из списка постов
    highest_rated_post = session.query(Post).filter(Post.id.in_(post_ids)).order_by(Post.rate.desc()).first()

    return highest_rated_post






"""

Здесь кончились вспомогательные функции





"""
def process_news():
    """
    Обработка новостей, полученных из feed_parser.
    """
    news_items = fetch_news()

    for news in news_items:
        prompt = get_rate(news["title"], available_ratings)
        # y = add_comment(news)
        rate = ask(prompt_text=prompt)
        # x = ai_comment(prompt_text=y)
        # print('э блять', x)
        if rate == 10:
            send_news(news)
        if rate is not None and rate in available_ratings:
            update_available_ratings(rate)
            save_post(
                title=news["title"],
                url=news["link"],
                description=news["description"],
                rate=rate,
                source=news['source']
            )

            print(f"Saved post: {news['title']} with rate {rate}")
            if len(available_ratings) == 0:
                reset_ratings()

def last():
    """
    Процесс отправки новости с наивысшим рейтингом в телеграм-канал и создание нового сегмента.
    """
    highest_rated_post = get_highest_rated_post()

    if highest_rated_post:
        y = add_comment(highest_rated_post)
        x = ai_comment(prompt_text=y)
        send_news_to_channel(x)

        new_segment = Segment()
        session.add(new_segment)
        session.commit()

