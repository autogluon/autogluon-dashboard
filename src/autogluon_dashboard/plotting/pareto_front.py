from typing import List, Optional, Union

import hvplot
import pandas

from .all_plots import Plot


class ParetoFront(Plot):
    """
    This class is used to create a pareto frontier plot of inference time v/s winrate, by framework.

    Attributes
    ----------
    plot_title: str,
        title of the plot on the dashboard website
    df_process: hvplot.Interactive,
        interactive pandas dataframe that is used to create the plot
        this should be the dataset of all frameworks aggregated across all datasets
    plot_type: str,
        type of hvplot. hvplot, table, pareto
    x_axis: Optional[Union[str, List[str]]],
        values to plot on x-axis
    y_axis: Optional[Union[str, List[str]]],
        values to plot on y-axis
    xlabel: str,
        label of x-axis
    ylabel: str,
        label of y-axis
    label_rot: int,
        rotation value of labels on axes

    Usage
    ------
    >>> pareto_front = ParetoFront("pareto plot", all_frameworks_df, "pareto", x_axis=TIME_INFER_S_RESCALED, y_axis=WINRATE)

    You can now call the `.plot()` method on this object to render the table as a Panel object on the dashboard website.

    """

    def __init__(
        self,
        plot_title: str,
        df_process: hvplot.Interactive,
        plot_type: str,
        x_axis: Optional[Union[str, List[str]]] = None,
        y_axis: Optional[Union[str, List[str]]] = None,
        graph_type: str = "bar",
        xlabel: str = "",
        ylabel: str = "",
        label_rot: int = 90,
    ) -> None:
        super().__init__(
            plot_title,
            df_process,
            plot_type,
            x_axis,
            y_axis,
            graph_type,
            xlabel,
            ylabel,
            label_rot,
        )
