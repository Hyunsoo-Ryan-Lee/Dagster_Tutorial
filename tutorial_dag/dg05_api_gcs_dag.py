import dagster as dg
import requests
import pandas as pd
from .utils import get_bq_client
from google.cloud import bigquery
from dotenv import find_dotenv, load_dotenv
import os

load_dotenv(find_dotenv())

@dg.op
def dg05_fetch_api(context):
    """
    API 데이터를 가져옵니다.
    """
    URL = 'https://api.openbrewerydb.org/v1/breweries'
    response = requests.get(URL)
    return response.json()

@dg.op
def dg05_transform_api(context, fetch_api):
    """
    API 데이터를 Dataframe 형태로 변환합니다.
    """
    df = pd.json_normalize(fetch_api)
    return df


@dg.op
def dg05_load_gcs(context, df):
    """
    Dataframe 형태의 API 데이터를 GCS에 저장합니다.
    """
    context.log.info(f"Loading data to GCS bucket: {os.getenv('GCS_BUCKET_NAME')}")
    df.to_parquet(
        path=f'gs://{os.getenv('GCS_BUCKET_NAME')}/dagster_tutorial/brewery_data.parquet',
        engine='pyarrow',
        compression='gzip',
        index=False,
        storage_options=dict(token=os.getenv("GCS_CREDENTIALS_PATH"))
        )

@dg.op
def dg05_load_bq(context, df):
    """
    Dataframe 형태의 API 데이터를 BigQuery에 저장합니다.
    """
    context.log.info(f"Loading data to BigQuery")
    client = get_bq_client()
            
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND
    )

    client.load_table_from_dataframe(
        dataframe=df,
        destination=f'airbyte.brewery_data',
        job_config=job_config
    )


@dg.job
def dg05_api_gcs_job():
    fetch_api = dg05_fetch_api()
    df = dg05_transform_api(fetch_api)
    dg05_load_gcs(df)
    dg05_load_bq(df)

@dg.schedule(
    cron_schedule="0 8 * * *",
    job=dg05_api_gcs_job,
    execution_timezone="Asia/Seoul"
)
def dg05_api_gcs_schedule():
    return {}