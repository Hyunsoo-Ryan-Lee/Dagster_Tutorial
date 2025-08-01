import dagster as dg
import requests
import pandas as pd
from .utils import get_gcs_client
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())
import os


"""
GCS 버킷의 특정 경로에 파일이 업로드되면 트리거되는 센서 정의
API 데이터 수집 -> GCS 버킷 저장 -> 파이프라인 트리거 -> BigQuery 저장

pre 함수는 트리거 되기 이전 작업을 수행합니다.  
"""

@dg.asset
def dg06_fetch_api(context):
    """
    API 데이터를 가져옵니다.
    """
    URL = 'https://api.openbrewerydb.org/v1/breweries'
    response = requests.get(URL)
    return response.json()

@dg.asset
def dg06_transform_api(context, fetch_api):
    """
    API 데이터를 Dataframe 형태로 변환합니다.
    """
    df = pd.json_normalize(fetch_api)
    return df


@dg.asset
def dg06_load_gcs(context, df):
    """
    Dataframe 형태의 API 데이터를 GCS에 저장합니다.
    """
    context.log.info(f"Loading data to GCS bucket: {os.getenv('GCS_BUCKET_NAME')}")
    df.to_parquet(
        path=f'gs://{os.getenv('GCS_BUCKET_NAME')}/dagster_tutorial/sensor_data/brewery_data.parquet',
        engine='pyarrow',
        compression='gzip',
        index=False,
        storage_options=dict(token=os.getenv("GCS_CREDENTIALS_PATH"))
        )


@dg.job
def dg06_sensor_pre_job():
    fetch_api = dg06_fetch_api()
    df = dg06_transform_api(fetch_api)
    dg06_load_gcs(df)
    
@dg.schedule(cron_schedule="0 8 * * *", job=dg06_sensor_pre_job)
def dg06_sensor_pre_schedule():
    return {}




