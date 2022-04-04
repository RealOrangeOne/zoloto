import subprocess
import sys
from typing import List


def call_cli(args: List[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "zoloto"] + args,
        universal_newlines=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
