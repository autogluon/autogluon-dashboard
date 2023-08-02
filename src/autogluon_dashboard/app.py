import os

import panel as pn

from autogluon_dashboard.constants.app_layout_constants import (
    ALL_DATA_COMP,
    ALL_FRAMEWORKS_IDF,
    APP_HEADER_BACKGROUND,
    APP_TITLE,
    DOWNLOAD_FILES_TITLE,
    FRAMEWORK_BOX_PLOT,
    HARDWARE_METRICS_PLOT,
    NO_ERROR_CNTS,
    NO_RANK_COMP,
    PARETO_FRONT_PLOT,
    PER_DATA_COMP,
    PER_DATASET_IDF,
)
from autogluon_dashboard.constants.aws_s3_constants import (
    AGG_FRAMEWORK_DEFAULT_CSV_PATH,
    HARDWARE_METRICS_DEFAULT_CSV_PATH,
    PER_DATASET_DEFAULT_CSV_PATH,
)
from autogluon_dashboard.constants.df_constants import (
    DATASET,
    ERROR_COUNT,
    FRAMEWORK,
    RANK,
    TIME_INFER_S_RESCALED,
    WINRATE,
)
from autogluon_dashboard.constants.plots_constants import (
    AG_RANK_COUNTS_TITLE,
    AGG_FRAMEWORKS_DOWNLOAD_TITLE,
    AUTOGLUON_RANK1_TITLE,
    DATASETS_LABEL,
    DF_WIDGET_NAME,
    ERROR_COUNTS_TITLE,
    FRAMEWORK_BOX_PLOT_TITLE,
    FRAMEWORK_LABEL,
    GRAPH_TYPE_STR,
    HARDWARE_METRICS_DOWNLOAD_TITLE,
    HARDWARE_METRICS_PLOT_TITLE,
    HW_METRICS_WIDGET_NAME,
    METRICS_PLOT_TITLE,
    PER_DATASET_DOWNLOAD_TITLE,
    RANK_LABEL,
    TOP5_PERFORMERS_TITLE,
    YAXIS_LABEL,
)
from autogluon_dashboard.constants.widgets_constants import GRAPH_TYPES, METRICS_TO_PLOT
from autogluon_dashboard.plotting.errored_datasets import ErroredDatasets
from autogluon_dashboard.plotting.framework_boxplot import FrameworkBoxPlot
from autogluon_dashboard.plotting.framework_error import FrameworkError
from autogluon_dashboard.plotting.hardware_metrics import HardwareMetrics
from autogluon_dashboard.plotting.interactive_df import InteractiveDataframe
from autogluon_dashboard.plotting.metric_counts_framework import FrameworkMetricCounts
from autogluon_dashboard.plotting.metrics_all_datasets import MetricsPlotAll
from autogluon_dashboard.plotting.metrics_per_datasets import MetricsPlotPerDataset
from autogluon_dashboard.plotting.pareto_front import ParetoFront
from autogluon_dashboard.plotting.top5_all_datasets import Top5AllDatasets
from autogluon_dashboard.plotting.top5_per_dataset import Top5PerDataset
from autogluon_dashboard.utils.dataset_utils import (
    clean_up_framework_names,
    get_df_filter_by_framework,
    get_proportion_framework_rank1,
    get_sorted_names_from_col,
)
from autogluon_dashboard.utils.get_data import get_dataframes
from autogluon_dashboard.widgets.filedownload_widget import FileDownloadWidget
from autogluon_dashboard.widgets.number_widget import NumberWidget
from autogluon_dashboard.widgets.select_widget import SelectWidget
from autogluon_dashboard.widgets.slider_widget import SliderWidget

# Load Data
dataset_file = os.environ.get("PER_DATASET_S3_PATH", PER_DATASET_DEFAULT_CSV_PATH)
aggregated_file = os.environ.get("AGG_DATASET_S3_PATH", AGG_FRAMEWORK_DEFAULT_CSV_PATH)
hardware_metrics_file = os.environ.get("HWARE_METRICS_S3_PATH", HARDWARE_METRICS_DEFAULT_CSV_PATH)
dataset_paths = [dataset_file, aggregated_file, hardware_metrics_file]
per_dataset_df, all_framework_df, hware_metrics_df = get_dataframes(dataset_paths)

# clean up framework names
dataset_list = get_sorted_names_from_col(per_dataset_df, DATASET)
new_framework_names = clean_up_framework_names(per_dataset_df)
per_dataset_df[FRAMEWORK] = new_framework_names
all_framework_df[FRAMEWORK] = new_framework_names

frameworks_list = get_sorted_names_from_col(all_framework_df, FRAMEWORK)
frameworks_list.insert(0, "All Frameworks")

