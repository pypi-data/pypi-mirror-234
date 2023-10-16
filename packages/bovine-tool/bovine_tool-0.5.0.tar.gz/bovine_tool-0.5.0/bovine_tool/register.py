import asyncio

from argparse import ArgumentParser

from .store import InlineBovineStore


async def register_user(handle_name, domain=None):
    async with InlineBovineStore(domain=domain) as store:
        bovine_name = await store.register(handle_name)
        print(f"Bovine name: {bovine_name}")


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "handle_name",
        help="Register a new user, argument is the FediVerse handle name",
    )
    parser.add_argument(
        "--domain",
        help="domain the actor should be on, otherwise taken from bovine_config.toml",
        default=None,
    )

    args = parser.parse_args()

    asyncio.run(register_user(args.handle_name, args.domain))


if __name__ == "__main__":
    main()
