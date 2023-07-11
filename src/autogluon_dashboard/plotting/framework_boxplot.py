from typing import List, Optional, Union

import hvplot
import pandas

from ..scripts.utils import get_df_filter_by_dataset
from .all_plots import Plot


class FrameworkBoxPlot(Plot):
    def __init__(
        self,
        plot_title: str,
        dataset_to_plot: hvplot.Interactive,
        plot_type: str = "hvplot",
        dataset: Optional[str] = None,
        x_axis: Optional[Union[str, List[str]]] = None,
        y_axis: Optional[Union[str, List[str]]] = None,
        graph_type: str = "box",
        xlabel: str = "",
        ylabel: str = "",
        label_rot: int = 90,
        table_cols: list = [],
    ) -> None:
        df = self._preprocess(df=dataset_to_plot, dataset=dataset)
        super(FrameworkBoxPlot, self).__init__(
            plot_title,
            df,
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

    def _preprocess(self, df, dataset, **kwargs) -> pandas.Series:
        data = get_df_filter_by_dataset(df, dataset) if dataset else df
        return data

    def _box_plot(self) -> hvplot.hvPlot.box:
        return self.df.hvplot.box(self.plot_y, by="framework", rot=self.label_rot, width=1000, height=500, grid=True)
