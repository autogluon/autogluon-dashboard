import os
import subprocess
import sys
import boto3

s3 = boto3.client('s3')
BUCKET = "dashboard-test-yash"

def upload_to_s3(file_name: str, object_name: str):
    """
    Uploads a file from local filesystem to a specified S3 bucket
    
    Parameters
    ----------
    file_name: str,
        Name of local file to upload to S3
    object_name: str,
        Name of object to store file contents in S3 bucket
    """
    global s3
    global BUCKET
    with open(file_name, "rb") as f:
        s3.upload_fileobj(f, BUCKET, object_name)


def run_dashboard():
    per_dataset_csv_path = sys.argv[2]
    aggregated_csv_path = sys.argv[4]
    upload_to_s3(per_dataset_csv_path, 'dev_data/all_data.csv')
    upload_to_s3(aggregated_csv_path, 'dev_data/autogluon.csv')
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
    upload_to_s3('web_files/app.html', 'app.html')
    upload_to_s3('web_files/app.html', 'app.js')


if __name__ == "__main__":
    run_dashboard()
