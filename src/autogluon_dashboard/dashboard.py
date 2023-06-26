import os
import subprocess
import sys

def run_dashboard():
    csv1 = sys.argv[2]
    csv2 = sys.argv[4]
    wrapper_dir = os.path.dirname(__file__)
    app_location = os.path.join(wrapper_dir, "app.py")
    subprocess.run(
        [
            "panel",
            "convert",
            f"{app_location}",
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


if __name__ == "__main__":
    run_dashboard()