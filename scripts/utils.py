def replace_df_column(df, col_name, new_col_data):
    """
    Replace data in a given column.
    
    Parameters
    ----------
    df: Pandas dataframe,
    col_name: str,
        Name of Column to get names from.
    new_col_data: list,
        New column data to replace old column data.
    """
    df[col_name] = new_col_data

def get_sorted_names_from_col(df, col_name):
    """
    Get a sorted list of unique names in a given column.
    
    Parameters
    ----------
    df: Pandas dataframe,
    col_name: str,
        Name of Column to get names from.
    """
    return sorted(list(set(df[col_name])))

def get_df_filter_by_dataset(df, dataset):
    """
    Get rows from dataframe pertaining to a particular dataset.
    
    Parameters
    ----------
    df: Pandas dataframe,
    dataset: str,
        Name of dataset to filter by.
    """
    return df[(df.dataset.isin([dataset]))]

def get_df_filter_by_framework(df, framework):
    """
    Get rows from dataframe pertaining to a particular framework.
    
    Parameters
    ----------
    df: Pandas dataframe,
    framework: str,
        Name of dataset to filter by.
    """
    return df.loc[(df['framework'].isin([framework]))]

def sort_df_by_col(df, col_name):
    """
    Sort the entire dataframe based on a given column name.
    
    Parameters
    ----------
    df: Pandas dataframe,
    col_name: str,
        Name of Column to sort by.
    """
    return df.sort_values(by=[col_name])

def get_col_metric_counts(df, metric):
    """
    Get counts of different unique values in a given column.
    
    Parameters
    ----------
    df: Pandas dataframe,
    metric: str,
        Name of Column to get counts from.
    """
    df_ag_only = sort_df_by_col(df, metric)
    return df_ag_only[metric].value_counts()[df_ag_only[metric].unique()]

def get_proportion_framework_rank1(framework_df, datsets_df, total_runs):
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
    return framework_df.loc[(datsets_df['rank'] == 1.0)].shape[0] / total_runs

def get_top5_performers(df, metric):
    """
    Get top 5 performers for a given metric
    
    Parameters
    ----------
    df: Pandas dataframe,
    metric: str,
        Name of Column to get top 5 performers from.
    """
    return df.sort_values(metric).head()

def get_name_before_first_underscore(df, col_name):
    return df[col_name].str.extract(r"^(.*?)(?:_|$)")[0]
    