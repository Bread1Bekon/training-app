from app.db import async_session
from app.elasticsearch import get_elasticsearch
from db_seed import seed_postgres
from elasticsearch_seed import index_skills_to_elasticsearch
import asyncio

async def seed_all ():
    session = async_session()
    await seed_postgres(session, num_users=10)

    elastic = await get_elasticsearch()

    await index_skills_to_elasticsearch(session, elastic)

    session.close()
    print("Seeding completed.")

if __name__ == "__main__":
    asyncio.run(seed_all())