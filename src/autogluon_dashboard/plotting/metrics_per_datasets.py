from typing import List, Optional, Union

import hvplot
import pandas

from ..utils.dataset_utils import get_df_filter_by_dataset
from .plot import Plot


class MetricsPlotPerDataset(Plot):
    """
    This class is used to create a plot of frameworks v/s desired metrics (for a particular dataset)

    Attributes
    ----------
    plot_title: str,
        title of the plot on the dashboard website
    dataset_to_plot: hvplot.Interactive,
        interactive pandas dataframe that is used to create the plot
        this should be the dataset of all frameworks and all datasets
    plot_type: str,
        type of hvplot. hvplot, table, pareto
    dataset: str,
        dataset to filter table by
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
        returns a filtered dataframe by provided dataset

    Usage
    ------
    >>> metrics_plot_all_datasets = MetricsPlotPerDataset(
            METRICS_PLOT_TITLE,
            benchmark_df,
            "hvplot",
            dataset="Dataset A",
            x_axis="framework",
            y_axis="loss_rescaled",
            graph_type=graph_dropdown,
            xlabel=FRAMEWORK_LABELS,
        )

    You can now call the `.plot()` method on this object to render the table as a Panel object on the dashboard website.

    """

    def __init__(
        self,
        plot_title: str,
        df_process: hvplot.Interactive,
        plot_type: str,
        dataset: str,
        x_axis: Optional[Union[str, List[str]]] = None,
        y_axis: Optional[Union[str, List[str]]] = None,
        graph_type: str = "bar",
        xlabel: str = "",
        ylabel: str = "",
        label_rot: int = 90,
    ) -> None:
        dataset_to_plot = self._preprocess(df=df_process, dataset_name=dataset)
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

    def _preprocess(self, df, dataset_name, **kwargs) -> pandas.DataFrame:
        return get_df_filter_by_dataset(df, dataset_name)