# Make DataFrame Interactive
per_dataset_idf = per_dataset_df.interactive()
all_framework_idf = all_framework_df.interactive()
hware_metrics_idf = hware_metrics_df.interactive()

# Define Panel widgets
frameworks_widget = SelectWidget(name=FRAMEWORK_LABEL, options=frameworks_list).create_widget()
frameworks_widget2 = SelectWidget(name=FRAMEWORK_LABEL, options=frameworks_list).create_widget()
yaxis_widget = SelectWidget(name=YAXIS_LABEL, options=METRICS_TO_PLOT).create_widget()
yaxis_widget2 = SelectWidget(name=YAXIS_LABEL, options=METRICS_TO_PLOT).create_widget()
yaxis_widget3 = SelectWidget(name=YAXIS_LABEL, options=METRICS_TO_PLOT).create_widget()
dataset_dropdown = SelectWidget(name=DATASETS_LABEL, options=dataset_list).create_widget()
dataset_dropdown2 = SelectWidget(name=DATASETS_LABEL, options=dataset_list).create_widget()
graph_dropdown = SelectWidget(name=GRAPH_TYPE_STR, options=GRAPH_TYPES).create_widget()
graph_dropdown2 = SelectWidget(name=GRAPH_TYPE_STR, options=GRAPH_TYPES).create_widget()
nrows = SliderWidget(name=DF_WIDGET_NAME, start=1, end=len(frameworks_list) - 1, value=10).create_widget()
nrows2 = SliderWidget(name=DF_WIDGET_NAME, start=1, end=len(frameworks_list) - 1, value=10).create_widget()
yaxis_widget4 = SelectWidget(
    name=HW_METRICS_WIDGET_NAME, options=list(hware_metrics_df.metric.unique())
).create_widget()

per_dataset_df.to_csv(PER_DATASET_DOWNLOAD_TITLE)
per_dataset_csv_widget = FileDownloadWidget(file=PER_DATASET_DOWNLOAD_TITLE).create_widget()
all_framework_df.to_csv(AGG_FRAMEWORKS_DOWNLOAD_TITLE)
all_framework_csv_widget = FileDownloadWidget(file=AGG_FRAMEWORKS_DOWNLOAD_TITLE).create_widget()
hware_metrics_df.to_csv(HARDWARE_METRICS_DOWNLOAD_TITLE)
hware_metrics_csv_widget = FileDownloadWidget(file=HARDWARE_METRICS_DOWNLOAD_TITLE).create_widget()

df_ag_only = get_df_filter_by_framework(per_dataset_df, "AutoGluon")
prop_ag_best = get_proportion_framework_rank1(df_ag_only, per_dataset_df, len(dataset_list))
ag_pct_rank1 = NumberWidget(
    name=AUTOGLUON_RANK1_TITLE,
    value=round(prop_ag_best * 100, 2),
    format="{value}%",
).create_widget()

# Plots
metrics_plot_all_datasets = MetricsPlotAll(
    METRICS_PLOT_TITLE,
    all_framework_idf,
    "hvplot",
    x_axis=FRAMEWORK,
    y_axis=yaxis_widget,
    graph_type=graph_dropdown,
    xlabel=FRAMEWORK_LABEL,
)
top5frameworks_all_datasets = Top5AllDatasets(
    TOP5_PERFORMERS_TITLE + " (all datasets)",
    all_framework_idf,
    "table",
    RANK,
    table_cols=[FRAMEWORK, RANK],
)

metrics_plot_per_datasets = MetricsPlotPerDataset(
    METRICS_PLOT_TITLE,
    per_dataset_idf,
    "hvplot",
    dataset_dropdown,
    x_axis=FRAMEWORK,
    y_axis=yaxis_widget2,
    graph_type=graph_dropdown2,
    xlabel=FRAMEWORK_LABEL,
)

top5frameworks_per_dataset = Top5PerDataset(
    TOP5_PERFORMERS_TITLE,
    per_dataset_idf,
    "table",
    RANK,
    dataset_dropdown,
    table_cols=[FRAMEWORK, RANK],
)
ag_rank_counts = FrameworkMetricCounts(
    AG_RANK_COUNTS_TITLE,
    per_dataset_df,
    "hvplot",
    RANK,
    "AutoGluon",
    xlabel=RANK_LABEL,
    label_rot=0,
)
framework_error = FrameworkError(
    ERROR_COUNTS_TITLE,
    all_framework_idf,
    "hvplot",
    x_axis=FRAMEWORK,
    y_axis=ERROR_COUNT,
    xlabel=FRAMEWORK_LABEL,
)

interactive_df_dataset = InteractiveDataframe(
    per_dataset_df.sort_values(by=RANK), frameworks_widget2, width=3000, dataset=dataset_dropdown2
)
per_dataset_dfi = interactive_df_dataset.get_interactive_df().head(nrows)

