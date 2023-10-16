import argparse
import asyncio

from .utils.msg import process, validate


def build_parser():
    parser = argparse.ArgumentParser("Send a message through your ActivityPub Actor")
    parser.add_argument(
        "--secret",
        help="Secret corresponding to a did-key deposited with your actor",
    )
    parser.add_argument("--host", help="Hostname your actor is on")
    parser.add_argument(
        "--to",
        nargs="+",
        help="Recipients either as FediVerse handle or actor id",
        default=[],
    )
    parser.add_argument("--public", action="store_true", default=False)
    parser.add_argument("message", help="You message text")

    return parser


def main():
    args = (build_parser()).parse_args()

    validate(args)

    asyncio.run(process(args))


if __name__ == "__main__":
    main()
