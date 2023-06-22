import subprocess
import sys

from autogluon.common.loaders import load_pd

if __name__ == "__main__":
    csv1 = sys.argv[2]
    csv2 = sys.argv[4]
    subprocess.run(["panel", "serve", "src/app/app.py", "--autoreload", "--args", f"{csv1}", f"{csv2}"])
    # subprocess.run(["panel", "convert", "app.py", "--to", "pyodide-worker", "--out", "docs/app"])
