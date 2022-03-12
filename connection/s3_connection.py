import boto3
from file_settings import file_save


# s3 접속 함수
def s3_connection():
    try:
        s3 = boto3.client(
            service_name="s3",
            region_name="ap-northeast-2",
            aws_access_key_id="AKIAS27VBE5WCLOVVEUY",
            aws_secret_access_key="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",
        )
    except Exception as e:
        print(e)
    else:
        print("s3 bucket connected!")
        return s3



# S3로 파일 업로드 함수
def s3_upload_file(filename):
    s3 = s3_connection()
    filename = "{}_{}.csv".format(filename, file_save.collection_date)
    try:
        s3.upload_file("data/{}/{}".format(file_save.collection_date, filename),
                       "s3-yong",
                       "smart_shopping_data/{}/{}".format(file_save.collection_date, filename))
    except Exception as e:
        print(e)





