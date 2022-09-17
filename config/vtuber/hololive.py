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
            # '潤羽るしあ' : 'uruharushia',       #'潤羽るしあ'
            '戌神ころね' : 'inugamikorone',     #'戌神ころね'
            '角巻わため' : 'tsunomakiwatame',        #'角巻わため' 
            '白銀ノエル' : 'shiroganenoel',     #'白銀ノエル'
            '兎田ぺこら' : 'usadapekora',       #'兎田ぺこら'
            'さくらみこ' : 'sakuramiko35',      #'さくらみこ'
            '紫咲シオン' : 'murasakishionch',       #'紫咲シオン'
            '湊あくあ' : 'minatoaqua',        #'湊あくあ'
            '常闇トワ' : 'tokoyamitowa',      #'常闇トワ'
            '夜空メル'  : 'yozoramel',      #'夜空メル' 
            '天音かなた' : 'amanekanatach',     #天音かなた
            '癒月ちょこ' : 'yuzukichococh',     #癒月ちょこ
            '癒月ちょこ(サブ)' : 'yuzukichococh',     #癒月ちょこ
            'ときのそら' : 'tokino_sora',       #'ときのそら'
            # 5期生
            '雪花ラミィ' : 'yukihanalamy',     #雪花ラミィ
            '桃鈴ねね' : 'momosuzunene',     #桃鈴ねね
            '獅白ぼたん' : 'shishirobotan',        #獅白ぼたん
            # '魔乃アロエ' : 'manoaloe',     #魔乃アロエ
            '尾丸ポルカ' : 'omarupolka',      #尾丸ポルカ
            # holoX 6期生
            'ラプラス・ダークネス' : 'LaplusDarknesss',
            '鷹嶺ルイ' : 'takanelui',
            '博衣こより' : 'hakuikoyori',
            '沙花叉クロヱ' : 'sakamatachloe',
            '風真いろは' : 'kazamairohach',

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
            'ベスティア・ゼータ' : 'vestiazeta',       #vestiazeta / ベスティア・ゼータ
            'カエラ・コヴァルスキア' : 'kaelakovalskia',       #Kaela Kovalskia / カエラ・コヴァルスキア
            'こぼ・かなえる' : 'kobokanaeru',       #kobokanaeru/こぼ・かなえる
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
                '赤井はあと(サブ)' : 'UCHj_mh57PVMXhAUDphUQDFA',    #赤井はあと
                '猫又おかゆ' : 'UCvaTdHTWBGv3MKj3KVqJVCw',    #猫又おかゆ
                '姫森ルーナ' : 'UCa9Y57gfeY0Zro_noHRVrnw',     #姫森ルーナ
                '星街すいせい' : 'UC5CwaMl1eIgY8h02uZw7u8A',   #星街すいせい
                '夏色まつり' : 'UCQ0UDLQCjY0rmuxCDE38FGg',  #夏色まつり
                '宝鐘マリン' : 'UCCzUftO8KOVkV4wQG1vkUvg',   #宝鐘マリン
                '百鬼あやめ' : 'UC7fk0CB07ly8oSl0aqKkqFg',   #百鬼あやめ
                '白銀ノエル' : 'UCdyqAaZDKHXg4Ahi7VENThQ',     #白銀ノエル
                # '潤羽るしあ' : 'UCl_gCybOJRIgOXw6Qb4qJzQ',   #潤羽るしあ
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
                'ラプラス・ダークネス' : 'UCENwRMx5Yh42zWpzURebzTw',
                '鷹嶺ルイ' : 'UCs9_O1tRPMQTHQ-N_L6FU2g',
                '博衣こより' : 'UC6eWCld0KwmyHFbAqK3V-Rw',
                '沙花叉クロヱ' : 'UCIBY1ollUsauvVi4hW4cumw',
                '風真いろは' : 'UC_vMYWcDjmfdpH6r4TTn1MQ',
                
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
                'ベスティア・ゼータ' : 'UCTvHWSfBZgtxE4sILOaurIQ',       #vestiazeta / ベスティア・ゼータ
                'カエラ・コヴァルスキア' : 'UCZLZ8Jjx_RN2CXloOmgTHVg',       #Kaela Kovalskia / カエラ・コヴァルスキア
                'こぼ・かなえる' : 'UCjLEmnpCNeisMxy134KPwWw',       #kobokanaeru/こぼ・かなえる
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
        elif ID == 'UCHj_mh57PVMXhAUDphUQDFA' : HoloName,live_tag = '赤井はあと', '#はあちゃまなう' # サブ
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
        elif ID == 'UC1uv2Oq6kNxgATlCiez59hw' : HoloName,live_tag = '常闇トワ', '#トワイライヴ'
        elif ID == 'UCqm3BQLlJfvkTsX_hvm0UmA' : HoloName,live_tag = '角巻わため', '#ドドドライブ'
        elif ID == 'UCFKOVgVbGmX65RxO3EtH3iw' : HoloName,live_tag = '雪花ラミィ', '#らみらいぶ'
        elif ID == 'UCAWSyEs_Io8MtpY3m-zqILA' : HoloName,live_tag = '桃鈴ねね', '#ねねいろらいぶ'
        elif ID == 'UCUKD-uaobj9jiqB-VXt71mA' : HoloName,live_tag = '獅白ぼたん', '#ぐうたらいぶ'
        elif ID == 'UCK9V2B22uJYu3N7eR_BT9QA' : HoloName,live_tag = '尾丸ポルカ', '#ポルカ公演中'
        # elif ID == 'UCgZuwn-O7Szh9cAgHqJ6vjw' : HoloName = '魔乃アロエ'
        elif ID == 'UCENwRMx5Yh42zWpzURebzTw' : HoloName,live_tag = 'ラプラス・ダークネス', '#laplus_great'
        elif ID == 'UCs9_O1tRPMQTHQ-N_L6FU2g' : HoloName,live_tag = '鷹嶺ルイ', '#たかねの見物'
        elif ID == 'UC6eWCld0KwmyHFbAqK3V-Rw' : HoloName,live_tag = '博衣こより', '#こより実験中'
        elif ID == 'UCIBY1ollUsauvVi4hW4cumw' : HoloName,live_tag = '沙花叉クロヱ', '#またまたさかまた'
        elif ID == 'UC_vMYWcDjmfdpH6r4TTn1MQ' : HoloName,live_tag = '風真いろは', '#かざま修行中'
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
        elif ID == 'UCTvHWSfBZgtxE4sILOaurIQ' : HoloName,live_tag =  'ベスティア・ゼータ', '#ZecretLive'
        elif ID == 'UCZLZ8Jjx_RN2CXloOmgTHVg' : HoloName,live_tag =  'カエラ・コヴァルスキア', '#Kaelaif'
        elif ID == 'UCjLEmnpCNeisMxy134KPwWw' : HoloName,live_tag =  'こぼ・かなえる', '#OnAeru'

        # 運営
        elif ID == 'UCJFZiqLMntJufDCHc6bQixg' : HoloName,live_tag = 'Hololive','#Hololive'
        elif ID == 'UCotXwY6s8pWmuWd_snKYjhg' : HoloName,live_tag = 'holoEN','#holoEN'
        elif ID == 'UCfrWoRGlawPQDQxxeIDRP0Q' : HoloName,live_tag = 'holoID','#holoID'
        
        return HoloName,live_tag

    @staticmethod
    def getLiveTag(ID:str):
        HoloName = ''
        live_tag = ''
        holo_tag  = ''
        if ID == 'UChAnqc_AY5_I3Px5dig3X1Q': HoloName, live_tag, holo_tag = '戌神ころね', '#生神もんざえもん','🥐'
        elif ID == 'UC-hM6YJuNYVAmUWxeIr9FeA' : HoloName, live_tag, holo_tag  = 'さくらみこ', '#みこなま', '🌸'
        elif ID == 'UCdn5BQ06XqgXoAxIhbqw5Rg' : HoloName, live_tag, holo_tag  = '白上フブキ', '#フブキCh', '🌽'
        elif ID == 'UC1opHUrw8rvnsadT-iGp7Cg' : HoloName, live_tag, holo_tag  = '湊あくあ', '#湊あくあ生放送', '⚓️'
        elif ID == 'UC1DCedRgGHBdm81E1llLhOQ' : HoloName, live_tag, holo_tag  = '兎田ぺこら', '#ぺこらいぶ', '👯'
        elif ID == 'UCFTLzh12_nrtzqBPsTCqenA' : HoloName, live_tag, holo_tag  = 'アキ・ローゼンタール', '#アキびゅーわーるど', '🍎'
        elif ID == 'UCp6993wxpyDPHUpavwDFqgg' : HoloName, live_tag, holo_tag  = 'ときのそら', '#ときのそら生放送', '🐻'
        elif ID == 'UCvzGlP9oQwU--Y0r9id_jnA' : HoloName, live_tag, holo_tag  = '大空スバル', '#生スバル', '🚑'
        elif ID == 'UCDqI2jOz0weumE8s7paEk6g' : HoloName, live_tag, holo_tag  = 'ロボ子さん', '#ロボ子生放送', '🤖'
        elif ID == 'UCXTpFs_3PqI41qX2d9tL2Rw' : HoloName, live_tag, holo_tag  = '紫咲シオン', '#紫咲シオン', '🌙'
        elif ID == 'UCvInZx9h3jC2JzsIzoOebWg' : HoloName, live_tag, holo_tag  = '不知火フレア', '#フレアストリーム', '🔥'
        elif ID == 'UCD8HOxPs4Xvsm8H0ZxXGiBw' : HoloName, live_tag, holo_tag  = '夜空メル', '#メル生放送', '🌟'
        elif ID == 'UC1suqwovbL1kzsoaZgFZLKg' : HoloName, live_tag, holo_tag  = '癒月ちょこ', '#癒月診療所', '💋'
        elif ID == 'UCp3tgHXw_HI0QMk1K8qh3gQ' : HoloName, live_tag, holo_tag  = '癒月ちょこ', '#癒月診療所', '💋' #サブ
        elif ID == 'UC1CfXB_kRs3C-zaeTG3oGyg' : HoloName, live_tag, holo_tag  = '赤井はあと', '#はあちゃまなう', '❤️'
        elif ID == 'UCvaTdHTWBGv3MKj3KVqJVCw' : HoloName, live_tag, holo_tag  = '猫又おかゆ', '#生おかゆ', '🍙'
        elif ID == 'UCa9Y57gfeY0Zro_noHRVrnw' : HoloName, live_tag, holo_tag  = '姫森ルーナ', '#なのらいぶ', '🍬'
        elif ID == 'UC5CwaMl1eIgY8h02uZw7u8A' : HoloName, live_tag, holo_tag  = '星街すいせい', '#ほしまちすたじお', '☄️'
        elif ID == 'UCQ0UDLQCjY0rmuxCDE38FGg' : HoloName, live_tag, holo_tag  = '夏色まつり', '#夏まつch', '🏮'
        elif ID == 'UCCzUftO8KOVkV4wQG1vkUvg' : HoloName, live_tag, holo_tag  = '宝鐘マリン', '#マリン航海記', '🏴‍☠️'
        elif ID == 'UC7fk0CB07ly8oSl0aqKkqFg' : HoloName, live_tag, holo_tag  = '百鬼あやめ', '#百鬼あやめch', '😈'
        elif ID == 'UCdyqAaZDKHXg4Ahi7VENThQ' : HoloName, live_tag, holo_tag  = '白銀ノエル', '#ノエルーム', '⚔️'
        elif ID == 'UCl_gCybOJRIgOXw6Qb4qJzQ' : HoloName, live_tag, holo_tag  = '潤羽るしあ', '#るしあらいぶ', '🦋'
        elif ID == 'UCS9uQI-jC3DE0L4IpXyvr6w' : HoloName, live_tag, holo_tag  = '桐生ココ', '#桐生ココ', '🐉'
        elif ID == 'UCZlDXzGoo7d44bwdNObFacg' : HoloName, live_tag, holo_tag  = '天音かなた', '#天界学園放送部', '💫'
        elif ID == 'UCp-5t9SrOQwXMU7iIjQfARg' : HoloName, live_tag, holo_tag  = '大神ミオ', '#ミオかわいい', '🌲'
        elif ID == 'UC1uv2Oq6kNxgATlCiez59hw' : HoloName, live_tag, holo_tag  = '常闇トワ', '#トワイライブ', '👾'
        elif ID == 'UCqm3BQLlJfvkTsX_hvm0UmA' : HoloName, live_tag, holo_tag  = '角巻わため', '#ドドドライブ', '🐏'
        elif ID == 'UCFKOVgVbGmX65RxO3EtH3iw' : HoloName, live_tag, holo_tag  = '雪花ラミィ', '#らみらいぶ', '☃️'
        elif ID == 'UCAWSyEs_Io8MtpY3m-zqILA' : HoloName, live_tag, holo_tag  = '桃鈴ねね', '#桃鈴ねね生放送', '🍑'
        elif ID == 'UCUKD-uaobj9jiqB-VXt71mA' : HoloName, live_tag, holo_tag  = '獅白ぼたん', '#ぐうたらいぶ', '👅'
        elif ID == 'UCK9V2B22uJYu3N7eR_BT9QA' : HoloName, live_tag, holo_tag  = '尾丸ポルカ', '#ポルカ公演中', '🎪'
        elif ID == 'UCENwRMx5Yh42zWpzURebzTw' : HoloName, live_tag, holo_tag = 'ラプラス・ダークネス', '#laplus_great', '🛸💜'
        elif ID == 'UCs9_O1tRPMQTHQ-N_L6FU2g' : HoloName, live_tag, holo_tag = '鷹嶺ルイ', '#たかねの見物', '🥀'
        elif ID == 'UC6eWCld0KwmyHFbAqK3V-Rw' : HoloName, live_tag, holo_tag = '博衣こより', '#こより実験中', '🧪'
        elif ID == 'UCIBY1ollUsauvVi4hW4cumw' : HoloName, live_tag, holo_tag = '沙花叉クロヱ', '#またまたさかまた', '🎣'
        elif ID == 'UC_vMYWcDjmfdpH6r4TTn1MQ' : HoloName, live_tag, holo_tag = '風真いろは', '#かざま修行中', '🍃'
        # elif ID == 'UCgZuwn-O7Szh9cAgHqJ6vjw' : HoloName = '魔乃アロエ'
        # イノナカミュージック
        elif ID == 'UC0TXe_LYZ4scaW2XMyi5_kw' : HoloName, live_tag, holo_tag  = 'AZKi', '#AZKi', '⚒️'
        #ホロライブ　EN
        elif ID == 'UCL_qhgtOy0dy1Agp8vkySQg' : HoloName, live_tag, holo_tag  = '森美声', '#calliolive', '💀'
        elif ID == 'UCHsx4Hqa-1ORjQTh9TYDhww' : HoloName, live_tag, holo_tag  = '小鳥遊キアラ', '#キアライブ', '🐔'
        elif ID == 'UCMwGHR0BTZuLsmjY_NT5Pwg' : HoloName, live_tag, holo_tag  = '一伊那尓栖', '#TAKOTIME', '🐙'
        elif ID == 'UCoSrY_IQQVpmIRZ9Xf-y93g' : HoloName, live_tag, holo_tag  = 'がうる・ぐら', '#gawrgura', '🔱'
        elif ID == 'UCyl1z3jo3XHR1riLFKG5UAg' : HoloName, live_tag, holo_tag  = 'ワトソン・アメリア', '#amelive', '🔎'
        elif ID == 'UC8rcEBzJSleTkf_-agPM20g' : HoloName, live_tag, holo_tag  = 'アイリス', '#IRyShow', '💎'

        elif ID == 'UCsUj0dszADCGbF3gNrQEuSQ' : HoloName, live_tag, holo_tag   = 'つくもさな', '#SanaLanding', '🪐'
        elif ID == 'UCO_aKKYxn4tvrqPjcTzZ6EQ' : HoloName, live_tag, holo_tag   = 'セレス・ファウナ', '#faunline', '🌿' 
        elif ID == 'UCmbs8T6MWqUHP1tIQvSgKrg' : HoloName, live_tag, holo_tag   = 'オーロ・クロニー', '#krotime', '⏳'
        elif ID == 'UC3n5uGu18FoCy23ggWWp8tA' : HoloName, live_tag, holo_tag   = 'ななしむめい', '#watchMEI', '🪶'
        elif ID == 'UCgmPnx-EEeOrZSg5Tiw7ZRQ' : HoloName, live_tag, holo_tag   = 'ハコス・ベールズ', '#enterbaelz', '🎲'

        #ホロライブ ID
        elif ID == 'UCOyYb1c43VlX9rc_lT6NKQw' : HoloName, live_tag, holo_tag  = 'アユンダ・リス', '#Risu_Live', '🐿'
        elif ID == 'UCP0BspO_AMEe3aQqqpo89Dg' : HoloName, live_tag, holo_tag  = 'ムーナ・ホシノヴァ', '#MoonA_Live', '🔮'
        elif ID == 'UCAoy6rzhSf4ydcYjJw3WoVg' : HoloName, live_tag, holo_tag  =  'アイラニ・イオフィフティーン', '#ioLYFE', '🎨'
        elif ID == 'UCYz_5n-uDuChHtLo7My1HnQ' : HoloName, live_tag, holo_tag  =  'クレイジー・オリー', '#Kureiji_Ollie', '🧟‍♀️'
        elif ID == 'UC727SQYUvx5pDDGQpTICNWg' : HoloName, live_tag, holo_tag  =  'アーニャ・メルフィッサ', '#Anya_Melfissa', '🍂'
        elif ID == 'UChgTyjG-pdNvxxhdsXfHQ5Q' : HoloName, live_tag, holo_tag  =  'パヴォリア・レイネ', '#Pavolive', '🦚'

        elif ID == 'UCTvHWSfBZgtxE4sILOaurIQ' : HoloName, live_tag, holo_tag  =  'ベスティア・ゼータ', '#ZecretLive', '📜'
        elif ID == 'UCZLZ8Jjx_RN2CXloOmgTHVg' : HoloName, live_tag, holo_tag  =  'カエラ・コヴァルスキア', '#Kaelaif', '🔨'
        elif ID == 'UCjLEmnpCNeisMxy134KPwWw' : HoloName, live_tag, holo_tag  =  'こぼ・かなえる', '#OnAeru', '☔'
        # 運営
        elif ID == 'UCJFZiqLMntJufDCHc6bQixg' : HoloName, live_tag, holo_tag  = 'Hololive','#Hololive', '▶️'
        # 絵師
        elif ID == 'UCt30jJgChL8qeT9VPadidSw' : HoloName, live_tag, holo_tag  = 'しぐれうい', '#ういの校内放送', '🌂'
        # のりプロ
        elif ID == 'UC8NZiqKx6fsDT3AVcMiVFyA' : HoloName, live_tag, holo_tag  = '犬山たまき', '#犬山たまき', '🐶'
        elif ID == 'UCC0i9nECi4Gz7TU63xZwodg' : HoloName, live_tag, holo_tag  = '白雪みしろ', '#白雪みしろ', '❄️'
        elif ID == 'UCJCzy0Fyrm0UhIrGQ7tHpjg' : HoloName, live_tag, holo_tag  = '愛宮みるく', '#愛宮みくる', '🍼'
        elif ID == 'UCle1cz6rcyH0a-xoMYwLlAg' : HoloName, live_tag, holo_tag  = '姫咲ゆずる', '#姫咲ゆずる', '🐰'
        elif ID == 'UCLyTXfCZtl7dyhta9Jg3pZg' : HoloName, live_tag, holo_tag  = '鬼灯わらべ', '#鬼灯わらべ', '👹'
        elif ID == 'UCH11P1Hq4PXdznyw1Hhr3qw' : HoloName, live_tag, holo_tag  = '夢乃リリス', '#夢乃リリス', '🏩'
        elif ID == 'UCxrmkJf_X1Yhte_a4devFzA' : HoloName, live_tag, holo_tag  = '胡桃澤もも', '#胡桃澤もも', '🎀'
        elif ID == 'UCBAeKqEIugv69Q2GIgcH7oA' : HoloName, live_tag, holo_tag  = '逢魔きらら', '#逢魔きらら', '👿'
        elif ID == 'UCIRzELGzTVUOARi3Gwf1-yg' : HoloName, live_tag, holo_tag  = '看谷にぃあ', '#看谷にぃあ', '🌙❤️'
        elif ID == 'UCCXME7oZmXB2VFHJbz5496A' : HoloName, live_tag, holo_tag  = '熊谷タクマ', '#熊谷タクマ', '🐻🍨'
        elif ID == 'UCWIPfdcux1WxuX5yZLPJDww' : HoloName, live_tag, holo_tag = '稲荷いろは', '#稲荷いろは', '🦊🍂'
        elif ID == 'UCuycJ_IsA5ESbTYhe05ozqQ' : HoloName, live_tag, holo_tag = 'レグルシュ・ライオンハート', '#レグライブ', '🔔🐾'
        elif ID == 'UCMxIxoMdtcLkZ1wTq7qjztg' : HoloName, live_tag, holo_tag = '猫瀬乃しん' , ' #猫瀬乃しん', '🐈🎩'
        return live_tag, holo_tag 
    
    @staticmethod
    def get_twitter_num():
        return {
            '友人A(えーちゃん)' : 1064352899705143297,
            # 0期生
            'ときのそら' : 880317891249188864,
            'AZKi' : 1062499145267605504,
            'さくらみこ' : 979891380616019968,
            'ロボ子さん' : 960340787782299648,
            '星街すいせい' : 975275878673408001,
            # 1期生
            'アキ・ローゼンタール' : 996643748862836736,
            '夜空メル' : 985703615758123008,
            '赤井はあと' : 998336069992001537,
            '夏色まつり' : 996645451045617664,
            'まちゅり໒꒱· ﾟ' : 1122810226153938944,
            # 2期生
            '大空スバル' : 1027853566780698624,
            '癒月ちょこ' : 1024970912859189248,
            '紫咲シオン' : 1024533638879166464,
            '湊あくあ' : 1024528894940987392,
            '百鬼あやめ' : 1024532356554608640,
            # ゲーマーズ
            '白上フブキ' : 997786053124616192,
            '戌神ころね' : 1109748792721432577,
            '大神ミオ' : 1063337246231687169,
            '猫又おかゆ' : 1109751762733301760,
            'おかう' : 1508759123285856256,
            # 3期生
            '宝鐘マリン' : 1153192638645821440,
            '白銀ノエル' : 1153195295573856256,
            '不知火フレア' : 1154304634569150464,
            '兎田ぺこら' : 1133215093246664706,
            # '潤羽るしあ' : 1142975277175205888,
            # 4期生
            '天音かなた' : 1200396304360206337,
            '常闇トワ' : 1200357161747939328,
            '姫森ルーナ' : 1200396798281445376,
            '角巻わため' : 1200397643479805957,
            # '桐生ココ' : 1200397238788247552,
            # 5期生
            '桃鈴ねね' : 1255017971363090432,
            '尾丸ポルカ' : 1270551806993547265,
            '雪花ラミィ' : 1255013740799356929,
            '獅白ぼたん' : 1255015814979186689,
            # '魔乃アロエ' : 1255019046119989248,
            #　6期生
            'ラプラス・ダークネス' : 1433657158067896325,
            '鷹嶺ルイ' : 1433660866063339527,
            '沙花叉クロヱ' : 1433669866406375432,
            '博衣こより' : 1433667543806267393,
            '風真いろは' : 1434755250049589252,
            # Myth
            'Watson Amelia' : 1283656034305769472,
            'Gawr Gura' : 1283657064410017793,
            'Takanashi Kiara' : 1283646922406760448,
            'Ninomae Ina’nis' : 1283650008835743744,
            'Mori Calliope' : 1283653858510598144,
            # Project:HOPE
            'IRyS' : 1363705980261855232,
            # Council
            'Nanashi Mumei' : 1409817941705515015,
            'Ouro Kronii' : 1409817096523968513,
            'Ceres Fauna' : 1409784760805650436,
            'Tsukumo Sana' : 1409819816194576394,
            'Hakos Baelz' : 1409783149211443200,
            # ID1期生
            'Ayunda Risu(リス)' : 1234752200145899520,
            'Moona Hoshinova (ムーナ)' : 1234753886520393729,
            'Airani iofifteen (イオフィ)' : 1235180878449397764,
            # ID2期生
            'Anya Melfissa(アーニャ)' : 1328277750000492545,
            'Kureiji Ollie (オリー)' : 1328277233492844544,
            'Pavolia Reine (レイネ)' : 1328275136575799297,
            # ID3期生
            'Kobo Kanaeru(こぼ)': 1486629076005634049,
            'Kaela Kovalskia(カエラ)' : 1486636197908602880,
            'Vestia Zeta (ゼータ)' : 1486633489101307907,
        }
        
    @staticmethod
    def get_art_tag():
        return {
            'えーちゃん' : ['#絵ーちゃん'],          #えーちゃん
            'さくらみこ' : ['#miko_Art'],             #さくらみこ
            '戌神ころね' : ['#できたてころね'],       #戌神ころね
            '天音かなた' : ['#かなたーと'],          #天音かなた
            '猫又おかゆ' : ['#絵かゆ'],               #猫又おかゆ
            'アキロゼ' : ['#アロ絵'],             #アキロゼ
            # 'AKIROSE_tg' : ['#アロ絵','#スケべなアロ絵'],       #アキロゼ
            '大神みお' : ['#みおーん絵'],               #大神みお
            'ときのそら' : ['#soraArt'],               #ときのそら
            'ロボ子' : ['#ロボ子Art'],           #ロボ子
            '星街すいせい' : ['#ほしまちぎゃらりー'],     #星街すいせい
            '夜空メル' : ['#メルArt'],                #夜空メル
            '夏色まつり' : ['#祭絵'],      #夏色祭り
            # 'MATSURI_tg' : ['#祭絵','まつりは絵っち'],      #夏色まつり
            '白上フブキ' : ['#絵フブキ'],         #白上フブキ
            '赤井はあと' : ['#はあとart'],        #赤井はあと
            '湊あくあ' : ['#あくあーと'],         #湊あくあ
            '百鬼あやめ' : ['#百鬼絵巻'],         #百鬼あやめ
            '紫咲シオン' : ['#シオンの書物'],     #紫咲シオン
            '癒月ちょこ' : ['#しょこらーと'],     #癒月ちょこ
            '大空スバル' : ['#プロテインザスバル'],       #大空スバル
            'えーちゃん' : ['#絵ーちゃん'],       #えーちゃん
            '兎田ぺこら' : ['#ぺこらーと'],       #兎田ぺこら
            '潤羽るしあ' : ['#絵クロマンサー'],       #潤羽るしあ
            '宝鐘マリン' : ['#マリンのお宝'],     #宝鐘マリン
            '白銀ノエル' : ['#ノエラート'],        #白銀ノエル
            '不知火フレア' : ['#しらぬえ'],       #不知火フレア
            '常闇トワ' : ['#TOWART'],          #常闇トワ
            '姫森ルーナ' : ['#ルーナート'],      #姫森ルーナ
            # 'LUNA_tg' : ['#ルーナート','#セクシールーナート'],      #姫森ルーナ
            '桐生ココ' : ['#みかじ絵'],        #桐生ココ
            '角巻わため' : ['#つのまきあーと'],       #角巻わため
            # 'LAMY_tg' : ['#らみあ〜と', 'LamyArt'],      #雪花ラミィ
            '雪花ラミィ' : ['#LamyArt'],      #雪花ラミィ
            '獅白ぼたん' : ['#ししらーと'],      #獅白ぼたん
            '桃鈴ねね' : ['#ねねアルバム'],        #桃鈴ねね
            '魔乃アロエ' : ['#まのあろ絵'],       #魔乃アロエ
            '尾丸ポルカ' : ['#絵まる'],      #尾丸ポルカ

            'AZKi' : ['#AZKiART'],        #AZKI

            '森カリオペ' : ['#callillust'],   #森カリオペ
            '小鳥遊キアラ' : ['#絵ニックス'],       #小鳥遊キアラ
            '一伊那尓栖' : ['#inART','#いなート'],       #一伊那尓栖
            'がうる・ぐら' : ['#gawrt'],     #がうる・ぐら
            'ワトソン・アメリア' : ['#ameliaRT'],      #ワトソン・アメリア

            'アユンダ・リス' : ['#GambaRisu'],   #Ayunda Risu / アユンダ・リス
            'ムーナ・ホシノヴァ' : ['#HoshinovArt'],       #Moona Hoshinova / ムーナ・ホシノヴァ
            'アイラニ・イオフィフティーン' : ['#ioarts'],       #Airani Iofifteen / アイラニ・イオフィフティーン
            'クレイジー・オリー ' : ['#graveyART'],     #Kureiji Ollie / クレイジー・オリー 
            'アーニャ・メルフィッサ' : ['#anyatelier'],      #Anya Melfissa / アーニャ・メルフィッサ
            'パヴォリア・レイネ' : ['#Reinessance'],     #Pavolia Reine / パヴォリア・レイネ
            'アイリス' : ['#IRySart'],           #IRyS / アイリス
            'ベスティア・ゼータ' : ['#Zecretary'],       #vestiazeta / ベスティア・ゼータ
            'カエラ・コヴァルスキア' : ['#inKaela'],       #Kaela Kovalskia / カエラ・コヴァルスキア
            'こぼ・かなえる' : ['#AeruSeni'],       #kobokanaeru/こぼ・かなえる

            'ラプラス・ダークネス' : ['#Laplus_Artdesu'],     #ラプラス・ダークネス
            '鷹嶺ルイ' : ['#Luillust'],              #鷹嶺ルイ
            '博衣こより' : ['#こよりすけっち'],     #博衣こより
            '沙花叉クロヱ' : ['#さかまた飼育日記'],    #沙花叉クロヱ
            '風真いろは' : ['#いろはにも絵を'],      #風真いろは

            '九十九佐命/つくもさな' : ['#galaxillust'],           #九十九佐命/つくもさな
            'セレス・ファウナ' : ['#FineFaunart'],           #セレス・ファウナ
            'オーロ・クロニー' : ['#kronillust'],           #オーロ・クロニー
            '七詩ムメイ/ななしむめい' : ['#drawMEI'],           #七詩ムメイ/ななしむめい
            'ハコス・ベールズ' : ['#illustrayBAE'],           #ハコス・ベールズ
        }