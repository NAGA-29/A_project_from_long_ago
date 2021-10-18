from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BIGINT, Integer, String, TEXT, Float, DateTime, Date

import sys
# sys.path.append('../')
from model.setting import Base
# from config import Base
# from config import ENGINE

class HoloData(Base):
    """
    HoloDatasモデル
    """
    __tablename__ = 'holo_datas'

    id = Column('id', BIGINT, primary_key = True)
    all_youtube_subscriber = Column('all_youtube_subscriber', BIGINT)
    all_youtube_videoCount = Column('all_youtube_videoCount', BIGINT)
    all_youtube_viewCount = Column('all_youtube_viewCount', BIGINT)
    updated_at = Column('updated_at', DateTime)

# def main(args):
#     """
#     メイン関数
#     """
#     Base.metadata.create_all(bind=ENGINE)

# if __name__ == "__main__":
    # main(sys.argv)