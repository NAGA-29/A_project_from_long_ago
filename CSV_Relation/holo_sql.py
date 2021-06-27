import mysql.connector as mydb
from pprint import pprint


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
            user='root',
            password='root',
            database='HololiveProject'
        )

        # コネクションが切れた時に再接続してくれるよう設定
        conn.ping(reconnect=True)
        # 接続できているかどうか確認
        print(conn.is_connected())
        # DB操作用にカーソルを作成
        cur = conn.cursor(buffered=True)


    def dbClose(self):
        cur.close()
        conn.close()


    def dropTable(self ,table_name):
        cur.execute("DROP TABLE IF EXISTS `%(table_name)s`",{'table_name':table_name})


# HoloLive Profile ----------------------------------------------------------
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

    def searchTweetId(self,value):
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
# keep_watches Table----------------------------------------------------------
# ----------------------------------------------------------
    """
    liveStreamingDetails.actualStartTime　（ライブ開始時間）
    liveStreamingDetails.scheduledStartTime　（ライブ開始予定時間）
    liveStreamingDetails.actualEndTime　（ライブ終了時間）
    liveStreamingDetails.concurrentViewers　（リアルタイム視聴者数）
    liveStreamingDetails.activeLiveChatId　（チャット取得用ID）
    """
    def createKeepWatchTable(self):
        result = cur.execute("""CREATE TABLE IF NOT EXISTS `keep_watches` (
            `id` BIGINT UNSIGNED PRIMARY KEY NOT NULL AUTO_INCREMENT,
            `name` varchar(255)  CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL ,
            `title` varchar(255)  CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL ,
            `video_id` varchar(255)  CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL UNIQUE,
            `channel_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
            `channel_url` TEXT NOT NULL SET utf8mb4 COLLATE utf8mb4_bin,
            `uploaded_at` DATETIME NOT NULL,
            `scheduled_start_time_at` DATETIME DEFAULT NULL,
            `actual_start_time_at` DATETIME DEFAULT NULL,
            `concurrent_viewers` INT UNSIGNED DEFAULT NULL,
            `active_live_chat_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin ,
            `image` TEXT SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
            `status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
            )""")
        conn.commit()

    def insert_FromRss_KeepWatchTable(self,HoloName,holo_id,values):
        cur.execute("INSERT INTO keep_watches VALUES(0,%(watch_id)s,%(video_id)s,%(name)s,%(holo_id)s,%(scheduled_start_time_at)s,%(actfive_live_chat_id)s,%(status)s)", 
                {'video_id': values[0][1], 'name': HoloName, 
                'holo_id': holo_id, 'scheduled_start_time_at': values[0][6],
                'active_live_chat_id': values[0][4],'status': values[0][5] })
        conn.commit()

    def updateKeepWatchTable(self,HoloName,values):
        cur.execute("UPDATE keep_watches SET where video_id = VALUES(0,%(watch_id)s,%(video_id)s,%(name)s,%(holo_id)s,%(scheduled_start_time)s,%(actual_start_time)s,%(concurrent_viewers)s,%(active_live_chat_id)s,%(on_air)s)", 
                {'watch_id': values[0][0], 'video_id': values[0][1], 'name': HoloName, 
                'holo_id': values[0][2], 'scheduled_start_time': values[0][3], 'actual_start_time': values[0][4], 
                'concurrent_viewers': values[0][5], 'active_live_chat_id': values[0][6],'on_air': values[0][7] })
        conn.commit()


    def searchFromHolo_Profile(self,values):
        cur.execute("SELECT * FROM holo_profiles WHERE video_id = %(video_id)s ORDER BY id DESC LIMIT 1;",
                    {'video_id':values['yt_videoid']}
                    )
        result = cur.fetchall()

        # video_idが存在する(既存)
        if result:
            return result
        # video_idが存在しない（新規）
        else:
            return False


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


    def insertYoutubeVideoTable(self,video_info:list):
        cur.execute("INSERT INTO youtube_videos VALUES(0,%(holo_name)s,%(title)s,%(video_id)s,%(channel_id)s,%(channel_url)s,%(view_count)s,%(like_count)s,%(dislike_count)s,%(comment_count)s,%(game_name)s,%(tag)s,%(uploaded_at)s,%(scheduled_start_time_at)s,%(actual_start_time_at)s,%(actual_end_time_at)s,%(max_concurrent_viewers)s,%(active_live_chat_id)s,%(image_L)s,%(image_M)s,%(image_S)s,%(image_XS)s,%(image_Default)s,%(status)s,%(notification_last_time_at)s)",
                {'holo_name':video_info[0][0], 'title':video_info[0][1], 'video_id':video_info[0][2], 'channel_id':video_info[0][3], 'channel_url': video_info[0][4],
                'view_count': video_info[0][5], 'like_count': video_info[0][6], 'dislike_count': video_info[0][7], 'comment_count': video_info[0][8],'game_name': video_info[0][9], 'tag': video_info[0][10],
                'uploaded_at': video_info[0][11],'scheduled_start_time_at': video_info[0][12], 'actual_start_time_at': video_info[0][13], 'actual_end_time_at': video_info[0][14],
                'max_concurrent_viewers': video_info[0][15], 'active_live_chat_id': video_info[0][16], 
                'image_L': video_info[0][17], 'image_M': video_info[0][18], 'image_S': video_info[0][19], 'image_XS': video_info[0][20], 'image_Default': video_info[0][21],
                'status': video_info[0][22], 'notification_last_time_at': '2020-01-01 00:00:00' })
        conn.commit()


    def updateYoutubeVideoTable(self,HoloName,values):
        cur.execute("UPDATE youtube_videos SET where video_id = VALUES(0,%(watch_id)s,%(video_id)s,%(name)s,%(holo_id)s,%(scheduled_start_time)s,%(actual_start_time)s,%(concurrent_viewers)s,%(active_live_chat_id)s,%(on_air)s)", 
                {'watch_id': values[0][0], 'video_id': values[0][1], 'name': HoloName, 
                'holo_id': values[0][2], 'scheduled_start_time': values[0][3], 'actual_start_time': values[0][4], 
                'concurrent_viewers': values[0][5], 'active_live_chat_id': values[0][6],'on_air': values[0][7] })
        conn.commit()

















