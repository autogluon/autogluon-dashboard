from typing import Optional

import hvplot
import pandas

from ..utils.dataset_utils import get_df_filter_by_dataset, get_df_filter_by_framework
from .plot import Plot


class InteractiveDataframe(Plot):
    """
    This class is used to create an ineractive python dataframe, displayed as a table
    This allows the user to view the source data (csv files) being used to compose the plots

    Attributes
    ----------
    df_process: hvplot.Interactive,
        interactive pandas dataframe that is used to create the plot
        this dataframe will first go through the preprocess method
    framework: str,
        if desired, what framework the table should be filered by
        default = All Frameworks
    width: int,
        width of output table
    dataset: Optional[str],
        if desired, what dataset the table should be filered by

    Methods
    -------
    _preprocess():
        inherited from parent `Plot` class
        returns the dataframe filtered by provided framework and dataset

    get_interactive_df():
        returns an interactive table of the pandas dataframe

    Usage
    ------
    >>> interactive_df = InteractiveDataframe(benchmark_df, "AutoGluon", width=3000, dataset="Dataset A")

    You can now call the `.get_interactive_df()` method on this object to render the table as a Panel object on the dashboard website.

    """

    def __init__(
        self, df_process: hvplot.Interactive, framework: str, width: int, dataset: Optional[str] = None
    ) -> None:
        self.dataset_to_plot = df_process
        self.framework = framework
        self.table_width = width
        self.dataset = dataset

    def get_interactive_df(self) -> hvplot.Interactive:
        return hvplot.bind(self._preprocess, framework=self.framework, dataset=self.dataset).interactive(
            width=self.table_width
        )

    def _preprocess(self, framework, dataset, **kwargs) -> pandas.DataFrame:
        df = self.dataset_to_plot
        if dataset:
            df = get_df_filter_by_dataset(df, dataset)
        if "All Frameworks" in framework:
            return df
        return get_df_filter_by_framework(df, framework)
