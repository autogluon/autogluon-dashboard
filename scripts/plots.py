import hvplot.pandas

def create_hvplot(idf, title, x_axis=None, y_axis=None, 
                  graph_type='bar', xlabel='', ylabel='',
                  color_scheme=["#ff6f69", "#ffcc5c", "#88d8b0"],
                  line_width=6, height=500, rot=90):
    """
    Create a plot of a given type leveraging the hvplot library, 
    and using data from a pandas interactive dataframe.
    
    Parameters
    ----------
    idf: Pandas dataframe,
        Data to plot on.
    x_axis: str or list, default=None,
       Column name (as string) in dataframe or, list of values to plot on.
    y_axis: str or list, default=None,
        Column name (as string) in dataframe or, list of values to plot on.
    graph_type: str, default='bar',
        Type of plot. Examples: line, hist, bar, scatter
    xlabel: str,
        x-axis Label.
    ylabel: str,
        y-axis Label.
    color_scheme: list, default=["#ff6f69", "#ffcc5c", "#88d8b0"],
        Color scheme of plot.
    line_width: int, default=6,
        Width of line in plot.
    height: int, default=500,
        Height of plot frame.
    rot: int, default=0,
        Rotation amount for x-axis labels
    """
    if x_axis is None or y_axis is None:
        return idf.hvplot(title=title, 
                      kind=graph_type, color=color_scheme, 
                      line_width=line_width, height=height, 
                      rot=rot, xlabel=xlabel, ylabel=ylabel)
    return idf.hvplot(title=title, x=x_axis, y=y_axis, 
                      kind=graph_type, color=color_scheme, 
                      line_width=line_width, height=height, 
                      rot=rot, xlabel=xlabel)

def create_table(idf, title, columns, width=800):
    """
    Create a table leveraging the hvplot library, 
    and using data from a pandas interactive dataframe.
    
    Parameters
    ----------
    idf: Pandas dataframe,
        Data to create the table from.
    title: str,
        Title of the table.
    columns: list,
        List of strings of column names to create the table. 
        The strings should match column names in the provided idf.
    width: int, default=800,
        Width of the table.
    """
    return idf.hvplot.table(title=title, columns=columns, width=width)
