import enum
from dataclasses import dataclass
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class StatusUser(enum.IntEnum):
    not_auth = 0
    not_playing = 1
    finding = 2
    in_match = 3
    instructor = 4
    sapper = 5


@dataclass
class User:
    tg_id: str
    tg_username: str = None
    rating: int = 0
    status: StatusUser = StatusUser.not_auth
    current_round = None
    current_dialog = None
    teammate = None
    count_current_round: int = 0


class UserModel(Base):
    __tablename__ = 'users'

    tg_id = Column(String, primary_key=True)
    tg_username = Column(String, nullable=True)
    rating = Column(Integer, default=0)
    status = Column(Integer, default=StatusUser.not_auth.value)


class SqlModule:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def add_new_user(self, tg_id: str):
        session = self.Session()
        if not session.query(UserModel).filter_by(tg_id=tg_id).first():
            new_user = UserModel(tg_id=tg_id)
            session.add(new_user)
            session.commit()
        session.close()

    def get_rating(self, tg_id: str) -> int:
        session = self.Session()
        user = session.query(UserModel).filter_by(tg_id=tg_id).first()
        session.close()
        return user.rating if user else 0

    def update_rating(self, tg_id: str, value: int):
        session = self.Session()
        user = session.query(UserModel).filter_by(tg_id=tg_id).first()
        if user:
            user.rating = value
            session.commit()
        session.close()

    def get_user_by_tg_id(self, tg_id: str) -> User:
        session = self.Session()
        user_model = session.query(UserModel).filter_by(tg_id=tg_id).first()
        session.close()
        if user_model:
            return User(
                tg_id=user_model.tg_id,
                tg_username=user_model.tg_username,
                rating=user_model.rating,
                status=StatusUser(user_model.status)
            )
        return None

    def save_user(self, user: User):
        session = self.Session()
        user_model = session.query(UserModel).filter_by(tg_id=user.tg_id).first()
        if user_model:
            user_model.tg_username = user.tg_username
            user_model.rating = user.rating
            user_model.status = user.status.value
        else:
            user_model = UserModel(
                tg_id=user.tg_id,
                tg_username=user.tg_username,
                rating=user.rating,
                status=user.status.value
            )
            session.add(user_model)
        session.commit()
        session.close()
