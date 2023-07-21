import unittest
from unittest.mock import MagicMock, call, mock_open, patch

import boto3

from autogluon_dashboard.dashboard import get_args, run_dashboard, upload_to_s3


class TestDashboardWrapper(unittest.TestCase):
    def test_get_args(self):
        with patch(
            "sys.argv",
            [
                "agdash",
                "--per_dataset_csv",
                "dev_data/all_data.csv",
                "--agg_dataset_csv",
                "dev_data/autogluon.csv",
                "--s3_bucket",
                "test-bucket",
                "--s3_prefix",
                "sub_folder",
                "--s3_region",
                "us-east-2",
            ],
        ):
            args = get_args()
            self.assertEqual(args.per_dataset_csv, "dev_data/all_data.csv")
            self.assertEqual(args.agg_dataset_csv, "dev_data/autogluon.csv")
            self.assertEqual(args.s3_bucket, "test-bucket")
            self.assertEqual(args.s3_prefix, "sub_folder")
            self.assertEqual(args.s3_region, "us-east-2")

    @patch("boto3.client")
    def test_upload_to_s3(self, mock_client):
        s3_client = MagicMock()
        mock_client.side_effect = [s3_client]
        mock_client.upload_fileobj.return_value = "upload"
        with patch("builtins.open", mock_open(read_data="data")) as mock_file:
            s3_client = boto3.client("s3")
            upload_to_s3(s3_client, "somefile.csv", "folder/s3file.csv", "test-bucket")
            upload_to_s3(
                s3_client,
                "someotherfile.csv",
                "folder/s3file2.csv",
                "other-test-bucket",
                args={"ContentType": "text/html"},
            )
            calls = [
                call(mock_file.return_value, "test-bucket", "folder/s3file.csv", ExtraArgs=None),
                call(
                    mock_file.return_value,
                    "other-test-bucket",
                    "folder/s3file2.csv",
                    ExtraArgs={"ContentType": "text/html"},
                ),
            ]
            s3_client.upload_fileobj.assert_has_calls(calls, any_order=False)
            assert s3_client.upload_fileobj.call_count == 2


if __name__ == "__main__":
    unittest.main()
