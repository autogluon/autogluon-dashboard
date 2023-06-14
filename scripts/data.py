import pandas as pd
from autogluon.common.loaders import load_pd

"""
df = load_pd.load(s3_PATH)
"""

PER_DATASET_TEST_CSV= 'dev_data/all_data.csv'
ALL_DATASETS_COMBINED_TEST_CSV = 'dev_data/autogluon.csv'

per_dataset_df = load_pd.load(PER_DATASET_TEST_CSV)
all_framework_df = load_pd.load(ALL_DATASETS_COMBINED_TEST_CSV)
