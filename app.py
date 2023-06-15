import panel as pn
import hvplot.pandas # noqa

# Load Data
from scripts.data import per_dataset_df, all_framework_df

# Import helpers
from scripts.widget import Widget
from plots.metrics_all_datasets import MetricsPlotAll
from plots.metrics_per_datasets import MetricsPlotPerDataset
from plots.top5_all_datasets import Top5AllDatasets
from plots.top5_per_dataset import Top5PerDataset
from plots.ag_rank_counts import AGRankCounts
from plots.framework_error import FrameworkError
from scripts.config.widgets_config import METRICS_TO_PLOT, GRAPH_TYPES
from scripts.config.app_layout_config import APP_HEADER_BACKGROUND, APP_TITLE
from scripts.config.plots_config import METRICS_PLOT_TITLE, TOP5_PERFORMERS_TITLE, AG_RANK_COUNTS_TITLE, FRAMEWORK_LABEL, YAXIS_LABEL, DATASETS_LABEL, GRAPH_TYPE_STR, RANK_LABEL, ERROR_COUNTS_TITLE, AUTOGLUON_RANK1_TITLE
from scripts import utils

#clean up framework names
dataset_list = utils.get_sorted_names_from_col(per_dataset_df, 'dataset')
new_framework_names = utils.get_name_before_first_underscore(per_dataset_df, 'framework')
num_frameworks = len(set(new_framework_names))
# dummy replacement
for i in range(len(new_framework_names)):
    new_framework_names[i] = "AutoGluon" if i%num_frameworks==0 else "AutoGluon v" + f"0.{i%num_frameworks}"
per_dataset_df['framework'] =  new_framework_names
all_framework_df['framework'] = new_framework_names

# Make DataFrame Interactive
per_dataset_idf = per_dataset_df.interactive()
all_framework_idf = all_framework_df.interactive()

# Define Panel widgets
frameworks_widget = Widget("select", name=FRAMEWORK_LABEL, options=new_framework_names.to_list()).create_widget()
yaxis_widget =  Widget("select", name=YAXIS_LABEL, options=METRICS_TO_PLOT).create_widget()
yaxis_widget2 =  Widget("select", name=YAXIS_LABEL, options=METRICS_TO_PLOT).create_widget()
dataset_dropdown = Widget("select", name=DATASETS_LABEL, options=dataset_list).create_widget()
graph_dropdown = Widget("select", name=GRAPH_TYPE_STR, options=GRAPH_TYPES).create_widget()
graph_dropdown2 = Widget("select", name=GRAPH_TYPE_STR, options=GRAPH_TYPES).create_widget()

df_ag_only = utils.get_df_filter_by_framework(per_dataset_df, 'AutoGluon')
prop_ag_best = utils.get_proportion_framework_rank1(df_ag_only, per_dataset_df, len(dataset_list))
ag_pct_rank1 = Widget("number", name=AUTOGLUON_RANK1_TITLE, value=round(prop_ag_best*100, 2), format='{value}%').create_widget()

# Plots
metrics_plot_all_datasets = MetricsPlotAll(METRICS_PLOT_TITLE, all_framework_idf, "hvplot",
                                 x_axis='framework', y_axis=yaxis_widget, 
                                 graph_type=graph_dropdown, xlabel=FRAMEWORK_LABEL)
top5frameworks_all_datasets = Top5AllDatasets(TOP5_PERFORMERS_TITLE+" (all datasets)", 
                                   all_framework_idf, "table", 
                                   'rank', table_cols=['framework', 'rank'])

metrics_plot_per_datasets = MetricsPlotPerDataset(METRICS_PLOT_TITLE, per_dataset_idf, "hvplot",
                                 dataset_dropdown, x_axis='framework', y_axis=yaxis_widget2, 
                                 graph_type=graph_dropdown2, xlabel=FRAMEWORK_LABEL)

top5frameworks_per_dataset = Top5PerDataset(TOP5_PERFORMERS_TITLE, 
                                   per_dataset_idf, "table", 
                                   'rank', dataset_dropdown,
                                   table_cols=['framework', 'rank'])
ag_rank_counts = AGRankCounts(AG_RANK_COUNTS_TITLE, per_dataset_df, "hvplot",
                              'rank', 'AutoGluon', xlabel=RANK_LABEL, label_rot=0)
framework_error = FrameworkError(ERROR_COUNTS_TITLE, all_framework_idf, "hvplot",
                       x_axis='framework', y_axis='error_count', xlabel=FRAMEWORK_LABEL)

# Layout using Template

plots = [metrics_plot_all_datasets, top5frameworks_all_datasets, metrics_plot_per_datasets, top5frameworks_per_dataset, ag_rank_counts, framework_error]
plots = [plot.plot() for plot in plots]

template = pn.template.FastListTemplate(
    title=APP_TITLE, 
    main=[pn.Row('# All Datasets Comparison', 
                 pn.WidgetBox(yaxis_widget, graph_dropdown), 
                    plots[0].panel(), 
                    plots[1]
                ), 
          pn.Row('# Per Dataset Comparison\n', 
                 pn.WidgetBox(yaxis_widget2, dataset_dropdown, graph_dropdown2), 
                    plots[2].panel(), 
                    plots[3]
                ), 
          pn.Row('# Rank Comparisons', ag_pct_rank1, plots[4]),
          pn.Row('# Error Counts', plots[5])],
    header_background=APP_HEADER_BACKGROUND,
)
template.servable()
