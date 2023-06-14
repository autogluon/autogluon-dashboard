import panel as pn
import hvplot.pandas # noqa

# Load Data
from scripts.data import per_dataset_df, all_framework_df
# Import helpers
from scripts.widgets import create_selectwidget, create_togglewidget, create_numberwidget
from scripts.plots import create_hvplot,create_table
from scripts.constants import METRICS_TO_PLOT, GRAPH_TYPES, FRAMEWORK_LABEL, YAXIS_LABEL, DATASETS_LABEL, GRAPH_TYPE_STR
from scripts import utils

#clean up framework names
original_framework_names = all_framework_df['framework']
dataset_list = utils.get_sorted_names_from_col(per_dataset_df, 'dataset')
new_framework_names = per_dataset_df['framework'].str.extract(r"^(.*?)(?:_|$)")[0]
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
autogluon_ranks = utils.get_col_metric_counts(df_ag_only, 'rank')
per_dataset_top5 = utils.get_top5_performers(selected_dataset_df, 'rank')
all_datasets_top5 = utils.get_top5_performers(all_framework_idf, 'rank')

# Plots
ihvplot_all = create_hvplot(idf=all_framework_idf, 
                            title="Framework v/s Loss/Training Time/Inference Time/Best Diff ALL Datasets", 
                            x_axis='framework', 
                            y_axis=yaxis_widget, 
                            graph_type=graph_type, 
                            xlabel=FRAMEWORK_LABEL)
ihvplot_dataset = create_hvplot(idf=selected_dataset_df, 
                            title="Framework v/s Loss/Training Time/Inference Time/Best Diff per Dataset", 
                            x_axis='framework', 
                            y_axis=yaxis_widget2, 
                            graph_type=graph_type2, 
                            xlabel=FRAMEWORK_LABEL)
top5_all_datasets = create_table(all_datasets_top5, 
                                 "Top 5 Performers (all datasets)", 
                                 ['framework', 'rank'])
top5frameworks_per_dataset = create_table(per_dataset_top5, 
                                          "Top 5 Performers", 
                                          ['framework', 'rank'])
ag_rank_hist = create_hvplot(idf=autogluon_ranks,
                             title="Rank Frequency of AutoGluon", 
                             rot=0,
                             xlabel="Rank") 
framework_error = create_hvplot(idf=all_framework_idf,
                             title="Framework v/s Error Counts",
                             x_axis='framework', 
                             y_axis='error_count',  
                             xlabel=FRAMEWORK_LABEL)
ag_best = create_numberwidget('% 1st Rank for AutoGluon', round(prop_ag_best*100, 2), '{value}%')

# Layout using Template
template = pn.template.FastListTemplate(
    title='Interactive AutoGluon Dashboards', 
    #sidebar=[yaxis, dataset_dropdown],
    main=[pn.Row('# All Datasets Comparison', 
                 pn.WidgetBox(
                     yaxis_widget, 
                     graph_type
                    ), 
                    ihvplot_all.panel(), 
                    top5_all_datasets
                ), 
          pn.Row('# Per Dataset Comparison\n', 
                 pn.WidgetBox(
                     yaxis_widget2, 
                     dataset_dropdown, 
                     graph_type2
                    ), 
                    ihvplot_dataset.panel(), 
                    top5frameworks_per_dataset
                ), 
          pn.Row('# Rank Comparisons', ag_best, ag_rank_hist),
          pn.Row('# Error Counts', framework_error)],
    header_background="#88d8b0",
)

template.servable()
