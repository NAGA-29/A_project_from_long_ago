import mysql.connector as mydb
from pprint import pprint

from pyasn1.type.univ import Boolean


class holo_sql:

    cur = None
    conn = None
        # コンストラクタの定義
    def __init__(self):
        global cur
        global conn
        # コネクションの作成
        conn = mydb.connect(
            host='localhost',
            port='8889',
            user='root',
            password='root',
            database='Hololive_Project'
        )

        # コネクションが切れた時に再接続してくれるよう設定
        conn.ping(reconnect=True)
        # 接続できているかどうか確認
        print(conn.is_connected())
        # DB操作用にカーソルを作成
        # cur = conn.cursor(buffered=True)
        cur = conn.cursor(buffered=True, dictionary=True)


    def dbClose(self):
        cur.close()
        conn.close()


    def dropTable(self ,table_name):
        cur.execute("DROP TABLE IF EXISTS `%(table_name)s`",{'table_name':table_name})


# ----------------------------------------------------------
# HoloLive Profile ----------------------------------------------------------
# ----------------------------------------------------------
    def createProfileTable(self):
        result = cur.execute("""CREATE TABLE IF NOT EXISTS `holo_profiles` (
            `id` BIGINT UNSIGNED PRIMARY KEY NOT NULL AUTO_INCREMENT,
            `holo_id` varchar(255)  CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL UNIQUE,
            `holo_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
            `profile_text` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
            `channel_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
            `channel_url` TEXT NOT NULL ,
            `twitter_account` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
            `twitter_url` TEXT NOT NULL ,
            `image1` TEXT NOT NULL,
            `image2` TEXT NOT NULL,
            `image3` TEXT NOT NULL,
            `image4` TEXT NOT NULL,
            `image_tag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
            `tw_arts_tag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
            `live_tag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL
            )""")

        conn.commit()

    def selectHolo(self,channel_id:str):
        try:
            cur.execute("SELECT * FROM holo_profiles WHERE channel_id = %(channel_id)s ORDER BY id DESC LIMIT 1;",
                        {'channel_id':channel_id}
                        )
            result = cur.fetchall()
            if result:
                return result
            else:
                return False
        except Exception as err:
            conn.rollback()
            pprint('selectTubeSubHoloエラー:{}'.format(err))

    def selectOSHolo(self,channel_id:str):
        try:
            cur.execute("SELECT * FROM holo_overseas_profiles WHERE channel_id = %(channel_id)s ORDER BY id DESC LIMIT 1;",
                        {'channel_id':channel_id}
                        )
            result = cur.fetchall()
            if result:
                return result
            else:
                return False
        except Exception as err:
            conn.rollback()
            pprint('selectOSHoloエラー:{}'.format(err))

    def selectFriendsHolo(self,channel_id:str):
        try:
            cur.execute("SELECT * FROM holo_friends_profiles WHERE channel_id = %(channel_id)s ORDER BY id DESC LIMIT 1;",
                        {'channel_id':channel_id}
                        )
            result = cur.fetchall()
            if result:
                return result
            else:
                return False
        except Exception as err:
            conn.rollback()
            pprint('selectFriendsHoloエラー:{}'.format(err))


    def insert_HoloJP_ProfileTable(self,channelID:str,infoList:list):
        try:
            cur.execute("UPDATE holo_profiles SET youtube_subscriber = %(subscriber)s, youtube_videoCount = %(videoCount)s, youtube_viewCount = %(viewCount)s where channel_id = %(channel_id)s;",
                        {'channel_id': channelID, 'subscriber': infoList[0], 'videoCount': infoList[1], 'viewCount': infoList[2],}
            )
            conn.commit()
            return True
        except Exception as err:
            pprint(err)
            conn.rollback()
            return False
        
    def insert_HoloOS_ProfileTable(self,channelID:str,infoList:list):
        try:
            cur.execute("UPDATE holo_overseas_profiles SET youtube_subscriber = %(subscriber)s, youtube_videoCount = %(videoCount)s, youtube_viewCount = %(viewCount)s where channel_id = %(channel_id)s;",
                        {'channel_id': channelID, 'subscriber': infoList[0], 'videoCount': infoList[1], 'viewCount': infoList[2],}
            )
            conn.commit()
            return True
        except Exception as err:
            pprint(err)
            conn.rollback()
            return False

    def insert_HoloFri_ProfileTable(self,channelID:str,infoList:list):
        try:
            cur.execute("UPDATE holo_friends_profiles SET youtube_subscriber = %(subscriber)s, youtube_videoCount = %(videoCount)s, youtube_viewCount = %(viewCount)s where channel_id = %(channel_id)s;",
                        {'channel_id': channelID, 'subscriber': infoList[0], 'videoCount': infoList[1], 'viewCount': infoList[2],}
            )
            conn.commit()
            return True
        except Exception as err:
            pprint(err)
            conn.rollback()
            return False

    def insert_HoloJP_ProfileTable_tw(self,channelID:str,follower:int):
        try:
            cur.execute("UPDATE holo_profiles SET twitter_subscriber = %(twitter_subscriber)s where channel_id = %(channel_id)s;",
                        {'channel_id': channelID, 'twitter_subscriber': follower, }
            )
            conn.commit()
            return True
        except Exception as err:
            pprint(err)
            conn.rollback()
            return False
        
    def insert_HoloOS_ProfileTable_tw(self,channelID:str,follower:int):
        try:
            cur.execute("UPDATE holo_overseas_profiles SET twitter_subscriber = %(twitter_subscriber)s where channel_id = %(channel_id)s;",
                        {'channel_id': channelID, 'twitter_subscriber': follower, }
            )
            conn.commit()
            return True
        except Exception as err:
            pprint(err)
            conn.rollback()
            return False

    def insert_HoloFri_ProfileTable_tw(self,channelID:str,follower:int):
        try:
            cur.execute("UPDATE holo_friends_profiles SET twitter_subscriber = %(twitter_subscriber)s where channel_id = %(channel_id)s;",
                        {'channel_id': channelID, 'twitter_subscriber': follower,}
            )
            conn.commit()
            return True
        except Exception as err:
            pprint(err)
            conn.rollback()
            return False

