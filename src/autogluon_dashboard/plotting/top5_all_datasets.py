from typing import List, Optional, Union

import hvplot
import pandas

from ..scripts.utils import get_top5_performers
from .all_plots import Plot


class Top5AllDatasets(Plot):
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
        label_rot: int = 90,
        table_cols: list = [],
    ) -> None:
        dataset_to_plot = self._preprocess(df=df_process, col_name=col_name)
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
        col_name_for_metrics = kwargs["col_name"]
        return get_top5_performers(df, col_name_for_metrics)
