import dagster as dg
import requests
import pandas as pd


@dg.asset
def dg04_fetch_api(context):
    """
    API 데이터를 가져옵니다.
    """
    URL = 'https://api.openbrewerydb.org/v1/breweries'
    response = requests.get(URL)
    return response.json()

@dg.multi_asset(
    ins={"fetch_api": dg.AssetIn('dg04_fetch_api')},
    outs={
        "df": dg.AssetOut(),
        "desc_df": dg.AssetOut()
    }
)
def dg04_transform_api(context, fetch_api):
    """
    API 데이터를 Dataframe 형태로 변환합니다.
    """
    df = pd.json_normalize(fetch_api)
    desc_df = df.describe()
    return df, desc_df


@dg.asset
def dg04_load_data(context, df):
    """
    Dataframe 형태의 API 데이터를 CSV 파일로 저장합니다.
    """
    df.to_csv('brewery_data.csv', index=False)

@dg.asset
def dg04_load_metadata(context, desc_df):
    """
    Dataframe 형태의 API 데이터 설명을 CSV 파일로 저장합니다.
    """
    desc_df.to_csv('brewery_data_metadata.csv', index=False)


@dg.job
def dg04_multi_dataframe_file_job():
    fetch_api = dg04_fetch_api()
    df, desc_df = dg04_transform_api(fetch_api)
    dg04_load_data(df)
    dg04_load_metadata(desc_df)

@dg.schedule(
    cron_schedule="0 8 * * *",
    job=dg04_multi_dataframe_file_job,
    execution_timezone="Asia/Seoul"
)
def dg04_multi_dataframe_file_schedule():
    return {}