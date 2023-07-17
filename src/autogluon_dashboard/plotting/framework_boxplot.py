from typing import List, Optional, Union

import hvplot

from autogluon_dashboard.scripts.constants.df_constants import FRAMEWORK

from .all_plots import Plot


class FrameworkBoxPlot(Plot):
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
    _box_plot():
        `plot` function from parent `Plot` class is set to this
        returns a box plot for a given y-axis metric, plotted by framework

    Usage
    ------
    >>> framework_box = FrameworkBoxPlot("box plot", per_dataset_df, y_axis=["loss"])

    You can now call the `.plot()` method on this object to render the plot as a Panel object on the dashboard website.

    """

    def __init__(
        self,
        plot_title: str,
        dataset_to_plot: hvplot.Interactive,
        plot_type: str = "hvplot",
        x_axis: Optional[Union[str, List[str]]] = None,
        y_axis: Optional[Union[str, List[str]]] = None,
        graph_type: str = "box",
        xlabel: str = "",
        ylabel: str = "",
        label_rot: int = 90,
    ) -> None:
        super(FrameworkBoxPlot, self).__init__(
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
        self.plot = self._box_plot

    def _box_plot(self) -> hvplot.hvPlot.box:
        return self.df.hvplot.box(self.plot_y, by=FRAMEWORK, rot=self.label_rot)