interactive_df_framework = InteractiveDataframe(all_framework_df, frameworks_widget, width=3000)
agg_framework_dfi = interactive_df_framework.get_interactive_df().head(nrows2)

framework_box = FrameworkBoxPlot(FRAMEWORK_BOX_PLOT_TITLE, per_dataset_df, y_axis=yaxis_widget3)

pareto_front = ParetoFront(PARETO_FRONT_PLOT, all_framework_df, "pareto", x_axis=TIME_INFER_S_RESCALED, y_axis=WINRATE)

hware_metrics_by_mode_plot = HardwareMetrics(
    HARDWARE_METRICS_PLOT_TITLE,
    hware_metrics_idf,
    "hvplot",
    col_name=yaxis_widget4,
    x_axis="framework",
    y_axis="statistic_value",
    ylabel=yaxis_widget4,
    by="mode",
)

hware_metrics_by_dataset_plot = HardwareMetrics(
    HARDWARE_METRICS_PLOT_TITLE,
    hware_metrics_idf,
    "hvplot",
    col_name=yaxis_widget4,
    x_axis="framework",
    y_axis="statistic_value",
    ylabel=yaxis_widget4,
    by="dataset",
)

framework_error_list = all_framework_df.sort_values(by=ERROR_COUNT, ascending=False)
error_tables = [
    ErroredDatasets(f"{framework} Errored Datasets", per_dataset_df, "table", framework).plot(width=225)
    for framework in framework_error_list[FRAMEWORK]
]

# Order matters here!
plots = [
    metrics_plot_all_datasets,
    top5frameworks_all_datasets,
    metrics_plot_per_datasets,
    top5frameworks_per_dataset,
    ag_rank_counts,
    framework_error,
    framework_box,
    pareto_front,
    hware_metrics_by_mode_plot,
    hware_metrics_by_dataset_plot,
]

plots = [plot.plot() for plot in plots]
plot_ctr = iter(range(len(plots)))
error_table_ctr = iter(range(len(error_tables)))
template = pn.template.FastListTemplate(
    title=APP_TITLE,
    main=[
        pn.Card(agg_framework_dfi, title=ALL_FRAMEWORKS_IDF[1:], collapsed=True),
        pn.Card(per_dataset_dfi, title=PER_DATASET_IDF[1:], collapsed=True),
        pn.Row(
            pn.Column(
                DOWNLOAD_FILES_TITLE,
                pn.Row(per_dataset_csv_widget, all_framework_csv_widget, hware_metrics_csv_widget),
            )
        ),
        pn.Row(
            ALL_DATA_COMP,
            pn.WidgetBox(yaxis_widget, graph_dropdown),
            plots[next(plot_ctr)].opts(active_tools=[]).panel(),
            plots[next(plot_ctr)],
        ),
        pn.Row(
            PER_DATA_COMP,
            pn.WidgetBox(yaxis_widget2, dataset_dropdown, graph_dropdown2),
            plots[next(plot_ctr)].opts(active_tools=[]).panel(),
            plots[next(plot_ctr)],
        ),
        pn.Row(NO_RANK_COMP, ag_pct_rank1, plots[next(plot_ctr)].opts(active_tools=[])),
        pn.Row(
            NO_ERROR_CNTS,
            plots[next(plot_ctr)].opts(active_tools=[]),
            pn.Column(
                pn.Row(
                    error_tables[next(error_table_ctr)],
                    error_tables[next(error_table_ctr)],
                    error_tables[next(error_table_ctr)],
                    error_tables[next(error_table_ctr)],
                ),
                pn.Row(
                    error_tables[next(error_table_ctr)],
                    error_tables[next(error_table_ctr)],
                    error_tables[next(error_table_ctr)],
                ),
                pn.Row(
                    error_tables[next(error_table_ctr)],
                    error_tables[next(error_table_ctr)],
                    error_tables[next(error_table_ctr)],
                ),
            ),
        ),
        pn.Row(FRAMEWORK_BOX_PLOT, yaxis_widget3, plots[next(plot_ctr)]),
        pn.Row(PARETO_FRONT_PLOT, plots[next(plot_ctr)].opts(active_tools=[])),
        pn.Row(
            HARDWARE_METRICS_PLOT,
            pn.Column(
                plots[next(plot_ctr)].opts(active_tools=[]), plots[next(plot_ctr)].opts(active_tools=[]).panel()
            ),
        ),
    ],
    header_background=APP_HEADER_BACKGROUND,
    logo="https://user-images.githubusercontent.com/16392542/77208906-224aa500-6aba-11ea-96bd-e81806074030.png",
)
template.servable()
