import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def run(script):
    print(f"\n===== Running {script} =====")
    result = subprocess.run([sys.executable, str(ROOT / script)], cwd=ROOT)
    if result.returncode != 0:
        raise SystemExit(result.returncode)

if __name__ == "__main__":
    run("run_primary_analysis.py")
    run("run_workplace_analysis.py")
    print("\nAll OSMI analyses completed successfully.")