# rss_datas RSS data ----------------------------------------------------------
    def createRssTable(self):
        result = cur.execute("""CREATE TABLE IF NOT EXISTS `rss_datas` (
            `id` BIGINT UNSIGNED PRIMARY KEY NOT NULL AUTO_INCREMENT,
            `name` varchar(255)  CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL ,
            `title` varchar(255)  CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL ,
            `video_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL UNIQUE,
            `channel_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
            `url` TEXT NOT NULL ,
            `uploaded_at` DATETIME NOT NULL,
            `scheduled_start_time_at` DATETIME DEFAULT NULL,
            `actual_start_time_at` DATETIME DEFAULT NULL,
            `actual_end_time_at` DATETIME DEFAULT NULL,
            `image` TEXT NOT NULL
            )""")

        conn.commit()
            
    def searchVideoIdFromRss(self,values):
        cur.execute("SELECT * FROM rss_datas WHERE video_id = %(video_id)s ORDER BY id DESC LIMIT 1;",
                    {'video_id':values['yt_videoid']}
                    )
        result = cur.fetchall()

        # video_idが存在する(既存)
        if result:
            return result
        # video_idが存在しない（新規）
        else:
            return False

    def insertTable(self,HoloName,values):
        try:
            cur.execute("INSERT INTO rss_datas VALUES(0,%(name)s,%(title)s,%(video_id)s,%(channel_id)s,%(url)s,%(uploaded_at)s,%(scheduled_start_time_at)s,%(actual_start_time_at)s,%(actual_end_time_at)s,%(image)s)", 
                    {'name': HoloName,'title': values[0], 'video_id': values[1], 'channel_id':values[2], 'url':values[3],'uploaded_at':values[4],'image':values[5],'scheduled_start_time_at':values[6],'actual_start_time_at':None,'actual_end_time_at':None}
                    )
            conn.commit()
        except Exception as e:
            pprint(e)


    def updateTitle(self,values):
        cur.execute("UPDATE rss_datas SET title = %(title)s where video_id = %(video_id)s;",
                    {'title': values[0], 'video_id': values[1]}
                )
        conn.commit() 

    def updateImage(self,values): 
        cur.execute("UPDATE rss_datas SET image = %(image)s where video_id = %(video_id)s;", 
                    {'image': values[5], 'video_id': values[1]} 
        )
        conn.commit() 

    def update2Items(self,values):
        cur.execute("UPDATE rss_datas SET title = %(title)s, image = %(image)s where video_id = %(video_id)s;",
                    {'title': values[0], 'image': values[5], 'video_id': values[1]}
        )
        conn.commit()

