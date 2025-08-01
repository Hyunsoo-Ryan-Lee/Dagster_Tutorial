import dagster as dg
from .resources import bq_client, gcs_client

@dg.op(required_resource_keys={"bq_client"})
def dg09_list_bq_datasets(context):
    """
    BigQuery 데이터셋 목록 조회
    """
    bq_client = context.resources.bq_client
    datasets = [dataset.dataset_id for dataset in bq_client.list_datasets()]
    context.log.info(f"dataset list : {datasets}")
    return datasets

@dg.op(required_resource_keys={"gcs_client"})
def dg09_list_gcs_buckets(context):
    """
    GCS 버킷 목록 조회
    """
    gcs_client = context.resources.gcs_client
    buckets = [bucket.name for bucket in gcs_client.list_buckets()]
    context.log.info(f"bucket list : {buckets}")
    return buckets

# 3. job 정의: 파이프라인 역할
@dg.job
def dg09_gcp_resource_job():
    dg09_list_bq_datasets()
    dg09_list_gcs_buckets()
    
@dg.schedule(
    cron_schedule="0 8 * * *",
    job=dg09_gcp_resource_job,
    execution_timezone="Asia/Seoul"
)
def dg09_gcp_resource_schedule():
    return {}