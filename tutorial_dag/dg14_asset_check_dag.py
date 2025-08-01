# import dagster as dg
# import pandas as pd
# from .resources import api_client

# # 2. asset 정의: API를 호출해서 데이터 가져오기
# @dg.asset(required_resource_keys={"api_client"})
# def dg_14_get_breweries(context):
#     """
#     API를 호출해서 데이터 가져오기
#     """
#     client = context.resources.api_client
#     response = client["session"].get(client["base_url"])  # API 호출
#     data = response.json()
#     context.log.info(f"Got {len(data)} breweries!")
#     return data

# @dg.asset
# def dg_14_transform_breweries(context, get_breweries):
#     """
#     API 데이터를 Dataframe 형태로 변환
#     """
#     df = pd.json_normalize(get_breweries)
#     context.log.info(f"Transformed {df.head()} breweries!")
#     return df

# # 4. 자산 체크: DataFrame 품질 검증
# @dg.asset_check(
#     asset=dg_14_transform_breweries,
#     description="Check if DataFrame has at least 10 rows"
#     )
# def dg14_row_count_check(context: dg.AssetCheckExecutionContext):
#     df = context.get_asset_output_data()
#     row_count = len(df)
#     passed = row_count >= 100
#     return dg.AssetCheckResult(
#         passed=passed,
#         metadata={"row_count": row_count},
#         description=f"Found {row_count} rows, required at least 10"
#     )

# # 3. job 정의: 파이프라인 역할
# @dg.job
# def dg14_api_resource_job():
#     breweries = dg_14_get_breweries()
#     dg_14_transform_breweries(breweries)
    
# @dg.schedule(
#     cron_schedule="0 8 * * *",
#     job=dg14_api_resource_job,
#     execution_timezone="Asia/Seoul"
# )
# def dg14_api_resource_schedule():
#     return {}


import dagster as dg
import pandas as pd
from .resources import api_client


# 2. 자산 정의: API 데이터 가져오기
@dg.asset(required_resource_keys={"api_client"})
def breweries(context: dg.AssetExecutionContext):
    client = context.resources.api_client
    response = client["session"].get(client["base_url"])
    data = response.json()
    context.log.info(f"Got {len(data)} breweries!")
    return data

# 3. 자산 정의: DataFrame 변환
@dg.asset(deps=[breweries])
def brewery_df(context: dg.AssetExecutionContext, breweries):
    df = pd.json_normalize(breweries)
    context.log.info(f"Transformed {len(df)} breweries!")
    return df

# 4. 자산 체크: 행 수 검증 (의도적 실패)
@dg.asset_check(
    asset=brewery_df,
    description="Check if DataFrame has at least 100 rows"
)
def dg14_row_count_check(context: dg.AssetCheckExecutionContext, brewery_df):
    row_count = len(brewery_df)
    passed = row_count >= 10  # 50개만 가져오므로 실패
    result = dg.AssetCheckResult(
        passed=passed,
        metadata={"row_count": row_count},
        description=f"Found {row_count} rows, required at least 100"
    )
    print(result)
    return result

@dg.asset(deps=[brewery_df])
def processed_brewery_df(context: dg.AssetExecutionContext, brewery_df):
    processed_df = brewery_df[["name", "city"]]  # 간단한 처리
    context.log.info(f"Processed {len(processed_df)} breweries!")
    return processed_df