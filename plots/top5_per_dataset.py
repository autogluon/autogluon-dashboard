from scripts.plot import Plot
from scripts.utils import get_top5_performers, get_df_filter_by_dataset
import pandas
import hvplot
from typing import Union

class Top5PerDataset(Plot):
    def __init__(self, plot_title:str, df_process:hvplot.Interactive, plot_type:str, col_name:str, 
                 dataset:str, x_axis:Union[str, list]=None, y_axis:Union[str, list]=None, graph_type:str='bar', 
                 xlabel:str='', ylabel:str='', label_rot:int=90, table_cols:list=...,) -> None:
        dataset_to_plot = self._preprocess(df_process, dataset, col_name)
        super().__init__(plot_title, dataset_to_plot, plot_type, x_axis,
                         y_axis, graph_type, xlabel, ylabel, 
                         label_rot, table_cols)
    
    def _preprocess(self, *args) -> pandas.DataFrame:
        df_filtered_by_dataset = get_df_filter_by_dataset(args[0], args[1])
        return get_top5_performers(df_filtered_by_dataset, args[2])
