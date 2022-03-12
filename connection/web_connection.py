import requests
from bs4 import BeautifulSoup

# 웹 페이지 접속 함수
def web_connection(url,headers):
    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "lxml")

    except Exception as e:
        print(e)
    else:
        return soup



