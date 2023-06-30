from abc import abstractmethod
from typing import Union

import hvplot.pandas


class Plot:
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
        table_cols: list = [],
    ) -> None:
        self.plot_title = plot_title
        self.df = dataset_to_plot
        self.plot_x = x_axis
        self.plot_y = y_axis
        self.graph_type = graph_type
        self.plot_x_label = xlabel
        self.plot_y_label = ylabel
        self.label_rot = label_rot
        self.table_cols = table_cols

        self.plot = self._create_table if plot_type == "table" else self._create_hvplot

    @abstractmethod
    def _preprocess(self, *args):
        return

    def _create_hvplot(
        self,
        color_scheme: list = ["#ff6f69", "#ffcc5c", "#88d8b0"],
        line_width: Union[int, float] = 6,
        height: Union[int, float] = 500,
        by=None,
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
            )
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
            grid=True,
        )

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
        return self.df.hvplot.table(title=self.plot_title, columns=self.table_cols, width=width)
