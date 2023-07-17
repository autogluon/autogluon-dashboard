from typing import List, Union

import panel as pn

from .widget import Widget


class SelectWidget(Widget):
    """
    This class is used to define a Panel widget for selecting a value from different options.

    Attributes
    ----------
    name: str
        name of the widget on the website
    options: Union[str, List[str]]
        list of options that will be displayed

    Methods
    -------
    create_widget():
        creates a panel `Select` widget.

    Usage
    -------
    >>> frameworks_widget = SelectWidget(name="select widget", options=frameworks_list).create_widget()

    This will return a Panel widget that can be directly added to the dashboard and rendered by Panel
    """

    def __init__(
        self,
        name: str = "",
        options: Union[str, List[str]] = [],
    ):
        super().__init__(name=name, options=options)

    def create_widget(self) -> pn.widgets.Select:
        """
        Creates a panel `Select` widget.
        The `Select` widget allows selecting a `value` from a list of `options`.
        """
        return pn.widgets.Select(name=self.name, options=self.options)
