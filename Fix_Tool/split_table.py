'''
１つのテーブルからのりプロのデータのみ抽出し,
その元のテーブルからはのりプロのデータを削除しつつ、、別のテーブルに保存する
'''
import sys
from pprint import pprint 
'''
Origin Module
'''
# Userモデルの取得
from model.YoutubeVideo import YoutubeVideo
from model.YoutubeNoriproVideos import YoutubeNoriproVideos
from config import session
# sys.path.append('../')
# セッション変数の取得


Noripro_Channels = {
    'SHIGURE_UI_ch' : 'UCt30jJgChL8qeT9VPadidSw', #時雨うい
    'TAKUMA_ch' : 'UCCXME7oZmXB2VFHJbz5496A',     #熊谷タクマ
    'TAMAKI_ch' : 'UC8NZiqKx6fsDT3AVcMiVFyA',     #佃煮のりお
    'SHIRAYUKI_ch' : 'UCC0i9nECi4Gz7TU63xZwodg',  #白雪みしろ
    'MILK_ch' : 'UCJCzy0Fyrm0UhIrGQ7tHpjg',       #愛宮みるく
    'YUZURU_ch' : 'UCle1cz6rcyH0a-xoMYwLlAg',     #姫咲ゆずる
    'HOOZUKI_ch' : 'UCLyTXfCZtl7dyhta9Jg3pZg',    #鬼灯わらべ
    'YUMENO_ch' : 'UCH11P1Hq4PXdznyw1Hhr3qw',     #夢乃リリス
    'KURUMIZAWA_ch' : 'UCxrmkJf_X1Yhte_a4devFzA', #胡桃澤もも
    'OUMAKI_ch' : 'UCBAeKqEIugv69Q2GIgcH7oA',     #逢魔きらら
    'NIA_ch' : 'UCIRzELGzTVUOARi3Gwf1-yg',        #看谷にぃあ
}

if __name__ == '__main__':
    for key,ch_id in Noripro_Channels.items():
        # videos = session.query(YoutubeVideo.title).all()
        videos = session.query(YoutubeVideo).filter(YoutubeVideo.channel_id == ch_id ).all()
        # videos = session.query(YoutubeNoriproVideos.title).all()
        # pprint(videos.video_id)
        for video in videos:
            print(video.id)
            print(video.holo_name)
            print(video.video_id)
            print(video.channel_id)

            try:
                '''
                Select
                '''
                Insert = YoutubeNoriproVideos()
                # Insert.id = videos.id
                Insert.holo_name = video.holo_name 
                Insert.title = video.title 
                Insert.video_id = video.video_id
                Insert.channel_id = video.channel_id
                Insert.channel_url = video.channel_url
                Insert.view_count = video.view_count
                Insert.like_count = video.like_count
                Insert.dislike_count = video.dislike_count
                Insert.comment_count = video.comment_count
                Insert.game_name = video.game_name
                Insert.tag = video.tag 
                Insert.uploaded_at = video.uploaded_at
                Insert.scheduled_start_time_at = video.scheduled_start_time_at
                Insert.actual_start_time_at = video.actual_start_time_at
                Insert.actual_end_time_at = video.actual_end_time_at
                Insert.max_concurrent_viewers = video.max_concurrent_viewers
                Insert.active_live_chat_id = video.active_live_chat_id
                Insert.image_L = video.image_L
                Insert.image_M = video.image_M
                Insert.image_S = video.image_S
                Insert.image_XS = video.image_XS
                Insert.image_Default = video.image_Default
                Insert.status = video.status
                Insert.notification_last_time_at = video.notification_last_time_at
                session.add(Insert)
                session.commit()

                '''
                Delete
                '''
                # session.query(YoutubeVideo).filter(YoutubeVideo.video_id == video.video_id).delete()
                # session.commit()
            except Exception as e:
                pprint(e)
                break
