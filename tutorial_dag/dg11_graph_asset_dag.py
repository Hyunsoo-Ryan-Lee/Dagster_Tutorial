import dagster as dg


@dg.op
def dg11_first_func(context):
    """
    first_func 입니다.
    """
    result = [1,2,3]
    context.log.info(f"first func log : {result}")
    print(f"first func print : {result}")
    return result

@dg.op
def dg11_second_func(context, data):
    """
    second_func 입니다.
    """
    result = data + [4,5,6]
    context.log.info(f"second func log : {result}")
    print(f"second func print : {result}")
    return result

@dg.graph_asset
def dg11_graph():
    data = dg11_first_func()
    result = dg11_second_func(data)
    print({"result": result})
    return result

@dg.job
def dg11_graph_asset_job():
    dg11_graph()

@dg.schedule(
    cron_schedule="0 8 * * *",
    job=dg11_graph_asset_job,
    execution_timezone="Asia/Seoul"
)
def dg11_graph_asset_schedule():
    return {}

# defs = dg.Definitions(
#     jobs=[dg11_graph_asset_job], 
#     schedules=[dg11_graph_asset_schedule]
# )

