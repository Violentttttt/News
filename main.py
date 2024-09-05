from views import process_news, last
from apscheduler.schedulers.blocking import BlockingScheduler

# Создаём экземпляр планировщика
scheduler = BlockingScheduler()

last()
process_news()

scheduler.add_job(process_news, 'interval', minutes=96, max_instances=3)


scheduler.add_job(last, 'interval', minutes=288)


if __name__ == "__main__":
    scheduler.start()
