import dagster as dg


@dg.asset
def dg02_branch_decision(context, value):
    """
    임의의 조건 분기 예시
    """
    value = 10
    if value > 5:
        context.log.info("분기: A 경로 선택")
        return "A"
    else:
        context.log.info("분기: B 경로 선택")
        return "B"

@dg.asset
def dg02_branch_a(context, branch_decision):
    """
    A 경로 실행
    """
    if branch_decision == "A":
        context.log.info("A 경로 실행")
        return "A 경로 결과"
    return None

@dg.asset
def dg02_branch_b(context, branch_decision):
    """
    B 경로 실행
    """
    if branch_decision == "B":
        context.log.info("B 경로 실행")
        return "B 경로 결과"
    return None


@dg.job
def dg02_branch_pipeline_job():
    decision = dg02_branch_decision()
    dg02_branch_a(decision)
    dg02_branch_b(decision)

@dg.schedule(
    cron_schedule="0 8 * * *",
    job=dg02_branch_pipeline_job,
    execution_timezone="Asia/Seoul"
)
def dg02_branch_pipeline_schedule():
    return {}

dg02_defs = dg.Definitions(
    jobs=[dg02_branch_pipeline_job],
    schedules=[dg02_branch_pipeline_schedule]
)

