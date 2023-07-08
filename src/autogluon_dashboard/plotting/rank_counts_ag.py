from typing import List, Optional, Union

import hvplot
import pandas

from ..scripts.utils import get_col_metric_counts, get_df_filter_by_framework
from .all_plots import Plot


class AGRankCounts(Plot):
    def __init__(
        self,
        plot_title: str,
        df_process: hvplot.Interactive,
        plot_type: str,
        col_name: str,
        framework: str,
        x_axis: Optional[Union[str, List[str]]] = None,
        y_axis: Optional[Union[str, List[str]]] = None,
        graph_type: str = "bar",
        xlabel: str = "",
        ylabel: str = "",
        label_rot: int = 90,
        table_cols: list = [],
    ) -> None:
        dataset_to_plot = self._preprocess(df=df_process, framework=framework, col_name_for_metrics=col_name)
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

    def _preprocess(self, df, framework, col_name_for_metrics, **kwargs) -> pandas.Series:
        df_filtered_by_framework = get_df_filter_by_framework(df, framework)
        return get_col_metric_counts(df_filtered_by_framework, col_name_for_metrics)
