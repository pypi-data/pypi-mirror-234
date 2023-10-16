from .functions import get_request

class Status():
    def __init__(self, arg_api_key : str):
        """
        클래스 생성 시 Neople Open API key를 입력받는다
            Args :
                arg_api_key(str) : Neople Open API key
        """
        self.__api_key = arg_api_key
        self.adventure_name = None
        self.guild_name = None
        self.adventure_level = None
        self.strength = None
        self.intellect = None
        self.health = None
        self.mentality = None
        self.fame = None

    def get_data(self, arg_server_id : str, arg_character_id : str):
        """
        캐릭터의 모험단명부터 명성등 정보를 반환한다
            Args:
                arg_server_id(str) :  서버 ID
                
                arg_character_id(str) : 캐릭터 ID
        """

        url = f'https://api.neople.co.kr/df/servers/{arg_server_id}/characters/{arg_character_id}/status?apikey={self.__api_key}'
        data = get_request(url)
        try:
            self.adventure_name = data['adventureName']
        except:
            pass
        try:
            self.guild_name = data['guildName']    
        except:
            pass
        try:
            self.adventure_level = data['buff'][0]['level']
        except:
            pass   
        try:             
            status_dict = dict()
            for item in data['status']:
                status_dict[item['name']] = item['value']                    
        except:
            pass        
        try:
            self.strength = status_dict["힘"]
        except:
            pass        
        try:
            self.intellect = status_dict["지능"]
        except:
            pass
        try:
            self.health = status_dict["체력"]
        except:
            pass                
        try:
            self.mentality = status_dict["정신력"]
        except:
            pass        
        try:
            self.fame = status_dict["모험가 명성"]
        except:
            pass        
        
        
        
        
        
