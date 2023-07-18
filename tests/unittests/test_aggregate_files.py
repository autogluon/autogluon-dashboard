import os
import subprocess
import unittest


class TestAggregateFiles(unittest.TestCase):
    def test_run_aggregate_script(self):
        test_file_dir = os.path.dirname(__file__)
        aggregate_file_dir = os.path.join(test_file_dir, "../../src/autogluon_dashboard/utils/")
        process = subprocess.run(["python3", f"{aggregate_file_dir}aggregate_file.py"], capture_output=True, text=True)
        self.assertEqual(process.returncode, 0, f"Aggregate Script did not run successfully. {process.stderr}")


if __name__ == "__main__":
    unittest.main()
