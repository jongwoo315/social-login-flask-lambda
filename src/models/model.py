from datetime import datetime
import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from config import DevelopmentConfig

try:
    os.environ['AWS_EXECUTION_ENV']
except KeyError:
    database_uri = DevelopmentConfig.SQLALCHEMY_DATABASE_URI_LOCAL
else:
    database_uri = DevelopmentConfig.SQLALCHEMY_DATABASE_URI

engine = create_engine(database_uri)
Base = declarative_base(engine)


class User(Base):
    __tablename__ = 'users'
    idx  = Column('idx', Integer, primary_key=True)
    platform = Column(String(30))
    screen_name = Column(String(60))
    user_id = Column(String(60))
    regist_date = Column(DateTime, default=datetime.now())
    update_date = Column(DateTime, default=datetime.now())

    UniqueConstraint(user_id, name='user_id_idx')

    def __init__(self, platform, screen_name, user_id):
        self.platform = platform
        self.screen_name = screen_name
        self.user_id = user_id

Base.metadata.create_all(bind=engine)
db_session = Session(bind=engine)
