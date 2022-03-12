import re
from connection.web_connection import *
from connection.s3_connection import *
from file_settings.file_save import *

# 웹 접속
url = "https://www.yoox.com/us/men/sale/shoponline#/dept=salemen&gender=U&page=1&season=X"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}
soup = web_connection(url,headers)

# 파일 이름
filename = "yoox"

# 파일 저장
writer = file_save(filename)

# 마지막 페이지 길이
link=soup.select('li.text-light')


for i in range(1,int(link[5].text)+1):
    soup = web_connection(url,headers)
    item = soup.find_all('div', {'class': 'col-8-24'})

    for it in item:
        item_info = []

        # 편집샵 명
        shop_name = filename
        item_info.append(shop_name)

        # 브랜드명
        try:
            item_brand = it.select_one('a.itemlink > div').text
            str_item_brand = re.sub('[^0-9a-zA-Z-./ ]', '', item_brand)
            item_info.append(str_item_brand.strip().lower())
        except Exception as e:
            print(e)
            continue

        # 아이템명
        try:
            item_name = it.select_one('div.microcategory').text.strip()
            str_item_brand = re.sub('[^0-9a-zA-Z-./ ]', '', item_name)
            item_info.append(str_item_brand.strip().lower())
        except Exception as e:
            print(e)
            continue

        # 정가
        try:
            str_price = it.select_one('div.oldprice-wrapper').text
            num_price = re.sub('[^0-9.]','', str_price)
            # 달러 계산
            float_price = round(float(num_price) * 1216.92)
            item_info.append(float_price)
        except Exception as e:
            print(e)
            continue

        # 할인가격
        try:
            str_down_price = it.find('div',{'class' : 'retail-newprice font-bold'}).text
            num_down_price = re.sub('[^0-9.]','',str_down_price)
            # 달러 계산
            float_down_price = round(float(num_down_price) * 1216.92)
            item_info.append(float_down_price)
        except Exception as e:
            print(e)
            continue

        # 제품url
        try:
            item_url='https://www.yoox.com/'+it.select_one('a.itemlink')['href']+'&cod10=14116773NA&sizeId=-1'
            item_info.append(item_url)
        except Exception as e:
            print(e)
            continue

        # 파일 저장
        writer.writerow(item_info)

# s3 파일 업로드
s3_upload_file(filename)