from bot.config import twitter_api, SCREEN_NAME
# from config import twitter_api, SCREEN_NAME
from pprint import pprint

class Tweet():

    def __init__(self, tweet):
        self.tweet = tweet

    def has_required_keys(self, required_keys_list):
        for required_key in required_keys_list:
            if required_key not in self.tweet:
                return False
        return True

    def reply(self, text):
        status = '@' + self.get_user_screenname() + '\n'
        status += text
        return twitter_api.statuses.update(status=status, in_reply_to_status_id=self.tweet['id_str'])

    def is_retweet(self):
        return 'retweeted_status' in self.tweet

    def is_reply_from_me(self):
        return self.get_user_screenname() == SCREEN_NAME

    def is_reply_from_follower(self):
        followers = twitter_api.followers.ids(screen_name=SCREEN_NAME, count=5000) # int型のフォロワーのID配列
        return self.get_user_id() in followers['ids']

    def get_user_id(self):
        return self.tweet['user']['id']

    def get_user_name(self):
        return self.tweet['user']['name']

    def get_user_screenname(self):
        return self.tweet['user']['screen_name']

    def get_tweet_text(self):
        return self.tweet['text']

    def get_wl_list(self):
        twitter_api.lists.members(owner_screen_name="HololiveP", list_id="1374873110961221641")
        member_list = twitter_api.lists.members(owner_screen_name="HololiveP", list_id="1374873110961221641")
        wl = [mem['screen_name'] for mem in member_list['users']]
        return wl

# if __name__ == '__main__':
#     # replay_for_wl.start()

#     wl = []
#     member_list = twitter_api.lists.members(owner_screen_name="HololiveP", list_id="1374873110961221641")
#     wl = [mem['screen_name'] for mem in member_list['users']]
#     pprint(wl)