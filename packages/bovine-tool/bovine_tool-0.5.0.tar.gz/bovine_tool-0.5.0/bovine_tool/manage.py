import asyncio
import json

from argparse import ArgumentParser

from bovine.crypto import generate_ed25519_private_key, private_key_to_did_key
from bovine.types import Visibility

from .store import InlineBovineStore


async def manage_user(args):
    async with InlineBovineStore() as store:
        if not (args.new_did_key or args.did_key or args.properties):
            actor = await store.actor_for_name(args.bovine_name)

            print(
                json.dumps(
                    actor.actor_object.build(visibility=Visibility.OWNER), indent=2
                )
            )

            await actor.session.close()

        if args.new_did_key:
            secret = generate_ed25519_private_key()
            print(f"Your new secret: {secret}")
            didkey = private_key_to_did_key(secret)
            await store.add_identity_string_to_actor(
                args.bovine_name, "key-from-tool", didkey
            )

        if args.did_key:
            name, didkey = args.did_key
            await store.add_identity_string_to_actor(args.bovine_name, name, didkey)

        if args.properties:
            property_file = args.properties
            with open(property_file) as fp:
                properties = json.load(fp)
            await store.set_properties_for_actor(args.bovine_name, properties)


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "bovine_name",
        help="Bovine name of the user to manage",
    )
    parser.add_argument(
        "--new_did_key",
        help="Generates a new did key for the Moo Client Flow",
        action="store_true",
    )
    parser.add_argument(
        "--did_key",
        help="Add a new did key for the Moo Client Flow",
        metavar=("key_name", "did_key"),
        nargs=2,
    )
    parser.add_argument(
        "--properties",
        help="sets the properties of the actor to the new file",
        metavar="properties_file",
    )

    args = parser.parse_args()

    asyncio.run(manage_user(args))


if __name__ == "__main__":
    main()
