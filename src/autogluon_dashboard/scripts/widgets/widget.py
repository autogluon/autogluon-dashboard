from abc import abstractmethod


class Widget:
    """
    This parent class is used to define any Panel widgets that are used on the dashboard website.
    These widgets can be independent or attached to a dashboard to control the plot.
    """

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @abstractmethod
    def create_widget(self):
        raise NotImplementedError
