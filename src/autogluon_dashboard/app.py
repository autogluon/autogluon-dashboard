import os

import panel as pn

from autogluon_dashboard.plotting.framework_error import FrameworkError
from autogluon_dashboard.plotting.metrics_all_datasets import MetricsPlotAll
from autogluon_dashboard.plotting.metrics_per_datasets import MetricsPlotPerDataset
from autogluon_dashboard.plotting.rank_counts_ag import AGRankCounts
from autogluon_dashboard.plotting.top5_all_datasets import Top5AllDatasets
from autogluon_dashboard.plotting.top5_per_dataset import Top5PerDataset
from autogluon_dashboard.scripts import utils
from autogluon_dashboard.scripts.constants.app_layout_constants import (
    ALL_DATA_COMP,
    APP_HEADER_BACKGROUND,
    APP_TITLE,
    NO_ERROR_CNTS,
    NO_RANK_COMP,
    PER_DATA_COMP,
)
from autogluon_dashboard.scripts.constants.plots_constants import (
    AG_RANK_COUNTS_TITLE,
    AUTOGLUON_RANK1_TITLE,
    DATASETS_LABEL,
    ERROR_COUNTS_TITLE,
    FRAMEWORK_LABEL,
    GRAPH_TYPE_STR,
    METRICS_PLOT_TITLE,
    RANK_LABEL,
    TOP5_PERFORMERS_TITLE,
    YAXIS_LABEL,
)
from autogluon_dashboard.scripts.constants.widgets_constants import GRAPH_TYPES, METRICS_TO_PLOT

# Load Data
from autogluon_dashboard.scripts.data import get_dataframes
from autogluon_dashboard.scripts.widget import Widget

# TODO: Remove hardcoded default csv path
dataset_file = os.environ.get(
    "PER_DATASET_S3_PATH", "https://dashboard-test-yash.s3.us-west-2.amazonaws.com/dev_data/all_data.csv"
)
aggregated_file = os.environ.get(
    "AGG_DATASET_S3_PATH", "https://dashboard-test-yash.s3.us-west-2.amazonaws.com/dev_data/autogluon.csv"
)
per_dataset_df, all_framework_df = get_dataframes(dataset_file, aggregated_file)

# clean up framework names
dataset_list = utils.get_sorted_names_from_col(per_dataset_df, "dataset")
new_framework_names = utils.clean_up_framework_names(per_dataset_df)
per_dataset_df["framework"] = new_framework_names
all_framework_df["framework"] = new_framework_names

# Make DataFrame Interactive
per_dataset_idf = per_dataset_df.interactive()
all_framework_idf = all_framework_df.interactive()

# Define Panel widgets
frameworks_widget = Widget("select", name=FRAMEWORK_LABEL, options=new_framework_names.to_list()).create_widget()
yaxis_widget = Widget("select", name=YAXIS_LABEL, options=METRICS_TO_PLOT).create_widget()
yaxis_widget2 = Widget("select", name=YAXIS_LABEL, options=METRICS_TO_PLOT).create_widget()
dataset_dropdown = Widget("select", name=DATASETS_LABEL, options=dataset_list).create_widget()
graph_dropdown = Widget("select", name=GRAPH_TYPE_STR, options=GRAPH_TYPES).create_widget()
graph_dropdown2 = Widget("select", name=GRAPH_TYPE_STR, options=GRAPH_TYPES).create_widget()

df_ag_only = utils.get_df_filter_by_framework(per_dataset_df, "AutoGluon")
prop_ag_best = utils.get_proportion_framework_rank1(df_ag_only, per_dataset_df, len(dataset_list))
ag_pct_rank1 = Widget(
    "number",
    name=AUTOGLUON_RANK1_TITLE,
    value=round(prop_ag_best * 100, 2),
    format="{value}%",
).create_widget()

# Plots
metrics_plot_all_datasets = MetricsPlotAll(
    METRICS_PLOT_TITLE,
    all_framework_idf,
    "hvplot",
    x_axis="framework",
    y_axis=yaxis_widget,
    graph_type=graph_dropdown,
    xlabel=FRAMEWORK_LABEL,
)
top5frameworks_all_datasets = Top5AllDatasets(
    TOP5_PERFORMERS_TITLE + " (all datasets)",
    all_framework_idf,
    "table",
    "rank",
    table_cols=["framework", "rank"],
)

metrics_plot_per_datasets = MetricsPlotPerDataset(
    METRICS_PLOT_TITLE,
    per_dataset_idf,
    "hvplot",
    dataset_dropdown,
    x_axis="framework",
    y_axis=yaxis_widget2,
    graph_type=graph_dropdown2,
    xlabel=FRAMEWORK_LABEL,
)

top5frameworks_per_dataset = Top5PerDataset(
    TOP5_PERFORMERS_TITLE,
    per_dataset_idf,
    "table",
    "rank",
    dataset_dropdown,
    table_cols=["framework", "rank"],
)
ag_rank_counts = AGRankCounts(
    AG_RANK_COUNTS_TITLE,
    per_dataset_df,
    "hvplot",
    "rank",
    "AutoGluon",
    xlabel=RANK_LABEL,
    label_rot=0,
)
framework_error = FrameworkError(
    ERROR_COUNTS_TITLE,
    all_framework_idf,
    "hvplot",
    x_axis="framework",
    y_axis="error_count",
    xlabel=FRAMEWORK_LABEL,
)

# Order matters here!
plots = [
    metrics_plot_all_datasets,
    top5frameworks_all_datasets,
    metrics_plot_per_datasets,
    top5frameworks_per_dataset,
    ag_rank_counts,
    framework_error,
]
plots = [plot.plot() for plot in plots]
plot_ctr = iter(range(len(plots)))
template = pn.template.FastListTemplate(
    title=APP_TITLE,
    main=[
        pn.Row(
            ALL_DATA_COMP,
            pn.WidgetBox(yaxis_widget, graph_dropdown),
            plots[next(plot_ctr)].panel(),
            plots[next(plot_ctr)],
        ),
        pn.Row(
            PER_DATA_COMP,
            pn.WidgetBox(yaxis_widget2, dataset_dropdown, graph_dropdown2),
            plots[next(plot_ctr)].panel(),
            plots[next(plot_ctr)],
        ),
        pn.Row(NO_RANK_COMP, ag_pct_rank1, plots[next(plot_ctr)]),
        pn.Row(NO_ERROR_CNTS, plots[next(plot_ctr)]),
    ],
    header_background=APP_HEADER_BACKGROUND,
)
template.servable()
