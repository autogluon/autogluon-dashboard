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

class TestMetricsPlotAllDatasets(unittest.TestCase):
    def test_init(self):
        plot = MetricsPlotAll("title", mock_df, "hvplot")
        self.assertEqual(plot.plot_title, "title")
        assert plot.df.equals(mock_df)
        self.assertEqual(plot.graph_type, "bar")
        self.assertIsNone(plot.plot_x)
        self.assertIsNone(plot.plot_y)
        self.assertEqual(plot.plot_x_label, '')
        self.assertEqual(plot.plot_y_label, '')
        self.assertEqual(plot.label_rot, 90)
        self.assertEqual(plot.table_cols, Ellipsis)
        
        #metrics_plot_all_datasets = MetricsPlotAll("title", mock_df, "hvplot", x_axis='xaxis', y_axis='yaxis')
    
    def test_preprocess(self):
        plot = MetricsPlotAll("title", mock_df, "hvplot")
        plot._preprocess()
        assert plot.df.equals(mock_df)


if __name__ == '__main__':
    unittest.main()
