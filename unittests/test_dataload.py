import unittest
from unittest import mock
from unittest.mock import call
from scripts.data import get_dataframes, PER_DATASET_TEST_CSV_PATH, ALL_DATASETS_COMBINED_TEST_CSV_PATH

class TestDataLoad(unittest.TestCase):
    @mock.patch('autogluon.common.loaders.load_pd.load')
    def test_data_load(self, mock_data):
        mock_data.return_value = "some data" 
        df1, df2 = get_dataframes(PER_DATASET_TEST_CSV_PATH, ALL_DATASETS_COMBINED_TEST_CSV_PATH)
        self.assertEqual(df1, mock_data.return_value)
        self.assertEqual(df2, mock_data.return_value)
        calls = [call(PER_DATASET_TEST_CSV_PATH), call(ALL_DATASETS_COMBINED_TEST_CSV_PATH)]
        mock_data.assert_has_calls(calls, any_order=False)
        assert mock_data.call_count == 2


if __name__ == '__main__':
    unittest.main()
