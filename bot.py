import telebot
from telebot import types
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from datetime import datetime
from database import Rate10
import threading

# Настройка базы данных
database_path = 'postgresql+psycopg2://postgres:12385279@127.0.0.1:5432/news'
engine = create_engine(database_path, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

API_TOKEN = '7333169074:AAGB9iqwvj0W9YL0Cv3tGiAwiOg4LZgtHJk'
YOUR_USER_ID = 1079583778

bot = telebot.TeleBot(API_TOKEN)


# Обработка нажатий на кнопки "Принять"
@bot.callback_query_handler(func=lambda call: call.data.startswith("accept_"))
def accept_news(call):
    post_id = call.data.split("_")[1]

    # Создание объекта Rate10 для сохранения в базу данных
    new_post = Rate10(
        title=call.message.text.split('\n\n')[1].split('Заголовок: ')[1],
        url=call.message.text.split('Ссылка: ')[1],
        description=call.message.text.split('\n')[3].split('Описание: ')[1],
        rate=10,
        source=call.message.text.split('\n')[4].split('Источник: ')[1],
        created_on=datetime.now()
    )

    # Добавление и сохранение объекта в базе данных
    session.add(new_post)
    session.commit()

    bot.answer_callback_query(call.id, f"Новость с ID {post_id} принята и сохранена!")
    bot.delete_message(call.message.chat.id, call.message.message_id)  # Удаляем сообщение


@bot.callback_query_handler(func=lambda call: call.data.startswith("reject_"))
def reject_news(call):
    post_id = call.data.split("_")[1]
    bot.answer_callback_query(call.id, f"Новость с ID {post_id} отклонена!")
    bot.delete_message(call.message.chat.id, call.message.message_id)


# Функция отправки новости
def send_news(post):
    inline_kb = types.InlineKeyboardMarkup(row_width=2)
    btn_accept = types.InlineKeyboardButton(text="✅ Accept", callback_data=f"accept_{post.id}")
    btn_reject = types.InlineKeyboardButton(text="❌ Reject", callback_data=f"reject_{post.id}")
    inline_kb.add(btn_accept, btn_reject)

    # Отправляем новость
    bot.send_message(
        YOUR_USER_ID,
        f"🚨 Срочная новость!\n\n"
        f"Заголовок: {post.title}\n"
        f"Описание: {post.description}\n"
        f"Источник: {post.source}\n"
        f"Ссылка: {post.url}",
        reply_markup=inline_kb
    )


class TestPost:
    def __init__(self, title, url, description, rate, source="Test Source"):
        self.id = 1
        self.title = title
        self.url = url
        self.description = description
        self.rate = rate
        self.source = source


# test_post = TestPost(
#     title='Test News',
#     url='https://await.lol',
#     description='Это тестовая новость',
#     rate=10
# )
#
# # Отправка тестовой новости
# send_news(test_post)

def start_bot():
    bot.polling(none_stop=True, interval=0)


bot_thread = threading.Thread(target=start_bot)
bot_thread.start()
