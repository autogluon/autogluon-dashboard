from typing import List, Optional, Union

import hvplot
import pandas

from ..scripts.utils import get_df_filter_by_dataset
from .all_plots import Plot


class MetricsPlotPerDataset(Plot):
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
        table_cols: list = [],
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
            table_cols,
        )

    def _preprocess(self, **kwargs) -> pandas.DataFrame:
        df = kwargs["df"]
        dataset_str = kwargs["dataset_name"]
        return get_df_filter_by_dataset(df, dataset_str)
