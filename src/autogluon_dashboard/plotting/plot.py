from abc import abstractmethod
from typing import List, Optional, Union

import hvplot.pandas
import pandas as pd

from autogluon_dashboard.constants.df_constants import FRAMEWORK


class Plot:
    """
    This parent class is used to define all plots that are used on the dashboard website.
    It is inherited by subplot classes for individual plots

    Attributes
    ----------
    plot_title: str,
        title of the plot on the dashboard website
    dataset_to_plot: hvplot.Interactive,
        interactive pandas dataframe that is used to create the plot
    plot_type: str,
        type of hvplot. hvplot, table, pareto
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
    table_cols: list,
        list of columns to use for table plots
    table_width: Optional[int],
        width of table

    Methods
    -------
    _preprocess():
        preprocess data from dataframe before plotting. Inherited and redefined by appropriate subclasses.

    _create_hvplot():
        Create a plot of a given type leveraging the hvplot library,
        and using data from a pandas interactive dataframe.

    _create_table():
        Create a table leveraging the hvplot library,
        and using data from a pandas interactive dataframe.

    _create_pareto_front():
        Create a Pareto frontier plot leveraging the hvplot library
    """

    def __init__(
        self,
        plot_title: str,
        dataset_to_plot: hvplot.Interactive,
        plot_type: str,
        x_axis: Optional[Union[str, List[str]]] = None,
        y_axis: Optional[Union[str, List[str]]] = None,
        graph_type: str = "bar",
        xlabel: str = "",
        ylabel: str = "",
        label_rot: int = 90,
        table_cols: list = [],
        table_width: Optional[int] = None,
        by: str = "",
    ) -> None:
        self.plot_title = plot_title
        self.df = dataset_to_plot
        self.plot_x = x_axis
        self.plot_y = y_axis
        self.graph_type = graph_type
        self.plot_x_label = xlabel
        self.plot_y_label = ylabel
        self.by = by
        self.label_rot = label_rot
        self.table_cols = table_cols
        self.table_width = table_width

        if plot_type == "table":
            self.plot = self._create_table
        elif plot_type == "hvplot":
            self.plot = self._create_hvplot
        elif plot_type == "pareto":
            self.plot = self._create_pareto_front

    @abstractmethod
    def _preprocess(self, **kwargs):
        return

    def _create_hvplot(
        self,
        color_scheme: list = ["#ff6f69", "#ffcc5c", "#88d8b0"],
        line_width: Union[int, float] = 6,
        height: Union[int, float] = 500,
    ) -> hvplot.hvPlot:
        """
        Create a plot of a given type leveraging the hvplot library,
        and using data from a pandas interactive dataframe.

        Parameters
        ----------
        idf: Pandas dataframe,
            Data to plot on.
        x_axis: str or list, default=None,
        Column name (as string) in dataframe or, list of values to plot on.
        y_axis: str or list, default=None,
            Column name (as string) in dataframe or, list of values to plot on.
        graph_type: str, default='bar',
            Type of plot. Examples: line, hist, bar, scatter
        xlabel: str,
            x-axis Label.
        ylabel: str,
            y-axis Label.
        color_scheme: list, default=["#ff6f69", "#ffcc5c", "#88d8b0"],
            Color scheme of plot.
        line_width: int, default=6,
            Width of line in plot.
        height: int, default=500,
            Height of plot frame.
        rot: int, default=0,
            Rotation amount for x-axis labels
        """
        if self.plot_x is None or self.plot_y is None:
            return self.df.hvplot(
                title=self.plot_title,
                kind=self.graph_type,
                color=color_scheme,
                line_width=line_width,
                height=height,
                rot=self.label_rot,
                xlabel=self.plot_x_label,
                ylabel=self.plot_y_label,
                grid=True,
            ).opts(active_tools=[])
        if self.by:
            return self.df.hvplot(
                title=self.plot_title,
                x=self.plot_x,
                y=self.plot_y,
                kind=self.graph_type,
                ylabel=self.plot_y_label,
                by=self.by,
                grid=True,
            ).opts(active_tools=[])
        return self.df.hvplot(
            title=self.plot_title,
            x=self.plot_x,
            y=self.plot_y,
            kind=self.graph_type,
            color=color_scheme,
            line_width=line_width,
            height=height,
            rot=self.label_rot,
            xlabel=self.plot_x_label,
            ylabel=self.plot_y_label,
            grid=True,
        ).opts(active_tools=[])

    def _create_table(self, width: Union[int, float] = 800) -> hvplot.hvPlot.table:
        """
        Create a table leveraging the hvplot library,
        and using data from a pandas interactive dataframe.

        Parameters
        ----------
        idf: Pandas dataframe,
            Data to create the table from.
        title: str,
            Title of the table.
        columns: list,
            List of strings of column names to create the table.
            The strings should match column names in the provided idf.
        width: int, default=800,
            Width of the table.
        """
        table_width = width if not self.table_width else self.table_width
        return self.df.hvplot.table(title=self.plot_title, columns=self.table_cols, width=table_width)

    def _create_pareto_front(
        self, maxY: bool = True, width: Union[int, float] = 900, size: int = 400
    ) -> hvplot.hvPlot:
        """
        Create a Pareto frontier plot leveraging the hvplot library
        The plot is inference time v/s winrate for each framework
        The pareto frontier line is created by looking at smallest inference time and best winrate

        Parameters
        ----------
        maxY: bool,
            Boolean value whether to maximize y-axis values in logic to calculate pareto front plots
        width: int, default=800,
            Width of the table.
        size: int, default = 400,
            Size of points in scatter plot -> represents framework
        """
        Xs, Ys = self.df[self.plot_x], self.df[self.plot_y]
        sorted_list = sorted([[Xs[i], Ys[i]] for i in range(len(Xs))], reverse=False)
        pareto_front = [sorted_list[0]]
        for pair in sorted_list[1:]:
            if maxY:
                if pair[1] >= pareto_front[-1][1]:
                    pareto_front.append(pair)
            else:
                if pair[1] <= pareto_front[-1][1]:
                    pareto_front.append(pair)

        pf_X = [pair[0] for pair in pareto_front]
        pf_Y = [pair[1] for pair in pareto_front]
        pareto_df = pd.DataFrame({"col1": pf_X, "col2": pf_Y})

        plot = self.df.hvplot(
            x=self.plot_x,
            y=self.plot_y,
            c=FRAMEWORK,
            kind="scatter",
            size=size,
            height=800,
            width=width,
            grid=True,
        ).opts(active_tools=[]) * pareto_df.hvplot.step(x="col1", y="col2").opts(active_tools=[])
        return plot
