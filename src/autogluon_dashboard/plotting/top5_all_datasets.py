from typing import List, Optional, Union

import hvplot
import pandas

from ..scripts.utils import get_top5_performers
from .all_plots import Plot


class Top5AllDatasets(Plot):
    """
    This class is used to create a table the top 5 performers (frameworks) for a given metric aggregated across all datasets

    Attributes
    ----------
    plot_title: str,
        title of the plot on the dashboard website
    dataset_to_plot: hvplot.Interactive,
        interactive pandas dataframe that is used to create the plot
        this dataframe will first go through the preprocess method
        this should be the dataframe of all framworks aggregated across all datasets
    plot_type: str,
        type of hvplot. hvplot, table, pareto
    framework: str,
        framework to query for errored datasets
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
        returns a Series of the top 5 performers (frameworks) for a given metric aggregated across all dataset

    Usage
    ------
    >>> top5frameworks_all_datasets = Top5AllDatasets(
            TOP5_PERFORMERS_TITLE + " (all datasets)",
            all_frameworks_df,
            "table",
            "rank",
            table_cols=["framework", "rank"],
        )

    You can now call the `.plot()` method on this object to render the plot as a Panel object on the dashboard website.
    """

    def __init__(
        self,
        plot_title: str,
        df_process: hvplot.Interactive,
        plot_type: str,
        col_name: str,
        x_axis: Optional[Union[str, List[str]]] = None,
        y_axis: Optional[Union[str, List[str]]] = None,
        graph_type: str = "bar",
        xlabel: str = "",
        ylabel: str = "",
        label_rot: int = 90,
        table_cols: list = [],
    ) -> None:
        dataset_to_plot = self._preprocess(df=df_process, col_name_for_metrics=col_name)
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

    def _preprocess(self, df, col_name_for_metrics, **kwargs) -> pandas.DataFrame:
        return get_top5_performers(df, col_name_for_metrics)
