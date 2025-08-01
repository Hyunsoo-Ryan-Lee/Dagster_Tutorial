import dagster as dg


@dg.asset
def dg01_first_func(context):
    """
    first_func 입니다.
    """
    context.log.info("This is a log message from first func")
    print("This is a print message from first func")
    return [1,2,3]

@dg.asset
def dg01_second_func(context, data):
    """
    second_func 입니다.
    """
    context.log.info("This is a log message from second func")
    print("This is a print message from second func")
    
    return data + [4,5,6]

@dg.job
def dg01_pipeline_job():
    data = dg01_first_func()
    dg01_second_func(data)

@dg.schedule(
    cron_schedule="20 10 * * *",
    job=dg01_pipeline_job,
    execution_timezone="Asia/Seoul"
)
def dg01_pipeline_schedule():
    return {}

dg01_defs = dg.Definitions(
    jobs=[dg01_pipeline_job],
    schedules=[dg01_pipeline_schedule]
)

