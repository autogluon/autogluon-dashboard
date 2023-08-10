import logging
from typing import List

import hvplot
import panel as pn

logger = logging.getLogger("dashboard-logger")
failure_text_widget = pn.widgets.StaticText(name="Unable to render", value="Error while trying to plot")


def create_panel_object(
    panel_objs: List[pn.Row],
    title: str,
    widgets: List = [pn.widgets],
    plots: List = [hvplot.hvPlot],
    extra_plots: list = [],
):
    """
    This method is used to create a panel object as a Row using the provided title, widgets, and plots.
    The panel object is added to a global, shared panel_objs list which is served through the website to display all the plots in `app.py`

    Parameters
    ----------
    panel_objs: List[pn.Row],
        list of panel objects to serve on the website
    title: str,
        title of each panel row
    widgets: List[pn.widgets.Widget]
        panel widgets in this row
    plots: List[hvplot.hvPlot]
        panel plots in this row
    extra_plots: list,
        any additional plots or panel/hvplot objects to add to this row
    """
    try:
        for i in range(len(plots)):
            try:
                plots[i] = plots[i].plot()
            # AttributeError will occur if .plot() is called on the plot object before it is passed into this function.
            # This would be done if the user needed to call .plot() with modified arguments.
            except AttributeError:
                continue
            except Exception as e:
                raise e
            try:
                # set active_tools=[] to prevent zooming-in of plots when scrolling through the website.
                # users can toggle the controls of the plot using the buttons on the website to zoom-in and customize the layout.
                plots[i] = plots[i].opts(active_tools=[]).panel()
            except Exception:
                continue
        panel_obj = pn.Row(title, *widgets, *plots, *extra_plots)
        panel_objs.append(panel_obj)
    except Exception as e:
        logger.exception(e)
        panel_obj = pn.Row(
            title,
            failure_text_widget,
        )
        panel_objs.append(panel_obj)


def get_error_tables_grid(error_tables: List, num_rows: int = 3, num_cols: int = 3) -> pn.Column:
    """
    This method is used to create a grid of tables that contain the datasets that did not successfully run for a given framework's benchmark run

    Parameters
    ----------
    error_tables: List,
        list of ErroredDatasets objects that are individual tables of errored datasets for a given framework
    num_rows: int,
        number of rows in the grid
    num_cols: int,
        number of columns in the grid
    """
    error_table_ctr = iter(range(len(error_tables)))
    num_cols = 3
    num_rows = int(len(error_tables) // num_cols) + (len(error_tables) % num_cols > 0)
    rows = []
    for _ in range(num_rows):
        row = []
        try:
            for _ in range(num_cols):
                error_framework_table = error_tables[next(error_table_ctr)]
                row.append(error_framework_table)
        except Exception:
            break
        rows.append(pn.Row(*row))
    grid = pn.Column(*rows)
    return grid
