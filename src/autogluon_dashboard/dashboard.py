import argparse
import logging
import os
import subprocess

import boto3
import botocore

from autogluon_dashboard.scripts.constants.aws_s3_constants import CSV_FILES_DIR, DEFAULT_BUCKET_NAME, S3_REGION


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
        required=True,
        help="Location of csv file in local filesystem to upload to S3 bucket. Example: sub_folder/file_name.csv",
    )
    parser.add_argument(
        "--all_dataset_csv",
        type=str,
        required=True,
        help="Location of csv file in local filesystem to upload to S3 bucket. Example: sub_folder/file_name.csv",
    )
    parser.add_argument(
        "--per_dataset_s3",
        type=str,
        help="Location in S3 bucket to save csv file. Example: sub_folder/file_name.csv",
        default=CSV_FILES_DIR + "all_data.csv",  # TODO: Add commit ID (if applicable) to S3 file path
    )
    parser.add_argument(
        "--all_dataset_s3",
        type=str,
        help="Location in S3 bucket to save csv file. Example: sub_folder/file_name.csv",
        default=CSV_FILES_DIR + "autogluon.csv",  # TODO: Add commit ID (if applicable) to S3 file path
    )

    parser.add_argument(
        "--s3_bucket", type=str, help="Name of S3 bucket that results to aggregate get outputted to", nargs="?"
    )
    parser.add_argument("--s3_prefix", type=str, nargs="?", default="")
    parser.add_argument("--s3_region", type=str, help="S3 Region to deploy the dashboard website", nargs="?")

    args = parser.parse_args()
    return args


def run_dashboard():
    args = get_args()
    # Set variables to corrensponding command line args
    per_dataset_csv_path = args.per_dataset_csv
    aggregated_csv_path = args.all_dataset_csv
    per_dataset_s3_loc = args.per_dataset_s3
    aggregated_s3_loc = args.all_dataset_s3
    bucket_name = args.s3_bucket
    region = args.s3_region
    prefix = args.s3_prefix

    logger = logging.getLogger("dashboard-logger")

    if not bucket_name:
        if region:
            logger.warning(
                "Cannot specify region if no bucket has been provded. Defaulting to AutoGluon bucket and region (%s)",
                S3_REGION,
            )
        else:
            logger.warning(
                "No bucket or region has been provided. Defaulting to AutoGluon bucket and region (%s)",
                S3_REGION,
            )
        region = S3_REGION
        bucket_name = DEFAULT_BUCKET_NAME  # TODO: Change default bucket name
    else:
        if not region:
            raise ValueError("You must specify a region if you provide a bucket")
        else:
            logger.info(f"You have specified Bucket {bucket_name} and Region {region}.")

    # Set s3 public urls to CSVs as environment variables
    prefix = prefix if prefix.startswith("/") else "/" + prefix
    prefix = prefix if prefix.endswith("/") else prefix + "/"
    s3_url = f"https://{bucket_name}{prefix}.s3.{region}.amazonaws.com/"
    s3_url = s3_url if s3_url.endswith("/") else s3_url + "/"
    os.environ["PER_DATASET_S3_PATH"] = s3_url + per_dataset_s3_loc
    os.environ["AGG_DATASET_S3_PATH"] = s3_url + aggregated_s3_loc

    s3_client = boto3.client("s3")

    # Upload CSV files to S3
    upload_to_s3(s3_client, per_dataset_csv_path, per_dataset_s3_loc, bucket_name)
    upload_to_s3(s3_client, aggregated_csv_path, aggregated_s3_loc, bucket_name)
    logger.info(
        f"Evaluation CSV files have been successfully uploaded to bucket - {bucket_name}, at location {s3_url + per_dataset_s3_loc} and {s3_url + aggregated_s3_loc}.",
    )

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
        s3_client, os.path.join(web_files_dir, "out.html"), "out.html", bucket_name, args={"ContentType": "text/html"}
    )
    upload_to_s3(s3_client, os.path.join(web_files_dir, "out.js"), "out.js", bucket_name)
    logger.info("WebAssembly files have been successfully uploaded to bucket - %s", bucket_name)

    logger.info("The dashboard website is: " + f"https://{bucket_name}{prefix}.s3-website-{region}.amazonaws.com/")


if __name__ == "__main__":
    run_dashboard()
