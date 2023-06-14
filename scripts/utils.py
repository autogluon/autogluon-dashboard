def replace_df_column(df, col_name, new_col_data):
    df[col_name] = new_col_data

def get_sorted_names_from_col(df, col_name):
    return sorted(list(set(df[col_name].to_list())))