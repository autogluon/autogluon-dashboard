import hvplot
import pandas

from ..scripts.utils import get_df_filter_by_framework
from .all_plots import Plot


class InteractiveDataframe(Plot):
    def __init__(
        self,
        df_process: hvplot.Interactive,
        framework: str,
        width: int,
    ) -> None:
        self.dataset_to_plot = df_process
        self.framework = framework
        self.table_width = width

    def get_interactive_df(self) -> hvplot.Interactive:
        return hvplot.bind(self._preprocess, self.framework).interactive(width=self.table_width)

    def _preprocess(*args) -> pandas.DataFrame:
        if "All Frameworks" in args[1]:
            return args[0].dataset_to_plot
        df = get_df_filter_by_framework(args[0].dataset_to_plot, args[1])
        return df
