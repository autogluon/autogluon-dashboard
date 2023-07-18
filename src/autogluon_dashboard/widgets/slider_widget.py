from typing import List, Union

import panel as pn

from autogluon_dashboard.widgets.all_widgets import Widget


class SliderWidget(Widget):
    """
    This class is used to define a Panel widget for creating a slider with a start and end value.

    Attributes
    ----------
    name: str
        name of the widget on the website
    value: Union[int, str, float]
        default value on the slider
    start: int
        start of a range being displayed
    end: int
        end of a range being displayed

    Methods
    -------
    create_widget():
        creates a panel `IntSlider` widget.

    Usage
    -------
    >>> slider_widget = SliderWidget(name="slider widget", value=5, start=0, end=10).create_widget()

    This will return a Panel widget that can be directly added to the dashboard and rendered by Panel
    """

    def __init__(
        self,
        name: str = "",
        value: Union[int, str] = "",
        start: int = 0,
        end: int = 15,
    ):
        super().__init__(name=name, value=value, start=start, end=end)

    def create_widget(self) -> pn.widgets.IntSlider:
        """
        Creates a panel `IntSlider` widget.
        The `IntSlider` widget allows selecting an integer value within a set of bounds using a slider.
        """
        return pn.widgets.IntSlider(name=self.name, start=self.start, end=self.end, value=self.value)
