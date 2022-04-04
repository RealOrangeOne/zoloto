import subprocess

import zoloto

from . import call_cli


def test_module_main() -> None:
    rtn = call_cli(["--help"])
    rtn.check_returncode()


def test_cli_entrypoint() -> None:
    rtn = subprocess.run(["zoloto", "--help"])
    rtn.check_returncode()


def test_version() -> None:
    rtn = call_cli(["--version"])
    rtn.check_returncode()
    assert rtn.stdout.strip() == zoloto.__version__
