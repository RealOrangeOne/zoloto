from __future__ import annotations

import subprocess
import sys
from typing import List


def call_cli(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "zoloto"] + args,
        text=True,
        capture_output=True,
    )
