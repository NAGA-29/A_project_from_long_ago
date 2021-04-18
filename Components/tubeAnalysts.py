from pprint import pprint

class Analyzer:
    
    def __init__(self, data_list) -> None:
        self.channel_id = data_list[0]
        self.sub = data_list[1]
        

    def ratio(self, data_list:list)->list:
        day_ratio = 0 #前日比
        week_ration = 0 #先週比
        month_ratio = 0 #先月比
        # 平均
        # 前日増加量
        # 先週増加量
        ratio = []
        return ratio