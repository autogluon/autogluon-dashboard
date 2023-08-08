import panel as pn

from autogluon_dashboard.widgets.widget import Widget


class CheckboxWidget(Widget):
    """
    This class is used to define a Panel widget for a checkbox boolean widget.

    Attributes
    ----------
    name: str
        this is the name of the widget to display

    Methods
    -------
    create_widget():
        creates a panel `CheckBox` widget.

    Usage
    -------
    >>> log_scale = pn.widgets.Checkbox(name='log scale for y-axis')

    This will return a Panel widget that can be directly added to the dashboard and rendered by Panel
    """

    def __init__(self, name):
        super().__init__(name=name)

    def create_widget(self) -> pn.widgets.Checkbox:
        """
        Creates a panel `Checkbox` widget.
        The `Checkbox` widget is diplayed as a checkbox and returns a True or False.
        """
        return pn.widgets.Checkbox(name=self.name)
