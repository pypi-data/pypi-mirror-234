import asyncio
import json
from argparse import ArgumentParser

from asyncstdlib.itertools import islice
from ptpython.repl import embed

from bovine import BovineClient
from bovine.activitystreams.utils.print import print_activity


def build_parser():
    parser = ArgumentParser("Opens a REPL with preloaded BovineClient client")
    parser.add_argument("--domain", help="Domain the actor can be found on")
    parser.add_argument("--secret", help="Secret associated with the account")
    parser.add_argument("--config_file", help="Toml fail containing domain and secret")

    parser.add_argument("--inbox", action="store_true", help="Display the inbox")
    parser.add_argument("--outbox", action="store_true", help="Display the outbox")
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Display a summary of the activity instead of the full json",
    )

    parser.add_argument(
        "--max_number",
        type=int,
        help="Number of elements to display in inbox or outbox",
        default=20,
    )

    return parser


def config(repl):
    repl.use_code_colorscheme("dracula")
    repl.enable_output_formatting = True


async def repl(client):
    async with client:
        activity_factory, object_factory = client.factories
        print("The variable client contains your BovineClient")
        print("The variables activity_factory and object_factory")
        print("contain the corresponding objects")
        print("With await client.inbox() and await client.outbox()")
        print("one can interface with these two")
        print()
        await embed(
            globals=globals(),
            locals=locals(),
            return_asyncio_coroutine=True,
            patch_stdout=True,
            configure=config,
        )


async def show_inbox(client: BovineClient, max_number: int = 10, summary: bool = False):
    async with client:
        await display_box(await client.inbox(), max_number, summary)


async def show_outbox(
    client: BovineClient, max_number: int = 10, summary: bool = False
):
    async with client:
        await display_box(await client.outbox(), max_number, summary)


async def display_box(box, max_number: int, summary: bool):
    async for item in islice(box, max_number):
        if summary:
            print_activity(item)
        else:
            print(json.dumps(item, indent=2))
            print()


def main():
    args = build_parser().parse_args()

    if args.config_file:
        client = BovineClient.from_file(args.config_file)
    elif args.domain and args.secret:
        client = BovineClient(host=args.domain, secret=args.secret)
    else:
        default_config_file = "bovine_user.toml"
        client = BovineClient.from_file(default_config_file)

        print(f"Config file not specified using fallback value '{default_config_file}'")

    if args.inbox:
        asyncio.run(
            show_inbox(client, max_number=args.max_number, summary=args.summary)
        )
    elif args.outbox:
        asyncio.run(
            show_outbox(client, max_number=args.max_number, summary=args.summart)
        )
    else:
        loop = asyncio.new_event_loop()
        loop.run_until_complete(repl(client))


if __name__ == "__main__":
    main()
