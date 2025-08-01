import dagster as dg
import requests
import pandas as pd
from .utils import get_bq_client, get_gcs_client
from google.cloud import bigquery
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())
import os

"""
GCS 버킷의 특정 경로에 파일이 업로드되면 트리거되는 센서 정의
API 데이터 수집 -> GCS 버킷 저장 -> 파이프라인 트리거 -> BigQuery 저장

post 함수는 트리거 되기 이후 작업을 수행합니다.
"""


@dg.asset
def dg06_fetch_gcs(context):
    """
    GCS 버킷에 저장된 데이터를 가져옵니다.
    """
    context.log.info(f"Loading data to GCS bucket: {os.getenv('GCS_BUCKET_NAME')}")
    df = pd.read_parquet(
        path=f'gs://{os.getenv('GCS_BUCKET_NAME')}/dagster_tutorial/sensor_data/brewery_data.parquet',
        storage_options=dict(token=os.getenv("GCS_CREDENTIALS_PATH"))
    )
    return df

@dg.asset
def dg06_load_bq(context, df):
    """
    Dataframe 형태로 저장된 데이터를 BigQuery에 저장합니다.
    """
    context.log.info(f"Loading data to BigQuery")
    client = get_bq_client()
            
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND
    )

    client.load_table_from_dataframe(
        dataframe=df,
        destination=f'airbyte.sensor_data',
        job_config=job_config
    )


@dg.job
def dg06_sensor_post_job():
    df = dg06_fetch_gcs()
    dg06_load_bq(df)


@dg.sensor(
    job=dg06_sensor_post_job,
    minimum_interval_seconds=60,
    default_status=dg.DefaultSensorStatus.STOPPED,
)
def dg06_gcs_sensor(context):
    """
    GCS 버킷의 특정 경로에 pokemon.csv 파일이 업로드되면 트리거되는 센서
    """
    client = get_gcs_client()

    bucket = client.get_bucket(os.getenv("GCS_BUCKET_NAME"))
    # 감지할 파일 경로 지정
    blob_path = "dagster_tutorial/sensor_data/brewery_data.parquet"
    blob = bucket.blob(blob_path)

    if blob.exists():
        context.log.info(f"{blob_path} 파일이 GCS에 존재합니다. 파이프라인을 트리거합니다.")
        yield dg.RunRequest(run_key=None)
    else:
        yield dg.SkipReason("No new files found")
        context.log.info(f"{blob_path} 파일이 아직 GCS에 없습니다.")
        
        # blob(파일)을 삭제하지 않고 단발성으로 한 번만 실행되는 센서를 만들고 싶다면,
        # 센서의 default_status를 STOPPED로 두고, 필요할 때만 수동으로 센서를 ON(START)해서 한 번만 트리거되도록 운영하는 것이 가장 간단합니다.
        # 또는, 센서 내부에서 context.instance.get_runs() 등을 활용해 이미 해당 blob로 트리거된 적이 있는지 체크하여
        # 중복 트리거를 방지할 수도 있습니다.
        #
        # 아래는 run_key에 blob의 고유값(예: updated time 등)을 넣어서, 같은 파일로는 한 번만 트리거되도록 하는 예시입니다.

        # if blob.exists():
        #     # 파일의 updated time을 run_key로 사용하여, 같은 파일로는 한 번만 트리거
        #     run_key = str(blob.updated) if blob.updated else None
        #     context.log.info(f"{blob_path} 파일이 GCS에 존재합니다. 파이프라인을 트리거합니다.")
        #     yield dg.RunRequest(run_key=run_key)
        # else:
        #     yield dg.SkipReason("No new files found")
        #     context.log.info(f"{blob_path} 파일이 아직 GCS에 없습니다.")

