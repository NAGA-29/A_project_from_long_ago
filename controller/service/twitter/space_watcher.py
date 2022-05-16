import time
from datetime import datetime, timedelta
from dateutil.tz import gettz
from dotenv import load_dotenv
import tweepy
import os
from os.path import join, dirname
import pickle
from pprint import pprint
import sys

'''origin'''
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from config.vtuber.hololive import Hololive

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


### initialize
# # 本番アカウント
# # ###############################################################################
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')
BEARER_TOKEN = os.environ.get('BEARER_TOKEN')

# twitter api V2 本番
Client = tweepy.Client(bearer_token=BEARER_TOKEN, consumer_key=CONSUMER_KEY, 
                        consumer_secret=CONSUMER_SECRET, access_token=ACCESS_TOKEN, 
                        access_token_secret=ACCESS_TOKEN_SECRET, wait_on_rate_limit=True,)

# os.path.dirname(os.path.abspath(__file__))
LAST_TW_FILE = os.path.dirname(os.path.abspath(__file__)) + '/last_tw_id.pkl'

# # ###############################################################################

# # 開発用アカウント
# # ###############################################################################
# CONSUMER_KEY_DEV = os.environ.get('CONSUMER_KEY_TEST')
# CONSUMER_SECRET_DEV = os.environ.get('CONSUMER_SECRET_TEST')
# ACCESS_TOKEN_DEV = os.environ.get('ACCESS_TOKEN_TEST')
# ACCESS_TOKEN_SECRET_DEV = os.environ.get('ACCESS_TOKEN_SECRET_TEST')
# BEARER_TOKEN_DEV = os.environ.get('BEARER_TOKEN_TEST')

# ## twitter api V2
# Client = tweepy.Client(bearer_token=BEARER_TOKEN_DEV, consumer_key=CONSUMER_KEY_DEV, 
#                         consumer_secret=CONSUMER_SECRET_DEV, access_token=ACCESS_TOKEN_DEV, 
#                         access_token_secret=ACCESS_TOKEN_SECRET_DEV, wait_on_rate_limit=True,)
# LAST_TW_FILE = 'last_tw_id_dev.pkl'
# # ###############################################################################    
space_owner = Hololive().get_twitter_num().values()
print(space_owner)
    
def main():
    # space_owner = hololive.space_owner_id.values()
    space_owner_convert2str = [str(i) for i in space_owner]
    # pprint(space_owner_convert2str)

    expansions_4search = ['invited_user_ids', 'speaker_ids', 'creator_id', 'host_ids']
    space_fields_4search = ['host_ids', 'created_at', 'creator_id', 'id', 'lang',
                    'invited_user_ids', 'participant_count', 'speaker_ids', 'started_at',
                    'ended_at','subscriber_count', 'topic_ids', 'state', 'title', 
                    'updated_at', 'scheduled_start', 'is_ticketed']
    user_fields_4search = ['created_at', 'description', 'entities', 'id', 'location', 
                    'name', 'pinned_tweet_id', 'profile_image_url', 'protected', 
                    'public_metrics', 'url', 'username', 'verified', 'withheld']

    expansions = ['invited_user_ids', 'speaker_ids', 'creator_id', 'host_ids']
    space_fields = ['host_ids', 'created_at', 'creator_id', 'id', 'lang',
                    'invited_user_ids', 'participant_count', 'speaker_ids', 
                    'started_at', 'ended_at', 'subscriber_count', 'topic_ids', 
                    'state', 'title', 'updated_at', 'scheduled_start', 'is_ticketed']
    user_fields = ['created_at', 'description', 'entities', 'id', 
                    'location, name', 'pinned_tweet_id', 'profile_image_url',
                    'protected', 'public_metrics', 'url', 'username', 'verified', 'withheld']

    # live中のスペースidを取得
    search_result = Client.get_spaces(user_ids=space_owner_convert2str, expansions=expansions_4search,
                            space_fields=space_fields_4search, user_fields=user_fields_4search)
    # pprint( datetime.now().astimezone(gettz('Asia/Tokyo')) - (search_result[0][0]['started_at']).astimezone(gettz('Asia/Tokyo')) )
    # if ( datetime.now().astimezone(gettz('Asia/Tokyo')) - (search_result[0][0]['started_at']).astimezone(gettz('Asia/Tokyo')) ) > timedelta(seconds=300):
    #     print('条件に合うスペースはありません')
    #     return
        # (search_result[0][0]['started_at']).astimezone(gettz('Asia/Tokyo')).strftime('%Y-%m-%d %H:%M:%S') #start time
        # (datetime.now() - timedelta(seconds=300,)).strftime('%Y-%m-%d %H:%M:%S'): #now time - 5min
        # pprint(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) #now time

    if search_result[3]['result_count'] > 0:
        live_space_id = [{i['id']:i['title']} for i in search_result.data]
        
        tw_result = None
        last_tw_id = None
        for n in live_space_id:
            for id, title in n.items():
                try:
                    with open(LAST_TW_FILE, 'rb') as f:
                        last_tw_id = pickle.load(f)
                except EOFError as err:
                        print(f'EOFError on load pickle file: {err}')
                tw_result = Client.create_tweet(text=f"<Twitter Space>\n\n{title}\n\nスペース展開中です!\nhttps://twitter.com/i/spaces/{id}",
                                                in_reply_to_tweet_id=last_tw_id if last_tw_id else None,)
                time.sleep(3)
        try:
            with open(LAST_TW_FILE, 'wb') as f:
                pickle.dump(tw_result[0]['id'], f)
        except EOFError as err:
            print(f'ERROR on save pickle file: {err}')
                    # self.logger.error(f'ERROR on save pickle file: {err}')
    else:
        print('条件に合うスペースはありません')
                    
if __name__ == '__main__':
    while True:
        main()
        time.sleep(300)