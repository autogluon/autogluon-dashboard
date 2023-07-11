import pandas


def get_sorted_names_from_col(df: pandas.DataFrame, col_name: str) -> list:
    """
    Get a sorted list of unique names in a given column.

    Parameters
    ----------
    df: Pandas dataframe,
    col_name: str,
        Name of Column to get names from.
    """
    return sorted(list(set(df[col_name])))


def get_df_filter_by_dataset(df: pandas.DataFrame, dataset: str) -> pandas.DataFrame:
    """
    Get rows from dataframe pertaining to a particular dataset.

    Parameters
    ----------
    df: Pandas dataframe,
    dataset: str,
        Name of dataset to filter by.
    """
    return df[(df.dataset.isin([dataset]))]


def get_df_filter_by_framework(df: pandas.DataFrame, framework: str) -> pandas.DataFrame:
    """
    Get rows from dataframe pertaining to a particular framework.

    Parameters
    ----------
    df: Pandas dataframe,
    framework: str,
        Name of dataset to filter by.
    """
    return df[(df.framework.isin([framework]))]


def get_col_metric_counts(df: pandas.DataFrame, metric: str) -> pandas.Series:
    """
    Get counts of different unique values in a given column.

    Parameters
    ----------
    df: Pandas dataframe,
    metric: str,
        Name of Column to get counts from.
    """
    df_sorted = df.sort_values(by=[metric])
    return df_sorted[metric].value_counts()[df_sorted[metric].unique()]


def get_proportion_framework_rank1(
    framework_df: pandas.DataFrame, datsets_df: pandas.DataFrame, total_runs: int
) -> float:
    """
    Get proportion of #1 ranks for a given framework across all runs.

    Parameters
    ----------
    framework_df: Pandas dataframe,
        Dataframe for specific framework.
    datsets_df: Pandas dataframe,
        Dataframe for all datasets and frameworks.
    total_runs: int,
        Total #runs for a given framework = Total number of datasets.
    """
    return framework_df.loc[(datsets_df["rank"] == 1.0)].shape[0] / total_runs


def get_top5_performers(df: pandas.DataFrame, metric: str) -> pandas.DataFrame:
    """
    Get top 5 performers for a given metric

    Parameters
    ----------
    df: Pandas dataframe,
    metric: str,
        Name of Column to get top 5 performers from.
    """
    return df.sort_values(metric).head()


def get_name_before_first_underscore(df: pandas.DataFrame, col_name: str) -> pandas.DataFrame:
    """
    Get the part of the string before the first underscore.
    Example: AutoGluonv0.1_gc8h8_2022 becomes AutoGluonv0.1

    Parameters
    ----------
    df: Pandas dataframe,
    col_name: str,
        Name of Column to perform regex on.
    """
    return df[col_name].str.extract(r"^(.*?)(?:_|$)")[0]


def clean_up_framework_names(df: pandas.DataFrame, dummy: bool = False) -> list:
    new_framework_names = get_name_before_first_underscore(df, "framework")
    if dummy:
        num_frameworks = len(set(new_framework_names))
        # dummy framework replacement
        for i in range(len(new_framework_names)):
            new_framework_names[i] = (
                "AutoGluon"
                if i % num_frameworks == 0 or new_framework_names[i] == "AutoGluon"
                else "AutoGluon v" + f"0.{i%num_frameworks}"
            )
    return new_framework_names
