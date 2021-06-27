from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BIGINT, Integer, String, TEXT, Float, DateTime

import sys
sys.path.append('../')
from config import Base
from config import ENGINE

class YoutubeVideo(Base):
    """
    YoutubeVideoモデル
    """
    __tablename__ = 'youtube_videos_20210522'
    # __tablename__ = 'youtube_videos_20210307'
    id = Column('id', BIGINT, primary_key = True)
    holo_name = Column('holo_name', String(255))
    title = Column('title', String(255))
    video_id = Column('video_id', String(255))
    channel_id = Column('channel_id', String(255))
    channel_url = Column('channel_url', String(255))
    view_count = Column('view_count', Integer)
    like_count = Column('like_count', Integer)
    dislike_count = Column('dislike_count', Integer)
    comment_count = Column('comment_count', Integer)
    game_name = Column('game_name', String(255))
    tag = Column('tag', String(255))
    uploaded_at = Column('uploaded_at', DateTime)
    scheduled_start_time_at = Column('scheduled_start_time_at', DateTime)
    actual_start_time_at = Column('actual_start_time_at', DateTime)
    actual_end_time_at = Column('actual_end_time_at', DateTime)
    max_concurrent_viewers = Column('max_concurrent_viewers', Integer)
    active_live_chat_id = Column('active_live_chat_id', String(255))
    image_L = Column('image_L', TEXT)
    image_M = Column('image_M', TEXT)
    image_S = Column('image_S', TEXT)
    image_XS = Column('image_XS', TEXT)
    image_Default = Column('image_Default', TEXT)
    status = Column('status', DateTime)
    notification_last_time_at = Column('notification_last_time_at', DateTime)

# def main(args):
#     """
#     メイン関数
#     """
#     Base.metadata.create_all(bind=ENGINE)

# if __name__ == "__main__":
#     main(sys.argv)