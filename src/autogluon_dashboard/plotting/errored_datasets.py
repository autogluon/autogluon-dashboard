from typing import List, Optional, Union

import hvplot
import pandas

from autogluon_dashboard.scripts.constants.df_constants import DATASET

from ..scripts.utils import get_df_filter_by_framework, get_sorted_names_from_col
from .all_plots import Plot

ERRORED_DATASETS = "Errored Datasets"


class ErroredDatasets(Plot):
    """
    This class is used to create a table of datasets that errored out during a benchmark run for a given framework.

    Attributes
    ----------
    plot_title: str,
        title of the plot on the dashboard website
    df_process: hvplot.Interactive,
        interactive pandas dataframe that is used to create the plot
        this dataframe will first go through the preprocess method
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
        returns a table containing the datasets that errored out for a provided framework
    
    Usage
    ------
    >>> errored_datasets_plot = ErroredDatasets("AutoGluon Errored Datasets", benchmark_df, "table", framework)

    You can now call the `.plot()` method on this object to render the plot as a Panel object on the dashboard website.
    
    """
    def __init__(
        self,
        plot_title: str,
        df_process: hvplot.Interactive,
        plot_type: str,
        framework: str,
        x_axis: Optional[Union[str, List[str]]] = None,
        y_axis: Optional[Union[str, List[str]]] = None,
        graph_type: str = "bar",
        xlabel: str = "",
        ylabel: str = "",
        label_rot: int = 90,
    ) -> None:
        dataset_to_plot = self._preprocess(df=df_process, framework=framework)
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
            [ERRORED_DATASETS],
        )

    def _preprocess(self, df, framework, **kwargs) -> pandas.DataFrame:
        dataset_list = get_sorted_names_from_col(df, DATASET)
        df_filtered_by_framework = get_df_filter_by_framework(df, framework)
        datasets = df_filtered_by_framework.dataset.values
        errored_datasets = list(set(dataset_list).difference(datasets))
        return pandas.DataFrame({ERRORED_DATASETS: errored_datasets})
