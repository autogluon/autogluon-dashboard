import sys
import subprocess

if __name__ == '__main__':
    csv1 = sys.argv[2]
    csv2 = sys.argv[4]
    subprocess.run(["panel", "serve", "app.py", "--autoreload", "--args", f"{csv1}", f"{csv2}"])
