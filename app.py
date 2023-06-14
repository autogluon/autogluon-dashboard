import panel as pn
import hvplot.pandas # noqa

# Load Data
from scripts.data import per_dataset_df, all_framework_df
# Import helpers
from scripts.widgets import create_selectwidget, create_togglewidget, create_numberwidget
from scripts.plots import create_hvplot,create_table
from scripts.constants import METRICS_TO_PLOT, GRAPH_TYPES, FRAMEWORK_LABEL, YAXIS_LABEL, DATASETS_LABEL, GRAPH_TYPE_STR
from scripts.utils import replace_df_column, get_sorted_names_from_col

#clean up framework names
original_framework_names = all_framework_df['framework']
dataset_list = get_sorted_names_from_col(per_dataset_df, 'dataset')
new_framework_names = per_dataset_df['framework'].str.extract(r"^(.*?)(?:_|$)")[0]
replace_df_column(per_dataset_df, 'framework', new_framework_names)
replace_df_column(all_framework_df, 'framework', new_framework_names)

# Make DataFrame Pipeline Interactive
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
idf_dataset = per_dataset_idf[(per_dataset_idf.dataset.isin([dataset_dropdown]))]
df_ag_only = per_dataset_df.loc[(per_dataset_df['framework'].isin(['AutoGluon']))]
df_ag_only = df_ag_only.sort_values(by=['rank'])
prop_ag_best = df_ag_only.loc[(per_dataset_df['rank'] == 1.0)].shape[0] / len(dataset_list)
# ALT METHOD: prop_ag_best = all_framework_df[all_framework_df['framework'] == 'AutoGluon']['winrate'][0]
ag_best = create_numberwidget('% 1st Rank for AutoGluon', round(prop_ag_best*100, 2), '{value}%')
autogluon_ranks = df_ag_only['rank'].value_counts()[df_ag_only['rank'].unique()]
per_dataset_top5 = idf_dataset[idf_dataset['rank'] <= 5].sort_values('rank')
all_datasets_top5 = all_framework_idf.sort_values('rank').head()

# Plots
ihvplot_all = create_hvplot(idf=all_framework_idf, 
                            title="Framework v/s Loss/Training Time/Inference Time/Best Diff ALL Datasets", 
                            x_axis='framework', 
                            y_axis=yaxis_widget, 
                            graph_type=graph_type, 
                            xlabel="Framework")
ihvplot_dataset = create_hvplot(idf=idf_dataset, 
                            title="Framework v/s Loss/Training Time/Inference Time/Best Diff per Dataset", 
                            x_axis='framework', 
                            y_axis=yaxis_widget2, 
                            graph_type=graph_type2, 
                            xlabel="Framework")
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
                             xlabel="Framework")

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