# artstable、twitter　tag検索----------------------------------------------------------
    def createArtsTable(self):
        result = cur.execute("""CREATE TABLE IF NOT EXISTS `arts` (
            `id` BIGINT UNSIGNED PRIMARY KEY NOT NULL AUTO_INCREMENT,
            `name` varchar(255)  CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL ,
            `tag` varchar(255)  CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL ,
            `tweet_id` BIGINT UNSIGNED NOT NULL UNIQUE,
            `text` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL ,
            `favorite` BIGINT UNSIGNED NOT NULL,
            `retweet` BIGINT UNSIGNED NOT NULL,
            `file_name1` varchar(255)  CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT NULL,
            `file_name2` varchar(255)  CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
            `file_name3` varchar(255)  CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
            `file_name4` varchar(255)  CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
            `creator_path` varchar(255)  CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT NULL,
            `uploadJST` DATETIME NOT NULL,
            `url` TEXT NOT NULL
            )""")
            
    def searchAll(self):
        cur.execute("SELECT * FROM arts ;")
        result = cur.fetchall()
        return result

    def searchArtsById(self, arts_id):
        cur.execute("SELECT * FROM arts WHERE id = %(id)s ORDER BY id DESC LIMIT 1;",
                    {'id': arts_id}
                    )
        result = cur.fetchall()

        # video_idが存在する(既存)
        if result:
            return result
        # video_idが存在しない（新規）
        else:
            return False

    def searchTweetId(self, value):
        cur.execute("SELECT * FROM arts WHERE tweet_id = %(tweet_id)s ORDER BY id DESC LIMIT 1;",
                    {'tweet_id':value}
                    )
        result = cur.fetchall()

        # video_idが存在する(既存)
        if result:
            return result
        # video_idが存在しない（新規）
        else:
            return False

    def insertArtsTable(self,HoloName,hTag,values):
        try:
            pprint(HoloName)
            cur.execute("INSERT INTO arts VALUES(0,%(name)s,%(tag)s,%(tweet_id)s,%(text)s,%(favorite)s,%(retweet)s,%(file_name1)s,null,null,null,%(creator_path)s,%(uploadJST)s,%(url)s)", 
                    {'name': HoloName,'tag': hTag, 'tweet_id': values[0][0], 'text':values[0][2], 
                    'favorite':values[0][3],'retweet':values[0][4],'file_name1':values[0][5],'creator_path':values[0][6],'uploadJST':values[0][1],'url':values[0][7]})
            conn.commit()
        except IndexError as e:
            conn.rollback()
            pprint(e)


    def updateArtsFavorite(self,tweet_id,favorite): 
        cur.execute("UPDATE arts SET favorite = %(favorite)s where tweet_id = %(tweet_id)s;", 
                    {'favorite': favorite, 'tweet_id': tweet_id} 
        )
        conn.commit() 

    def updateArtsRetweet(self,tweet_id,retweet):
        cur.execute("UPDATE arts SET retweet = %(retweet)s where tweet_id = %(tweet_id)s;",
                    {'retweet': retweet, 'tweet_id': tweet_id}
        )
        conn.commit()

    def updateArtsImage(self,tweet_id,file_name,num):
        cur.execute("UPDATE arts SET file_name%(num)s = %(file_name)s where tweet_id = %(tweet_id)s;",
                    {'num': num, 'file_name': file_name, 'tweet_id': tweet_id}
        )
        conn.commit()


