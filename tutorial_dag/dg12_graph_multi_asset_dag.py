import dagster as dg
import pandas as pd
from .resources import api_client, mysql_connection, postgres_connection

"""
API 호출 작업 그룹
"""
@dg.op(required_resource_keys={"api_client"})
def dg12_get_breweries(context):
    """
    API 호출 작업
    """
    client = context.resources.api_client
    response = client["session"].get(client["base_url"])  # API 호출
    data = response.json()
    context.log.info(f"Got {len(data)} breweries!")
    return data

@dg.op
def dg12_transform_breweries(context, data):
    """
    API 데이터 변환 작업
    """
    df = pd.json_normalize(data)
    context.log.info(f"Transformed {df.head()} breweries!")
    return df

@dg.graph_asset
def dg12_api_graph():
    """
    API 호출 작업 그룹
    """
    data = dg12_get_breweries()
    tdf = dg12_transform_breweries(data)
    print(f"tdf: {tdf}")
    return tdf


"""
데이터베이스 작업 그룹
"""
@dg.op(required_resource_keys={"mysql_connection"})
def dg12_extract_mysql(context):
    """
    MYSQL 데이터베이스 조회 작업
    """
    mysql_conn = context.resources.mysql_connection
    mysql_df = pd.read_sql_table("tips", mysql_conn)
    print(f"mysql_df: {mysql_df}")
    return mysql_df

@dg.op(required_resource_keys={"postgres_connection"})
def dg12_extract_postgres(context):
    """
    POSTGRES데이터베이스 조회 작업
    """
    postgres_conn = context.resources.postgres_connection
    postgres_df = pd.read_sql_table("user_summary", postgres_conn)
    print(f"postgres_df: {postgres_df}")
    return postgres_df

@dg.graph_multi_asset(
    outs={
        "mysql_df": dg.AssetOut(),
        "postgres_df": dg.AssetOut()
    }
)
def dg12_db_graph():
    """
    데이터베이스 작업 그룹
    """
    mysql_df = dg12_extract_mysql()
    postgres_df = dg12_extract_postgres()
    # mysql_df = dg11_mysql_transform(mysql_df)
    # postgres_df = dg11_postgres_transform(postgres_df)

    return mysql_df, postgres_df

@dg.asset
def dg12_mysql_transform(context, mysql_df):
    context.log.info(f"Transformed {mysql_df.head()} mysql_df!")
    return mysql_df

@dg.asset
def dg12_postgres_transform(context, postgres_df):
    context.log.info(f"Transformed {postgres_df.head()} postgres_df!")
    return postgres_df

@dg.job
def dg12_graph_multi_asset_job():
    api_df = dg12_api_graph()
    mysql_df, postgres_df = dg12_db_graph()
    mysql_df = dg12_mysql_transform(mysql_df)
    postgres_df = dg12_postgres_transform(postgres_df)
    api_tdf = dg12_postgres_transform(api_df)

@dg.schedule(
    cron_schedule="0 8 * * *",
    job=dg12_graph_multi_asset_job,
    execution_timezone="Asia/Seoul"
)
def dg12_graph_multi_asset_schedule():
    return {}


