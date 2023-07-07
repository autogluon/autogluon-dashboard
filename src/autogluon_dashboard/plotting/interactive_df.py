from typing import Optional

import hvplot
import pandas

from ..scripts.utils import get_df_filter_by_dataset, get_df_filter_by_framework
from .all_plots import Plot


class InteractiveDataframe(Plot):
    def __init__(
        self, df_process: hvplot.Interactive, framework: str, width: int, dataset: Optional[str] = None
    ) -> None:
        self.dataset_to_plot = df_process
        self.framework = framework
        self.table_width = width
        self.dataset = dataset

    def get_interactive_df(self) -> hvplot.Interactive:
        return hvplot.bind(self._preprocess, self.framework, self.dataset).interactive(width=self.table_width)

    def _preprocess(*args) -> pandas.DataFrame:
        df = args[0].dataset_to_plot
        if args[2]:
            df = get_df_filter_by_dataset(df, args[2])
        if "All Frameworks" in args[1]:
            return df
        return get_df_filter_by_framework(df, args[1])

    def _process_df(self, df_process, dataset) -> pandas.DataFrame:
        print(dataset)
        if dataset:
            df_process = get_df_filter_by_dataset(df_process, dataset)
        return df_process