# ----------------------------------------------------------
# keep_watchs Table----------------------------------------------------------
# ----------------------------------------------------------
    """
    liveStreamingDetails.actualStartTime　（ライブ開始時間）
    liveStreamingDetails.scheduledStartTime　（ライブ開始予定時間）
    liveStreamingDetails.actualEndTime　（ライブ終了時間）
    liveStreamingDetails.concurrentViewers　（リアルタイム視聴者数）
    liveStreamingDetails.activeLiveChatId　（チャット取得用ID）
    """
    def createKeepWatchTable(self):
        result = cur.execute("""CREATE TABLE IF NOT EXISTS `keep_watchs` (
            `id` BIGINT UNSIGNED PRIMARY KEY NOT NULL AUTO_INCREMENT,
            `video_id` varchar(255)  CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL UNIQUE,
            `holo_name` varchar(255)  CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL ,
            `title` varchar(255)  CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL ,
            `channel_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
            `channel_url` TEXT NOT NULL SET utf8mb4 COLLATE utf8mb4_bin,
            `uploaded_at` DATETIME NOT NULL,
            `scheduled_start_time_at` DATETIME DEFAULT NULL,
            `actual_start_time_at` DATETIME DEFAULT NULL,
            `concurrent_viewers` INT UNSIGNED DEFAULT NULL,
            `active_live_chat_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin ,
            `image_L` TEXT SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
            `image_default` TEXT SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
            `status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
            )""")
        conn.commit()

    def insertKeepWatchTable(self,values):
        try:
            cur.execute("INSERT INTO keep_watchs VALUES(0,%(video_id)s,%(holo_name)s,%(belongs)s,%(title)s,%(channel_id)s,%(channel_url)s,%(uploaded_at)s,%(scheduled_start_time_at)s,%(actual_start_time_at)s,%(concurrent_viewers)s,%(active_live_chat_id)s,%(image_L)s,%(image_default)s,%(status)s)", 
                    {'holo_name': values[0], 'belongs': values[24], 'title': values[1],'video_id': values[2], 'channel_id': values[3], 'channel_url': values[4], 'uploaded_at': values[11], 
                    'scheduled_start_time_at': values[12], 'actual_start_time_at': values[13], 'concurrent_viewers': values[15],
                    'active_live_chat_id': values[16], 'image_L': values[17], 'image_default': values[21], 'status': values[22] })
            conn.commit()
        except Exception as err:
            conn.rollback()
            pprint('insertKeepWatchTable:{}'.format(err))

    def updateKeepWatchTable(self,values):
        try:
            cur.execute("UPDATE keep_watchs SET scheduled_start_time_at = %(scheduled_start_time_at)s, actual_start_time_at = %(actual_start_time_at)s, concurrent_viewers = %(concurrent_viewers)s, active_live_chat_id = %(active_live_chat_id)s, status = %(status)s where video_id = %(video_id)s ", 
                    {'video_id': values[0][0], 
                    'scheduled_start_time_at': values[0][1], 'actual_start_time_at': values[0][2], 
                    'actual_end_time_at': values[0][3], 'concurrent_viewers': values[0][4], 'active_live_chat_id': values[0][5], 'status': values[0][6] })
            conn.commit()
        except Exception as err:
            conn.rollback()
            pprint('updateKeepWatchTableメソッドエラー:{}'.format(err))

    def update_schedule_keep_watch(self,video_id, schedule_start_time_at):
        try:
            cur.execute("UPDATE keep_watchs SET scheduled_start_time_at = %(scheduled_start_time_at)s where video_id = %(video_id)s ", 
                    {'video_id': video_id, 'scheduled_start_time_at': schedule_start_time_at})
            conn.commit()
            return True
        except Exception as err:
            conn.rollback()
            pprint(f'update_schedule_keep_watchメソッドエラー:{err}')
            return False

    def deleteKeepWatchTable(self,video_id):
        cur.execute('DELETE FROM keep_watchs WHERE video_id = %(video_id)s',
            { 'video_id':video_id })
        conn.commit()

    def selectAllKeepWatchTable(self):
        cur.execute("SELECT * FROM keep_watchs ;")
        result = cur.fetchall()
        return result

    def select_belongs_keep_watch(self, target):
        cur.execute("SELECT * FROM keep_watchs where belongs = %(belongs)s ;"
                    ,{ 'belongs': target })
        result = cur.fetchall()
        return result

    def selectTodayKeepWatchTable(self, target):
        cur.execute("SELECT * FROM keep_watchs where belongs = %(belongs)s AND DATE(scheduled_start_time_at) = CURDATE() ORDER BY scheduled_start_time_at ASC;"
                    ,{ 'belongs': target })
        result = cur.fetchall()
        return result

    def selectTomorrow_KeepWatch(self, target):
        cur.execute("SELECT * FROM keep_watchs where belongs = %(belongs)s AND DATE(scheduled_start_time_at) = DATE_ADD(CURDATE(), INTERVAL 1 DAY) ORDER BY scheduled_start_time_at ASC;"
                    ,{ 'belongs': target })
        result = cur.fetchall()
        return result

    def one_year_ago_TubeTable(self):
        cur.execute("SELECT * FROM youtube_videos where DATE(scheduled_start_time_at) =  DATE_SUB(CURDATE(), INTERVAL 1 YEAR);")
                    # ,{ 'belongs': target })
        result = cur.fetchall()
        return result

