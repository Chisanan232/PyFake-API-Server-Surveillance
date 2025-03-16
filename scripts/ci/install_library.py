import argparse
import subprocess
import traceback

parser = argparse.ArgumentParser(
    prog="Python dependency installer",
    description="Only be use in CI workflow",
)
parser.add_argument("-l", "--library", type=str, help="The Python library to install")
args = parser.parse_args()

try:
    subprocess.run(f"pip3 install -U {args.library}", shell=True)
except Exception:
    print("[DEBUG] get exception:")
    traceback.print_exc()
