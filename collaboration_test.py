from difflib import SequenceMatcher
text = '【Miitopia】プロ級！？１時間でそっくりMii🌸みこ先輩編【天音かなた/ホロライブ】'

holo_dict = {
    'ときのそら' : ['ときのそら','そら','UCp6993wxpyDPHUpavwDFqgg'],
    'さくらみこ' : ['さくらみこ','みこ','エリート巫女','UC-hM6YJuNYVAmUWxeIr9FeA'],
    'ムーナ' : ['ムーナ','https://www.youtube.com/channel/', 'Moona Hoshinova']
}

if 'みこ' in text:
    print('コラボ')
else:
    print('シングル')

src = 'さくらみこ' 
s_len, t_len = len(src), len(text)

r = max([SequenceMatcher(None, src, text[i:i+s_len]).ratio() for i in range(t_len-s_len+1)])
print(r)