# ----------------------------------------------------------
# now_live_keep_watchs Table----------------------------------------------------------
# ----------------------------------------------------------
    def insertLiveKeepWatchTable(self,values:dict,live_data:list)->Boolean:
        try:
            cur.execute("INSERT INTO now_live_keep_watchs VALUES(0,%(video_id)s,%(holo_name)s,%(title)s,%(channel_id)s,%(channel_url)s,%(uploaded_at)s,%(scheduled_start_time_at)s,%(actual_start_time_at)s,%(concurrent_viewers)s,%(active_live_chat_id)s,%(image_L)s,%(image_default)s,%(notification_last_time_at)s,%(compared_point)s,%(status)s)", 
                {'holo_name': values['holo_name'], 'title': live_data[0][7],'video_id': values['video_id'], 'channel_id': values['channel_id'], 'channel_url': values['channel_url'], 'uploaded_at': values['uploaded_at'], 
                'scheduled_start_time_at': live_data[0][1], 'actual_start_time_at': live_data[0][2], 'concurrent_viewers': live_data[0][4],
                'active_live_chat_id': live_data[0][5], 'image_L': values['image_L'], 'image_default': values['image_default'], 
                'notification_last_time_at': live_data[0][2], 'compared_point': 0, 'status': live_data[0][6] })
            conn.commit()
            return True
        except Exception as err:
            conn.rollback()
            pprint('insertLiveKeepWatchTableメソッドエラー:{}'.format(err))
            pprint(values)
            pprint(live_data)
            return False

    def insertLiveKeepWatchTable_test(self,values:dict,live_data:list)->Boolean:
        try:
            cur.execute("INSERT INTO now_live_keep_watchs VALUES(0,%(video_id)s,%(holo_name)s,%(belongs)s,%(title)s,%(channel_id)s,%(channel_url)s,%(uploaded_at)s,%(scheduled_start_time_at)s,%(actual_start_time_at)s,%(concurrent_viewers)s,%(active_live_chat_id)s,%(image_L)s,%(image_default)s,%(notification_last_time_at)s,%(compared_point)s,%(status)s)", 
                {'holo_name': values['holo_name'], 'belongs': values['belongs'], 'title': live_data[0][7],'video_id': values['video_id'], 'channel_id': values['channel_id'], 'channel_url': values['channel_url'], 'uploaded_at': values['uploaded_at'], 
                'scheduled_start_time_at': live_data[0][1], 'actual_start_time_at': live_data[0][2], 'concurrent_viewers': live_data[0][4],
                'active_live_chat_id': live_data[0][5], 'image_L': values['image_L'], 'image_default': values['image_default'], 
                'notification_last_time_at': '2020-01-01 00:00:00', 'compared_point': 0, 'status': live_data[0][6] })
                # 'notification_last_time_at': live_data[0][2],
            conn.commit()
            return True
        except Exception as err:
            conn.rollback()
            pprint('insertLiveKeepWatchTableメソッドエラー:{}'.format(err))
            pprint(values)
            pprint(live_data)
            return False

    # def selectAllLiveTable(self):
    #     cur.execute("SELECT * FROM now_live_keep_watchs ;")
    #     result = cur.fetchall()
    #     # データが存在する
    #     if result:
    #         return result
    #     # データが存在しない
    #     else:
    #         return False

    def selectAllLiveTable(self, Belongs):
        cur.execute("SELECT * FROM now_live_keep_watchs WHERE belongs = %(belongs)s;"
                    ,{'belongs': Belongs })
        result = cur.fetchall()
        # データが存在する
        if result:
            return result
        # データが存在しない
        else:
            return False

    def updateViewersLiveTable(self,values):
        try:
            cur.execute("UPDATE now_live_keep_watchs SET concurrent_viewers = %(concurrent_viewers)s where video_id = %(video_id)s ", 
                    {'video_id': values[0][0], 'concurrent_viewers': values[0][4] })
            conn.commit()
        except Exception as err:
            conn.rollback()
            pprint('updateLiveTableメソッドエラー:{}'.format(err))

    '''
    @TODO このメソッドは無駄にスペースを取っている 代替え案が必要
    '''
    def updateTitleLiveTable(self,values):
        try:
            cur.execute("UPDATE now_live_keep_watchs SET title = %(title)s where video_id = %(video_id)s ", 
                    {'video_id': values[0][0], 'title': values[0][7] })
            conn.commit()
        except Exception as err:
            conn.rollback()
            pprint('updateTitleLiveTableエラー:{}'.format(err))

    def updateNotificationLiveTable(self,video_id, time, compared_point):
        try:
            cur.execute("UPDATE now_live_keep_watchs SET notification_last_time_at = %(notification_last_time_at)s, compared_point = %(compared_point)s where video_id = %(video_id)s ", 
                    {'video_id': video_id, 'notification_last_time_at': time,  'compared_point': compared_point})
            conn.commit()
        except Exception as err:
            conn.rollback()
            pprint('updateNotificationLiveTableメソッドエラー:{}'.format(err))

    def deletelLiveTable(self,video_id):
        cur.execute('DELETE FROM now_live_keep_watchs WHERE video_id = %(video_id)s',
            { 'video_id':video_id })
        conn.commit()

    def select(self, video_id):
        cur.execute("SELECT * FROM now_live_keep_watchs where video_id = %(video_id)s ;",{ 'video_id':video_id })
        result = cur.fetchall()

        # データが存在する
        if result:
            return result
        # データが存在しない
        else:
            return False

    # def select2ndAllKeepWatchTable(self):
    #     cur.execute("SELECT * FROM now_live_keep_watchs ;")
    #     result = cur.fetchall()

    #     # データが存在する
    #     if result:
    #         return result
    #     # データが存在しない
    #     else:
    #         return False


