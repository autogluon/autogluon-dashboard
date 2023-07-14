from typing import List, Optional, Union

import panel as pn


class Widget:
    """
    This class is used to define any Panel widgets that are used on the dashboard website.
    These widgets can be independent or attached to a dashboard to control the plot.
    ...

    Attributes
    ----------
    widget_type: str
        the widget type is used to decide what type of panel widget will be created [refer to the if-else statements in __init__]
    name: str
        name of the widget on the website
    value: (int/str)
        for applicable widgets, this is the value that will be displayed [refer to number and slider widgets]
    options: (str/List[str])
        for applicable widgets, this is the list of options that will be displayed [refer to select and toggle widgets]
    format: str
        for applicable widgets, this is the format of the "value" being displayed [refer to the number indicator widget]
    start: int
        for applicable widgets, this is the start of a range being displayed [refer to the slider widget]
    end: int
        for applicable widgets, this is the end of a range being displayed [refer to the slider widget]
    file: str
        for applicable widgets, this is a file object to upload/download
    filename: str
        for applicable widgets, this is the name of the file to upload/download

    Methods
    -------
    _create_selectwidget():
        Creates a panel `Select` widget.
        The `Select` widget allows selecting a `value` from a list of `options`.

    _create_togglewidget():
        Creates a panel `ToggleGroup` widget.
        The `ToggleGroup` is a group of widgets which can be switched 'on' or 'off'. It can be displayed as buttons or boxes (default).

    _create_numberwidget():
        Creates a panel `Number` indicator.
        The `Number` indicator renders the `value` as text.

    _create_sliderwidget():
        Creates a panel `IntSlider` widget.
        The `IntSlider` widget allows selecting an integer value within a set of bounds using a slider.

    _create_downloadwidget():
        Creates a panel `FileDownload` widget.
        The `FileDownload` widget allows a user to download a file.
        It works either by sending the file data to the browser on initialization (`embed`=True), or when the button is clicked.
    ...

    Usage
    -------
    widget = Widget(widget_type=<widget_type>, name=<widget_name>).create_widget()
    Example: frameworks_widget = Widget("select", name=FRAMEWORK_LABEL, options=frameworks_list).create_widget()
    This will return a Panel widget that can be directly added to the dashboard and rendered by Panel
    """

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
            embed=True,
        )
