from typing import List, Union

import panel as pn

from .widget import Widget


class ToggleWidget(Widget):
    """
    This class is used to define a Panel widget for creating a list of options to toggle between.

    Attributes
    ----------
    name: str
        name of the widget on the website
    options: Union[str, List[str]]
        list of options that will be displayed

    Methods
    -------
    create_widget():
        creates a panel `ToggleGroup` widget.

    Usage
    -------
    >>> toggle_widget = ToggleWidget(name="Toggle widget", options=["A", "B", "C"]).create_widget()

    This will return a Panel widget that can be directly added to the dashboard and rendered by Panel
    """

    def __init__(
        self,
        name: str = "",
        options: Union[str, List[str]] = [],
    ):
        super().__init__(name=name, options=options)

    def create_widget(self) -> pn.widgets.ToggleGroup:
        """
        Creates a panel `ToggleGroup` widget.
        The `ToggleGroup` is a group of widgets which can be switched 'on' or 'off'.
        It can be displayed as buttons or boxes (default).
        """
        return pn.widgets.ToggleGroup(name=self.name, options=self.options, button_type="success")
