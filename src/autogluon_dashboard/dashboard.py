import argparse
import os
import subprocess

import boto3
import botocore


def upload_to_s3(s3_client: botocore.client, file_name: str, object_name: str, bucket_name: str, args: dict = None):
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
    with open(file_name, "rb") as f:
        s3_client.upload_fileobj(f, bucket_name, object_name, ExtraArgs=args)


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--per_dataset_csv",
        type=str,
        help="Location of csv file in local filesystem to upload to S3 bucket. Example: sub_folder/file_name.csv",
    )
    parser.add_argument(
        "--all_dataset_csv",
        type=str,
        help="Location of csv file in local filesystem to upload to S3 bucket. Example: sub_folder/file_name.csv",
    )
    parser.add_argument(
        "--per_dataset_s3",
        type=str,
        help="Location in S3 bucket to save csv file. Example: sub_folder/file_name.csv",
        default="dev_data/all_data.csv",
    )
    parser.add_argument(
        "--all_dataset_s3",
        type=str,
        help="Location in S3 bucket to save csv file. Example: sub_folder/file_name.csv",
        default="dev_data/autogluon.csv",
    )

    parser.add_argument(
        "--s3_bucket",
        type=str,
        help="Name of S3 bucket that results to aggregate get outputted to",
        default="dashboard-test-yash",
    )
    parser.add_argument("--s3_prefix", type=str, help="Prefix for path to results needing aggregation", default="")

    args = parser.parse_args()
    return args


def run_dashboard():
    args = get_args()
    # Set variables to corrensponding command line args
    per_dataset_csv_path = args.per_dataset_csv
    aggregated_csv_path = args.all_dataset_csv
    per_dataset_s3_loc = args.per_dataset_s3
    aggregated_s3_loc = args.all_dataset_s3
    global BUCKET
    BUCKET = args.s3_bucket
    global s3_url
    s3_url = f"https://{BUCKET}.s3.us-west-2.amazonaws.com/"
    s3_url = s3_url if s3_url.endswith("/") else s3_url + "/"

    s3_client = boto3.client("s3")

    # Set s3 public urls to CSVs as environment variables
    os.environ["PER_DATASET_S3_PATH"] = s3_url + per_dataset_s3_loc
    os.environ["AGG_DATASET_S3_PATH"] = s3_url + aggregated_s3_loc

    # Upload CSV files to S3
    upload_to_s3(s3_client, per_dataset_csv_path, per_dataset_s3_loc, BUCKET)
    upload_to_s3(s3_client, aggregated_csv_path, aggregated_s3_loc, BUCKET)

    wrapper_dir = os.path.dirname(__file__)
    agg_script_location = os.path.join(wrapper_dir, "aggregate_file.py")
    agg_file_location = os.path.join(wrapper_dir, "out.py")
    # Aggregate all code into output file
    subprocess.run(["python3", f"{agg_script_location}"])

    web_files_dir = os.path.join(wrapper_dir, "web_files/")
    # Run panel convert to generate WebAssembly
    subprocess.run(
        [
            "panel",
            "convert",
            f"{agg_file_location}",
            "--to",
            "pyodide-worker",
            "--out",
            f"{web_files_dir}",
            "--requirements",
            "pandas",
            "holoviews",
            "hvplot",
        ]
    )
    # Upload WebAssembly to S3 bucket
    upload_to_s3(
        s3_client, os.path.join(web_files_dir, "out.html"), "out.html", BUCKET, args={"ContentType": "text/html"}
    )
    upload_to_s3(s3_client, os.path.join(web_files_dir, "out.js"), "out.js", BUCKET)


if __name__ == "__main__":
    run_dashboard()
