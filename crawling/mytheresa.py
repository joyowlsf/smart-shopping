from connection.s3_connection import *
import re
from connection.web_connection import *
from file_settings.file_save import *

# 웹 접속
url = "https://www.mytheresa.com/en-us/men/sale.html?p=1"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}
soup = web_connection(url,headers)

# 파일 이름
filename = "mytheresa"

# 파일 저장
writer = file_save(filename)

for i in range(1,60):
    soup = web_connection(f"https://www.mytheresa.com/en-us/men/sale.html?p={i}",headers=headers)
    item = soup.find_all('li',{'class' : 'item'})

    for it in item:
        item_info = []

        # 편집샵 명
        shop_name = filename
        item_info.append(shop_name)

        # 브랜드명
        item_brand = it.find('span',{'class' : 'ph1'}).text
        str_item_brand = re.sub('[^0-9a-zA-Z-./ ]', '', item_brand)
        item_info.append(str_item_brand.strip().lower())

        # 아이템명
        item_name = it.select_one('h2.product-name > a').text
        str_item_name = re.sub('[^0-9a-zA-Z-./ ]', '', item_name)
        item_info.append(str_item_name.strip().lower())

        # 정가
        try:
            str_price = it.select_one('.old-price > span').text
            num_price = re.sub('[^0-9]', '', str_price)
            # 달러 계산
            float_price = round(float(num_price) * 1216.92)
            item_info.append(float_price)
        except Exception as e:
            print(e)
            continue

        # 할인가격
        try:
            str_down_price = it.select_one('.special-price > span').text
            num_down_price = re.sub('[^0-9]', '', str_down_price)
            # 달러 계산
            float_down_price = round(float(num_down_price) * 1216.92)
            item_info.append(float_down_price)
        except Exception as e:
            print(e)
            continue

        # 제품url
        item_url = it.select_one('li.item a')['href']
        item_info.append(item_url)

        # 파일 저장
        writer.writerow(item_info)


# s3 파일 업로드
s3_upload_file(filename)