# ----------------------------------------------------------
# Youtube_videos Table----------------------------------------------------------
# ----------------------------------------------------------
    def createYoutubeVideoTable(self):
        result = cur.execute("""CREATE TABLE IF NOT EXISTS `youtube_videos` (
            `id` BIGINT UNSIGNED PRIMARY KEY NOT NULL AUTO_INCREMENT,
            `holo_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
            `title` varchar(255)  CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
            `video_id` varchar(255)  CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL UNIQUE,
            `channel_id` varchar(255)  CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
            `channel_url` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
            `view_count` int(11) unsigned NOT NULL,
            `like_count` int(11) unsigned NOT NULL,
            `dislike_count` int(11) unsigned NOT NULL,
            `comment_count` int(11) unsigned NOT NULL,
            `game_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
            `tag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
            `uploaded_at` datetime DEFAULT NULL,
            `scheduled_start_time_at` datetime DEFAULT NULL,
            `actual_start_time_at` datetime DEFAULT NULL,
            `actual_end_time_at` datetime DEFAULT NULL,
            `max_concurrent_viewers` int(11) unsigned DEFAULT NULL,
            `active_live_chat_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
            `image_L` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
            `image_M` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
            `image_S` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
            `image_XS` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
            `image_Default` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
            `status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL
            `notification_last_time_at` datetime DEFAULT `2000-01-01 00:00:00`,
            )""")
        conn.commit()


    def searchVideoIdFromYoutubeVideoTable(self,values):
        cur.execute("SELECT * FROM youtube_videos WHERE video_id = %(video_id)s ORDER BY id DESC LIMIT 1;",
                    {'video_id': values['yt_videoid']}
                    )
        result = cur.fetchall()

        # video_idが存在する(既存)
        if result:
            return result
        # video_idが存在しない（新規）
        else:
            return False

    def searchVideoIdFromYoutubeVideoTable_test(self,video_id):
        cur.execute("SELECT * FROM youtube_videos WHERE video_id = %(video_id)s ORDER BY id DESC LIMIT 1;",
                    {'video_id': video_id}
                    )
        result = cur.fetchall()

        # video_idが存在する(既存)
        if result:
            return result
        # video_idが存在しない（新規）
        else:
            return False


    def selectVideoIdYoutubeVideoTable(self,video_id):
        cur.execute("SELECT * FROM youtube_videos WHERE video_id = %(video_id)s ORDER BY id DESC LIMIT 1;",
                    {'video_id': video_id}
                    )
        result = cur.fetchall()

        # video_idが存在する(既存)
        if result:
            return result
        # video_idが存在しない（新規）
        else:
            return False


    def insertYoutubeVideoTable_R(self,video_info:list):
        try:
            cur.execute("INSERT INTO youtube_videos VALUES(0,%(holo_name)s,%(title)s,%(video_id)s,%(channel_id)s,%(channel_url)s,%(view_count)s,%(like_count)s,%(dislike_count)s,%(comment_count)s,%(game_name)s,%(tag)s,%(uploaded_at)s,%(scheduled_start_time_at)s,%(actual_start_time_at)s,%(actual_end_time_at)s,%(max_concurrent_viewers)s,%(active_live_chat_id)s,%(image_L)s,%(image_M)s,%(image_S)s,%(image_XS)s,%(image_Default)s,%(status)s,%(notification_last_time_at)s)",
                    {'holo_name':video_info[0], 'title':video_info[1], 'video_id':video_info[2], 'channel_id':video_info[3], 'channel_url': video_info[4],
                    'view_count': video_info[5], 'like_count': video_info[6], 'dislike_count': video_info[7], 'comment_count': video_info[8],'game_name': video_info[9], 'tag': video_info[10],
                    'uploaded_at': video_info[11],'scheduled_start_time_at': video_info[12], 'actual_start_time_at': video_info[13], 'actual_end_time_at': video_info[14],
                    'max_concurrent_viewers': video_info[15], 'active_live_chat_id': video_info[16], 
                    'image_L': video_info[17], 'image_M': video_info[18], 'image_S': video_info[19], 'image_XS': video_info[20], 'image_Default': video_info[21],
                    'status': video_info[22], 'notification_last_time_at': video_info[23] })
            conn.commit()
        except Exception as err:
            conn.rollback()
            pprint('insertYoutubeVideoTable_Rメソッドエラー:{}'.format(err))


    def updateTitleYoutubeVideoTable(self,values):
        cur.execute("UPDATE youtube_videos SET title = %(title)s, notification_last_time_at = %(notification_last_time_at)s where video_id = %(video_id)s;",
                    {'title': values[0], 'video_id': values[1], 'notification_last_time_at': values[7]}
                )
        conn.commit() 


    def updateTimeYoutubeVideoTable(self,values):
        try:
            cur.execute("UPDATE youtube_videos SET scheduled_start_time_at = %(scheduled_start_time_at)s, actual_start_time_at = %(actual_start_time_at)s, actual_end_time_at = %(actual_end_time_at)s, active_live_chat_id = %(active_live_chat_id)s, status = %(status)s where video_id = %(video_id)s ", 
                    {'video_id': values[0][0], 
                    'scheduled_start_time_at': values[0][1], 'actual_start_time_at': values[0][2], 
                    'actual_end_time_at': values[0][3], 'active_live_chat_id': values[0][5], 'status': values[0][6] })
            conn.commit()
            return True
        except Exception as err:
            conn.rollback()
            pprint('updateTimeYoutubeVideoTableメソッドエラー:{}'.format(err))
            return False


    def update_schedule_youtube_videos_table(self, video_id, scheduled_start_time_at):
        try:
            cur.execute("UPDATE youtube_videos SET scheduled_start_time_at = %(scheduled_start_time_at)s where video_id = %(video_id)s ", 
                    {'video_id': video_id, 'scheduled_start_time_at': scheduled_start_time_at})
            conn.commit()
            return True
        except Exception as err:
            conn.rollback()
            pprint(f'update_schedule_youtube_videos_tableメソッドエラー:{err}')
            return False


    def updateMAXViewersYoutubeVideoTable(self,values):
        try:
            cur.execute("UPDATE youtube_videos SET max_concurrent_viewers = %(max_concurrent_viewers)s where video_id = %(video_id)s ", 
                    {'video_id': values[0][0], 'max_concurrent_viewers': values[0][4] })
            conn.commit()
            return True
        except Exception as err:
            conn.rollback()
            pprint('updateMAXViewersYoutubeVideoTableメソッドエラー:{}'.format(err))
            return False


    def updateImage_YoutubeVideoTable_R(self,values): 
        cur.execute("UPDATE youtube_videos SET image = %(image)s where video_id = %(video_id)s;", 
                    {'image': values[5], 'video_id': values[1]} 
        )
        conn.commit() 


    def update2Items_YoutubeVideoTable_R(self,values):
        cur.execute("UPDATE youtube_videos SET title = %(title)s, image = %(image)s where video_id = %(video_id)s;",
                    {'title': values[0], 'image': values[5], 'video_id': values[1]})
        conn.commit()


    def updateScrapingYoutubeVideoTable(self,values):
        cur.execute("UPDATE youtube_videos SET title = %(title)s, view_count = %(view_count)s, like_count = %(like_count)s, dislike_count = %(dislike_count)s, comment_count = %(comment_count)s, image_L = %(image_L)s, image_M = %(image_M)s, image_S = %(image_S)s, image_XS = %(image_XS)s, image_Default = %(image_Default)s  where video_id = %(video_id)s;",
                    {'video_id':values[0], 'title': values[1], 'view_count': values[2], 'like_count': values[3], 
                    'dislike_count': values[4], 'comment_count': values[5], 'image_L': values[8], 'image_M': values[9],
                    'image_S': values[10], 'image_XS': values[11], 'image_Default': values[12]})
        conn.commit()
