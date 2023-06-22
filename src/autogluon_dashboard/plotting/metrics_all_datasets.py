from typing import Union

import hvplot

from src.autogluon_dashboard.plotting.all_plots import Plot


class MetricsPlotAll(Plot):
    def __init__(
        self,
        plot_title: str,
        dataset_to_plot: hvplot.Interactive,
        plot_type: str,
        x_axis: Union[str, list] = None,
        y_axis: Union[str, list] = None,
        graph_type: str = "bar",
        xlabel: str = "",
        ylabel: str = "",
        label_rot: int = 90,
        table_cols: list = ...,
    ) -> None:
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

    def _preprocess(*args) -> None:
        return Plot._preprocess(*args)
