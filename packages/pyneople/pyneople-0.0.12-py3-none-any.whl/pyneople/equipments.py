from .functions import get_request, explain_enchant, one_slot
from .METADATA import EQUIPMENT_LIST

class OptionInfo():
    def __init__(self):
        self.explain = None
    
    def get_option_info_data(self, arg_option_info_dict):
        try:
            self.explain = arg_option_info_dict['explain'].replace("'", "") # 얼음 땡 옵션 예외처리를 위한 replace
        except:
            pass    

class GrowInfo():
    def __init__(self):
        self.level = None
        self.exp_rate = None        
        self.option_1 = OptionInfo()
        self.option_2 = OptionInfo()
        self.option_3 = OptionInfo()
        self.option_4 = OptionInfo()  
    def get_grow_info_data(self, arg_grow_info_dict):
        try: 
            self.level = arg_grow_info_dict['level']
            self.exp_rate = arg_grow_info_dict['expRate']
            for i in range(4):
                exec(f"self.option_{i+1}.get_option_info_data(arg_grow_info_dict['options'][{i}])")
        except:
            pass

class Equipment():
    def __init__(self):
        self.item_name = None
        self.item_available_level = None
        self.item_rarity = None
        self.reinforce = None
        self.item_grade_name = None
        self.enchant = None
        self.amplification_name = None
        self.refine = None
        self.upgrade_info = None
        self.grow_info = GrowInfo() 
    
    def get_equipment_data(self, arg_equipment_dict):
        try:
            self.item_name = arg_equipment_dict['itemName'].replace("'", "").lower() # 이름
            self.item_available_level = arg_equipment_dict['itemAvailableLevel'] # 레벨 제한
            self.item_rarity = arg_equipment_dict['itemRarity'] # 레어도
            self.reinforce = arg_equipment_dict['reinforce'] # 강화수치             
            self.amplification_name = arg_equipment_dict['amplificationName'] # 차원의 기운 여부 ex 차원의 힘, 차원의 지능, None
            self.refine = arg_equipment_dict['refine'] # 제련   
        except:
            pass    

        try:
            self.item_grade_name = arg_equipment_dict['itemGradeName'] # 등금(최상~최하)
        except:
            pass   

        try:
            self.enchant = explain_enchant(arg_equipment_dict['enchant']) # 마법부여
        except:
            pass         

        try:
            self.upgrade_info = arg_equipment_dict["upgradeInfo"]['itemName'] # 융합장비
        except:
            pass

        try:
            self.grow_info.get_grow_info_data(arg_equipment_dict["fixedOption"]) # 105제 성장 장비 정보(고정 에픽)
        except:
            pass

        try:
            self.grow_info.get_grow_info_data(arg_equipment_dict["customOption"]) # 105제 성장 장비 정보(커스텀 에픽)
        except:
            pass


class BakalInfo():
    def __init__(self):
        self.option_1 = None
        self.option_2 = None
        self.option_3 = None
    def get_bakal_info_data(self, arg_bakal_info_dict):        
        try:
            self.option_1 = arg_bakal_info_dict['options'][0]['explain']
        except:
            pass

        try:
            self.option_2 = arg_bakal_info_dict['options'][1]['explain']
        except:
            pass

        try:
            self.option_3 = arg_bakal_info_dict['options'][2]['explain']
        except:
            pass                

class Weapon(Equipment):
    def __init__(self):
        super().__init__()
        self.bakal_info = BakalInfo()

    def get_equipment_data(self, arg_equipment_dict):
        super().get_equipment_data(arg_equipment_dict)
        try:
            self.bakal_info.get_bakal_info_data(arg_equipment_dict["bakalInfo"]) # 바칼 무기 융합
        except:
            pass                


class Equipments():
    
    def __init__(self, arg_api_key : str):
        """
        클래스 생성 시 Neople Open API key를 입력받는다
            Args :
                arg_api_key(str) : Neople Open API key
        """
        self.__api_key = arg_api_key
        self.weapon = Weapon()
        for equipment in EQUIPMENT_LIST[1:]:
            exec(f"self.{equipment} = Equipment()")

    def get_data(self, arg_server_id : str, arg_character_id : str):
        url = f'https://api.neople.co.kr/df/servers/{arg_server_id}/characters/{arg_character_id}/equip/equipment?apikey={self.__api_key}'
        data = get_request(url)
        data = data['equipment']
        for equipment in EQUIPMENT_LIST:
            try:
                exec(f"self.{equipment}.get_equipment_data(one_slot(data, '{equipment}'.upper()))")
            except:
                pass                 
    
