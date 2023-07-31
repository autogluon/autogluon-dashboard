import os
import subprocess
import unittest


class TestPanelConvert(unittest.TestCase):
    def test_run_panel_convert(self):
        test_file_dir = os.path.dirname(__file__)
        autogluon_dir = os.path.join(test_file_dir, "../../src/autogluon_dashboard/")
        aggregate_file_dir = os.path.join(test_file_dir, f"{autogluon_dir}utils/")
        autogluon_dir = os.path.join(test_file_dir, "../../src/autogluon_dashboard/")
        aggregate_file_dir = os.path.join(test_file_dir, f"{autogluon_dir}utils/")
        process = subprocess.run(["python3", f"{aggregate_file_dir}aggregate_file.py"], capture_output=True, text=True)
        self.assertEqual(process.returncode, 0, f"Aggregate Script did not run successfully. {process.stderr}")
        agg_file_location = os.path.join(os.path.join(test_file_dir, f"{autogluon_dir}"), "out.py")
        web_files_dir = os.path.join(f"{autogluon_dir}", "web_files/")
        per_dataset_test_loc = os.path.join(test_file_dir, "resources/all_data.csv")
        aggregated_test_loc = os.path.join(test_file_dir, "resources/aggregated.csv")
        hware_test_loc = os.path.join(test_file_dir, "resources/metrics.csv")
        os.environ["PER_DATASET_S3_PATH"] = per_dataset_test_loc
        os.environ["AGG_DATASET_S3_PATH"] = aggregated_test_loc
        os.environ["HWARE_METRICS_S3_PATH"] = hware_test_loc
        process = subprocess.run(
            [
                "panel",
                "convert",
                f"{agg_file_location}",
                "--to",
                "pyodide-worker",
                "--out",
                f"{web_files_dir}",
                "--requirements",
                "pandas",
                "holoviews",
                "hvplot",
            ],
            capture_output=True,
            text=True,
        )

        self.assertEqual(process.returncode, 0, f"panel convert did not run successfully. {process.stderr}")
        self.assertEqual(process.stderr.find("Error"), -1, f"panel convert did not run successfully. {process.stderr}")


if __name__ == "__main__":
    unittest.main()
