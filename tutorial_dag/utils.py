import dagster as dg
from google.oauth2 import service_account
from google.cloud import bigquery
from google.cloud import storage
import os
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())


def get_bq_client():
    """
    GCP 클라이언트를 반환하는 함수
    """

    client = bigquery.Client(
        project=os.getenv("GCP_PROJECT_ID"),
        credentials=service_account.Credentials.from_service_account_file(os.getenv("GCP_CREDENTIALS_PATH")),
        location=os.getenv("GCP_LOCATION")
    )
    return client

def get_gcs_client():
    """
    GCS 클라이언트를 반환하는 함수
    """
    client = storage.Client(
        project=os.getenv("GCP_PROJECT_ID"),
        credentials=service_account.Credentials.from_service_account_file(os.getenv("GCP_CREDENTIALS_PATH"))
    )
    return client


def data_transformer(pandas_df):
    """
    MySQL에서 추출한 dataframe을 가공하는 함수
    """
    current_year = 2025

    try:
        # 도시 이름 컬럼 생성
        pandas_df["city"] = pandas_df["residence"].str.split().str[0]

        # 출생년도 컬럼 생성
        pandas_df['birthdate'] = pandas_df['birthdate'].astype(str)
        pandas_df["birthyear"] = pandas_df["birthdate"].str.slice(0, 4)

        # 혈액형 컬럼 생성
        pandas_df["blood"] = pandas_df["blood_group"].str.slice(0, -1)

        # 나이 컬럼 생성
        pandas_df["age"] = current_year - pandas_df["birthyear"].astype(int)

        # 나이가 0 이하인 데이터 제거
        pandas_df = pandas_df[pandas_df["age"] > 0].copy()

        # 나이대 컬럼 생성
        pandas_df["age_category"] = pandas_df["age"].apply(categorize_age)
        
        # 컬럼 순서 세팅
        df = pandas_df[["name", 'job', "sex", "city", "birthyear", "age", "blood", "age_category"]]
        
        return df

    except Exception as e:
        print(f"TRANSFORM 단계 오류 발생! : {e}")
        
        return False


def categorize_age(age):
    if age >= 100:
        return "90대 이상"
    else:
        return str(age // 10 * 10) + "대"