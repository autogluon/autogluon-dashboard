import unittest
from unittest import mock
from unittest.mock import MagicMock

import pandas as pd

import autogluon_dashboard
from autogluon_dashboard.plotting.errored_datasets import ErroredDatasets
from autogluon_dashboard.plotting.framework_boxplot import FrameworkBoxPlot
from autogluon_dashboard.plotting.framework_error import FrameworkError
from autogluon_dashboard.plotting.interactive_df import InteractiveDataframe
from autogluon_dashboard.plotting.metrics_all_datasets import MetricsPlotAll
from autogluon_dashboard.plotting.metrics_per_datasets import MetricsPlotPerDataset
from autogluon_dashboard.plotting.pareto_front import ParetoFront
from autogluon_dashboard.plotting.rank_counts_ag import AGRankCounts
from autogluon_dashboard.plotting.top5_all_datasets import Top5AllDatasets
from autogluon_dashboard.plotting.top5_per_dataset import Top5PerDataset

d = {
    "rank": [5, 2, 3, 1, 3, 4, 5, 1],
    "dataset": ["D", "C", "A", "B", "A", "D", "C", "A"],
    "framework": ["A", "B", "C", "D", "A", "C", "B", "A"],
}
mock_df = pd.DataFrame(data=d)


class TestPlot(unittest.TestCase):
    def plot_init_test(self, plot):
        self.assertEqual(plot.plot_title, "title")
        self.assertEqual(plot.graph_type, "bar")
        self.assertIsNone(plot.plot_x)
        self.assertIsNone(plot.plot_y)
        self.assertEqual(plot.plot_x_label, "")
        self.assertEqual(plot.plot_y_label, "")
        self.assertEqual(plot.label_rot, 90)
        self.assertEqual(plot.table_cols, [])

    def plot_test(self, plot_obj, mock_plot):
        plot = plot_obj.plot()
        self.assertEqual(plot, mock_plot.return_value)
        mock_plot.assert_called_once_with(
            title="title",
            kind="bar",
            color=["#ff6f69", "#ffcc5c", "#88d8b0"],
            line_width=6,
            height=500,
            rot=90,
            xlabel="",
            ylabel="",
            grid=True,
        )


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
        plot = MetricsPlotPerDataset("title", mock_df, "hvplot", dataset="dataset")
        plot_test = TestPlot()
        plot_test.plot_init_test(plot)

    def test_preprocess(self):
        plot = MetricsPlotPerDataset("title", mock_df, "hvplot", dataset="A")
        data = {
            "rank": [3, 3, 1],
            "dataset": ["A", "A", "A"],
            "framework": ["C", "A", "A"],
        }
        expected_df = pd.DataFrame(data)
        plot_df = plot.df.reset_index().drop(columns=["index"])
        assert plot_df.equals(expected_df)

    @mock.patch("pandas.DataFrame.hvplot")
    def test_plot(self, mock_plot):
        mock_plot.return_value = "plot"
        plot_obj = MetricsPlotPerDataset("title", mock_df, "hvplot", dataset="A")
        plot_test = TestPlot()
        plot_test.plot_test(plot_obj, mock_plot)


class TestTop5AllDatasets(unittest.TestCase):
    def test_init(self):
        plot = Top5AllDatasets("title", mock_df, "table", col_name="rank")
        plot_test = TestPlot()
        plot_test.plot_init_test(plot)

    def test_preprocess(self):
        plot = Top5AllDatasets("title", mock_df, "table", col_name="rank", table_cols=["framework", "rank"])
        data = {
            "rank": [1, 1, 2, 3, 3],
            "dataset": ["B", "A", "C", "A", "A"],
            "framework": ["D", "A", "B", "C", "A"],
        }
        expected_df = pd.DataFrame(data)
        plot_df = plot.df.reset_index().drop(columns=["index"])
        assert plot_df.equals(expected_df)

    @mock.patch("hvplot.plotting.core.hvPlotTabular.table")
    def test_plot(self, mock_plot):
        mock_plot.return_value = "plot"
        plot_obj = Top5AllDatasets("title", mock_df, "table", col_name="rank")
        plot = plot_obj.plot()
        self.assertEqual(plot, mock_plot.return_value)


class TestTop5PerDataset(unittest.TestCase):
    def test_init(self):
        plot = Top5PerDataset("title", mock_df, "table", col_name="rank", dataset="A")
        plot_test = TestPlot()
        plot_test.plot_init_test(plot)

    def test_preprocess(self):
        plot = Top5PerDataset("title", mock_df, "table", col_name="rank", dataset="A")
        data = {
            "rank": [1, 3, 3],
            "dataset": ["A", "A", "A"],
            "framework": ["A", "C", "A"],
        }
        expected_df = pd.DataFrame(data)
        plot_df = plot.df.reset_index().drop(columns=["index"])
        assert plot_df.equals(expected_df)

    @mock.patch("hvplot.plotting.core.hvPlotTabular.table")
    def test_plot(self, mock_plot):
        mock_plot.return_value = "plot"
        plot_obj = Top5PerDataset("title", mock_df, "table", col_name="rank", dataset="A", table_cols=["framework"])
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
        plot = AGRankCounts("title", mock_df, "hvplot", col_name="rank", framework="A")
        data = {"rank": [1, 1, 1]}
        expected_df = pd.DataFrame(data)
        plot_df = plot.df.reset_index().drop(columns=["index"])
        assert plot_df.equals(expected_df)

    @mock.patch("hvplot.plotting.core.hvPlotTabular.table")
    def test_plot(self, mock_plot):
        mock_plot.return_value = "plot"
        plot_obj = AGRankCounts("title", mock_df, "table", col_name="rank", framework="A")
        plot = plot_obj.plot()
        self.assertEqual(plot, mock_plot.return_value)


