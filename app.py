import panel as pn
import hvplot.pandas # noqa

# Load Data
from scripts.data import per_dataset_df, all_framework_df
# Import helpers
from scripts.widgets import create_selectwidget, create_togglewidget, create_numberwidget
from scripts.plots import create_hvplot,create_table
from scripts.config.widgets_config import METRICS_TO_PLOT, GRAPH_TYPES
from scripts.config.app_layout_config import APP_HEADER_BACKGROUND, APP_TITLE
from scripts.config.plots_config import METRICS_PLOT_TITLE, TOP5_PERFORMERS_TITLE, AG_RANK_COUNTS_TITLE, FRAMEWORK_LABEL, YAXIS_LABEL, DATASETS_LABEL, GRAPH_TYPE_STR, RANK_LABEL, ERROR_COUNTS_TITLE, AUTOGLUON_RANK1_TITLE
from scripts import utils

#clean up framework names
dataset_list = utils.get_sorted_names_from_col(per_dataset_df, 'dataset')
new_framework_names = per_dataset_df['framework'].str.extract(r"^(.*?)(?:_|$)")[0]
num_frameworks = len(set(new_framework_names))
for i in range(len(new_framework_names)):
    new_framework_names[i] = "AutoGluon" if i%num_frameworks==0 else "AutoGluon v" + f"0.{i%num_frameworks}"
utils.replace_df_column(per_dataset_df, 'framework', new_framework_names)
utils.replace_df_column(all_framework_df, 'framework', new_framework_names)

# Make DataFrame Interactive
per_dataset_idf = per_dataset_df.interactive()
all_framework_idf = all_framework_df.interactive()

# Define Panel widgets
frameworks_widget = create_selectwidget(FRAMEWORK_LABEL, options=new_framework_names.to_list())
yaxis_widget =  create_selectwidget(YAXIS_LABEL, options=METRICS_TO_PLOT)
yaxis_widget2 =  create_selectwidget(YAXIS_LABEL, options=METRICS_TO_PLOT)
datasets_widget = create_togglewidget(DATASETS_LABEL, dataset_list)
dataset_dropdown = create_selectwidget(DATASETS_LABEL, options=dataset_list)
graph_type = create_selectwidget(GRAPH_TYPE_STR, 'bar', GRAPH_TYPES)
graph_type2 = create_selectwidget(GRAPH_TYPE_STR, 'bar', GRAPH_TYPES)

#Some data processing
selected_dataset_df = utils.get_df_filter_by_dataset(per_dataset_idf, dataset_dropdown)
df_ag_only = utils.get_df_filter_by_framework(per_dataset_df, 'AutoGluon')
prop_ag_best = utils.get_proportion_framework_rank1(df_ag_only, per_dataset_df, len(dataset_list))
autogluon_rank_counts = utils.get_col_metric_counts(df_ag_only, 'rank')
per_dataset_top5 = utils.get_top5_performers(selected_dataset_df, 'rank')
all_datasets_top5 = utils.get_top5_performers(all_framework_idf, 'rank')

# Plots
metrics_plot_all_datasets = create_hvplot(idf=all_framework_idf, 
                            title=METRICS_PLOT_TITLE, 
                            x_axis='framework', 
                            y_axis=yaxis_widget, 
                            graph_type=graph_type, 
                            xlabel=FRAMEWORK_LABEL)
metrics_plot_per_datasets = create_hvplot(idf=selected_dataset_df, 
                            title=METRICS_PLOT_TITLE, 
                            x_axis='framework', 
                            y_axis=yaxis_widget2, 
                            graph_type=graph_type2, 
                            xlabel=FRAMEWORK_LABEL)
top5frameworks_all_datasets = create_table(all_datasets_top5, 
                                 TOP5_PERFORMERS_TITLE+" (all datasets)", 
                                 ['framework', 'rank'])
top5frameworks_per_dataset = create_table(per_dataset_top5, 
                                          TOP5_PERFORMERS_TITLE, 
                                          ['framework', 'rank'])
ag_rank_counts = create_hvplot(idf=autogluon_rank_counts,
                             title=AG_RANK_COUNTS_TITLE, 
                             rot=0,
                             xlabel=RANK_LABEL) 
framework_error = create_hvplot(idf=all_framework_idf,
                             title=ERROR_COUNTS_TITLE,
                             x_axis='framework', 
                             y_axis='error_count',  
                             xlabel=FRAMEWORK_LABEL)
ag_pct_rank1 = create_numberwidget(AUTOGLUON_RANK1_TITLE, round(prop_ag_best*100, 2), '{value}%')

# Layout using Template
template = pn.template.FastListTemplate(
    title=APP_TITLE, 
    main=[pn.Row('# All Datasets Comparison', 
                 pn.WidgetBox(
                     yaxis_widget, 
                     graph_type
                    ), 
                    metrics_plot_all_datasets.panel(), 
                    top5frameworks_all_datasets
                ), 
          pn.Row('# Per Dataset Comparison\n', 
                 pn.WidgetBox(
                     yaxis_widget2, 
                     dataset_dropdown, 
                     graph_type2
                    ), 
                    metrics_plot_per_datasets.panel(), 
                    top5frameworks_per_dataset
                ), 
          pn.Row('# Rank Comparisons', ag_pct_rank1, ag_rank_counts),
          pn.Row('# Error Counts', framework_error)],
    header_background=APP_HEADER_BACKGROUND,
)

template.servable()