# ----------------------------------------------------------
# other_videos Table----------------------------------------------------------
# ----------------------------------------------------------
    def search_VideoId_from_othervideos(self,values):
        try:
            cur.execute("SELECT * FROM other_videos WHERE video_id = %(video_id)s ORDER BY id DESC LIMIT 1;",
                        {'video_id': values['yt_videoid']}
                        )
            result = cur.fetchall()
            # video_idが存在する(既存)
            if result:
                return result
        except Exception as err:
            # video_idが存在しない（新規）
            pprint(err)
            return False

    def insertOtherVideoTable(self,video_info:list):
        try:
            cur.execute("INSERT INTO other_videos VALUES(0,%(holo_name)s,%(title)s,%(video_id)s,%(channel_id)s,%(channel_url)s,%(view_count)s,%(like_count)s,%(dislike_count)s,%(comment_count)s,%(game_name)s,%(tag)s,%(uploaded_at)s,%(scheduled_start_time_at)s,%(actual_start_time_at)s,%(actual_end_time_at)s,%(max_concurrent_viewers)s,%(active_live_chat_id)s,%(image_L)s,%(image_M)s,%(image_S)s,%(image_XS)s,%(image_Default)s,%(status)s,%(notification_last_time_at)s)",
                    {'holo_name':video_info[0], 'title':video_info[1], 'video_id':video_info[2], 'channel_id':video_info[3], 'channel_url': video_info[4],
                    'view_count': video_info[5], 'like_count': video_info[6], 'dislike_count': video_info[7], 'comment_count': video_info[8],'game_name': video_info[9], 'tag': video_info[10],
                    'uploaded_at': video_info[11],'scheduled_start_time_at': video_info[12], 'actual_start_time_at': video_info[13], 'actual_end_time_at': video_info[14],
                    'max_concurrent_viewers': video_info[15], 'active_live_chat_id': video_info[16], 
                    'image_L': video_info[17], 'image_M': video_info[18], 'image_S': video_info[19], 'image_XS': video_info[20], 'image_Default': video_info[21],
                    'status': video_info[22], 'notification_last_time_at': video_info[23] })
            conn.commit()
        except Exception as err:
            conn.rollback()
            pprint('insertYoutubeVideoTable_Rメソッドエラー:{}'.format(err))

# ----------------------------------------------------------
# holo_datas Table----------------------------------------------------------
# ----------------------------------------------------------

    def insertHoloData(self,data_list):
        try:
            cur.execute("INSERT INTO holo_datas VALUES(0,%(all_youtube_subscriber)s,%(all_youtube_videoCount)s,%(all_youtube_viewCount)s,%(updated_at)s)",
                    {'all_youtube_subscriber':data_list[0][0], 'all_youtube_videoCount':data_list[0][1], 'all_youtube_viewCount': data_list[0][2], 'updated_at': data_list[0][3],})
            conn.commit()
        except Exception as err:
            conn.rollback()
            pprint('insertHoloDataメソッドエラー:{}'.format(err))
            # raise err


# ----------------------------------------------------------
# event_schedules Table----------------------------------------------------------
# ----------------------------------------------------------
    def selectEventSchedulesTable(self,status='upcoming'):
        cur.execute("SELECT * FROM event_schedules WHERE status = %(status)s ;",
                    {'status': status}
                    )
        result = cur.fetchall()

        if result:
            return result
        else:
            return False

    def updateStatus_SchedulesTable(self,event_id,status='end'):
        try:
            cur.execute("UPDATE event_schedules SET status = %(status)s where event_id = %(event_id)s;",
                        {'event_id':event_id, 'status':status,})
            conn.commit()
        except Exception as err:
            conn.rollback()
            pprint('updateStatus_SchedulesTable:{}'.format(err))
            # raise err



