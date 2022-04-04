import subprocess

import zoloto

from . import call_cli


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
