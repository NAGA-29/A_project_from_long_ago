from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BIGINT, Integer, String, TEXT, Float, DateTime

import sys
# sys.path.append('../')
import setting
# from DB_config import Base
# from DB_config import ENGINE


class TwitchVideo(setting.Base):
    """
    twitch_videosテーブル用モデル
    """
    __tablename__ = 'twitch_videos'
    id = Column('id', BIGINT, primary_key = True)
    holo_name = Column('holo_name', String(255))
    belongs = Column('belongs', String(255))
    title = Column('title', String(255))
    video_id = Column('video_id', String(255))
    user_id = Column('user_id', String(255))
    user_login = Column('user_login', String(255))
    url = Column('url', TEXT)
    view_count = Column('view_count', Integer) #再生回数
    duration = Column('duration', String) #再生時間
    game_name = Column('game_name', String(255))
    game_id = Column('game_id', String(255))
    published_at = Column('published_at', DateTime)
    thumbnail_url = Column('thumbnail_url', TEXT)
    viewable = Column('viewable', String)
    notification_last_time_at = Column('notification_last_time_at', DateTime)

# def main(args):
#     """
#     メイン関数
#     """
#     Base.metadata.create_all(bind=ENGINE)

# if __name__ == "__main__":
#     main(sys.argv)