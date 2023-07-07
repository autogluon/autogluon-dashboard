from typing import List, Optional, Union

import hvplot
import pandas

from ..scripts.utils import get_df_filter_by_dataset, get_top5_performers
from .all_plots import Plot


class Top5PerDataset(Plot):
    def __init__(
        self,
        plot_title: str,
        df_process: hvplot.Interactive,
        plot_type: str,
        col_name: str,
        dataset: str,
        x_axis: Optional[Union[str, List[str]]] = None,
        y_axis: Optional[Union[str, List[str]]] = None,
        graph_type: str = "bar",
        xlabel: str = "",
        ylabel: str = "",
        label_rot: int = 90,
        table_cols: list = [],
    ) -> None:
        dataset_to_plot = self._preprocess(df=df_process, dataset=dataset, col_name_for_metrics=col_name)
        super().__init__(
            plot_title,
            dataset_to_plot,
            plot_type,
            x_axis,
            y_axis,
            graph_type,
            xlabel,
            ylabel,
            label_rot,
            table_cols,
        )

    def _preprocess(self, df, dataset, col_name_for_metrics, **kwargs) -> pandas.DataFrame:
        df_filtered_by_dataset = get_df_filter_by_dataset(df, dataset)
        return get_top5_performers(df_filtered_by_dataset, col_name_for_metrics)
