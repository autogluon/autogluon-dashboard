import os
import subprocess
import sys

import boto3
import botocore

BUCKET = "dashboard-test-yash"
s3_url = "https://dashboard-test-yash.s3.us-west-2.amazonaws.com/"


def upload_to_s3(s3_client: botocore.client, file_name: str, object_name: str):
    """
    Uploads a file from local filesystem to a specified S3 bucket

    Parameters
    ----------
    s3_client: botocore.client.S3,
        S3 client to interact with bucket
    file_name: str,
        Name of local file to upload to S3
    object_name: str,
        Name of object to store file contents in S3 bucket
    """
    global BUCKET
    with open(file_name, "rb") as f:
        s3_client.upload_fileobj(f, BUCKET, object_name)


def run_dashboard():
    per_dataset_csv_path = sys.argv[2]
    aggregated_csv_path = sys.argv[4]
    per_dataset_s3_loc = "dev_data/all_data.csv"
    aggregated_s3_loc = "dev_data/autogluon.csv"
    global s3_url
    s3_client = boto3.client("s3")
    os.environ["PER_DATASET_S3_PATH"] = s3_url + per_dataset_s3_loc
    os.environ["AGG_DATASET_S3_PATH"] = s3_url + aggregated_s3_loc
    upload_to_s3(s3_client, per_dataset_csv_path, per_dataset_s3_loc)
    upload_to_s3(s3_client, aggregated_csv_path, aggregated_s3_loc)
    wrapper_dir = os.path.dirname(__file__)
    agg_script_location = os.path.join(wrapper_dir, "aggregate_file.py")
    agg_file_location = os.path.join(wrapper_dir, "out.py")
    subprocess.run(["python3", f"{agg_script_location}"])
    subprocess.run(
        [
            "panel",
            "convert",
            f"{agg_file_location}",
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
    upload_to_s3(s3_client, "web_files/app.html", "app.html")
    upload_to_s3(s3_client, "web_files/app.html", "app.js")


if __name__ == "__main__":
    run_dashboard()