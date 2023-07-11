import unittest

import pandas as pd

from autogluon_dashboard.scripts.utils import *

d = {
    "rank": [5, 2, 3, 1, 3, 4, 5, 1],
    "dataset": ["D", "C", "A", "B", "A", "D", "C", "A"],
    "framework": ["A", "B", "C", "D", "A", "C", "B", "A"],
}
mock_df = pd.DataFrame(data=d)


class TestUtils(unittest.TestCase):
    def test_get_sorted_names_from_col(self):
        sorted_names = get_sorted_names_from_col(mock_df, "dataset")
        self.assertEqual(sorted_names, ["A", "B", "C", "D"])

    def test_get_df_filter_by_dataset(self):
        data = {
            "rank": [3, 3, 1],
            "dataset": ["A", "A", "A"],
            "framework": ["C", "A", "A"],
        }
        expected_df = pd.DataFrame(data)
        filtered_df = get_df_filter_by_dataset(mock_df, "A").reset_index().drop(columns=["index"])
        assert filtered_df.equals(expected_df)

    def test_get_df_filter_by_framework(self):
        data = {
            "rank": [5, 3, 1],
            "dataset": ["D", "A", "A"],
            "framework": ["A", "A", "A"],
        }
        expected_df = pd.DataFrame(data)
        filtered_df = get_df_filter_by_framework(mock_df, "A").reset_index().drop(columns=["index"])
        assert filtered_df.equals(expected_df)

    def test_get_col_metric_counts(self):
        data = {"rank": [2, 1, 2, 1, 2]}
        expected = pd.DataFrame(data)
        counts = get_col_metric_counts(mock_df, "rank").reset_index().drop(columns=["index"])
        assert expected.equals(counts)

    def test_get_proportion_framework_rank1(self):
        framework_df = get_df_filter_by_framework(mock_df, "A")
        prop = get_proportion_framework_rank1(framework_df, mock_df, 4)
        self.assertEqual(prop, 1 / 4)

    def get_top5_performers(self):
        data = {
            "rank": [1, 1, 2, 3, 3],
            "dataset": ["B", "A", "C", "A", "A"],
            "framework": ["D", "A", "B", "C", "A"],
        }
        expected_df = pd.DataFrame(data)
        top5 = get_top5_performers(mock_df, "rank").reset_index().drop(columns=["index"])
        assert top5.equals(expected_df)

    def test_get_name_before_first_underscore(self):
        data = {"names": ["name_2_wfwe@_@323__2", "a__sas234", "1234_12", "_23edsdd"]}
        mock_df = pd.DataFrame(data)
        excepted_names = pd.Series(["name", "a", "1234", ""])
        new_names = get_name_before_first_underscore(mock_df, "names")
        assert new_names.equals(excepted_names)

    def test_clean_up_framework_names(self):
        expected_names = pd.Series(
            [
                "AutoGluon",
                "AutoGluon v0.1",
                "AutoGluon v0.2",
                "AutoGluon v0.3",
                "AutoGluon",
                "AutoGluon v0.1",
                "AutoGluon v0.2",
                "AutoGluon v0.3",
            ]
        )
        new_framework_names = clean_up_framework_names(mock_df, dummy=True)
        assert new_framework_names.equals(expected_names)


if __name__ == "__main__":
    unittest.main()
