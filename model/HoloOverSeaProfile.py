from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BIGINT, Integer, String, TEXT, Float, DateTime, Date

import sys
# sys.path.append('../')
from model.setting import Base
# from config import Base
# from config import ENGINE

class HoloOverSeaProfile(Base):
    """
    HoloOverSeaProfileモデル
    """
    __tablename__ = 'holo_overseas_profiles'

    id = Column('id', BIGINT, primary_key = True)
    holo_id = Column('holo_id', String(255))
    holo_name = Column('holo_name', String(255))
    profile_text = Column('profile_text', TEXT)
    birthday = Column('birthday', Date)
    debut = Column('debut', Date)
    channel_id = Column('channel_id', String(255))
    channel_url = Column('channel_url', TEXT)
    channel_short_url = Column('channel_short_url', TEXT)
    youtube_subscriber = Column('youtube_subscriber', BIGINT)
    youtube_videoCount = Column('youtube_videoCount', BIGINT)
    youtube_viewCount = Column('youtube_viewCount', BIGINT)
    twitter_account = Column('twitter_account', String(255))
    twitter_url = Column('twitter_url', TEXT)
    twitter_subscriber = Column('twitter_subscriber', BIGINT)

    # twitch_id = Column('twitch_id', String(255))
    # twitch_url = Column('twitch_url', TEXT)
    # twitch_follower = Column('twitch_follower', BIGINT)
    # twitch_view_count = Column('twitch_view_count', BIGINT)
    # offline_img_url = Column('offline_img_url ', TEXT)
    # twitcasting_name = Column('twitcasting_name', String(255))
    # twitcasting_id = Column('twitcasting_id', String(255))
    # twitcasting_screen_id = Column('twitcasting_screen_id', String(255))
    # twitcasting_level = Column('twitcasting_level', Integer)

    image1 = Column('image1', TEXT)
    image2 = Column('image2', TEXT)
    image3 = Column('image3', TEXT)
    image4 = Column('image4', TEXT)
    image_tag = Column('image_tag', String(255))
    tw_arts_tag = Column('tw_arts_tag', String(255))
    live_tag = Column('live_tag', String(255))
    _class = Column('class', String(255))

# def main(args):
#     """
#     メイン関数
#     """
#     Base.metadata.create_all(bind=ENGINE)

# if __name__ == "__main__":
#     main(sys.argv)