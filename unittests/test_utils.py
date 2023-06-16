from scripts.widget import Widget
import unittest
from unittest import mock
import pandas as pd
from scripts.utils import *

d = {'col1': [5, 2, 3, 1, 3, 4, 5, 0], 'dataset': ['D', 'C', 'A', 'B', 'A', 'D', 'C', 'A']}
mock_df = pd.DataFrame(data=d)

class TestUtils(unittest.TestCase):
    def test_get_sorted_names_from_col(self):
        sorted_names = get_sorted_names_from_col(mock_df, 'dataset')
        self.assertEqual(sorted_names, ['A', 'B', 'C', 'D'])
    
    def test_get_df_filter_by_dataset(self):
        data = {'col1': [3, 3, 0], 'dataset': ['A', 'A', 'A']}
        expected_df = pd.DataFrame(data) 
        filtered_df = get_df_filter_by_dataset(mock_df, 'A').reset_index()
        print(expected_df, "\n",filtered_df)
        self.assertEqual(filtered_df, expected_df)


if __name__ == '__main__':
    unittest.main()