from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BIGINT, Integer, String, TEXT, Float, DateTime

import sys
# from setting import Base
from model.setting import Base
# sys.path.append('../')
# from config import Base
# from config import ENGINE

class KeepWatch(Base):
    """
    KeepWatchモデル
    """
    # __tablename__ = 'keep_watchs'
    __tablename__ = 'keep_watchs'
    id = Column('id', BIGINT, primary_key = True)
    video_id = Column('video_id', String(255))
    holo_name = Column('holo_name', String(255))
    belongs = Column('belongs', String(255))
    title = Column('title', String(255))
    channel_id = Column('channel_id', String(255))
    channel_url = Column('channel_url', String(255))
    uploaded_at = Column('uploaded_at', DateTime)
    scheduled_start_time_at = Column('scheduled_start_time_at', DateTime)
    actual_start_time_at = Column('actual_start_time_at', DateTime)
    concurrent_viewers = Column('concurrent_viewers', Integer)
    active_live_chat_id = Column('active_live_chat_id', String(255))
    image_L = Column('image_L', TEXT)
    image_default = Column('image_default', TEXT)
    status = Column('status', DateTime)


# def main(args):
#     """
#     メイン関数
#     """
#     Base.metadata.create_all(bind=ENGINE)

# if __name__ == "__main__":
#     main(sys.argv)
