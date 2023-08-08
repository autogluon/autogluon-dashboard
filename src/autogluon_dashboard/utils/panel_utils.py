import logging

import panel as pn

logger = logging.getLogger("dashboard-logger")
failure_text_widget = pn.widgets.StaticText(name="Unable to render", value="Error while trying to plot")


def create_panel_object(panel_objs, title, widgets=[], plots=[], extra_plots=[]):
    try:
        for i in range(len(plots)):
            try:
                plots[i] = plots[i].plot()
            except AttributeError:
                continue
            except Exception as e:
                raise e
            try:
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


def get_error_tables_grid(error_tables, num_rows=3, num_cols=3) -> pn.Column:
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
