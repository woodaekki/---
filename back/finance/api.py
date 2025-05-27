import requests
from django.conf import settings

def fetch_deposit_products():
    url = 'https://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'
    params = {
        'auth': settings.FIN_API_KEY,
        'topFinGrpNo': '020000',   # 은행
        'pageNo': 1
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        # 에러 로깅 또는 예외 처리
        return None

def fetch_saving_products():
    url = 'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json'
    params = {
        'auth': settings.FIN_API_KEY,
        'topFinGrpNo': '020000',   # 은행
        'pageNo': 1
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        # 에러 로깅 또는 예외 처리
        return None