# # images Table----------------------------------------------------------
#     def createImagesTable(self):
#         result = cur.execute("""CREATE TABLE IF NOT EXISTS `images` (
#             `id` BIGINT UNSIGNED PRIMARY KEY NOT NULL AUTO_INCREMENT,
#             `image_id` varchar(255)  CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL UNIQUE,
#             `producter` varchar(255)  CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL ,
#             `belongs_id` varchar(255)  CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL ,
#             `file_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL UNIQUE,
#             `uploaded` DATETIME NOT NULL,
#             `downloaded` DATETIME NOT NULL
#             )""")

#     def insertImageTable(self):
#         cur.execute("INSERT INTO images VALUES(0,%(name)s,%(tag)s,%(tweet_id)s,%(text)s,%(favorite)s,%(retweet)s,%(uploadJST)s,%(url)s)", 
#                 {'name': HoloName,'tag': hTag, 'tweet_id': values[0][0], 'text':values[0][2], 
#                 'favorite':values[0][3],'retweet':values[0][4],'uploadJST':values[0][1],'url':values[0][5]})
#         conn.commit()


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

    def updateScrapingYoutubeVideoTable(self,values):
        cur.execute("UPDATE youtube_videos SET title = %(title)s, view_count = %(view_count)s, like_count = %(like_count)s, dislike_count = %(dislike_count)s, comment_count = %(comment_count)s, image_L = %(image_L)s, image_M = %(image_M)s, image_S = %(image_S)s, image_XS = %(image_XS)s, image_Default = %(image_Default)s  where video_id = %(video_id)s;",
                    {'video_id': values[0][0], 'title': values[0][1], 'view_count': values[0][2], 'like_count': values[0][3], 
                    'dislike_count': values[0][4], 'comment_count': values[0][5], 'image_L': values[0][8], 'image_M': values[0][9],
                    'image_S': values[0][10], 'image_XS': values[0][11], 'image_Default': values[0][12]})
        conn.commit()