# ----------------------------------------------------------
# DB修正用 一時的に使用----------------------------------------------------------
# ----------------------------------------------------------

    def selectArtTable(self,id):
        cur.execute("SELECT * FROM arts WHERE id = %(id)s ORDER BY id DESC LIMIT 1;",
                    {'id': id}
                    )
        result = cur.fetchall()

        # video_idが存在する(既存)
        if result:
            return result
        # video_idが存在しない（新規）
        else:
            return False

    def updateArts(self,id,creator_path,url_list):
        cur.execute("UPDATE arts SET  creator_path = %(creator_path)s, file_name1 = %(file_name1)s, file_name2 = %(file_name2)s, file_name3 = %(file_name3)s, file_name4 = %(file_name4)s where id = %(id)s;",
                    {'id':id, 'creator_path': creator_path, 'file_name1': url_list[0], 'file_name2': url_list[1], 'file_name3': url_list[2], 'file_name4': url_list[3],})
        conn.commit()


        # conn.close()
        # # プレースホルダを利用して挿入
        # cur.execute("INSERT INTO rss_datas VALUES (2, 'ETH', %s)", (5000, ))
        # cur.execute("INSERT INTO rss_datas VALUES (%s, %s, %s)", (3 ,'XEM', 2500))
        # cur.execute("INSERT INTO rss_datas VALUES (%(id)s, %(name)s, %(price)s)", {'id': 4, 'name': 'XRP', 'price': 1000})

        # # executemanyで複数データを一度に挿入
        # records = [
        #     (5, 'MONA', 3000),
        #     (6, 'XP', 1000),
        # ]
        # cur.executemany("INSERT INTO rss_datas VALUES (%s, %s, %s)", records)


        # cur.close()
        # conn.commit()
        # conn.close()
    '''
    スクレイピング用メソッド
    param video_id
    retrun Boolean
    '''
    def searchVideoIdYoutubeVideoTable(self,video_id):
        cur.execute("SELECT * FROM youtube_videos WHERE video_id = %(video_id)s ORDER BY id DESC LIMIT 1;",
                    {'video_id': video_id}
                    )
        result = cur.fetchall()

        # video_idが存在する(既存)
        if result:
            return result
        # video_idが存在しない（新規）
        else:
            return False


    def updateYoutubeVideoTable(self,HoloName,values):
        cur.execute("UPDATE youtube_videos SET where video_id = VALUES(0,%(watch_id)s,%(video_id)s,%(name)s,%(holo_id)s,%(scheduled_start_time)s,%(actual_start_time)s,%(concurrent_viewers)s,%(active_live_chat_id)s,%(on_air)s)", 
                {'watch_id': values[0][0], 'video_id': values[0][1], 'name': HoloName, 
                'holo_id': values[0][2], 'scheduled_start_time': values[0][3], 'actual_start_time': values[0][4], 
                'concurrent_viewers': values[0][5], 'active_live_chat_id': values[0][6],'on_air': values[0][7] })
        conn.commit()


    def insertYoutubeVideoTable(self,video_info:list):
        cur.execute("INSERT INTO youtube_videos VALUES(0,%(holo_name)s,%(title)s,%(video_id)s,%(channel_id)s,%(channel_url)s,%(view_count)s,%(like_count)s,%(dislike_count)s,%(comment_count)s,%(game_name)s,%(tag)s,%(uploaded_at)s,%(scheduled_start_time_at)s,%(actual_start_time_at)s,%(actual_end_time_at)s,%(max_concurrent_viewers)s,%(active_live_chat_id)s,%(image_L)s,%(image_M)s,%(image_S)s,%(image_XS)s,%(image_Default)s,%(status)s,%(notification_last_time_at)s)",
                {'holo_name':video_info[0][0], 'title':video_info[0][1], 'video_id':video_info[0][2], 'channel_id':video_info[0][3], 'channel_url': video_info[0][4],
                'view_count': video_info[0][5], 'like_count': video_info[0][6], 'dislike_count': video_info[0][7], 'comment_count': video_info[0][8],'game_name': video_info[0][9], 'tag': video_info[0][10],
                'uploaded_at': video_info[0][11],'scheduled_start_time_at': video_info[0][12], 'actual_start_time_at': video_info[0][13], 'actual_end_time_at': video_info[0][14],
                'max_concurrent_viewers': video_info[0][15], 'active_live_chat_id': video_info[0][16], 
                'image_L': video_info[0][17], 'image_M': video_info[0][18], 'image_S': video_info[0][19], 'image_XS': video_info[0][20], 'image_Default': video_info[0][21],
                'status': video_info[0][22], 'notification_last_time_at': '2020-01-01 00:00:00' })
        conn.commit()