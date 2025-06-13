import os
import subprocess
from airflow.decorators import dag, task
from pendulum import datetime
from airflow.utils.log.logging_mixin import LoggingMixin

# Define constants
DVC_DIR = '/opt/airflow/DVC'
SCRIPT_NAME = 'mlflow_main.py'

def track_model():
    """Tracks the model using mlflow_main.py in the DVC directory."""
    logger = LoggingMixin().log  # Airflow-compatible logging
    script_path = os.path.join(DVC_DIR, SCRIPT_NAME)
    
    # Ensure the script exists
    if not os.path.isfile(script_path):
        logger.error(f"Script not found: {script_path}")
        raise FileNotFoundError(f"Script not found: {script_path}")
    
    # Run the script
    try:
        result = subprocess.run(
            ['python', script_path],
            cwd=DVC_DIR,
            check=True,
            capture_output=True,
            text=True
        )
        logger.info(f"Output:\n{result.stdout}")
        logger.info(f"Errors (if any):\n{result.stderr}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error while running mlflow_main.py: {e.stderr}")
        raise

# Define the DAG
@dag(
    dag_id="mlflow_pipeline",
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    description="A DAG to track a model using mlflow_main.py"
)
def track_model_dag():
    @task
    def track_model_task():
        """Airflow task to track the model."""
        track_model()

    # Task execution
    track_model_task()

# Instantiate the DAG
track_model_pipeline = track_model_dag()
