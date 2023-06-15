import panel as pn

class Widget:
    def __init__(self, widget_type, name='', value='', options=[], format=''):
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

    def _create_selectwidget(self):
        return pn.widgets.Select(
            name=self.name, 
            options=self.options
        )

    def _create_togglewidget(self):
        return pn.widgets.ToggleGroup(
            name=self.name, 
            options=self.options, 
            button_type='success'
        )

    def _create_numberwidget(self):
        return pn.indicators.Number(
            name=self.name, 
            value=self.value, 
            format=self.format
        )
