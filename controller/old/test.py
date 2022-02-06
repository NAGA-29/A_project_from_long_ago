import ast
from pprint import pprint
import json


str = "{\"signature\":\"3cf8225f9889474b37b6fe99fdf7e4a3\",\"event\":\"liveend\",\"movie\":{\"id\":\"697441027\",\"user_id\":\"c:nagaki\",\"title\":\"Live #697441027 / test\",\"subtitle\":null,\"last_owner_comment\":null,\"category\":null,\"link\":\"http://twitcasting.tv/c:nagaki/movie/697441027\",\"is_live\":false,\"is_recorded\":false,\"comment_count\":0,\"large_thumbnail\":\"http://imagegw03.twitcasting.tv/image3/image.twitcasting.tv/image78_1/03/1b/29921b03-1.jpg\",\"small_thumbnail\":\"http://imagegw03.twitcasting.tv/image3/image.twitcasting.tv/image78_1/03/1b/29921b03-1-s.jpg\",\"country\":\"jp\",\"duration\":114,\"created\":1629384225,\"is_collabo\":false,\"is_protected\":false,\"max_view_count\":0,\"current_view_count\":0,\"total_view_count\":0,\"hls_url\":null},\"broadcaster\":{\"id\":\"c:nagaki\",\"screen_id\":\"c:nagaki\",\"name\":\"naga\",\"image\":\"http://twitcasting.tv/img/twitcas_bigger_8.png\",\"profile\":\"\",\"level\":1,\"last_movie_id\":\"697441027\",\"is_live\":false,\"supporter_count\":0,\"supporting_count\":0,\"created\":0}}"
# s = ast.literal_eval(str)
s = json.loads(str)

pprint(s)