from plotting.metrics_all_datasets import MetricsPlotAll
from plotting.metrics_per_datasets import MetricsPlotPerDataset
from plotting.top5_per_dataset import Top5PerDataset
from plotting.top5_all_datasets import Top5AllDatasets
from plotting.framework_error import FrameworkError
from plotting.rank_counts_ag import AGRankCounts
import unittest
from unittest import mock
from unittest.mock import MagicMock
import pandas as pd

d = {'rank': [5, 2, 3, 1, 3, 4, 5, 1], 'dataset': ['D', 'C', 'A', 'B', 'A', 'D', 'C', 'A'], 
     'framework':['A', 'B', 'C', 'D', 'A', 'C', 'B', 'A']}
mock_df = pd.DataFrame(data=d)

class TestPlot(unittest.TestCase):
    def plot_init_test(self, plot):
        self.assertEqual(plot.plot_title, "title")
        self.assertEqual(plot.graph_type, "bar")
        self.assertIsNone(plot.plot_x)
        self.assertIsNone(plot.plot_y)
        self.assertEqual(plot.plot_x_label, '')
        self.assertEqual(plot.plot_y_label, '')
        self.assertEqual(plot.label_rot, 90)
        self.assertEqual(plot.table_cols, Ellipsis)

    def plot_test(self, plot_obj, mock_plot):
        plot = plot_obj.plot()
        self.assertEqual(plot, mock_plot.return_value)
        mock_plot.assert_called_once_with(title='title', kind='bar', color=['#ff6f69', '#ffcc5c', '#88d8b0'], line_width=6, height=500, rot=90, xlabel='', ylabel='')

class TestMetricsPlotAllDatasets(unittest.TestCase):
    def test_init(self):
        plot = MetricsPlotAll("title", mock_df, "hvplot")
        plot_test = TestPlot()
        plot_test.plot_init_test(plot)
    
    def test_preprocess(self):
        plot = MetricsPlotAll("title", mock_df, "hvplot")
        plot._preprocess()
        assert plot.df.equals(mock_df)
    
    @mock.patch("pandas.DataFrame.hvplot")
    def test_plot(self, mock_plot):
        mock_plot.return_value = "plot"
        plot_obj = MetricsPlotAll("title", mock_df, "hvplot")
        plot_test = TestPlot()
        plot_test.plot_test(plot_obj, mock_plot)

class TestMetricsPlotPerDatasets(unittest.TestCase):
    def test_init(self):
        plot = MetricsPlotPerDataset("title", mock_df, "hvplot", dataset='dataset')
        plot_test = TestPlot()
        plot_test.plot_init_test(plot)
    
    def test_preprocess(self):
        plot = MetricsPlotPerDataset("title", mock_df, "hvplot", dataset='A')
        data = {'rank': [3, 3, 1], 'dataset': ['A', 'A', 'A'], 'framework': ['C', 'A', 'A']}
        expected_df = pd.DataFrame(data)
        plot_df = plot.df.reset_index().drop(columns=['index'])
        assert plot_df.equals(expected_df)
    
    @mock.patch("pandas.DataFrame.hvplot")
    def test_plot(self, mock_plot):
        mock_plot.return_value = "plot"
        plot_obj = MetricsPlotPerDataset("title", mock_df, "hvplot", dataset='A')
        plot_test = TestPlot()
        plot_test.plot_test(plot_obj, mock_plot)

class TestTop5AllDatasets(unittest.TestCase):
    def test_init(self):
        plot = Top5AllDatasets("title", mock_df, "table", col_name='rank')
        plot_test = TestPlot()
        plot_test.plot_init_test(plot)

    def test_preprocess(self):
        plot = Top5AllDatasets("title", mock_df, "table", col_name='rank', table_cols=['framework', 'rank'])
        data = {'rank': [1, 1, 2, 3, 3], 'dataset': ['B', 'A', 'C', 'A', 'A'], 'framework': ['D', 'A', 'B', 'C','A']}
        expected_df = pd.DataFrame(data) 
        plot_df = plot.df.reset_index().drop(columns=['index'])
        assert plot_df.equals(expected_df)
    
    @mock.patch("plotting.all_plots.Plot._create_table")
    def test_plot(self, mock_plot):
        mock_plot.return_value = MagicMock()
        plot_obj = Top5AllDatasets("title", mock_df, "table", col_name='rank')
        plot = plot_obj.plot()
        self.assertEqual(plot, mock_plot.return_value)


class TestTop5PerDataset(unittest.TestCase):
    def test_init(self):
        plot = Top5PerDataset("title", mock_df, "table", col_name='rank', dataset='A')
        plot_test = TestPlot()
        plot_test.plot_init_test(plot)
    
    def test_preprocess(self):
        plot = Top5PerDataset("title", mock_df, "table", col_name='rank', dataset='A')
        data = {'rank': [1, 3, 3], 'dataset': ['A', 'A', 'A'], 'framework': ['A', 'C','A']}
        expected_df = pd.DataFrame(data) 
        plot_df = plot.df.reset_index().drop(columns=['index'])
        assert plot_df.equals(expected_df)
    
    @mock.patch("plotting.all_plots.Plot._create_table")
    def test_plot(self, mock_plot):
        mock_plot.return_value = "plot"
        plot_obj = Top5PerDataset("title", mock_df, "table", col_name='rank', dataset='A')
        plot = plot_obj.plot()
        self.assertEqual(plot, mock_plot.return_value)

class TestFrameworkError(unittest.TestCase):
    def test_init(self):
        plot = FrameworkError("title", mock_df, "hvplot")
        plot_test = TestPlot()
        plot_test.plot_init_test(plot)

    def test_preprocess(self):
        plot = FrameworkError("title", mock_df, "hvplot")
        plot._preprocess()
        assert plot.df.equals(mock_df)
    
    @mock.patch("pandas.DataFrame.hvplot")
    def test_plot(self, mock_plot):
        mock_plot.return_value = "plot"
        plot_obj = FrameworkError("title", mock_df, "hvplot")
        plot_test = TestPlot()
        plot_test.plot_test(plot_obj, mock_plot)

class TestAGRankCounts(unittest.TestCase):
    def test_init(self):
        plot = AGRankCounts("title", mock_df, "hvplot", col_name="rank", framework="A")
        plot_test = TestPlot()
        plot_test.plot_init_test(plot)
    
    def test_preprocess(self):
        plot = AGRankCounts("title", mock_df, "hvplot", col_name='rank', framework='A')
        data = {'rank': [1, 1, 1]}
        expected_df = pd.DataFrame(data) 
        plot_df = plot.df.reset_index().drop(columns=['index'])
        assert plot_df.equals(expected_df)
    
    @mock.patch("plotting.all_plots.Plot._create_hvplot")
    def test_plot(self, mock_plot):
        mock_plot.return_value = "plot"
        plot_obj = AGRankCounts("title", mock_df, "hvplot", col_name='rank', framework='')
        plot = plot_obj.plot()
        self.assertEqual(plot, mock_plot.return_value)

if __name__ == '__main__':
    unittest.main()
