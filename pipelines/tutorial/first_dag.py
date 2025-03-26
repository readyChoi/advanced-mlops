from datetime import datetime, timedelta
from textwrap import dedent

import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator

from utils.callbacks import failure_callback, success_callback

local_timezone = pendulum.timezone("Asia/Seoul")

with DAG(
    dag_id="simple_dag",
    default_args={
        "owner": "user",
        "depends_on_past": False, #과거의 실행 결과에 의존할껀지 
        "email": "junc@lgcns.com",
        "email_on_failure": False,
        "email_on_retry": False, #네트워크 안열려있으면 어짜피 안됨 
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
        "on_failure_callback": failure_callback,
        "on_success_callback": success_callback,
    },
    description="Simple airflow dag",
    schedule="0 15 * * *", # timedelta 등등의 시간 관련 객체들 사용 가능
    start_date=datetime(2025, 3, 1, tzinfo=local_timezone),
    catchup=False, # 과거꺼까지 돌림
    tags=["lgcns", "mlops"],
) as dag:
    task1 = BashOperator(
        task_id="print_date",
        bash_command="date"
    )
    task2 = BashOperator(
        task_id="sleep",
        depends_on_past=False,
        bash_command="sleep 5",
        retries=3
    )

    # Jinja Template: airflow 사용할때 많이 사용 
    loop_command = dedent(
        """
        {% for i in range(5) %}
            echo "ds = {{ ds }}"
            echo "macros.ds_add(ds, {{ i }}) = {{ macros.ds_add(ds, i) }}"
        {% endfor %}
        """
    )
    task3 = BashOperator(
        task_id="print_with_loop",
        bash_command=loop_command,
    )

    task1 >> [task2, task3]
