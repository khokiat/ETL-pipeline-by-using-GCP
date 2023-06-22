from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
import pandas as pd
import requests

covid_url = "https://covid19.ddc.moph.go.th/api/Cases/timeline-cases-by-provinces"
output_path = "/home/airflow/gcs/data/output.csv"


def request_data(output):
    r = requests.get(covid_url)
    file = r.json()
    detail = pd.DataFrame(file)    
    detail.to_csv(output,index=True)
    

def change_to_csv(output,covid_report_path):
    report = pd.read_csv(output)
    report['update_date']= pd.to_datetime(report['update_date']).dt.date
    report.to_csv(covid_report_path,index=True)

with DAG('covid',
    default_args = {
    'owner': 'khokiat',
    'depends_on_past': False,
    'start_date': days_ago(0),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    },
    schedule_interval="@once"
) as dag :

    t1 = PythonOperator(
        task_id="get_data_from_API",
        python_callable=request_data,
        op_kwargs={"output" :output_path},
        )
    t2 = PythonOperator(
        task_id="Transform",
        python_callable=change_to_csv,
        op_kwargs={"output" :output_path,
                "covid_report_path" : "/home/airflow/gcs/data/covid19report.csv" },

        )
    t3 = GCSToBigQueryOperator(task_id='Load_to_bq',
                            bucket='asia-east2-covid19pipe-017abd08-bucket',
                            source_objects=['data/covid19report.csv'],
                            destination_project_dataset_table='covid.week_report',
                            autodetect=True,
                            write_disposition='WRITE_TRUNCATE',
                            )           

    t1>>t2>>t3