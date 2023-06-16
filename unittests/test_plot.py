from plots.metrics_all_datasets import MetricsPlotAll
from plots.metrics_per_datasets import MetricsPlotPerDataset
from plots.top5_per_dataset import Top5PerDataset
from plots.top5_all_datasets import Top5AllDatasets
from plots.framework_error import FrameworkError
from plots.ag_rank_counts import AGRankCounts
import unittest
from unittest import mock
import pandas as pd

d = {'rank': [5, 2, 3, 1, 3, 4, 5, 1], 'dataset': ['D', 'C', 'A', 'B', 'A', 'D', 'C', 'A'], 
     'framework':['A', 'B', 'C', 'D', 'A', 'C', 'B', 'A']}
mock_df = pd.DataFrame(data=d)

class TestPlotInit(unittest.TestCase):
    def plot_init_test(self, plot):
        self.assertEqual(plot.plot_title, "title")
        self.assertEqual(plot.graph_type, "bar")
        self.assertIsNone(plot.plot_x)
        self.assertIsNone(plot.plot_y)
        self.assertEqual(plot.plot_x_label, '')
        self.assertEqual(plot.plot_y_label, '')
        self.assertEqual(plot.label_rot, 90)
        self.assertEqual(plot.table_cols, Ellipsis)


class TestMetricsPlotAllDatasets(unittest.TestCase):
    def test_init(self):
        plot = MetricsPlotAll("title", mock_df, "hvplot")
        plot_test = TestPlotInit()
        plot_test.plot_init_test(plot)
    
    def test_preprocess(self):
        plot = MetricsPlotAll("title", mock_df, "hvplot")
        plot._preprocess()
        assert plot.df.equals(mock_df)

class TestMetricsPlotPerDatasets(unittest.TestCase):
    def test_init(self):
        plot = MetricsPlotPerDataset("title", mock_df, "hvplot", dataset='dataset')
        plot_test = TestPlotInit()
        plot_test.plot_init_test(plot)
    
    def test_preprocess(self):
        plot = MetricsPlotPerDataset("title", mock_df, "hvplot", dataset='A')
        data = {'rank': [3, 3, 1], 'dataset': ['A', 'A', 'A'], 'framework': ['C', 'A', 'A']}
        expected_df = pd.DataFrame(data)
        plot_df = plot.df.reset_index().drop(columns=['index'])
        assert plot_df.equals(expected_df)

class TestTop5AllDatasets(unittest.TestCase):
    def test_init(self):
        plot = Top5AllDatasets("title", mock_df, "table", col_name='rank')
        plot_test = TestPlotInit()
        plot_test.plot_init_test(plot)

    def test_preprocess(self):
        plot = Top5AllDatasets("title", mock_df, "table", col_name='rank')
        data = {'rank': [1, 1, 2, 3, 3], 'dataset': ['B', 'A', 'C', 'A', 'A'], 'framework': ['D', 'A', 'B', 'C','A']}
        expected_df = pd.DataFrame(data) 
        plot_df = plot.df.reset_index().drop(columns=['index'])
        assert plot_df.equals(expected_df)


class TestTop5PerDataset(unittest.TestCase):
    def test_init(self):
        plot = Top5PerDataset("title", mock_df, "table", col_name='rank', dataset='A')
        plot_test = TestPlotInit()
        plot_test.plot_init_test(plot)
    
    def test_preprocess(self):
        plot = Top5PerDataset("title", mock_df, "table", col_name='rank', dataset='A')
        data = {'rank': [1, 3, 3], 'dataset': ['A', 'A', 'A'], 'framework': ['A', 'C','A']}
        expected_df = pd.DataFrame(data) 
        plot_df = plot.df.reset_index().drop(columns=['index'])
        assert plot_df.equals(expected_df)

class TestFrameworkError(unittest.TestCase):
    def test_init(self):
        plot = FrameworkError("title", mock_df, "hvplot")
        plot_test = TestPlotInit()
        plot_test.plot_init_test(plot)


if __name__ == '__main__':
    unittest.main()
