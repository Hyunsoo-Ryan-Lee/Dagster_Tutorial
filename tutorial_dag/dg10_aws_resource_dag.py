import dagster as dg
import pandas as pd
from .resources import s3_client, glue_client

@dg.op(required_resource_keys={"s3_client"})
def dg10_list_s3_buckets(context):
    """
    S3 버킷 목록 조회
    """
    s3_client = context.resources.s3_client
    response = s3_client.list_buckets()
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    context.log.info(f"bucket list : {buckets}")
    return buckets

@dg.op(required_resource_keys={"glue_client"})
def dg10_list_glue_crawlers(context):
    """
    Glue Crawler 목록 조회
    """
    glue_client = context.resources.glue_client
    response = glue_client.get_crawlers()
    crawlers = [crawler['Name'] for crawler in response['Crawlers']]
    context.log.info(f"crawler list : {crawlers}")
    return crawlers

# 3. job 정의: 파이프라인 역할
@dg.job
def dg10_aws_resource_job():
    dg10_list_s3_buckets()
    dg10_list_glue_crawlers()
    
@dg.schedule(
    cron_schedule="0 8 * * *",
    job=dg10_aws_resource_job,
    execution_timezone="Asia/Seoul"
)
def dg10_aws_resource_schedule():
    return {}