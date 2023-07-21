import subprocess
import unittest


class TestTestCoverage(unittest.TestCase):
    def test_coverage(self):
        process = subprocess.run(["coverage-threshold", "--line-coverage-min", "80", "--file-line-coverage-min", "90"])
        self.assertEqual(process.returncode, 0, "Failed unittest coverage check")


if __name__ == "__main__":
    unittest.main()
