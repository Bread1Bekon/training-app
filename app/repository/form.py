import json
from typing import Any, Coroutine

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select
from elasticsearch.helpers import async_bulk
from elasticsearch import AsyncElasticsearch
from elasticsearch_dsl import AsyncSearch, Q
from sqlalchemy.orm import selectinload
from logging import getLogger
from app.redis_db import redis_db

from app.dto.form import FormDTO
from app.dto.skill import SkillDTO
from app.enums.skill import SkillType
from app.models.form import Form, RejectedForm
from app.models.skill import Skill
from app.elastic_models.skill import SkillDoc
from app.schemas.form import ScoredForm

LOGGER = getLogger(__name__)

class SkillRepository:
    def __init__(self, db: AsyncSession, elasticsearch: AsyncElasticsearch):
        self.db = db
        self.es_client = elasticsearch
        self.redis_client = redis_db

    async def create_skills(self, form_id: int, skills_data: list[dict]) -> list[Skill]:
        skills = [Skill(form_id=form_id, **data) for data in skills_data]
        self.db.add_all(skills)
        await self.db.commit()

        for skill in skills:
            await self.db.refresh(skill)

        await self._save_in_elastic(skills)

        return skills

    async def _save_in_elastic(self, skills: list[Skill]):
        actions = [
            SkillDoc(
                form_id=skill.form_id,
                name=skill.name,
                description=skill.description,
                type=skill.type.value
            ).to_dict(include_meta=True)
            for skill in skills
        ]
        await async_bulk(self.es_client, actions)

        return skills

    async def get_skills_by_form(self, form: FormDTO):
        result = await self.db.execute(select(Skill).where(form.id == Skill.form_id))
        skills_db = result.scalars().all()

        return [SkillDTO.model_validate(s) for s in skills_db]

    async def get_suitable_forms(self, skills: list[SkillDTO], user_id: int) -> list[ScoredForm]:
        s = AsyncSearch(index='skills')

        opposite_type = {
            SkillType.LEARN: SkillType.TEACH,
            SkillType.TEACH: SkillType.LEARN
        }

        should_queries = []

        for skill in skills:
            target_type = opposite_type.get(skill.type).lower()

            q = Q('bool',
                  filter=[Q('term', type=target_type)],
                  must=[Q('match', name={'query': skill.name, 'fuzziness': 'AUTO'})],
                  must_not=[Q('term', form_id=skill.form_id)]
                  )
            should_queries.append(q)

        s = s.query('bool', should=should_queries)
        s = s[0:15]

        print(json.dumps(s.to_dict(), indent=2))#for debug
        response = await s.using(self.es_client).execute()

        print(f"Total hits: {response.hits.total.value}") #for debug

        bloom_key = f"rejects:{user_id}"

        unique_forms: dict[int, ScoredForm] = {}

        for hit in response.hits:
            fid = hit.form_id
            score = hit.meta.score

            if await redis_db.execute_command("BF.EXISTS", bloom_key, fid):
                continue

            if fid not in unique_forms or score > unique_forms[fid].score:
                unique_forms[fid] = ScoredForm(form_id=fid, score=score)

        return list(unique_forms.values())


class FormRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.redis_client = redis_db

    async def create_form(self, form_data: dict, user_id: int) -> FormDTO:
        form = Form(**form_data)
        form.user_id = user_id

        self.db.add(form)
        await self.db.commit()
        await self.db.refresh(form)

        return FormDTO.model_validate(form)

    async def update_form_status(self, form_id: int, new_form_status) -> FormDTO:
        result = await self.db.execute(select(Form).where(form_id == Form.id))
        form = result.scalar_one_or_none()

        if form:
            form.status = new_form_status

            await self.db.commit()
            await self.db.refresh(form)
        return FormDTO.model_validate(form)

    async def delete_existing_form(self, user_id: int):
        result = await self.db.execute(select(Form).where(user_id == Form.user_id))
        existing_form = result.scalar_one_or_none()

        if existing_form:
            await self.db.delete(existing_form)
            await self.db.flush()

        return True

    async def get_form_by_id(self, user_id: int) -> FormDTO:
        query = (
            select(Form)
            .where(user_id == Form.user_id)
            .options(selectinload(Form.skills))
        )
        result = await self.db.execute(query)

        return FormDTO.model_validate(result.scalar_one_or_none())

    async def reject_form(self, user_id, rejected_form_id):
        bloom_key = f"rejects:{user_id}"

        await redis_db.execute_command("BF.ADD", bloom_key, rejected_form_id)

    async def add_rejected_to_db(self, user_id: int, rejected_form_id: int):
        stmt = insert(RejectedForm).values(
            user_id=user_id,
            rejected_form_id=rejected_form_id
        ).on_conflict_do_nothing()

        await self.db.execute(stmt)