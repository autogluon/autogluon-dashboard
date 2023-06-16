from scripts.widget import Widget
import unittest
from unittest import mock

class TestWidget(unittest.TestCase):
    def test_init(self):
        test_select_widget = Widget("select")
        self.assertEqual(test_select_widget.name, '')
        self.assertEqual(test_select_widget.value, '') 
        self.assertEqual(test_select_widget.options, []) 
        self.assertEqual(test_select_widget.format, '')

        test_select_widget2 = Widget("number", "test", 5, [0, 5, 10], 'format')
        self.assertEqual(test_select_widget2.name, 'test')
        self.assertEqual(test_select_widget2.value, 5) 
        self.assertEqual(test_select_widget2.options, [0, 5, 10]) 
        self.assertEqual(test_select_widget2.format, 'format')
        print("Init Test PASSED")
    
    @mock.patch('scripts.widget.Widget._create_selectwidget')
    def run_test_create_selectwidget(self, mock_create_widget):
        mock_create_widget.return_value = "select widget created"
        test_widget = Widget("select", "test_create", 2, [0, 1, 2, 3], 'format')
        widget = test_widget.create_widget()
        mock_create_widget.assert_called_once()
        self.assertEqual(widget, mock_create_widget.return_value)
        print("Create Select Test PASSED")
    
    @mock.patch('scripts.widget.Widget._create_numberwidget')
    def run_test_create_numberwidget(self, mock_create_widget):
        mock_create_widget.return_value = "select number created"
        test_widget = Widget("number", "test_create", 2, [0, 1, 2, 3], 'format')
        widget = test_widget.create_widget()
        mock_create_widget.assert_called_once()
        self.assertEqual(widget, mock_create_widget.return_value)
        print("Create Number Test PASSED")
    
    @mock.patch('scripts.widget.Widget._create_togglewidget')
    def run_test_create_togglewidget(self, mock_create_widget):
        mock_create_widget.return_value = "toggle widget created"
        test_widget = Widget(widget_type="toggle", name="test_create", value=2, options=[0, 1, 2, 3], format='format')
        widget = test_widget.create_widget()
        mock_create_widget.assert_called_once()
        self.assertEqual(widget, mock_create_widget.return_value)
        print("Create Toggle Test PASSED")
    
    def test_widgets(self):
        self.run_test_create_selectwidget()
        self.run_test_create_togglewidget()
        self.run_test_create_numberwidget()

if __name__ == '__main__':
    unittest.main()
