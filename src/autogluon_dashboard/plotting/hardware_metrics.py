from typing import List, Optional, Union

import hvplot
import pandas
import panel as pn

from .plot import Plot


class HardwareMetrics(Plot):
    """
    This class is used to create a bar plot of hardware metrics across datasets and frameworks

    Attributes
    ----------
    plot_title: str,
        title of the plot on the dashboard website
    dataset_to_plot: hvplot.Interactive,
        interactive pandas dataframe that is used to create the plot
        this dataframe will first go through the preprocess method
        this should be the dataframe of all hardware metrics from the evaluation module
    plot_type: str,
        type of hvplot. hvplot, table, pareto
    col_name: str,
        column to get hardware metrics for
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
        returns a dataframe filtered by hardware metric type

    Usage
    ------
    >>> hware_metrics_plot = HardwareMetrics(
            HARDWARE_METRICS_PLOT_TITLE,
            hware_metrics_idf, "hvplot",
            col_name=yaxis_widget4,
            x_axis="framework",
            y_axis="statistic_value",
            ylabel=yaxis_widget4,
            by=by_widget)

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
        by: pn.widgets.Select = "",
        label_rot: int = 90,
        table_cols: list = [],
    ) -> None:

        dataset_to_plot = self._preprocess(df=df_process, col_name_for_metrics=col_name, group_by=by)

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
            by=by,
        )

    def _preprocess(self, df, col_name_for_metrics, group_by, **kwargs) -> pandas.DataFrame:
        df = df[:]
        df = df.groupby(["framework", "metric", group_by]).mean(numeric_only=True).reset_index()
        df.statistic_value = df.statistic_value.apply(lambda x: round(float(x), 2))
        df = df[df.metric.isin([col_name_for_metrics])]
        return df
