from typing import List, Union

import panel as pn

from .widget import Widget


class NumberWidget(Widget):
    """
    This class is used to define a Panel widget for displaying a number on the dashboard website.
    For example, displaying a percentage.

    Attributes
    ----------
    name: str
        name of the widget on the website
    value: Union[int, str, float]
        value that will be displayed
    format: str
        format of the "value" being displayed

    Methods
    -------
    create_widget():
        creates a panel `Number` widget.

    Usage
    -------
    >>> number_widget = NumberWidget(name="number widget", value=10, format="{value}%").create_widget()

    This will return a Panel widget that can be directly added to the dashboard and rendered by Panel
    """

    def __init__(
        self,
        name: str = "",
        value: Union[int, str, float] = 0,
        format: str = "",
    ):
        super().__init__(name=name, value=value, format=format)

    def create_widget(self) -> pn.indicators.Number:
        """
        Creates a panel `Number` indicator.
        The `Number` indicator renders the `value` as text.
        """
        return pn.indicators.Number(name=self.name, value=self.value, format=self.format)
