from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError
from elasticsearch.helpers import async_bulk
from elasticsearch_dsl import connections
from elasticsearch_dsl.connections import connections
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select


from app.elastic_models.skill import SkillDoc
from app.models.skill import Skill


def delete_elasticsearch_index():
    try:
        SkillDoc._index.delete()
        print(f"Deleted existing index '{SkillDoc._index._name}'")
    except NotFoundError:
        pass


def create_elasticsearch_index():
    SkillDoc.init()
    print(f"Created index '{SkillDoc._index._name}' with mappings.")


async def index_skills_to_elasticsearch(session: AsyncSession, elasticsearch: AsyncElasticsearch):
    client = elasticsearch
    query = select(Skill)
    result = await session.execute(query)
    skills = result.scalars().all()

    if not skills:
        print("No skills found in PostgreSQL to index.")
        return

    actions = []
    for skill in skills:
        doc = SkillDoc(
            _id=skill.id,
            form_id=skill.form_id,
            name=skill.name,
            description=skill.description,
            type=skill.type.value,
        )
        actions.append(doc.to_dict(include_meta=True))

    await async_bulk(client, actions, index=SkillDoc._index._name)
    print(f"Indexed skills to Elasticsearch.")
