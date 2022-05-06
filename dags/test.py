#datetime
from datetime import timedelta, datetime

# The DAG object
from airflow import DAG

# Operators
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

# initializing the default arguments
default_args = {
		'owner': 'Moon',
		'start_date': datetime(2022, 3, 4),
		'retries': 3,
		'retry_delay': timedelta(minutes=1)
}

# Instantiate a DAG object
hello_world_dag = DAG('hello_world_dag',
		default_args=default_args,
		description='Hello World DAG',
		schedule_interval='@once',
		catchup=False,
		tags=['example, helloworld']
)

# python callable function
def print_hello():
		return 'Hello World!'

# Creating first task
start_task = DummyOperator(
    task_id='start_task',
    dag=hello_world_dag
    )

# Creating second task
hello_world_task = PythonOperator(
    task_id='hello_world_task',
    python_callable=print_hello,
    dag=hello_world_dag
    )

k8s = KubernetesPodOperator(
    namespace='airflow',
    task_id="k8s",
    #image='mathworks/matlab:r2022a',
    image='bmoon0702/matlab-custom:r2022a',
    cmds=["bash", "-cx"],
    #arguments=["matlab", "-batch", "test"],
    arguments=["pwd"],
    name="matlab-test-pod",
    dag=hello_world_dag
)

# Creating third task
end_task = DummyOperator(
    task_id='end_task',
    dag=hello_world_dag
    )

# Set the order of execution of tasks.
start_task >> hello_world_task >> k8s >> end_task
