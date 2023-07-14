import unittest
from unittest import mock

import pandas as pd

from autogluon_dashboard.scripts.widget import Widget


class TestWidget(unittest.TestCase):
    def test_init(self):
        test_select_widget = Widget("select")
        self.assertEqual(test_select_widget.name, "")
        self.assertEqual(test_select_widget.value, "")
        self.assertEqual(test_select_widget.options, [])
        self.assertEqual(test_select_widget.format, "")

        test_select_widget2 = Widget("number", "test", 5, [0, 5, 10], "format")
        self.assertEqual(test_select_widget2.name, "test")
        self.assertEqual(test_select_widget2.value, 5)
        self.assertEqual(test_select_widget2.options, [0, 5, 10])
        self.assertEqual(test_select_widget2.format, "format")

    @mock.patch("panel.widgets.Select")
    def test_create_selectwidget(self, mock_create_widget):
        mock_create_widget.return_value = "select widget created"
        test_widget = Widget("select", "test_create", 2, [0, 1, 2, 3], "format")
        widget = test_widget.create_widget()
        mock_create_widget.assert_called_once_with(name=test_widget.name, options=test_widget.options)
        self.assertEqual(widget, mock_create_widget.return_value)

    @mock.patch("panel.indicators.Number")
    def test_create_numberwidget(self, mock_create_widget):
        mock_create_widget.return_value = "select number created"
        test_widget = Widget("number", "test_create", 2, [0, 1, 2, 3], "format")
        widget = test_widget.create_widget()
        mock_create_widget.assert_called_once_with(
            name=test_widget.name, value=test_widget.value, format=test_widget.format
        )
        self.assertEqual(widget, mock_create_widget.return_value)

    @mock.patch("panel.widgets.ToggleGroup")
    def test_create_togglewidget(self, mock_create_widget):
        mock_create_widget.return_value = "toggle widget created"
        test_widget = Widget(
            widget_type="toggle",
            name="test_create",
            value=2,
            options=[0, 1, 2, 3],
            format="format",
        )
        widget = test_widget.create_widget()
        mock_create_widget.assert_called_once_with(
            name=test_widget.name, options=test_widget.options, button_type="success"
        )
        self.assertEqual(widget, mock_create_widget.return_value)

    @mock.patch("panel.widgets.IntSlider")
    def test_create_sliderwidget(self, mock_create_widget):
        mock_create_widget.return_value = "slider widget created"
        test_widget = Widget(widget_type="slider", name="test_slider", start=1, end=10, value=10)
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
        test_widget = Widget("download", file=mock_df, filename="Some File Dataset")
        widget = test_widget.create_widget()
        mock_create_widget.assert_called_once_with(
            icon="file-download",
            button_type="success",
            file=test_widget.file,
            icon_size="3em",
            embed=False,
        )
        self.assertEqual(widget, mock_create_widget.return_value)


if __name__ == "__main__":
    unittest.main()
