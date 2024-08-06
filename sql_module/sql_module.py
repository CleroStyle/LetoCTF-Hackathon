from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    tg_id = Column(String, primary_key=True)
    rating = Column(Integer, default=0)

class SqlModule:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def add_new_user(self, tg_id: str):
        session = self.Session()
        if not session.query(User).filter_by(tg_id=tg_id).first():
            new_user = User(tg_id=tg_id)
            session.add(new_user)
            session.commit()
        session.close()

    def get_rating(self, tg_id: str) -> int:
        session = self.Session()
        user = session.query(User).filter_by(tg_id=tg_id).first()
        session.close()
        return user.rating if user else 0

    def update_rating(self, tg_id: str, value: int):
        session = self.Session()
        user = session.query(User).filter_by(tg_id=tg_id).first()
        if user:
            user.rating = value
            session.commit()
        session.close()
