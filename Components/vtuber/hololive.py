import time
import datetime
from datetime import datetime as dt
import dateutil.parser
from pytz import timezone

from pprint import pprint

class Hololive:

    def __init__(self):
        pass

    @staticmethod
    def get_twitter_ids():
        ch_list = {
            # 運営
            'Hololive' : 'hololivetv',
            # 'HololiveEN' : 'UCotXwY6s8pWmuWd_snKYjhg',   #hololive EN
            # 'HololiveID' : 'UCfrWoRGlawPQDQxxeIDRP0Q',   #hololive ID
            # 'Cover' : 'cover_corp',
            'えーちゃん' : 'achan_UGA',
            # ホロライブ
            '桐生ココ' : 'kiryucoco',        #桐生ココ
            '星街すいせい' : 'suisei_hosimati',    #星街すいせい
            'ロボ子さん' : 'robocosan',     #'ロボ子さん'
            'アキ・ローゼンタール' : 'akirosenthal',    #'アキ・ローゼンタール'
            '大神ミオ' : 'ookamimio',     #'大神ミオ'
            '赤井はあと' : 'akaihaato',     #'赤井はあと'
            '不知火フレア' : 'shiranuiflare',     #'不知火フレア'
            '夏色まつり' : 'natsuiromatsuri',   #'夏色まつり'
            '宝鐘マリン' : 'houshoumarine',      #'宝鐘マリン' 
            '姫森ルーナ' : 'himemoriluna',       #'姫森ルーナ' 
            '白上フブキ' : 'shirakamifubuki',        #'白上フブキ' 
            '大空スバル' : 'oozorasubaru',      #'大空スバル'
            '百鬼あやめ' : 'nakiriayame',       #'百鬼あやめ'
            '猫又おかゆ' : 'nekomataokayu',      #'猫又おかゆ' 
            '潤羽るしあ' : 'uruharushia',       #'潤羽るしあ'
            '戌神ころね' : 'inugamikorone',     #'戌神ころね'
            '角巻わため' : 'tsunomakiwatame',        #'角巻わため' 
            '白銀ノエル' : 'shiroganenoel',     #'白銀ノエル'
            '兎田ぺこら' : 'usadapekora',       #'兎田ぺこら'
            'さくらみこ' : 'sakuramiko35',      #'さくらみこ'
            '紫咲シオン' : 'murasakishionch',       #'紫咲シオン'
            '湊あくあ' : 'minatoaqua',        #'湊あくあ'
            '常闇トワ' : 'tokoyamitowa',      #'常闇トワ'
            '夜空メル'  : 'yozoramel',      #'夜空メル' 
            '天音かなた' : 'amanekanatach',     #'天音かなた'
            '癒月ちょこ' : 'yuzukichococh',     #'癒月ちょこ'
            '癒月ちょこ(サブ)' : 'yuzukichococh',     #'癒月ちょこ'
            'ときのそら' : 'tokino_sora',       #'ときのそら'
            '雪花ラミィ' : 'yukihanalamy',     #雪花ラミィ
            '桃鈴ねね' : 'momosuzunene',     #桃鈴ねね
            '獅白ぼたん' : 'shishirobotan',        #獅白ぼたん
            # 'ALOE_tw' : 'manoaloe',     #魔乃アロエ
            '尾丸ポルカ' : 'omarupolka',      #尾丸ポルカ

            # イノナカミュージック
            'AZKi' : 'AZKi_VDiVA',     #'AZKI' 

            #ホロライブ　EN
            '森カリオペ' : 'moricalliope',    #森カリオペ モリ・カリオペ
            '小鳥遊キアラ' : 'takanashikiara',    #小鳥遊キアラ
            '一伊那尓栖' : 'ninomaeinanis',    #一伊那尓栖 にのまえいなにす
            'がうる・ぐら' : 'gawrgura',    #がうる・くら
            'ワトソン・アメリア' : 'watsonameliaEN',  #ワトソン・アメリア
            'IRyS' : 'irys_en', #IRyS アイリス
            'つくもさな' : 'tsukumosana',      # 九十九佐命/つくもさな
            'セレス・ファウナ' : 'ceresfauna',    # セレス・ファウナ
            'オーロ・クロニー' : 'ourokronii',   # オーロ・クロニー
            'ななしむめい' : 'nanashimumei_en',  # 七詩ムメイ/ななしむめい
            'ハコス・ベールズ' : 'hakosbaelz',    # ハコス・ベールズ

            #ホロライブ ID
            'アユンダ・リス' : 'ayunda_risu',    #Ayunda Risu / アユンダ・リス
            'ムーナ・ホシノヴァ' : 'moonahoshinova',      #Moona Hoshinova / ムーナ・ホシノヴァ
            'アイラニ・イオフィフティーン' : 'airaniiofifteen',      #Airani Iofifteen / アイラニ・イオフィフティーン
            'クレイジー・オリー' : 'kureijiollie',     #Kureiji Ollie / クレイジー・オリー 
            'アーニャ・メルフィッサ' : 'anyamelfissa',       #Anya Melfissa / アーニャ・メルフィッサ
            'パヴォリア・レイネ' : 'pavoliareine',       #Pavolia Reine / パヴォリア・レイネ
        }
        return ch_list

    @staticmethod
    def get_video_ids():
        Channel_JP = {
                # ホロライブ
                '戌神ころね' :'UChAnqc_AY5_I3Px5dig3X1Q',    #戌神ころね
                'さくらみこ' : 'UC-hM6YJuNYVAmUWxeIr9FeA',     #さくらみこ
                '白上フブキ' : 'UCdn5BQ06XqgXoAxIhbqw5Rg',   #白上フブキ
                '湊あくあ' : 'UC1opHUrw8rvnsadT-iGp7Cg',     #湊あくあ
                '兎田ぺこら' : 'UC1DCedRgGHBdm81E1llLhOQ',   #兎田ぺこら
                'アキ・ローゼンタール' : 'UCFTLzh12_nrtzqBPsTCqenA',   #アキ・ローゼンタール
                'ときのそら' : 'UCp6993wxpyDPHUpavwDFqgg',     #ときのそら
                '大空スバル' : 'UCvzGlP9oQwU--Y0r9id_jnA',   #大空スバル
                'ロボ子さん' : 'UCDqI2jOz0weumE8s7paEk6g',   #ロボ子さん
                '紫咲シオン' : 'UCXTpFs_3PqI41qX2d9tL2Rw',    #紫咲シオン
                '不知火フレア' : 'UCvInZx9h3jC2JzsIzoOebWg',    #不知火フレア
                '夜空メル' : 'UCD8HOxPs4Xvsm8H0ZxXGiBw',      #夜空メル
                '癒月ちょこ' : 'UC1suqwovbL1kzsoaZgFZLKg',    #癒月ちょこ
                '癒月ちょこ(サブ)' : 'UCp3tgHXw_HI0QMk1K8qh3gQ',    #癒月ちょこ(サブ)
                '赤井はあと' : 'UC1CfXB_kRs3C-zaeTG3oGyg',    #赤井はあと
                '猫又おかゆ' : 'UCvaTdHTWBGv3MKj3KVqJVCw',    #猫又おかゆ
                '姫森ルーナ' : 'UCa9Y57gfeY0Zro_noHRVrnw',     #姫森ルーナ
                '星街すいせい' : 'UC5CwaMl1eIgY8h02uZw7u8A',   #星街すいせい
                '夏色まつり' : 'UCQ0UDLQCjY0rmuxCDE38FGg',  #夏色まつり
                '宝鐘マリン' : 'UCCzUftO8KOVkV4wQG1vkUvg',   #宝鐘マリン
                '百鬼あやめ' : 'UC7fk0CB07ly8oSl0aqKkqFg',   #百鬼あやめ
                '白銀ノエル' : 'UCdyqAaZDKHXg4Ahi7VENThQ',     #白銀ノエル
                '潤羽るしあ' : 'UCl_gCybOJRIgOXw6Qb4qJzQ',   #潤羽るしあ
                '桐生ココ' : 'UCS9uQI-jC3DE0L4IpXyvr6w',     #桐生ココ
                '天音かなた' : 'UCZlDXzGoo7d44bwdNObFacg',   #天音かなた
                '大神ミオ' : 'UCp-5t9SrOQwXMU7iIjQfARg',      #大神ミオ
                '常闇トワ' : 'UC1uv2Oq6kNxgATlCiez59hw',     #常闇トワ
                '角巻わため' : 'UCqm3BQLlJfvkTsX_hvm0UmA',   #角巻わため
                '雪花ラミィ' : 'UCFKOVgVbGmX65RxO3EtH3iw',      #雪花ラミィ
                '桃鈴ねね' : 'UCAWSyEs_Io8MtpY3m-zqILA',     #桃鈴ねね
                '獅白ぼたん' : 'UCUKD-uaobj9jiqB-VXt71mA',      #獅白ぼたん
                '尾丸ポルカ' : 'UCK9V2B22uJYu3N7eR_BT9QA' ,      #尾丸ポルカ
                # 'ALOE_ch' : 'UCgZuwn-O7Szh9cAgHqJ6vjw',      #魔乃アロエ
                
                # イノナカミュージック
                'AZKi' : 'UC0TXe_LYZ4scaW2XMyi5_kw',     #AZKi

                # 運営
                'Hololive' : 'UCJFZiqLMntJufDCHc6bQixg',   #Hololive
                'HololiveEN' : 'UCotXwY6s8pWmuWd_snKYjhg',   #hololive EN
                'HololiveID' : 'UCfrWoRGlawPQDQxxeIDRP0Q',   #hololive ID
                }

        Channel_OSea = {
                #ホロライブ　EN
                '森カリオペ' : 'UCL_qhgtOy0dy1Agp8vkySQg',    #森カリオペ モリ・カリオペ
                '小鳥遊キアラ' : 'UCHsx4Hqa-1ORjQTh9TYDhww',    #小鳥遊キアラ
                '一伊那尓栖' : 'UCMwGHR0BTZuLsmjY_NT5Pwg',    #一伊那尓栖 にのまえいなにす
                'がうる・ぐら' : 'UCoSrY_IQQVpmIRZ9Xf-y93g',    #がうる・くら
                'ワトソン・アメリア' : 'UCyl1z3jo3XHR1riLFKG5UAg',  #ワトソン・アメリア
                'IRyS' : 'UC8rcEBzJSleTkf_-agPM20g',       #IRys / アイリス

                'つくもさな' : 'UCsUj0dszADCGbF3gNrQEuSQ',      # 九十九佐命/つくもさな
                'セレス・ファウナ' : 'UCO_aKKYxn4tvrqPjcTzZ6EQ',    # セレス・ファウナ
                'オーロ・クロニー' : 'UCmbs8T6MWqUHP1tIQvSgKrg',   # オーロ・クロニー
                'ななしむめい' : 'UC3n5uGu18FoCy23ggWWp8tA',  # 七詩ムメイ/ななしむめい
                'ハコス・ベールズ' : 'UCgmPnx-EEeOrZSg5Tiw7ZRQ',    # ハコス・ベールズ

                #ホロライブ ID
                'アユンダ・リス' : 'UCOyYb1c43VlX9rc_lT6NKQw',    #Ayunda Risu / アユンダ・リス
                'ムーナ・ホシノヴァ' : 'UCP0BspO_AMEe3aQqqpo89Dg',      #Moona Hoshinova / ムーナ・ホシノヴァ
                'アイラニ・イオフィフティーン' : 'UCAoy6rzhSf4ydcYjJw3WoVg',      #Airani Iofifteen / アイラニ・イオフィフティーン
                'クレイジー・オリー' : 'UCYz_5n-uDuChHtLo7My1HnQ',     #Kureiji Ollie / クレイジー・オリー 
                'アーニャ・メルフィッサ' : 'UC727SQYUvx5pDDGQpTICNWg',       #Anya Melfissa / アーニャ・メルフィッサ
                'パヴォリア・レイネ' : 'UChgTyjG-pdNvxxhdsXfHQ5Q',       #Pavolia Reine / パヴォリア・レイネ
                }
        return Channel_JP, Channel_OSea

    @staticmethod
    def get_name_tag(ID):
        # ホロライブ
        HoloName = ''
        live_tag  = ''
        if ID == 'UChAnqc_AY5_I3Px5dig3X1Q': HoloName,live_tag = '戌神ころね', '#生神もんざえもん'
        elif ID == 'UC-hM6YJuNYVAmUWxeIr9FeA' : HoloName,live_tag ='さくらみこ', '#みこなま'
        elif ID == 'UCdn5BQ06XqgXoAxIhbqw5Rg' : HoloName,live_tag = '白上フブキ', '#フブキCh'
        elif ID == 'UC1opHUrw8rvnsadT-iGp7Cg' : HoloName,live_tag = '湊あくあ', '#湊あくあ生放送'
        elif ID == 'UC1DCedRgGHBdm81E1llLhOQ' : HoloName,live_tag = '兎田ぺこら', '#ぺこらいぶ'
        elif ID == 'UCFTLzh12_nrtzqBPsTCqenA' : HoloName,live_tag = 'アキ・ローゼンタール', '#アキびゅーわーるど'
        elif ID == 'UCp6993wxpyDPHUpavwDFqgg' : HoloName,live_tag = 'ときのそら', '#ときのそら生放送'
        elif ID == 'UCvzGlP9oQwU--Y0r9id_jnA' : HoloName,live_tag = '大空スバル', '#生スバル'
        elif ID == 'UCDqI2jOz0weumE8s7paEk6g' : HoloName,live_tag = 'ロボ子さん', '#ロボ子生放送'
        elif ID == 'UCXTpFs_3PqI41qX2d9tL2Rw' : HoloName,live_tag = '紫咲シオン', '#紫咲シオン'
        elif ID == 'UCvInZx9h3jC2JzsIzoOebWg' : HoloName,live_tag = '不知火フレア', '#フレアストリーム'
        elif ID == 'UCD8HOxPs4Xvsm8H0ZxXGiBw' : HoloName,live_tag = '夜空メル', '#メル生放送'
        elif ID == 'UCp3tgHXw_HI0QMk1K8qh3gQ' : HoloName,live_tag = '癒月ちょこ', '#癒月診療所' # サブ
        elif ID == 'UC1suqwovbL1kzsoaZgFZLKg' : HoloName,live_tag = '癒月ちょこ', '#癒月診療所'
        elif ID == 'UC1CfXB_kRs3C-zaeTG3oGyg' : HoloName,live_tag = '赤井はあと', '#はあちゃまなう'
        elif ID == 'UCvaTdHTWBGv3MKj3KVqJVCw' : HoloName,live_tag = '猫又おかゆ', '#生おかゆ'
        elif ID == 'UCa9Y57gfeY0Zro_noHRVrnw' : HoloName,live_tag = '姫森ルーナ', '#なのらいぶ'
        elif ID == 'UC5CwaMl1eIgY8h02uZw7u8A' : HoloName,live_tag = '星街すいせい', '#ほしまちすたじお'
        elif ID == 'UCQ0UDLQCjY0rmuxCDE38FGg' : HoloName,live_tag = '夏色まつり', '#夏まつch'
        elif ID == 'UCCzUftO8KOVkV4wQG1vkUvg' : HoloName,live_tag = '宝鐘マリン', '#マリン航海記'
        elif ID == 'UC7fk0CB07ly8oSl0aqKkqFg' : HoloName,live_tag = '百鬼あやめ', '#百鬼あやめch'
        elif ID == 'UCdyqAaZDKHXg4Ahi7VENThQ' : HoloName,live_tag = '白銀ノエル', '#ノエルーム'
        elif ID == 'UCl_gCybOJRIgOXw6Qb4qJzQ' : HoloName,live_tag = '潤羽るしあ', '#るしあらいぶ'
        elif ID == 'UCS9uQI-jC3DE0L4IpXyvr6w' : HoloName,live_tag = '桐生ココ', '#桐生ココ'
        elif ID == 'UCZlDXzGoo7d44bwdNObFacg' : HoloName,live_tag = '天音かなた', '#天界学園放送部'
        elif ID == 'UCp-5t9SrOQwXMU7iIjQfARg' : HoloName,live_tag = '大神ミオ', '#ミオかわいい'
        elif ID == 'UC1uv2Oq6kNxgATlCiez59hw' : HoloName,live_tag = '常闇トワ', '#トワイライブ'
        elif ID == 'UCqm3BQLlJfvkTsX_hvm0UmA' : HoloName,live_tag = '角巻わため', '#ドドドライブ'
        elif ID == 'UCFKOVgVbGmX65RxO3EtH3iw' : HoloName,live_tag = '雪花ラミィ', '#らみらいぶ'
        elif ID == 'UCAWSyEs_Io8MtpY3m-zqILA' : HoloName,live_tag = '桃鈴ねね', '#ねねいろらいぶ'
        elif ID == 'UCUKD-uaobj9jiqB-VXt71mA' : HoloName,live_tag = '獅白ぼたん', '#ぐうたらいぶ'
        elif ID == 'UCK9V2B22uJYu3N7eR_BT9QA' : HoloName,live_tag = '尾丸ポルカ', '#ポルカ公演中'
        # elif ID == 'UCgZuwn-O7Szh9cAgHqJ6vjw' : HoloName = '魔乃アロエ'
        # イノナカミュージック
        elif ID == 'UC0TXe_LYZ4scaW2XMyi5_kw' : HoloName,live_tag = 'AZKi', '#AZKi'
        #ホロライブ　EN
        elif ID == 'UCL_qhgtOy0dy1Agp8vkySQg' : HoloName,live_tag = '森カリオペ', '#calliolive'
        elif ID == 'UCHsx4Hqa-1ORjQTh9TYDhww' : HoloName,live_tag = '小鳥遊キアラ', '#キアライブ'
        elif ID == 'UCMwGHR0BTZuLsmjY_NT5Pwg' : HoloName,live_tag = '一伊那尓栖', '#TAKOTIME'
        elif ID == 'UCoSrY_IQQVpmIRZ9Xf-y93g' : HoloName,live_tag = 'がうる・ぐら', '#gawrgura'
        elif ID == 'UCyl1z3jo3XHR1riLFKG5UAg' : HoloName,live_tag = 'ワトソン・アメリア', '#amelive'
        elif ID == 'UC8rcEBzJSleTkf_-agPM20g' : HoloName,live_tag = 'アイリス', '#IRyS'

        elif ID == 'UCsUj0dszADCGbF3gNrQEuSQ' : HoloName,live_tag = 'つくもさな', '#SanaLanding'
        elif ID == 'UCO_aKKYxn4tvrqPjcTzZ6EQ' : HoloName,live_tag = 'セレス・ファウナ', '#faunline'
        elif ID == 'UCmbs8T6MWqUHP1tIQvSgKrg' : HoloName,live_tag = 'オーロ・クロニー', '#krotime'
        elif ID == 'UC3n5uGu18FoCy23ggWWp8tA' : HoloName,live_tag = 'ななしむめい', '#watchMEI'
        elif ID == 'UCgmPnx-EEeOrZSg5Tiw7ZRQ' : HoloName,live_tag = 'ハコス・ベールズ', '#enterbaelz'
        #ホロライブ ID
        elif ID == 'UCOyYb1c43VlX9rc_lT6NKQw' : HoloName,live_tag = 'アユンダ・リス', '#Risu_Live'
        elif ID == 'UCP0BspO_AMEe3aQqqpo89Dg' : HoloName,live_tag = 'ムーナ・ホシノヴァ', '#MoonA_Live'
        elif ID == 'UCAoy6rzhSf4ydcYjJw3WoVg' : HoloName,live_tag =  'アイラニ・イオフィフティーン', '#ioLYFE'
        elif ID == 'UCYz_5n-uDuChHtLo7My1HnQ' : HoloName,live_tag =  'クレイジー・オリー', '#Kureiji_Ollie'
        elif ID == 'UC727SQYUvx5pDDGQpTICNWg' : HoloName,live_tag =  'アーニャ・メルフィッサ', '#Anya_Melfissa'
        elif ID == 'UChgTyjG-pdNvxxhdsXfHQ5Q' : HoloName,live_tag =  'パヴォリア・レイネ', '#Pavolive'
        # 運営
        elif ID == 'UCJFZiqLMntJufDCHc6bQixg' : HoloName,live_tag = 'Hololive','#Hololive'
        elif ID == 'UCotXwY6s8pWmuWd_snKYjhg' : HoloName,live_tag = 'holoEN','#holoEN'
        elif ID == 'UCfrWoRGlawPQDQxxeIDRP0Q' : HoloName,live_tag = 'holoID','#holoID'
        
        return HoloName,live_tag