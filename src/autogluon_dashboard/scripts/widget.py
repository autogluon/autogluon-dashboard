from io import StringIO
from typing import List, Optional, Union

import pandas as pd
import panel as pn


class Widget:
    def __init__(
        self,
        widget_type: str,
        name: str = "",
        value: Union[int, str] = "",
        options: Union[str, List[str]] = [],
        format: str = "",
        start: int = 0,
        end: int = 15,
        file: Optional[str] = None,
        filename: Optional[str] = None,
    ):
        if widget_type == "select":
            self.create_widget = self._create_selectwidget
        elif widget_type == "toggle":
            self.create_widget = self._create_togglewidget
        elif widget_type == "number":
            self.create_widget = self._create_numberwidget
        elif widget_type == "slider":
            self.create_widget = self._create_sliderwidget
            self.start = start
            self.end = end
        elif widget_type == "download":
            self.create_widget = self._create_downloadwidget
            self.file = file
            self.filename = filename

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

    def _create_sliderwidget(self) -> pn.widgets.IntSlider:
        return pn.widgets.IntSlider(name=self.name, start=self.start, end=self.end, value=self.value)

    def _create_downloadwidget(self) -> pn.widgets.FileDownload:
        return pn.widgets.FileDownload(
            icon="file-download",
            button_type="success",
            file=self.file,
            icon_size="3em",
            embed=False,
        )
