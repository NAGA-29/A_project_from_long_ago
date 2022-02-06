import logging
from bot.config import twitter_stream, SCREEN_NAME
from bot.tweet import Tweet


def start():

    # loggingの設定
    formatter = '%(levelname)s : %(asctime)s : %(message)s'
    logging.basicConfig(level=logging.INFO, format=formatter)

    replied_user_list = [] # 返信したユーザをリストで管理

    tracking_text = '@'+ SCREEN_NAME + ' 教えて'
    for tweet in twitter_stream.statuses.filter(language='ja', track=tracking_text):
        tweet_obj = Tweet(tweet)
        account = tweet_obj.get_user_screenname()

        # 必要なキーが含まれていない場合
        required_keys_list = [
            'id_str',
            'text',
            'user'
        ]
        if not tweet_obj.has_required_keys(required_keys_list):
            logging.warning('FALSE->required key is empty')
            print(tweet_obj.tweet)
            continue

        # リツイートの場合（tracking_textにマッチしていると反応してしまう）
        if tweet_obj.is_retweet():
            logging.warning('%s\n [user]: %s\n [tweet]: %s', 'FALSE->is retweet', tweet_obj.get_user_screenname(), tweet_obj.get_tweet_text())
            continue

        # 自身のツイートの場合
        if tweet_obj.is_reply_from_me():
            tweet_obj.reply(REPLY_TEXT)
            replied_user_list.append(user_id)
            logging.info('%s\n [user]: %s\n [tweet]: %s', 'SUCCESS->self tweet', tweet_obj.get_user_screenname(), tweet_obj.get_tweet_text())
            continue

        # 過去に返信したユーザの場合
        user_id = tweet_obj.get_user_id()
        if user_id in replied_user_list:
            logging.warning('%s\n [user]: %s\n [tweet]: %s', 'FALSE->has already replied', tweet_obj.get_user_screenname(), tweet_obj.get_tweet_text())
            continue

        # ホワイトリスト以外のユーザーの場合
        member_list = tweet_obj.get_wl_list()
        if not account in member_list:
            logging.warning('%s\n [user]: %s\n [tweet]: %s', 'FALSE->has already replied', tweet_obj.get_user_screenname(), tweet_obj.get_tweet_text())
            continue

        # フォロワーのツイートでない場合
        if not tweet_obj.is_reply_from_follower():
            logging.warning('%s\n [user]: %s\n [tweet]: %s', 'FALSE->not follwer', tweet_obj.get_user_screenname(), tweet_obj.get_tweet_text())
            continue

        # 正常系(リプライを行う)
        REPLY_TEXT = '今日のスケジュールは...テスト中'
        tweet_obj.reply(REPLY_TEXT)
        replied_user_list.append(user_id)
        logging.info('%s\n [user]: %s\n [tweet]: %s', 'SUCCESS', tweet_obj.get_user_screenname(), tweet_obj.get_tweet_text())