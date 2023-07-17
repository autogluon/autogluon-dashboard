import unittest
from unittest import mock

import pandas as pd

from autogluon_dashboard.scripts.widgets.filedownload_widget import FileDownloadWidget
from autogluon_dashboard.scripts.widgets.number_widget import NumberWidget
from autogluon_dashboard.scripts.widgets.select_widget import SelectWidget
from autogluon_dashboard.scripts.widgets.slider_widget import SliderWidget
from autogluon_dashboard.scripts.widgets.toggle_widget import ToggleWidget


class TestWidget(unittest.TestCase):
    def test_init(self):
        test_select_widget = SelectWidget()
        self.assertEqual(test_select_widget.name, "")
        self.assertEqual(test_select_widget.options, [])

        test_number_widget = NumberWidget("test", 5, "format")
        self.assertEqual(test_number_widget.name, "test")
        self.assertEqual(test_number_widget.value, 5)
        self.assertEqual(test_number_widget.format, "format")

        test_toggle_widget = ToggleWidget(name="test", options=[0, 1, 2, 3])
        self.assertEqual(test_toggle_widget.name, "test")
        self.assertEqual(test_toggle_widget.options, [0, 1, 2, 3])

        test_toggle_widget = SliderWidget(name="test", start=1, end=10, value=5)
        self.assertEqual(test_toggle_widget.name, "test")
        self.assertEqual(test_toggle_widget.start, 1)
        self.assertEqual(test_toggle_widget.end, 10)
        self.assertEqual(test_toggle_widget.value, 5)

        test_toggle_widget = FileDownloadWidget(file="file")
        self.assertEqual(test_toggle_widget.file, "file")

    @mock.patch("panel.widgets.Select")
    def test_create_selectwidget(self, mock_create_widget):
        mock_create_widget.return_value = "select widget created"
        test_widget = SelectWidget("test_create", [0, 1, 2, 3])
        widget = test_widget.create_widget()
        mock_create_widget.assert_called_once_with(name=test_widget.name, options=test_widget.options)
        self.assertEqual(widget, mock_create_widget.return_value)

    @mock.patch("panel.indicators.Number")
    def test_create_numberwidget(self, mock_create_widget):
        mock_create_widget.return_value = "select number created"
        test_widget = NumberWidget("test_create", 2, "format")
        widget = test_widget.create_widget()
        mock_create_widget.assert_called_once_with(
            name=test_widget.name, value=test_widget.value, format=test_widget.format
        )
        self.assertEqual(widget, mock_create_widget.return_value)

    @mock.patch("panel.widgets.ToggleGroup")
    def test_create_togglewidget(self, mock_create_widget):
        mock_create_widget.return_value = "toggle widget created"
        test_widget = ToggleWidget(
            name="test_create",
            options=[0, 1, 2, 3],
        )
        widget = test_widget.create_widget()
        mock_create_widget.assert_called_once_with(
            name=test_widget.name, options=test_widget.options, button_type="success"
        )
        self.assertEqual(widget, mock_create_widget.return_value)

    @mock.patch("panel.widgets.IntSlider")
    def test_create_sliderwidget(self, mock_create_widget):
        mock_create_widget.return_value = "slider widget created"
        test_widget = SliderWidget(name="test_slider", start=1, end=10, value=10)
        widget = test_widget.create_widget()
        mock_create_widget.assert_called_once_with(
            name=test_widget.name, start=test_widget.start, end=test_widget.end, value=test_widget.value
        )
        self.assertEqual(widget, mock_create_widget.return_value)

    @mock.patch("panel.widgets.FileDownload")
    def test_create_downloadwidget(self, mock_create_widget):
        mock_create_widget.return_value = "download widget created"
        d = {
            "dataset": [
                "D",
                "C",
                "A",
                "B",
            ],
            "framework": ["A", "B", "C", "D"],
        }
        mock_df = pd.DataFrame(data=d)
        test_widget = FileDownloadWidget(file=mock_df)
        widget = test_widget.create_widget()
        mock_create_widget.assert_called_once_with(
            icon="file-download",
            button_type="success",
            file=test_widget.file,
            icon_size="3em",
            embed=True,
        )
        self.assertEqual(widget, mock_create_widget.return_value)


if __name__ == "__main__":
    unittest.main()
