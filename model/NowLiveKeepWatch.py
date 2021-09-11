from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BIGINT, Integer, String, TEXT, Float, DateTime

import sys
# sys.path.append('../')
from setting import Base
# from config import Base
# from config import ENGINE

class NowLiveKeepWatch(Base):
    """
    YoutubeVideoモデル
    """
    __tablename__ = 'now_live_keep_watchs'

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
    notification_last_time_at = Column('notification_last_time_at', DateTime)
    compared_point = Column('compared_point', Integer)
    status = Column('status', DateTime)

# def main(args):
#     """
#     メイン関数
#     """
#     Base.metadata.create_all(bind=ENGINE)

# if __name__ == "__main__":
#     main(sys.argv)