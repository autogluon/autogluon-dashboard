from typing import Union

import hvplot
import pandas

from src.autogluon_dashboard.plotting.all_plots import Plot
from src.autogluon_dashboard.scripts.utils import get_df_filter_by_dataset


class MetricsPlotPerDataset(Plot):
    def __init__(
        self,
        plot_title: str,
        df_process: hvplot.Interactive,
        plot_type: str,
        dataset: str,
        x_axis: Union[str, list] = None,
        y_axis: Union[str, list] = None,
        graph_type: str = "bar",
        xlabel: str = "",
        ylabel: str = "",
        label_rot: int = 90,
        table_cols: list = ...,
    ) -> None:
        dataset_to_plot = self._preprocess(df_process, dataset)
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

    def _preprocess(self, *args) -> pandas.DataFrame:
        return get_df_filter_by_dataset(args[0], args[1])
