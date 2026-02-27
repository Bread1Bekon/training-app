from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.form import Form
from app.models.skill import Skill


class SkillRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_skills(self, form_id: int, skills_data: list[dict]) -> list[Skill]:
        skills = [Skill(form_id=form_id, **data) for data in skills_data]
        self.db.add_all(skills)
        await self.db.commit()

        for skill in skills:
            await self.db.refresh(skill)

        return skills

class FormRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_form(self, form_data: dict) -> Form:
        form = Form(**form_data)
        self.db.add(form)
        await self.db.commit()
        await self.db.refresh(form)
        return form

    async def get_form_by_user_id(self, user_id: int):
        result = await self.db.execute(select(Form).where(user_id == Form.user_id))
        return result.scalar_one_or_none()

    async def delete_form(self, form: Form) -> bool:
        await self.db.delete(form)
        await self.db.flush()
        return True