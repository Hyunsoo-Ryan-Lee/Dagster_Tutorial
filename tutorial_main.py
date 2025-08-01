import dagster as dg
from tutorial_dag.dg01_python_dag import dg01_pipeline_job, dg01_pipeline_schedule
from tutorial_dag.dg02_python_branch_dag import dg02_branch_pipeline_job, dg02_branch_pipeline_schedule
from tutorial_dag.dg03_python_branch2_dag import dg03_branch_pipeline_job, dg03_branch_pipeline_schedule
from tutorial_dag.dg04_multi_asset_dag import dg04_multi_dataframe_file_job, dg04_multi_dataframe_file_schedule
from tutorial_dag.dg05_api_gcs_dag import dg05_api_gcs_job, dg05_api_gcs_schedule
from tutorial_dag.dg06_sensor_pre_dag import dg06_sensor_pre_job, dg06_sensor_pre_schedule
from tutorial_dag.dg06_sensor_post_dag import dg06_sensor_post_job, dg06_gcs_sensor
from tutorial_dag.dg07_api_resource_dag import dg07_api_resource_job, dg07_api_resource_schedule
from tutorial_dag.dg08_db_resource_dag import dg08_db_resource_job, dg08_db_resource_schedule
from tutorial_dag.dg09_gcp_resource_dag import dg09_gcp_resource_job, dg09_gcp_resource_schedule, bq_client, gcs_client
from tutorial_dag.dg10_aws_resource_dag import dg10_aws_resource_job, dg10_aws_resource_schedule
from tutorial_dag.dg11_graph_asset_dag import dg11_graph_asset_job, dg11_graph_asset_schedule
from tutorial_dag.dg12_graph_multi_asset_dag import dg12_graph_multi_asset_job, dg12_graph_multi_asset_schedule
from tutorial_dag.dg13_partition_dag import dg13_partition_job, dg13_partition_schedule
from tutorial_dag.dg14_asset_check_dag import dg14_row_count_check, breweries, brewery_df, processed_brewery_df
from tutorial_dag.resources import api_client, mysql_connection, postgres_connection, s3_client, glue_client

defs = dg.Definitions(
    jobs=[
        dg01_pipeline_job,
        dg02_branch_pipeline_job,
        dg03_branch_pipeline_job,
        dg04_multi_dataframe_file_job,
        dg05_api_gcs_job,
        dg06_sensor_pre_job,
        dg06_sensor_post_job,
        dg07_api_resource_job,
        dg08_db_resource_job,
        dg09_gcp_resource_job,
        dg10_aws_resource_job,
        dg11_graph_asset_job,
        dg12_graph_multi_asset_job,
        dg13_partition_job,
    ],
    schedules=[
        dg01_pipeline_schedule,
        dg02_branch_pipeline_schedule,
        dg03_branch_pipeline_schedule,
        dg04_multi_dataframe_file_schedule,
        dg05_api_gcs_schedule,
        dg06_sensor_pre_schedule,
        dg07_api_resource_schedule,
        dg08_db_resource_schedule,
        dg09_gcp_resource_schedule,
        dg10_aws_resource_schedule,
        dg11_graph_asset_schedule,
        dg12_graph_multi_asset_schedule,
        dg13_partition_schedule,
    ],
    sensors=[
        dg06_gcs_sensor
    ],
    resources={
        "api_client": api_client,
        "mysql_connection": mysql_connection,
        "postgres_connection": postgres_connection,
        "bq_client": bq_client,
        "gcs_client": gcs_client,
        "s3_client": s3_client,
        "glue_client": glue_client
    },
    assets=[breweries, brewery_df, processed_brewery_df],
    asset_checks=[
        dg14_row_count_check
    ]
)