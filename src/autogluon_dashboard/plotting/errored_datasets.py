from typing import List, Optional, Union

import hvplot
import pandas

from autogluon_dashboard.scripts.constants.df_constants import DATASET

from ..scripts.utils import get_df_filter_by_framework, get_sorted_names_from_col
from .all_plots import Plot


class ErroredDatasets(Plot):
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
        table_cols: list = [],
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
            ["Errored Datasets"],
        )

    def _preprocess(self, df, framework, **kwargs) -> pandas.DataFrame:
        dataset_list = get_sorted_names_from_col(df, DATASET)
        df_filtered_by_framework = get_df_filter_by_framework(df, framework)
        datasets = df_filtered_by_framework.dataset.values
        errored_datasets = list(set(dataset_list).difference(datasets))
        return pandas.DataFrame({"Errored Datasets": errored_datasets})
