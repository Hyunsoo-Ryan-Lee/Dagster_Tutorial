import dagster as dg


@dg.asset
def dg10_first_func(context):
    """
    first_func 입니다.
    """
    context.log.info("This is a log message from first func")
    print("This is a print message from first func")
    return [1,2,3]

@dg.asset(
    deps=[dg10_first_func],
    automation_condition=dg.AutomationCondition.on_cron("* * * * *")
)
def dg10_second_func(context, data):
    """
    조건부 second_func 입니다.
    """
    result = data + [7,8,9]
    context.log.info(f"second func log : {result}")
    print(f"second func print : {result}")
    return result

@dg.job
def dg10_pipeline_job():
    data = dg10_first_func()
    dg10_second_func(data)

@dg.schedule(cron_schedule="0 8 * * *", job=dg10_pipeline_job)
def dg10_pipeline_schedule():
    return {}

# defs = dg.Definitions(
#     jobs=[dg10_pipeline_job],
#     schedules=[dg10_pipeline_schedule]
# )