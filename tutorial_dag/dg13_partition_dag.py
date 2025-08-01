import dagster as dg
import pandas as pd
import os
from .resources import postgres_connection
from .utils import data_transformer
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())


# 1. 파티션 정의
user_data_partitions_def = dg.DailyPartitionsDefinition(
    start_date="2025-03-01",
    end_date="2025-06-30"
)

# 2. 파티션 적용 asset
@dg.op
def dg13_read_source_data(context):
    """
    GCS 파일 읽기
    """
    partition_date = context.partition_key  # 'YYYY-MM-DD' 형식
    parquet_path = f"gs://{os.getenv('GCS_BUCKET_NAME')}/dataset/user_data.parquet"
    context.log.info(f"Reading Parquet file from {parquet_path} for partition {partition_date} ...")
    df = pd.read_parquet(
        path=parquet_path, 
        storage_options=dict(token=os.getenv("GCS_CREDENTIALS_PATH"))
    )
    df = df[df["credate"] == partition_date]
    return df

@dg.op
def dg13_transform_data(context, df):
    """
    Dataframe 가공
    """
    partition_date = context.partition_key  # 'YYYY-MM-DD' 형식
    context.log.info(f"Transforming data for partition {partition_date} ...")
    df = data_transformer(df)
    df['partition_date'] = partition_date
    return df

@dg.op(required_resource_keys={"postgres_connection"})
def dg13_load_postgres(context, df):
    """
    Postgres DB에 파일 저장
    """
    partition_date = context.partition_key  # 'YYYY-MM-DD' 형식
    context.log.info(f"Saving data to Postgres for partition {partition_date} ...")
    # 파티션 경로를 partition_date로 지정
    postgres_conn = context.resources.postgres_connection
    context.log.info(f"Saving to {postgres_conn}")
    df.to_sql(
        name="dagster_user",
        con=postgres_conn,
        if_exists="append",
        index=False
    )

# 3. 파티션 job 정의
@dg.job(partitions_def=user_data_partitions_def)
def dg13_partition_job():
    df = dg13_read_source_data()
    df = dg13_transform_data(df)
    dg13_load_postgres(df)


@dg.schedule(
    cron_schedule="0 8 * * *",
    job=dg13_partition_job,
    execution_timezone="Asia/Seoul"
)
def dg13_partition_schedule():
    """
    매일 0시에 실행되는 파티션 파이프라인 스케줄러
    """
    return {}


