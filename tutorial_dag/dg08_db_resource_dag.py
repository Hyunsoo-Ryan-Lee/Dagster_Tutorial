import dagster as dg
import pandas as pd
from .resources import mysql_connection, postgres_connection

# 2. op 정의: 데이터베이스에서 데이터 조회
@dg.multi_asset(
    outs={
        "mysql_df": dg.AssetOut(),
        "postgres_df": dg.AssetOut()
    },
    required_resource_keys={"mysql_connection", "postgres_connection"}
)
def dg08_extract_db(context):
    mysql_conn = context.resources.mysql_connection
    postgres_conn = context.resources.postgres_connection
    
    mysql_df = pd.read_sql_table("tips", mysql_conn)
    postgres_df = pd.read_sql_table("user_summary", postgres_conn)
    
    return mysql_df, postgres_df

@dg.asset
def dg08_mysql_transform(context, mysql_df):
    context.log.info(f"Transformed {mysql_df.head()} mysql_df!")
    return mysql_df

@dg.asset
def dg08_postgres_transform(context, postgres_df):
    context.log.info(f"Transformed {postgres_df.head()} postgres_df!")
    return postgres_df

# 3. job 정의: 파이프라인 역할
@dg.job
def dg08_db_resource_job():
    mysql_df, postgres_df = dg08_extract_db()
    mysql_df = dg08_mysql_transform(mysql_df)
    postgres_df = dg08_postgres_transform(postgres_df)
    
@dg.schedule(
    cron_schedule="0 8 * * *",
    job=dg08_db_resource_job,
    execution_timezone="Asia/Seoul"
)
def dg08_db_resource_schedule():
    return {}