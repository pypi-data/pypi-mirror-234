from .functions import get_request

class Flag():
    def __init__(self):
        self.item_rarity = None
        self.reinforce = None
        self.gem_1 = None
        self.gem_2 = None
        self.gem_3 = None
        self.gem_4 = None
    
    def get_flag_data(self, arg_flag_dict):
        try:
            self.item_rarity = arg_flag_dict['itemRarity']
            self.reinforce = arg_flag_dict['reinforce']
        except: 
            pass    
        try:
            arg_flag_dict = [gem['itemRarity'] for gem in arg_flag_dict['gems']]
        except:
            pass    
        for index, gem in enumerate(arg_flag_dict):
            try: 
                exec(f"self.gem_{index+1} = '{gem}'") 
            except:
                pass    

class Talismans():
    def __init__(self):
        self.item_name = None
        self.rune_1 = None
        self.rune_2 = None
        self.rune_3 = None
    def get_talismans_data(self, arg_talismans_dict):
        try: 
            self.item_name = arg_talismans_dict['talisman']['itemName']
        except:
            pass    
        try:
            arg_talismans_dict = [rune['itemName'] for rune in arg_talismans_dict['runes']]
        except:
            pass

        for index, rune in enumerate(arg_talismans_dict):
            try:
                exec(f"self.rune_{index+1} = '{rune}'")         
            except:
                pass    

class Others():
    def __init__(self, arg_api_key):
        """
        클래스 생성 시 Neople Open API key를 입력받는다
            Args :
                arg_api_key(str) : Neople Open API key
        """
        self.__api_key = arg_api_key
        self.creature = None
        self.flag = Flag()
        self.talisman_1 = Talismans()
        self.talisman_2 = Talismans()
        self.talisman_3 = Talismans()

    def get_data(self, arg_server_id, arg_character_id):
        
        
        # 크리쳐
        url = f"https://api.neople.co.kr/df/servers/{arg_server_id}/characters/{arg_character_id}/equip/creature?apikey={self.__api_key}"
        data = get_request(url)
        data = data["creature"]
        try:
            self.creature = data['itemName']
        except:
            pass    

        # 휘장
        url = f"https://api.neople.co.kr/df/servers/{arg_server_id}/characters/{arg_character_id}/equip/flag?apikey={self.__api_key}" 
        data = get_request(url)
        data = data["flag"]
        try:
            self.flag.get_flag_data(data)
        except:
            pass    

        # 탈리스만
        url = f"https://api.neople.co.kr/df/servers/{arg_server_id}/characters/{arg_character_id}/equip/talisman?apikey={self.__api_key}" 
        data = get_request(url)
        data = data["talismans"]
        try:
            for index, talismans_dict in enumerate(data):
                exec(f"self.talisman_{index+1}.get_talismans_data(talismans_dict)")
        except:
            pass    