import argparse
import logging
import os
import subprocess

import boto3
import botocore

from autogluon_dashboard.constants.aws_s3_constants import CSV_FILES_DIR


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
        help="Location of csv file of all datasets+frameworks data in local filesystem to upload to S3 bucket. Example: sub_folder/file_name.csv",
        metavar="",
    )
    parser.add_argument(
        "--agg_dataset_csv",
        type=str,
        required=True,
        help="Location of csv file of aggregated data across all frameworks in local filesystem to upload to S3 bucket. Example: sub_folder/file_name.csv",
        metavar="",
    )

    parser.add_argument(
        "--hware_metrics_csv",
        type=str,
        required=False,
        help="Location of csv file of hardware metrics in local filesystem to upload to S3 bucket. Example: sub_folder/file_name.csv",
        default="",
        metavar="",
    )

    parser.add_argument(
        "--s3_bucket",
        type=str,
        required=True,
        help="Name of S3 bucket that results to aggregate get outputted to",
        metavar="",
    )
    parser.add_argument(
        "--s3_prefix",
        type=str,
        required=False,
        help="Prefix for S3 URL. Example: sub_folder/sub_sub_folder",
        default="",
        metavar="",
    )
    parser.add_argument(
        "--s3_region",
        type=str,
        required=True,
        help="S3 Region to deploy the dashboard website. This should be the same region as the S3 bucket",
        metavar="",
    )

    args = parser.parse_args()
    return args


def run_dashboard():
    args = get_args()
    # Set variables to corresponding command line args
    per_dataset_csv_path = args.per_dataset_csv
    aggregated_csv_path = args.agg_dataset_csv
    hware_metrics_csv_path = args.hware_metrics_csv
    bucket_name = args.s3_bucket
    region = args.s3_region
    prefix = args.s3_prefix

    logger = logging.getLogger("dashboard-logger")
    logging.basicConfig(level=logging.INFO)

    logger.info(f"You have specified Bucket {bucket_name} and Region {region}.")

    # Set S3 URL with appropriate bucket, region, and prefix
    if prefix:
        prefix = prefix if prefix.endswith("/") else prefix + "/"
    s3_url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{prefix}"
    s3_url = s3_url if s3_url.endswith("/") else s3_url + "/"

    # Set s3 public urls to CSVs as environment variables
    global CSV_FILES_DIR
    CSV_FILES_DIR = CSV_FILES_DIR if CSV_FILES_DIR.endswith("/") else CSV_FILES_DIR + "/"
    per_dataset_s3_loc = CSV_FILES_DIR + "all_data.csv"
    aggregated_s3_loc = CSV_FILES_DIR + "autogluon.csv"
    hware_s3_loc = CSV_FILES_DIR + "hardware_metrics.csv"
    PER_DATASET_CSV_PATH = s3_url + per_dataset_s3_loc
    AGG_FRAMEWORK_CSV_PATH = s3_url + aggregated_s3_loc
    HARDWARE_METRICS_CSV_PATH = s3_url + hware_s3_loc if hware_metrics_csv_path else ""
    wrapper_dir = os.path.dirname(__file__)
    csv_path_file_location = os.path.join(wrapper_dir, "constants/csv_paths.py")
    # Write the CSV paths to a python file that can be accessed by app.py
    # We do this instead of using an environment variable since the website runs in a separate web environment, which cannot be accessed preemptively using this code.
    f = open(csv_path_file_location, "w")
    f.write(f"PER_DATASET_CSV_PATH = " + '"' + PER_DATASET_CSV_PATH + '"')
    f.write(f"\nAGG_FRAMEWORK_CSV_PATH = " + '"' + AGG_FRAMEWORK_CSV_PATH + '"')
    f.write(f"\nHARDWARE_METRICS_CSV_PATH = " + '"' + HARDWARE_METRICS_CSV_PATH + '"')
    f.close()

    # ignore bokeh warnings in the terminal
    os.environ["BOKEH_PY_LOG_LEVEL"] = "error"

    s3_client = boto3.client("s3")

    # Upload CSV files to S3
    upload_to_s3(
        s3_client, per_dataset_csv_path, prefix + per_dataset_s3_loc, bucket_name, args={"ACL": "public-read"}
    )
    upload_to_s3(s3_client, aggregated_csv_path, prefix + aggregated_s3_loc, bucket_name, args={"ACL": "public-read"})
    if hware_metrics_csv_path:
        upload_to_s3(
            s3_client, hware_metrics_csv_path, prefix + hware_s3_loc, bucket_name, args={"ACL": "public-read"}
        )
        logger.info(
            f"Evaluation CSV files have been successfully uploaded to bucket - {bucket_name}, at locations: {s3_url + per_dataset_s3_loc}, {s3_url + aggregated_s3_loc}, and {s3_url + hware_s3_loc}.",
        )
    else:
        logger.info(
            f"Evaluation CSV files have been successfully uploaded to bucket - {bucket_name}, at locations: {s3_url + per_dataset_s3_loc} and {s3_url + aggregated_s3_loc}.",
        )

    agg_script_location = os.path.join(wrapper_dir, "utils/aggregate_file.py")
    agg_file_location = os.path.join(wrapper_dir, "index.py")
    # Aggregate all code into output file
    subprocess.run(["python3", f"{agg_script_location}"])
    logger.info("Ran aggregation script successfully")

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
    logger.info("Ran panel convert successfully")
    # Upload WebAssembly to S3 bucket
    upload_to_s3(
        s3_client,
        os.path.join(web_files_dir, "index.html"),
        prefix + "index.html",
        bucket_name,
        args={"ContentType": "text/html", "ACL": "public-read"},
    )
    upload_to_s3(
        s3_client,
        os.path.join(web_files_dir, "index.js"),
        prefix + "index.js",
        bucket_name,
        args={"ACL": "public-read"},
    )
    logger.info("WebAssembly files have been successfully uploaded to bucket - %s", bucket_name)

    logger.info(
        "The dashboard website is: " + f"http://{bucket_name}.s3-website-{region}.amazonaws.com/{prefix}index.html"
    )
    # Use print so that the GitHub Actions bash script can pick up the URL from the CLI
    print("The dashboard website is: " + f"http://{bucket_name}.s3-website-{region}.amazonaws.com/{prefix}index.html")


if __name__ == "__main__":
    run_dashboard()
