import panel as pn

from .widget import Widget


class FileDownloadWidget(Widget):
    """
    This class is used to define a Panel widget for downloading files from the dashboard website.
    
    Attributes
    ----------
    file: str
        this is a file object to download

    Methods
    -------
    create_widget():
        creates a panel `FileDownload` widget.

    Usage
    ------- 
    >>> file_download_widget = FileDownloadWidget(file=pandas_df.to_csv()).create_widget()
    
    This will return a Panel widget that can be directly added to the dashboard and rendered by Panel
    """

    def __init__(self, file):
        super().__init__(file=file)

    def create_widget(self) -> pn.widgets.FileDownload:
        """
        Creates a panel `FileDownload` widget.
        The `FileDownload` widget allows a user to download a file.
        It works either by sending the file data to the browser on initialization (`embed`=True),
        or, when the button is clicked.
        """
        return pn.widgets.FileDownload(
            icon="file-download",
            button_type="success",
            file=self.file,
            icon_size="3em",
            embed=True,
        )
