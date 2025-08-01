import dagster as dg
import pandas as pd
from .resources import api_client

# 2. op 정의: API를 호출해서 데이터 가져오기
@dg.op(required_resource_keys={"api_client"})
def dg_07_get_breweries(context):
    """
    API를 호출해서 데이터 가져오기
    """
    client = context.resources.api_client
    response = client["session"].get(client["base_url"])  # API 호출
    data = response.json()
    context.log.info(f"Got {len(data)} breweries!")
    return data

@dg.op
def dg_07_transform_breweries(context, get_breweries):
    """
    API 데이터를 Dataframe 형태로 변환
    """
    df = pd.json_normalize(get_breweries)
    context.log.info(f"Transformed {df.head()} breweries!")
    return df

# 3. job 정의: 파이프라인 역할
@dg.job
def dg07_api_resource_job():
    breweries = dg_07_get_breweries()
    dg_07_transform_breweries(breweries)
    
@dg.schedule(
    cron_schedule="0 8 * * *",
    job=dg07_api_resource_job,
    execution_timezone="Asia/Seoul"
)
def dg07_api_resource_schedule():
    return {}