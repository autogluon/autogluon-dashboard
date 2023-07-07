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
        return hvplot.bind(self._preprocess, framework=self.framework, dataset=self.dataset).interactive(
            width=self.table_width
        )

    def _preprocess(self, framework, dataset, **kwargs) -> pandas.DataFrame:
        df = self.dataset_to_plot
        if dataset:
            df = get_df_filter_by_dataset(df, dataset)
        if "All Frameworks" in framework:
            return df
        return get_df_filter_by_framework(df, framework)

    def _process_df(self, df_process, dataset) -> pandas.DataFrame:
        print(dataset)
        if dataset:
            df_process = get_df_filter_by_dataset(df_process, dataset)
        return df_process
