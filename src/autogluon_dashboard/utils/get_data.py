import logging

import pandas as pd

logger = logging.getLogger("dashboard-logger")


def get_dataframes(paths: list) -> list[pd.DataFrame]:
    dfs = []
    for dataset_path in paths:
        try:
            df = pd.read_csv(dataset_path) if dataset_path else None
            dfs.append(df)
        except Exception as e:
            logger.exception(e)
            dfs.append(None)
    return dfs
