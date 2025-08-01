import dagster as dg

@dg.asset
def dg03_branch_decision(context, value):
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
def dg03_branch_a(context, branch_decision):
    """
    A 경로 실행
    """
    if branch_decision == "A":
        context.log.info("A 경로 실행")
        return "A 경로 결과"
    return None

@dg.asset
def dg03_branch_b(context, branch_decision):
    """
    B 경로 실행
    """
    if branch_decision == "B":
        context.log.info("B 경로 실행")
        return "B 경로 결과"
    return None

@dg.asset
def dg03_after_branch(context, branch_a_result, branch_b_result):
    """
    후처리 결과
    """
    result = [i for i in [branch_a_result, branch_b_result] if i is not None][0]
    message = f"{result} 단어가 선택되었습니다!!"
    context.log.info(f"후처리 결과: {message}")
    return message

@dg.job
def dg03_branch_pipeline_job():
    decision = dg03_branch_decision()
    a_result = dg03_branch_a(decision)
    b_result = dg03_branch_b(decision)
    dg03_after_branch(a_result, b_result)

@dg.schedule(
    cron_schedule="0 8 * * *",
    job=dg03_branch_pipeline_job,
    execution_timezone="Asia/Seoul"
)
def dg03_branch_pipeline_schedule():
    return {}

dg03_defs = dg.Definitions(
    jobs=[dg03_branch_pipeline_job],
    schedules=[dg03_branch_pipeline_schedule]
)

