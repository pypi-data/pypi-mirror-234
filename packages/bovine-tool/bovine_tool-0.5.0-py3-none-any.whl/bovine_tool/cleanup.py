import asyncio
from tortoise import Tortoise

from .store import InlineBovineStore


async def cleanup():
    async with InlineBovineStore():
        client = Tortoise.get_connection("default")

        batch_size = 1000

        sql_query_visible_to = f"""
        delete from visibleto where main_object_id in 
            (select id from storedjsonobject
                where object_type='REMOTE'
                    and updated < (current_date - interval '3 day')
                limit {batch_size}) RETURNING *;
        """

        delete_count = batch_size

        while delete_count >= batch_size:
            delete_count, _ = await client.execute_query(sql_query_visible_to)
            print(delete_count)

            await asyncio.sleep(0.1)

        print("Done with visible to")

        try:
            await client.execute_query(
                """alter table visibleto drop constraint 
                visibleto_main_object_id_fkey;"""
            )
        except Exception:
            ...

        sql_query = f"""
        delete from storedjsonobject where id in 
            (select id from storedjsonobject
                where object_type='REMOTE'
                    and updated < (current_date - interval '3 day')
                limit {batch_size}) RETURNING *;
        """

        delete_count = batch_size

        try:
            while delete_count == batch_size:
                delete_count, _ = await client.execute_query(sql_query)
                print(delete_count)

                await asyncio.sleep(0.1)
        finally:
            delete_visible_to = """
            delete from visibleto where main_object_id in 
                (select main_object_id from 
                    visibleto v left join storedjsonobject s on v.main_object_id = s.id 
                where s.id is null);"""
            await client.execute_query(delete_visible_to)

            await client.execute_query(
                """alter table visibleto add constraint visibleto_main_object_id_fkey 
                foreign key (main_object_id) references storedjsonobject (id);"""
            )


if __name__ == "__main__":
    asyncio.run(cleanup())
