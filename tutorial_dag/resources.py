import dagster as dg
import requests
from sqlalchemy import create_engine
from google.oauth2 import service_account
from google.cloud import bigquery
from google.cloud import storage
import boto3, os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

# 1. 리소스 정의
# 1-1. BigQuery 클라이언트
@dg.resource
def bq_client(context):
    project_id = os.getenv("GCP_PROJECT_ID")
    credentials_path = os.getenv("GCP_CREDENTIALS_PATH")
    location = os.getenv("GCP_LOCATION")
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    client = bigquery.Client(
        project=project_id,
        credentials=credentials,
        location=location
    )
    return client

# 1-2. GCS 리소스 정의
@dg.resource
def gcs_client(context):
    project_id = os.getenv("GCP_PROJECT_ID")
    credentials_path = os.getenv("GCP_CREDENTIALS_PATH")
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    client = storage.Client(
        project=project_id,
        credentials=credentials
    )
    return client

# 1-3. S3 리소스 정의
@dg.resource
def s3_client(context):
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region_name = os.getenv("AWS_REGION_NAME")
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region_name
    )
    return s3_client

# 1-4. Glue 리소스 정의
@dg.resource
def glue_client(context):
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region_name = os.getenv("AWS_REGION_NAME")
    
    glue_client = boto3.client(
        "glue",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region_name
    )
    return glue_client

# 1-3. API 리소스 정의
@dg.resource
def api_client(context):
    base_url = os.getenv("API_CLIENT_BASE_URL")
    session = requests.Session()  # 재사용 가능한 HTTP 세션
    return {"session": session, "base_url": base_url}

# 1-4. MySQL 리소스 정의
@dg.resource
def mysql_connection(context):
    mysql_conn_val = os.getenv("MYSQL_CONN_VAL")
    mysql_conn = create_engine(mysql_conn_val)
    return mysql_conn

# 1-5. Postgres 리소스 정의
@dg.resource
def postgres_connection(context):
    postgres_conn_val = os.getenv("POSTGRES_CONN_VAL")
    postgres_conn = create_engine(postgres_conn_val)
    return postgres_conn

