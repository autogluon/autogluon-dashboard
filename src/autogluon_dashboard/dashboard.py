import os
import subprocess
import sys
import boto3

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_SESSION_TOKEN = os.getenv('AWS_SESSION_TOKEN')
session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY, 
    aws_session_token=AWS_SESSION_TOKEN
)
s3 = session.resource('s3')
BUCKET = "dashboard-test-yash"

def upload_csv_to_s3(per_dataset_path, aggregated_path):
    global s3
    s3.meta.client.upload_file(Filename=f"{per_dataset_path}", 
                               Bucket=BUCKET, 
                               Key='dev_data/all_data.csv')
    s3.meta.client.upload_file(Filename=f"{aggregated_path}",
                               Bucket=BUCKET, 
                               Key='dev_data/autogluon.csv')

def upload_web_to_s3():
    global s3
    s3.meta.client.upload_file(Filename="web_files/app.html", 
                               Bucket=BUCKET, 
                               Key='app.html')
    s3.meta.client.upload_file(Filename="web_files/app.js",
                               Bucket=BUCKET, 
                               Key='app.js')


def run_dashboard():
    per_dataset_csv_path = sys.argv[2]
    aggregated_csv_path = sys.argv[4]
    upload_csv_to_s3(per_dataset_csv_path, aggregated_csv_path)
    wrapper_dir = os.path.dirname(__file__)
    app_location = os.path.join(wrapper_dir, "app.py")
    subprocess.run(
        [
            "panel",
            "convert",
            f"{app_location}",
            "--to",
            "pyodide-worker",
            "--out",
            "web_files",
            "--requirements",
            "pandas",
            "holoviews",
            "hvplot",
        ]
    )
    upload_web_to_s3()


if __name__ == "__main__":
    run_dashboard()