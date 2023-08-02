import unittest
from unittest import mock
from unittest.mock import call

from autogluon_dashboard.utils.get_data import get_dataframes

PER_DATASET_TEST_CSV_PATH = "random_csv.csv"
ALL_DATASETS_COMBINED_TEST_CSV_PATH = "random_csv2.csv"
HARDWARE_METRICS_PATH = "metrics.csv"


class TestDataLoad(unittest.TestCase):
    @mock.patch("pandas.read_csv")
    def test_data_load(self, mock_data):
        mock_data.return_value = "some data"
        paths = PER_DATASET_TEST_CSV_PATH, ALL_DATASETS_COMBINED_TEST_CSV_PATH, HARDWARE_METRICS_PATH
        df1, df2, df3 = get_dataframes(paths)
        self.assertEqual(df1, mock_data.return_value)
        self.assertEqual(df2, mock_data.return_value)
        self.assertEqual(df3, mock_data.return_value)
        calls = [
            call(PER_DATASET_TEST_CSV_PATH),
            call(ALL_DATASETS_COMBINED_TEST_CSV_PATH),
            call(HARDWARE_METRICS_PATH),
        ]
        mock_data.assert_has_calls(calls, any_order=False)
        assert mock_data.call_count == 3


if __name__ == "__main__":
    unittest.main()
