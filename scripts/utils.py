def replace_df_column(df, col_name, new_col_data):
    df[col_name] = new_col_data

def get_sorted_names_from_col(df, col_name):
    return sorted(list(set(df[col_name].to_list())))

def get_df_filter_by_dataset(df, dataset):
    return df[(df.dataset.isin([dataset]))]

def get_df_filter_by_framework(df, framework):
    return df.loc[(df['framework'].isin([framework]))]

def sort_df_by_col(df, col_name):
    return df.sort_values(by=[col_name])

def get_col_metric_counts(df, metric):
    df_ag_only = sort_df_by_col(df, metric)
    return df_ag_only[metric].value_counts()[df_ag_only[metric].unique()]

def get_proportion_framework_rank1(framework_df, datsets_df, total_runs):
    return framework_df.loc[(datsets_df['rank'] == 1.0)].shape[0] / total_runs

def get_top5_performers(df, metric):
    return df.sort_values(metric).head()
    