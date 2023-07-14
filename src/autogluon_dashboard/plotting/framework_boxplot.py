from typing import List, Optional, Union

import hvplot

from autogluon_dashboard.scripts.constants.df_constants import FRAMEWORK

from .all_plots import Plot


class FrameworkBoxPlot(Plot):
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
        table_cols: list = [],
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
            table_cols,
        )
        self.plot = self._box_plot

    def _box_plot(self) -> hvplot.hvPlot.box:
        return self.df.hvplot.box(self.plot_y, by=FRAMEWORK, rot=self.label_rot)
