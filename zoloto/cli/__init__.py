import argparse
import importlib

from zoloto import __version__

__all__ = ["preview"]


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version",
        help="Show version of the tools.",
        action="version",
        version=__version__,
    )

    subparsers = parser.add_subparsers()
    for command in __all__:
        name = "{}.{}".format(__name__, command)
        importlib.import_module(name).add_subparser(subparsers)  # type: ignore

    return parser


def main() -> None:
    parser = get_parser()
    args = parser.parse_args()

    if "func" in args:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
