from autogluon_dashboard.constants.df_constants import BESTDIFF, LOSS_RESCALED, TIME_INFER_S, TIME_TRAIN_S

METRICS_TO_PLOT = [
    LOSS_RESCALED,
    TIME_TRAIN_S,
    TIME_INFER_S,
    BESTDIFF,
]
GRAPH_TYPES = ["bar", "line", "hist", "scatter"]
