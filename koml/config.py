VERSION='1.0.0'

'''
*: anything

*** 조사
_j: 조사 전체
_jks: 주격 조사
_jkc: 보격 조사
_jkg: 관형격 조사
_jko: 목적격 조사
_jkb: 부사격 조사
_jkv: 호격 조사
_jkq: 인용격 조사
_jx: 보조사

*** 어미 
_e: 어말 어미 전체
_ef: 종결 어미
_ec: 연결 어미

*** 부사
_m: 부사 전체
_mm: 관형사
_mag: 일반 부사
_maj: 접속 부사



**** 부호 및 외국어
_s: 부호 전체
_sf: 마침표, 물음표, 느낌표
_sn: 숫자
'''
WILDCARDS = ['*'] + \
    ['_j', '_jks', '_jkc', '_jkg', '_jko', '_jkb', '_jkv', '_jkq', '_jx'] + \
    ['_e', '_ef', '_ec'] + \
    ['_m', '_mm', '_mag', '_maj'] + \
    ['_s', '_sf', '_sn']


'''
** 받침 O/받침 X **
_i: 이/가(I_GA)
_eun: 은/는(EUN_NEUN)
_gwa: 과/와(GWA_WA)
_eul: 을/를(EUL_REUL)
_a: 아/야(A_YA)
_euro: 으로/로(EURO_RO)
_ix: 이/x(I_X)
'''
JOSAS = ['_i', '_eun',  '_gwa', '_eul', '_a', '_euro', '_ix']