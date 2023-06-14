import hvplot.pandas

def create_hvplot(idf, title, x_axis=None, y_axis=None, 
                  graph_type='bar', xlabel='', ylabel='',
                  color_scheme=["#ff6f69", "#ffcc5c", "#88d8b0"],
                  line_width=6, height=500, rot=90):
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
    return idf.hvplot.table(title=title, columns=columns, width=width)
