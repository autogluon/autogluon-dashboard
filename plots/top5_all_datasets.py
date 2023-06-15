from scripts.plot import Plot
from scripts.utils import get_top5_performers

class Top5AllDatasets(Plot):
    def __init__(self, plot_title, df_process, plot_type, col_name, 
                 x_axis=None, y_axis=None, graph_type='bar', 
                 xlabel='', ylabel='', label_rot=90, table_cols=...,):
        dataset_to_plot = self.preprocess(df_process, col_name)
        super().__init__(plot_title, dataset_to_plot, plot_type, x_axis,
                         y_axis, graph_type, xlabel, ylabel, 
                         label_rot, table_cols)
    
    def preprocess(self, *args):
        return get_top5_performers(args[0], args[1])
