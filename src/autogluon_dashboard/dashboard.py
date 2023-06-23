import subprocess
import sys

if __name__ == "__main__":
    csv1 = sys.argv[2]
    csv2 = sys.argv[4]
    subprocess.run(
        [
            "panel",
            "convert",
            "src/autogluon_dashboard/app.py",
            "--to",
            "pyodide-worker",
            "--out",
            "docs/app",
            "--requirements",
            "pandas",
            "holoviews",
            "hvplot",
        ]
    )
