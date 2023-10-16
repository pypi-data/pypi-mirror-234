from .functions import get_request, one_slot
from .METADATA import AVATAR_LIST

class Avatar():
    def __init__(self):
        self.item_name = None
        self.item_rarity = None
        self.option_ability = None
        self.emblem_1 = None
        self.emblem_2 = None
        self.emblem_3 = None        
    def get_avatar_data(self, arg_avatar_dict):
        
        try:
            self.item_name = arg_avatar_dict["itemName"]
            self.item_rarity = arg_avatar_dict["itemRarity"]
        except:
            pass    
        
        try:
            self.option_ability = arg_avatar_dict["optionAbility"]
        except:
            pass
        
        try:    
            for index, emblem in enumerate(arg_avatar_dict['emblems']):
                exec(f"self.emblem_{index+1} = '{emblem['itemName']}'")
        except:
            pass        


class Avatars():
    def __init__(self, arg_api_key):
        """
        클래스 생성 시 Neople Open API key를 입력받는다
            Args :
                arg_api_key(str) : Neople Open API key
        """        
        self.__api_key = arg_api_key  
        for avatar in AVATAR_LIST:
            exec(f"self.{avatar} = Avatar()")  

    def get_data(self, arg_server_id, arg_character_id):    
        url = f'https://api.neople.co.kr/df/servers/{arg_server_id}/characters/{arg_character_id}/equip/avatar?apikey={self.__api_key}'
        data = get_request(url)
        data = data['avatar'] 
        for avatar in AVATAR_LIST:
            try:
                exec(f"self.{avatar}.get_avatar_data(one_slot(data, '{avatar}'.upper()))")
            except:
                pass    
