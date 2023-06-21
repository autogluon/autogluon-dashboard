from typing import Union

import panel as pn


class Widget:
    def __init__(
        self,
        widget_type: str,
        name: str = "",
        value: Union[int, str] = "",
        options: Union[str, list] = [],
        format: str = "",
    ):
        if widget_type == "select":
            self.create_widget = self._create_selectwidget
        elif widget_type == "toggle":
            self.create_widget = self._create_togglewidget
        elif widget_type == "number":
            self.create_widget = self._create_numberwidget
        self.name = name
        self.value = value
        self.options = options
        self.format = format

    def _create_selectwidget(self) -> pn.widgets.Select:
        return pn.widgets.Select(name=self.name, options=self.options)

    def _create_togglewidget(self) -> pn.widgets.ToggleGroup:
        return pn.widgets.ToggleGroup(name=self.name, options=self.options, button_type="success")

    def _create_numberwidget(self) -> pn.indicators.Number:
        return pn.indicators.Number(name=self.name, value=self.value, format=self.format)
