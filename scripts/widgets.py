import panel as pn

def create_selectwidget(name='', value='', options=[]):
    return pn.widgets.Select(
        name=name, 
        value=value, 
        options=options
    )

def create_togglewidget(name='', options=[]):
    return pn.widgets.ToggleGroup(
        name=name, 
        options=options, 
        button_type='success'
    )

def create_numberwidget(name='', value=0.0, format='{value}'):
    return pn.indicators.Number(name=name, value=value, format=format)
