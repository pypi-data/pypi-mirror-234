import datetime
from .functions import get_request

class Timeline():
    
    def __init__(self, arg_api_key : str):
        """
        클래스 생성 시 Neople Open API key를 입력받는다
            Args :
                arg_api_key(str) : Neople Open API key
        """
        self.__api_key = arg_api_key
    
    def get_data(self, arg_server_id : str, arg_character_id : str, arg_end_date : str, arg_last_end_date : str = "2017-09-21 00:00", arg_last_end_data : dict or None = None, arg_limit : int = 100, arg_code : int or str = "", arg_print_log : bool = False):
        """
        서버ID와 캐릭터ID 원하는 수집시간(arg_end_date)을 입력받으면 타임라인데이터를 반환한다.
            Args :
                arg_server_id(str) : 서버ID ex) cain
                
                arg_character_id(str) : 캐릭터ID 
                
                arg_end_date(str) : 이 시간까지 수집을 한다 ex) 2023-03-03 15:57
                
                arg_last_end_date(str) : 이 시간부터 수집을 한다 ex) 2018-03-03 15:57
                
                arg_last_end_data(dict) : 지금까지 수집한 해당 캐릭터의 마지막 타임라인 데이터
                
                arg_limit(int) : 한번 request할 때 수집 할 타임라인 데이터의 개수
                
                arg_code(int) : 수집하고 싶은 타임라인 코드 ex)201, 202 참조) https://developers.neople.co.kr/contents/guide/pages/all 
                
                arg_print_log(boolean) : 데이터 수집의 과정의 print 여부   
        """
        self.timeline = []
        
        end_date = datetime.datetime.strptime(arg_end_date, '%Y-%m-%d %H:%M')
        start_date = end_date - datetime.timedelta(days=90)
        if start_date < datetime.datetime.strptime(arg_last_end_date, '%Y-%m-%d %H:%M'):
            start_date = datetime.datetime.strptime(arg_last_end_date, '%Y-%m-%d %H:%M')
        next = ""
        while start_date < end_date:
            stop = False
            url = f"""https://api.neople.co.kr/df/servers/{arg_server_id}/characters/{arg_character_id}/timeline?limit={arg_limit}&code={arg_code}&startDate={start_date.strftime('%Y-%m-%d %H:%M')}&endDate={end_date.strftime('%Y-%m-%d %H:%M')}&next={next}&apikey={self.__api_key}"""
            if arg_print_log:
                print(f"서버 = {arg_server_id}, 캐릭터 = {arg_character_id} 시작 = {start_date.strftime('%Y-%m-%d %H:%M')}, 끝 = {end_date.strftime('%Y-%m-%d %H:%M')}")
            data = get_request(url)
            next = data['timeline']['next']

            # 데이터가 있다면
            if data['timeline']['rows']:                 
                for log in data['timeline']['rows']:
                    if log == arg_last_end_data:
                        stop = True
                        break
                    else:
                        self.timeline.append(log)
                # 마지막으로 수집된 타임라인 데이터와 일치하는 항목이 있다면
                if stop:
                    break        

            # 타임라인데이터가 있고 마지막 로그가 캐릭터 생성이라면
            if self.timeline and self.timeline[-1]['code'] == 101:
                print("캐릭터 생성 로그를 확인했습니다")
                break

            # 해당기간에 next 데이터가 있으면
            if next:
                continue
            # 해당기간에 next 없으면
            else:
                end_date = start_date
                start_date = end_date - datetime.timedelta(days=90)
                if start_date < datetime.datetime.strptime(arg_last_end_date, '%Y-%m-%d %H:%M'):
                    start_date = datetime.datetime.strptime(arg_last_end_date, '%Y-%m-%d %H:%M')
                next = ""    
                continue                     

