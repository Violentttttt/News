from xmlrpc.client import Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from ai_comment import ai_comment

from send import send_news_to_channel

database_path = 'postgresql+psycopg2://postgres:12385279@127.0.0.1:5432/news'
from sqlalchemy import create_engine, Float, BigInteger
from sqlalchemy import create_engine, MetaData, Table, Integer, String, Enum, Column, DateTime, ForeignKey, Numeric

from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Mapped
from datetime import datetime, timedelta

# makemigrations - alembic revision --autogenerate -m "Описание изменений"
# migrate - alembic upgrade head

engine = create_engine(database_path, pool_pre_ping=True)
engine.connect()
Session = sessionmaker(engine)
Session.configure(bind=engine)

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}


class Base:
    __allow_unmapped__ = True


metadata = MetaData(naming_convention=naming_convention)
Base = declarative_base(metadata=metadata, cls=Base)


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    url = Column(String(500), nullable=False)
    description = Column(String(2000), nullable=False)
    rate = Column(Integer, nullable=False)
    source = Column(String(500), nullable=True)
    created_on = Column(DateTime(), default=datetime.now)


class Segment(Base):
    __tablename__ = 'segment'
    id = Column(Integer, primary_key=True)
    post_with_rate_1 = Column(Integer, ForeignKey('post.id'), nullable=True)
    post_with_rate_2 = Column(Integer, ForeignKey('post.id'), nullable=True)
    post_with_rate_3 = Column(Integer, ForeignKey('post.id'), nullable=True)
    post_with_rate_4 = Column(Integer, ForeignKey('post.id'), nullable=True)
    post_with_rate_5 = Column(Integer, ForeignKey('post.id'), nullable=True)
    post_with_rate_6 = Column(Integer, ForeignKey('post.id'), nullable=True)
    post_with_rate_7 = Column(Integer, ForeignKey('post.id'), nullable=True)
    post_with_rate_8 = Column(Integer, ForeignKey('post.id'), nullable=True)
    post_with_rate_9 = Column(Integer, ForeignKey('post.id'), nullable=True)
    created_on = Column(DateTime(), default=datetime.now)
    filled_on = Column(DateTime(), nullable=True)

    def add_post(self, post, session: Session):
        """
        Добавляет пост в сегмент в зависимости от его рейтинга.
        Если сегмент полностью заполнен, обновляется поле filled_on и вызывается функция обработки.
        """
        rate_field = f'post_with_rate_{post.rate}'
        if getattr(self, rate_field) is None:
            setattr(self, rate_field, post.id)
            if self.is_fully_filled():
                self.filled_on = datetime.now()

    def is_fully_filled(self):
        """
        Проверяет, заполнены ли все позиции в сегменте.
        """
        for i in range(1, 10):
            if getattr(self, f'post_with_rate_{i}') is None:
                return False
        return True




class Rate10(Base):
    __tablename__ = 'rate10'
    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    url = Column(String(500), nullable=False)
    description = Column(String(2000), nullable=False)
    rate = Column(Integer, nullable=False)
    source = Column(String(500), nullable=True)
    created_on = Column(DateTime(), default=datetime.now)
