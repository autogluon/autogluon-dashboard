import pandas as pd


def get_dataframes(csv1_path: str, csv2_path: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    per_dataset_df = pd.read_csv(csv1_path)
    all_framework_df = pd.read_csv(csv2_path)
    return per_dataset_df, all_framework_df
