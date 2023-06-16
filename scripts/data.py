import pandas as pd
from autogluon.common.loaders import load_pd

"""
df = load_pd.load(s3_PATH)
"""

def get_dataframes(csv1_path, csv2_path):
    per_dataset_df = load_pd.load(csv1_path)
    all_framework_df = load_pd.load(csv2_path)
    return per_dataset_df, all_framework_df
