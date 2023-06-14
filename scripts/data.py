import pandas as pd

"""
import boto3

client = boto3.client('s3')
bucket_name = 'my_bucket'
object_key = 'my_file.csv'
csv_obj = client.get_object(Bucket=bucket_name, Key=object_key)
body = csv_obj['Body']
csv_string = body.read().decode('utf-8')
df = pd.read_csv(StringIO(csv_string))
"""

PER_DATASET_TEST_CSV= 'dev_data/all_data.csv'
ALL_DATASETS_COMBINED_TEST_CSV = 'dev_data/autogluon.csv'


per_dataset_df = pd.read_csv(PER_DATASET_TEST_CSV)
all_framework_df = pd.read_csv(ALL_DATASETS_COMBINED_TEST_CSV)