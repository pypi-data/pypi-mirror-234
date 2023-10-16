from .functions import get_request, one_slot
from .METADATA import EQUIPMENT_LIST, AVATAR_LIST, PLATINUM_AVATAR_LIST

class BuffAvatar():
    def __init__(self):
        self.item_name = None
    def get_buff_avatar_data(self, arg_avatar_dict):
        try: 
            self.item_name = arg_avatar_dict['itemName']
        except:
            pass
class BuffPlatimun(BuffAvatar):
    def __init__(self):
        super().__init__()    
        self.option = None
        self.platinum = None
    
    def get_buff_avatar_data(self, arg_avatar_dict):
        super().get_buff_avatar_data(arg_avatar_dict)
        try:
            self.option = arg_avatar_dict['optionAbility']
        except:
            pass
        try:    
            self.platinum = arg_avatar_dict['emblems'][0]['itemName']
        except:
            pass    

class Buff():
    def __init__(self, arg_api_key):
        """
        클래스 생성 시 Neople Open API key를 입력받는다
            Args :
                arg_api_key(str) : Neople Open API key
        """        
        self.__api_key = arg_api_key    
        self.buff_level = None
        self.buff_desc = None
        for equipment in EQUIPMENT_LIST:
            exec(f"self.buff_equipment_{equipment} = None")
        for avatar in list(set(AVATAR_LIST) - set(PLATINUM_AVATAR_LIST)):
            exec(f"self.buff_avatar_{avatar} = BuffAvatar()")
        for avatar in PLATINUM_AVATAR_LIST:
            exec(f"self.buff_avatar_{avatar} = BuffPlatimun()")
        self.buff_creature = None           
    
    def get_data(self, arg_server_id : str, arg_character_id : str):
        data = get_request(f"https://api.neople.co.kr/df/servers/{arg_server_id}/characters/{arg_character_id}/skill/buff/equip/equipment?apikey={self.__api_key}")
        data = data['skill']['buff']
        
        if data:
            try:
                for index, value in enumerate(data['skillInfo']['option']['values']):
                    data['skillInfo']['option']['desc'] = data['skillInfo']['option']['desc'].replace("{" + f"value{index + 1}" + "}", value)
                self.buff_level = data['skillInfo']['option']['level']
                self.buff_desc = data['skillInfo']['option']['desc']
            except:
                pass    
        if data:
            data = data['equipment']
        if data:
            for equipment in EQUIPMENT_LIST:
                try:    
                    exec(f"self.buff_equipment_{equipment} = one_slot(data, '{equipment.upper()}')['itemName']")
                except:
                    pass    
        
        data = get_request(f"https://api.neople.co.kr/df/servers/{arg_server_id}/characters/{arg_character_id}/skill/buff/equip/avatar?apikey={self.__api_key}")
        data = data['skill']['buff']
        if data:
            data = data['avatar']
        if data:
            for avatar in AVATAR_LIST:            
                try:
                    exec(f"self.buff_avatar_{avatar}.get_buff_avatar_data(one_slot(data, '{avatar.upper()}'))") 
                except:
                    pass    
        data = get_request(f"https://api.neople.co.kr/df/servers/{arg_server_id}/characters/{arg_character_id}/skill/buff/equip/creature?apikey={self.__api_key}")
        data = data['skill']['buff']
        if data:
            try:
                self.buff_creature = data['creature'][0]['itemName']
            except:
                pass    
