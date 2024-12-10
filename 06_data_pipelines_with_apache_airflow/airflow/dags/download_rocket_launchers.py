import json
import pathlib
import airflow
import airflow.utils
import airflow.utils.dates
import requests
import urllib.request
import requests.exceptions as requests_exceptions

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# instantiate a DAG project, starting point os any workflow
dag = DAG(
    dag_id="download_rocket_launches",
    # name of DAG (show in webserver)
    start_date=airflow.utils.dates.days_ago(14),
    # first day to run, DAG can backfill
    schedule_interval=None,
    # DAG not run automatically
)

download_launches = BashOperator(
    task_id="download_launches",
    bash_command="curl -o /tmp/launches.json -L 'https://ll.thespacedevs.com/2.0.0/launch/upcoming/'",
    dag=dag,  # reference to the DAG variable
)


def _get_pictures():
    # this is PythonOperator callable
    # ensure directory exists (mkdir if not exist)
    pathlib.Path("/tmp/images").mkdir(parents=True, exist_ok=True)

    # download all pictures in lauches.json
    with open("/tmp/launches.json") as f:
        launches = json.load(f)
        image_urls = [launch["image"] for launch in launches["results"]]
        for image_url in image_urls:
            try:
                response = requests.get(image_url)
                image_filename = image_url.split("/")[-1]
                target_file = f"/tmp/images/{image_filename}"
                print(f'downloading {image_filename}...')
                urllib.request.urlretrieve(
                    url=image_url,
                    filename=target_file
                )
                print(f"Downloaded {image_url} to {target_file}")
            except requests_exceptions.MissingSchema:
                print(f"{image_url} appears to be an invalid URL")
            except requests_exceptions.ConnectionError:
                print(f"Could not connect to {image_url}")


get_pictures = PythonOperator(
    task_id="get_pictures",
    python_callable=_get_pictures,  # call operation
    dag=dag,
)

notify = BashOperator(
    task_id="notify",
    bash_command='echo "There are now $(ls /tmp/images/ | wc -l) images"',
    dag=dag,
)

# set the order of execution of tasks
download_launches >> get_pictures >> notify
