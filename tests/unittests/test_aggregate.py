import filecmp
import os
import unittest

from autogluon_dashboard.aggregate_file import create_merged_file, extract_code, get_imports

TEST_FILE_PATH = "tests/unittests/mock_python_files/mock_file.py"
TEST_DIR_PATH = "tests/unittests/mock_python_files"
AGG_OUT_FILE_PATH = "tests/unittests/out_file/out.py"


class TestAggregate(unittest.TestCase):
    def test_get_code(self):
        code = extract_code(TEST_FILE_PATH)
        expected_code = """# This file is only consumed by test_aggregate.py to test the aggregation functions from the aggregate_file.py script.



def code():
    a = 1
    b = 2
    return lambda x: x + a * b
"""
        self.assertEqual(code, expected_code)

    def test_get_imports(self):
        imports = set()
        get_imports(TEST_FILE_PATH, imports)
        imports = sorted(list(imports))
        self.assertEqual(imports[0], "from module import pkg")
        self.assertEqual(imports[1], "from module import pkg as name")
        self.assertEqual(imports[2], "from module.sub_module import pkg as name")
        self.assertEqual(imports[3], "import pandas")
        self.assertEqual(imports[4], "import pandas as pd")
        self.assertEqual(imports[5], "import panel")
        self.assertEqual(imports[6], "import pkg.sub_pkg")
        self.assertEqual(imports[7], "import pkg.sub_pkg as name")

    def test_aggregation(self):
        out_file = AGG_OUT_FILE_PATH
        with open(os.path.join("tests/unittests/out_file", "out.py"), "w") as fp:
            pass
        create_merged_file(TEST_DIR_PATH, AGG_OUT_FILE_PATH)
        create_merged_file(TEST_DIR_PATH + "/sub_folder", AGG_OUT_FILE_PATH)
        assert filecmp.cmp(out_file, "tests/unittests/out_file/expected_out.py")

    def test_trailing_paran(self):
        code = extract_code("tests/unittests/mock_python_files/mock_import.py")
        expected_code = ""
        self.assertEqual(code, expected_code)


if __name__ == "__main__":
    unittest.main()
