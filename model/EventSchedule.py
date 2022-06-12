from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BIGINT, Integer, String, TEXT, Float, DateTime

import sys
# sys.path.append('../')
from model.setting import Base
# from DB_config import Base
# from DB_config import ENGINE


class EventSchedule(Base):
    """
    event_schedulesテーブル用モデル
    """
    __tablename__ = 'event_schedule'

    event_id = Column('event_id', BIGINT, primary_key = True)
    holo_id = Column('holo_id', String(255))
    title = Column('title', String(255))
    contents = Column('contents', String(255))
    schedule_start_time_at = Column('schedule_start_time_at', DateTime)
    message = Column('message', TEXT)
    image = Column('image', TEXT)
    status = Column('status', String(255))

# def main(args):
#     """
#     メイン関数
#     """
#     Base.metadata.create_all(bind=ENGINE)

# if __name__ == "__main__":
#     main(sys.argv)