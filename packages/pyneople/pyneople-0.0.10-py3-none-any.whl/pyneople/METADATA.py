# 초기 설정값
SETTINGS = {
    "request_time_out" : 5,
    "request_time_sleep" : 0.125
}

# 서버 NAME 이 key ID 가 value
SERVER_NAME_2_ID = {
    "안톤" : "anton",
    "바칼" : "bakal",
    "카인" : "cain",
    "카시야스" : "casillas",
    "디레지에" : "diregie",
    "힐더" : "hilder",
    "프레이" : "prey",
    "시로코" : "siroco"
    }

# 서버 ID 문자열 길이의 최대값
SERVERLENGTH = max(list(map(lambda x : len(x), list(SERVER_NAME_2_ID.values()))))

# 서버 ID 가 key NAME 이 value
SERVER_ID_2_NAME = {v : k for k , v in SERVER_NAME_2_ID.items()}

# 직업명
JOBCLASS = {
    "귀검사(남)" : ["웨펀마스터", "버서커", "소울브링어", "아수라", "검귀"],
    "격투가(남)" : ["넨마스터", "스트리트파이터", "그래플러", "스트라이커"],
    "거너(남)" : ["레인저", "메카닉", "런처", "스핏파이어", "어썰트"],
    "마법사(남)" : ["블러드 메이지", "엘레멘탈 바머", "빙결사", "디멘션워커", "스위프트 마스터"],
    "프리스트(남)" : ["크루세이더", "퇴마사", "인파이터", "어벤저"],
    "귀검사(여)" : ["소드마스터", "데몬슬레이어", "다크템플러", "베가본드", "블레이드"],
    "격투가(여)" : ["넨마스터", "스트리트파이터", "그래플러", "스트라이커"],
    "거너(여)" : ["레인저", "메카닉", "런처", "스핏파이어"],
    "마법사(여)" : ["엘레멘탈마스터", "마도학자", "소환사", "배틀메이지", "인챈트리스"],
    "프리스트(여)" : ["크루세이더", "이단심판관", "미스트리스", "무녀"],
    "도적" : ["로그", "쿠노이치", "섀도우댄서", "사령술사"],
    "나이트" : ["엘븐나이트", "카오스", "드래곤나이트", "팔라딘"],
    "마창사" : ["뱅가드", "듀얼리스트", "다크 랜서", "드래고니안 랜서"],
    "총검사" : ["요원", "트러블 슈터", "히트맨", "스페셜리스트"],
    "외전" : ["다크나이트", "크리에이터"],
    "아처" : ["뮤즈", "트래블러"]
}

jobclass_list = [item for sublist in list(JOBCLASS.values()) for item in sublist]

# 1차 전직명 문자열 길이의 최대값
JOB_GROW_NAME_LENGTH = max(list(map(lambda x : len(x), jobclass_list)))

# 직업명 문자열 길이의 최대값
JOB_NAME_LENGTH = max(list(map(lambda x : len(x), list(JOBCLASS.keys()))))

del jobclass_list

# 착용가능 장비
EQUIPMENT_LIST = ['weapon', 'title', 'jacket', 'shoulder', 'pants', 'shoes', 'waist', 'amulet', 'wrist', 'ring', 'support', 'magic_ston', 'earring']

# 착용가능 아바타
AVATAR_LIST = ['headgear', 'hair', 'face', 'jacket', 'pants', 'shoes', 'breast', 'waist', 'skin', 'aurora', 'weapon']

# 플래티넘 엠블렘 착용 가능 부위
PLATINUM_AVATAR_LIST = ['jacket', 'pants']