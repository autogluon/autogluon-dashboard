import pandas as pd


def get_dataframes(paths: list) -> list[pd.DataFrame]:
    dfs = []
    for dataset_path in paths:
        df = pd.read_csv(dataset_path) if dataset_path else None
        dfs.append(df)
    return dfs
