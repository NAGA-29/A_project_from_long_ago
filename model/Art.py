from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BIGINT, Integer, String, TEXT, Float, DateTime

import sys
# sys.path.append('../')
from setting import Base
# from config import Base
# from config import ENGINE

class Art(Base):
    """
    Artモデル
    """
    __tablename__ = 'arts'

    id = Column('id', BIGINT, primary_key = True)
    name = Column('name', String(255))
    tag = Column('tag', String(255))
    tweet_id = Column('tweet_id', BIGINT)
    text = Column('text', TEXT)
    favorite = Column('favorite', BIGINT)
    retweet = Column('retweet', BIGINT)
    file_name1 = Column('file_name1', String(255))
    file_name2 = Column('file_name2', String(255))
    file_name3 = Column('file_name3', String(255))
    file_name4 = Column('file_name4', String(255))
    creator_path = Column('creator_path', String(255))
    uploadJST = Column('uploadJST', DateTime)
    url = Column('url', TEXT)

# def main(args):
#     """
#     メイン関数
#     """
#     Base.metadata.create_all(bind=ENGINE)

# if __name__ == "__main__":
#     main(sys.argv)