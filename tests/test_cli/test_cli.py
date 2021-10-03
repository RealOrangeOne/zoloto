import subprocess
import sys
from typing import List

import zoloto


def call_cli(args: List[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "zoloto"] + args,
        universal_newlines=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def test_module_main() -> None:
    rtn = call_cli(["--help"])
    assert rtn.returncode == 0


def test_cli_entrypoint() -> None:
    rtn = subprocess.run(["zoloto", "--help"])
    assert rtn.returncode == 0


def test_version() -> None:
    rtn = call_cli(["--version"])
    assert rtn.returncode == 0
    assert rtn.stdout.strip() == zoloto.__version__
