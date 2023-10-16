import time
import json
import requests
from .METADATA import JOBCLASS
from .METADATA import SETTINGS

__all__ = ['change_settings', 'get_request', 'jobname_equalize', 'get_job_info', 'system_maintenance']

def change_settings(arg_time_out : int, arg_time_sleep : float):
    """
    request에 필요한 설정 값을 바꾸는 함수

    초기 설정 값은 각각 5초, 0.125초
        Args :
            arg_time_out(int) : 해당 시간동안 응답이 없으면 에러 처리한다
            
            arg_time_sleep(float) : 한 번의 요청 후 쉬는 시간
    """
    global SETTINGS
    SETTINGS['request_time_out'] = arg_time_out
    SETTINGS['request_time_sleep'] = arg_time_sleep

def get_request(arg_url):
    """
    url 입력시 data 가져오는 함수
    arg_url : 원하는 url 주소
    """

    # request.get 실패 할 경우 에러 발생시킴
    try:
        data = requests.get(arg_url, timeout = SETTINGS['request_time_out'])
    except:
        raise Exception("해당 url주소는 사용할 수 없습니다")    
    
    # 성공한다면 api 규칙에 따라 지정한 시간을 멈춘다
    time.sleep(SETTINGS['request_time_sleep'])

    # 데이터 저장
    data = json.loads(data.text)

    # request.get은 성공 했으나 받아온 데이터가 Open API 에서 error로 규정된 경우 에러 발생시킴
    if list(data.keys())[0] == 'error':  
        raise Exception(f"apikey혹은 url에 문제가 있습니다. 코드를 확인해주세요. error : {data}")
    else:    
        return data
    

def _next(arg_dict, arg_list):
    """
    get_job_info 함수를 위해 쓰이는 함수
    """
    if 'next' in arg_dict.keys():
        arg_list.append(arg_dict["jobGrowName"])
        return _next(arg_dict['next'], arg_list)
    else :
        arg_list.append(arg_dict["jobGrowName"])
        return arg_dict["jobGrowName"]


def get_job_info(arg_api_key):
    """
    직업 정보를 받아오는 함수
    전직명(각성명)을 1차 전직명으로 통일시키는 jobname_equalize 함수에 매개변수로 사용되는 객체를 반환함
    arg_api_key : Neople Open API key
    """
    data = get_request(f"https://api.neople.co.kr/df/jobs?apikey={arg_api_key}")
    job_list = []
    jobGroW_total_list = []
    for job in data['rows']:
        job_list.append(job['jobName'])
        jobGroW_list = []
        for jobGroW in job['rows']:
            job_lo = []
            _next(jobGroW, job_lo)
            jobGroW_list.append(job_lo)
        jobGroW_total_list.append(jobGroW_list)        
    job_info = dict(zip(job_list, jobGroW_total_list))
    return job_info


def jobname_equalize(arg_job_name : str, arg_job_grow_name : str ,arg_job_info : dict):
    """
    직업명과 전직명을 받으면 해당 전직명으로 반환
        Args :
            arg_job_name(str) : 직업명 ex) 총검사
            arg_job_grow_name(str) : 전직명 ex) 빅보스
            arg_job_info(dict) : get_job_info 함수를 통해 받은 직업 정보
        Retruns :
            해당 직업의 1차 전직명 ex) 히트맨
    """
    if (arg_job_name in ["다크나이트", "크리에이터"]) or (arg_job_grow_name in list(JOBCLASS.keys())):
        output = arg_job_name
    else:    
        for job in arg_job_info[arg_job_name]:
            if arg_job_grow_name in job:
                output = job
                break
        output = output[0]
    return output

def system_maintenance(arg_api_key: str):
    """
    현재 Neople Open API 서버가 점검중인지 확인하는 함수\\
    서버가 점검중이면 TRUE를 반환한다
        Args :
            arg_api_key : Neople Open API key
        Retruns : 
            boolean
    """
    try:
        data = requests.get(f"https://api.neople.co.kr/df/servers?apikey={arg_api_key}", timeout = SETTINGS['request_time_out'])
        time.sleep(SETTINGS['request_time_sleep'])
        data = json.loads(data.text)
    except:
        return False    
    if (list(data.keys())[0] == 'error') and (data['error']['status'] == 503): 
        return True
    else:
        return False

def explain_enchant(arg_enchant_dict):
    """
    마법부여 정보를 정리해주는 함수
    """
    if arg_enchant_dict == {}:
        return None
    output = ""
    if "status" in arg_enchant_dict.keys():
        output = ", ".join([f"{s['name']} {s['value']}" for s in arg_enchant_dict['status']])
    if "reinforceSkill" in arg_enchant_dict.keys():
        output = ", ".join([f"{s['name']} {s['value']}" for r in arg_enchant_dict['reinforceSkill'] for s in r['skills']]) + ", " + output 
    if "explain" in arg_enchant_dict.keys():
        output = arg_enchant_dict['explain'] + ", " + output
    return output

def is_attr(arg_object):
    """
    하위 속성이 있는지 확인하는 함수
    """
    try:
        arg_object.__dict__.keys()
        return True
    except:
        return False

def get_attr(arg_object, te = ""):
    """
    객체의 하위 속성명을 list로 만들어주는 함수
    """
    st = []
    for sub in list(arg_object.__dict__.keys()):
        if is_attr(getattr(arg_object, sub)) == False:
            if sub[0] != "_":
                st.append(te + sub)
        else :     
            st.append(get_attr(getattr(arg_object, sub), te + sub + "."))    
    return st    

def get_values(arg_object):
    """
    객체의 하위 속성값을 list로 만들어주는 함수
    """
    st = []
    for sub in list(arg_object.__dict__.keys()):
        if is_attr(getattr(arg_object, sub)) == False:
            if sub[0] != "_":
                st.append(getattr(arg_object, sub))
        else:
            st.append(get_values(getattr(arg_object, sub)))    
    return st    

def flatten(arg_list):
    result = []
    for item in arg_list:
        if isinstance(item, list):
            result += flatten(item)
        else:
            result.append(item)
    return result

def attr_flatten(arg_object):
    """
    객체를 입력받으면 모든 하위속성의 이름을 문자열 list로 반환한다
    """
    arg_object = get_attr(arg_object)
    arg_object = flatten(arg_object)
    return arg_object

def value_flatten(arg_object):
    """
    객체를 입력받으면 모든 하위속성의 값을 list로 반환한다
    """
    arg_object = get_values(arg_object)
    arg_object = flatten(arg_object)
    return arg_object

def one_slot(arg_equipment_list : list, arg_slot_name : str):
    """
    해당 부위의 정보만 반환하는 함수
        Args:
            arg_equipment_list(list) : 캐릭터 장비 데이터(dict)로 이루어진 list
            
            arg_slot_name(str) : 해당 장비의 이름
        Returns:
            해당 장비의 dict            
    """
    if arg_equipment_list == []:
        return None
    for equipment in arg_equipment_list:
        if equipment['slotId'] == arg_slot_name :
            return equipment
    return None