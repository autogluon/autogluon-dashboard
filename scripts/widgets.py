import panel as pn

class Widget:
    def __init__(self, widget_type):
        if widget_type == "select":
            self.create_widget = self._create_selectwidget
        elif widget_type == "toggle":
            self.create_widget = self._create_togglewidget
        elif widget_type == "number":
            self.create_widget = self._create_numberwidget

    def _create_selectwidget(name='', value='', options=[], format=''):
        return pn.widgets.Select(
            name=name, 
            value=value, 
            options=options
        )

    def _create_togglewidget(name='', value='', options=[], format=''):
        return pn.widgets.ToggleGroup(
            name=name, 
            options=options, 
            button_type='success'
        )

    def _create_numberwidget(name='', value=0.0, options=[], format='{value}'):
        return pn.indicators.Number(name=name, value=value, format=format)
