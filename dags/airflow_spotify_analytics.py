from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

with DAG(
        'airflow_spotify_analytics',
        # These args will get passed on to each operator
        # You can override them on a per-task basis during operator initialization
        default_args={
            'depends_on_past': False,
            'email': ['airflow@example.com'],
            'email_on_failure': False,
            'email_on_retry': False,
            'retries': 0,
            'retry_delay': timedelta(minutes=5)
        },
        description='Spotify DAG',
        schedule_interval=timedelta(hours=1),
        start_date=datetime(2023, 10, 21),
        catchup=False
) as dag:
    extract_from_spotify = KubernetesPodOperator(
        namespace="k8-executor",  
        service_account_name="composer", 
        image="us-central1-docker.pkg.dev/daring-card-399612/docker-aho/image_extraction:2",
        cmds=["bash", "-cx"],
        arguments=["python get_t_with_refresh_t_and_data.py"],
        labels={"foo": "bar"},
        name="extract_from_spotify-k8",
        task_id="extract_from_spotify_task",
        image_pull_policy="Always",
		config_file="/home/airflow/composer_kube_config",
        get_logs=True,
        dag=dag
    )
    dbt_run = KubernetesPodOperator(
        namespace="k8-executor",  
        service_account_name="composer", 
        image="us-central1-docker.pkg.dev/daring-card-399612/docker-aho/image_dbt:3",
        cmds=["bash", "-cx"],
        arguments=["dbt run --project-dir dbt_k8_demo"],
        labels={"foo": "bar"},
        name="dbt-run-k8",
        task_id="run_dbt_job",
        image_pull_policy="Always",
		config_file="/home/airflow/composer_kube_config",
        get_logs=True,
        dag=dag
    )
    extract_from_spotify >> dbt_run
