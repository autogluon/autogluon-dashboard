import panel as pn

class Widget:
    def __init__(self, widget_type):
        if widget_type == "select":
            self.create_widget = create_selectwidget
        elif widget_type == "toggle":
            self.create_widget = create_togglewidget
        elif widget_type == "number":
            self.create_widget = create_numberwidget

def create_selectwidget(name='', value='', options=[], format=''):
    return pn.widgets.Select(
        name=name, 
        value=value, 
        options=options
    )

def create_togglewidget(name='', value='', options=[], format=''):
    return pn.widgets.ToggleGroup(
        name=name, 
        options=options, 
        button_type='success'
    )

def create_numberwidget(name='', value=0.0, options=[], format='{value}'):
    return pn.indicators.Number(name=name, value=value, format=format)
