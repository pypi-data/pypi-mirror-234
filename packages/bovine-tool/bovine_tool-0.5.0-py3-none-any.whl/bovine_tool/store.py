import os
from tortoise import Tortoise

from bovine_store import BovineAdminStore


class InlineBovineStore(BovineAdminStore):
    def __init__(self, domain: str = None):
        self.db_url = os.environ.get("BOVINE_DB_URL", "sqlite://bovine.sqlite3")

        super().__init__(domain=domain)

    async def __aenter__(self):
        await Tortoise.init(
            db_url=self.db_url, modules={"models": ["bovine_store.models"]}
        )

        return self

    async def __aexit__(self, exc_type, exc, tb):
        await Tortoise.close_connections()