class TestInteractiveDataframe(unittest.TestCase):
    def test_init(self):
        plot = InteractiveDataframe(mock_df, "D", width=3000)
        assert plot.dataset_to_plot.equals(mock_df)
        self.assertEqual(plot.framework, "D")
        self.assertEqual(plot.table_width, 3000)

        plot = InteractiveDataframe(mock_df, "D", width=3000, dataset="C")
        assert plot.dataset_to_plot.equals(mock_df)
        self.assertEqual(plot.framework, "D")
        self.assertEqual(plot.dataset, "C")
        self.assertEqual(plot.table_width, 3000)

    def test_preprocess(self):
        plot = InteractiveDataframe(mock_df, "D", width=3000)
        data = {"rank": [1], "dataset": ["B"], "framework": ["D"]}
        expected_df = pd.DataFrame(data)
        plot_df = plot._preprocess(framework="D", dataset=None).reset_index().drop(columns=["index"])
        assert plot_df.equals(expected_df)

        plot = InteractiveDataframe(mock_df, framework="A", width=3000, dataset="D")
        data = {"rank": [5], "dataset": ["D"], "framework": ["A"]}
        expected_df = pd.DataFrame(data)
        plot_df = plot._preprocess(framework="A", dataset="D").reset_index().drop(columns=["index"])
        assert plot_df.equals(expected_df)

    @mock.patch("pandas.DataFrame.interactive")
    def test_plot(self, mock_plot):
        mock_plot.return_value = "plot"
        plot = InteractiveDataframe(mock_df, "D", width=3000)
        idf = plot.get_interactive_df()
        self.assertEqual(idf, mock_plot.return_value)

        mock_plot.return_value = "plot"
        plot = InteractiveDataframe(mock_df, framework="A", width=3000, dataset="D")
        idf = plot.get_interactive_df()
        self.assertEqual(idf, mock_plot.return_value)


class TestFrameworkBoxPlot(unittest.TestCase):
    def test_init(self):
        plot = FrameworkBoxPlot("title", mock_df, y_axis="dataset")
        self.assertEqual(plot.plot_title, "title")
        self.assertEqual(plot.graph_type, "box")
        self.assertIsNone(plot.plot_x)
        self.assertIsNotNone(plot.plot_y)
        self.assertEqual(plot.plot_x_label, "")
        self.assertEqual(plot.plot_y_label, "")
        self.assertEqual(plot.label_rot, 90)
        self.assertEqual(plot.table_cols, [])

    def test_preprocess(self):
        plot = FrameworkBoxPlot("title", mock_df, y_axis="dataset")
        plot._preprocess()
        assert plot.df.equals(mock_df)

    @mock.patch("hvplot.plotting.core.hvPlotTabular.box")
    def test_plot(self, mock_plot):
        mock_plot.return_value = "box plot"
        plot_obj = FrameworkBoxPlot("title", mock_df, y_axis="dataset")
        plot = plot_obj.plot()
        self.assertEqual(plot, mock_plot.return_value)


class TestParetoFront(unittest.TestCase):
    def test_init(self):
        plot = ParetoFront("title", mock_df, "pareto")
        plot_test = TestPlot()
        plot_test.plot_init_test(plot)

    def test_preprocess(self):
        plot = ParetoFront("title", mock_df, "pareto", x_axis="dataset", y_axis="rank")
        plot._preprocess()
        assert plot.df.equals(mock_df)

    @mock.patch("pandas.DataFrame.hvplot")
    @mock.patch("hvplot.plotting.core.hvPlotTabular.step")
    def test_plot(self, mock_stepplot, mock_hvplot):
        mock_hvplot.return_value = "plot"
        mock_stepplot.return_value = "step plot"
        plot_obj = ParetoFront("title", mock_df, "pareto", x_axis="dataset", y_axis="rank")
        plot = plot_obj.plot()
        mock_hvplot.assert_called_once_with(
            c="framework",
            kind="scatter",
            size=400,
            x="dataset",
            y="rank",
            height=800,
            width=900,
            grid=True,
        )


class TestErroredDatasets(unittest.TestCase):
    def test_init(self):
        plot = ErroredDatasets("title", mock_df, "table", framework="A")
        self.assertEqual(plot.plot_title, "title")
        self.assertEqual(plot.graph_type, "bar")
        self.assertIsNone(plot.plot_x)
        self.assertIsNone(plot.plot_y)
        self.assertEqual(plot.plot_x_label, "")
        self.assertEqual(plot.plot_y_label, "")
        self.assertEqual(plot.label_rot, 90)
        self.assertEqual(plot.table_cols, ["Errored Datasets"])

    def test_preprocess(self):
        plot = ErroredDatasets("title", mock_df, "table", framework="A")
        data = {
            "Errored Datasets": ["B", "C"],
        }
        expected_df = pd.DataFrame(data)
        plot_df = plot.df.sort_values(by="Errored Datasets").reset_index().drop(columns=["index"])
        assert plot_df.equals(expected_df)

    @mock.patch("hvplot.plotting.core.hvPlotTabular.table")
    def test_plot(self, mock_plot):
        mock_plot.return_value = "plot"
        plot_obj = ErroredDatasets("title", mock_df, "table", framework="A")
        plot = plot_obj.plot()
        self.assertEqual(plot, mock_plot.return_value)


if __name__ == "__main__":
    unittest.main()
