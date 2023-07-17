from typing import List, Optional, Union

import hvplot
import pandas

from ..scripts.utils import get_col_metric_counts, get_df_filter_by_framework
from .all_plots import Plot


class FrameworkMetricCounts(Plot):
    """
    This class is used to create a table of datasets that errored out during a benchmark run for a given framework.

    Attributes
    ----------
    plot_title: str,
        title of the plot on the dashboard website
    dataset_to_plot: hvplot.Interactive,
        interactive pandas dataframe that is used to create the plot
        this dataframe will first go through the preprocess method
    plot_type: str,
        type of hvplot. hvplot, table, pareto
    col_name: str,
        column name to get counts for a given framework
    framework: str,
        framework to filter dataset by for rank counts
    x_axis: Optional[Union[str, List[str]]],
        values to plot on x-axis
    y_axis: Optional[Union[str, List[str]]],
        values to plot on y-axis
    graph_type: str,
        type of graph. examples: bar, line, hist
    xlabel: str,
        label of x-axis
    ylabel: str,
        label of y-axis
    label_rot: int,
        rotation value of labels on axes

    Methods
    -------
    _preprocess():
        inherited from parent `Plot` class
        returns the counts of given column name filtered by provided framework
    """
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
        )

    def _preprocess(self, df, framework, col_name_for_metrics, **kwargs) -> pandas.Series:
        df_filtered_by_framework = get_df_filter_by_framework(df, framework)
        return get_col_metric_counts(df_filtered_by_framework, col_name_for_metrics)
