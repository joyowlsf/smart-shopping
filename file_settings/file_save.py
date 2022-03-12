import csv
import datetime
from file_settings.directory_create import createFolder

# 수집 날짜
collection_date = datetime.datetime.now().date()

# 파일 저장 함수
def file_save(filename):

    # 파일 이름
    filename = "{}_{}.csv".format(filename,collection_date)

    # 디렉토리 생성
    createFolder("C:/Users/YONG/PycharmProjects/ smart_shopping/crawling/data/{}/".format(collection_date))

    # 저장 경로
    path = "C:/Users/YONG/PycharmProjects/ smart_shopping/crawling/data/{}/".format(collection_date) + filename

    # 파일 열기
    f = open(path, "w", encoding="utf-8-sig", newline="")
    writer = csv.writer(f)

    # # 타이틀 제목
    # title ="shop_name item_brand item_name item_price item_down_price item_url".split()
    # writer.writerow(title)

    return writer

