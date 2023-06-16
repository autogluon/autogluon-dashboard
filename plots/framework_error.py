from scripts.plot import Plot

class FrameworkError(Plot):
    def __init__(self, plot_title, dataset_to_plot, plot_type, 
                 x_axis=None, y_axis=None, graph_type='bar', 
                 xlabel='', ylabel='', label_rot=90, table_cols=...):
        super().__init__(plot_title, dataset_to_plot, plot_type, x_axis,
                         y_axis, graph_type, xlabel, ylabel, 
                         label_rot, table_cols)
    
    def _preprocess(*args):
        return Plot._preprocess()
