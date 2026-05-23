from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from datetime import datetime, timedelta
import json
import random
import sqlite3
import os

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    'learning_data_pipeline',
    default_args=default_args,
    description='A simple learning DAG that interacts with our FastAPI',
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=['learning', 'fastapi'],
) as dag:

    # 1. Task to generate random readings
    def generate_data(**kwargs):
        readings = [round(random.uniform(10.0, 100.0), 2) for _ in range(5)]
        # Push to XCom so the next task can use it
        kwargs['ti'].xcom_push(key='readings', value=readings)
        print(f"Generated readings: {readings}")

    generate_task = PythonOperator(
        task_id='generate_random_data',
        python_callable=generate_data,
    )

    # 2. Task to call the FastAPI endpoint
    # Note: Use 'host.docker.internal' to reach the host machine from inside Docker
    process_task = SimpleHttpOperator(
        task_id='process_data_via_api',
        http_conn_id='http_default',
        endpoint='data/process',
        method='POST',
        # Use a raw string with the tojson filter for the list
        data='{"readings": {{ ti.xcom_pull(task_ids="generate_random_data", key="readings") | tojson }}, "multiplier": 1.2}',
        headers={"Content-Type": "application/json"},
        response_check=lambda response: response.status_code == 200,
        log_response=True,
    )

    # 3. Task to save the response to the SQLite database
    def save_to_db(**kwargs):
        # Pull the response from the previous task
        ti = kwargs['ti']
        response_str = ti.xcom_pull(task_ids='process_data_via_api')
        response_data = json.loads(response_str)
        
        metrics = response_data['metrics']
        
        # Connect to the local database file
        # Note: In a real Docker setup, we'd use a volume or a network DB.
        # Here we assume the DB is accessible at the mapped path or we're running locally.
        db_path = "/opt/airflow/database.db" # This depends on your docker-compose mount
        
        if not os.path.exists(db_path):
            print(f"Database file not found at {db_path}. Check docker-compose mounts.")
            return

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        query = """
        INSERT INTO processed_data (timestamp, original_count, mean, std_dev, min_val, max_val, raw_response)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        
        cursor.execute(query, (
            datetime.now().isoformat(),
            response_data['original_count'],
            metrics['mean'],
            metrics['standard_deviation'],
            metrics['min'],
            metrics['max'],
            response_str
        ))
        
        conn.commit()
        conn.close()
        print("Successfully saved data to database.")

    save_task = PythonOperator(
        task_id='save_data_to_db',
        python_callable=save_to_db,
    )

    # Set task dependencies
    generate_task >> process_task >> save_task
