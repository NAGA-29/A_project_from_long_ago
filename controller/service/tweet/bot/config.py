import os
from os.path import join, dirname
from dotenv import load_dotenv

import twitter

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)


oauth = twitter.OAuth(os.environ.get('ACCESS_TOKEN'),
                        os.environ.get('ACCESS_TOKEN_SECRET'),
                        os.environ.get('CONSUMER_KEY'),
                        os.environ.get('CONSUMER_SECRET'))

twitter_api = twitter.Twitter(auth=oauth)
twitter_stream = twitter.TwitterStream(auth=oauth)
SCREEN_NAME = os.environ.get('TWITTER_SCREEN_NAME') # @usernameの自分のusername