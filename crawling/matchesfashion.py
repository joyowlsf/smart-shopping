import re
from connection.s3_connection import *
from connection.web_connection import *
from file_settings.file_save import *

# 웹 접속
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}
url = "https://www.matchesfashion.com/us/mens/apac-sale?page=1&noOfRecordsPerPage=240&sort="
soup = web_connection(url,headers)

# 파일 이름
filename = "matchesfashion"

# 파일 저장
writer = file_save(filename)

# 마지막 페이지 길이
link = soup.select('.redefine__right__pager > li > a')


for i in range(1,int(link[2].text)+1):
    soup = web_connection(f"https://www.matchesfashion.com/us/mens/apac-sale?page={i}&noOfRecordsPerPage=240&sort=",headers=headers)
    item = soup.find_all('li',{'class':'lister__item'})

    for it in item:
        item_info = []

        # 편집샵 명
        shop_name = filename
        item_info.append(shop_name)

        # 브랜드명
        item_brand = it.select_one('.lister__item__title').text
        str_item_brand = re.sub('[^0-9a-zA-Z-./ ]','',item_brand)
        item_info.append(str_item_brand.strip().lower())

        # 아이템명
        item_name = it.select_one('.lister__item__details').text
        str_item_name = re.sub('[^0-9a-zA-Z-./ ]','',item_name)
        item_info.append(str_item_name.strip().lower())

        # 정가
        str_price = it.select_one('.lister__item__price > strike').text
        num_price = re.sub('[^0-9]','', str_price)
        # 달러 계산
        float_price = round(float(num_price) * 1216.92)
        item_info.append(float_price)

        # 할인가격
        str_down_price = it.select_one('.lister__item__price-down').text
        num_down_price = re.sub('[^0-9]','',str_down_price)
        # 달러 계산
        float_price = round(float(num_down_price) * 1216.92)
        item_info.append(float_price)

        # 제품url
        item_url="https://www.matchesfashion.com/" + it.select_one('div.lister__item__inner div a')['href']
        item_info.append(item_url)

        # 파일 저장
        writer.writerow(item_info)

# s3 파일 업로드
s3_upload_file(filename)
