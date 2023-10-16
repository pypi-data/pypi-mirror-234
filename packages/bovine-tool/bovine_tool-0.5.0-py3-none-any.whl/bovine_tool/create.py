import asyncio
from tortoise import Tortoise

from .store import InlineBovineStore


async def create_tables():
    async with InlineBovineStore():
        await Tortoise.generate_schemas()


def main():
    asyncio.run(create_tables())


if __name__ == "__main__":
    main()
