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

    async def create_form(self, form_data: dict, user_id: int) -> Form:
        form = Form(**form_data)
        form.user_id = user_id
        self.db.add(form)
        await self.db.commit()
        await self.db.refresh(form)
        return form

    async def update_form_status(self, form_id: int, new_form_status):
        result = await self.db.execute(select(Form).where(form_id == Form.id))
        form = result.scalar_one_or_none()

        if form:
            form.status = new_form_status

            await self.db.commit()
            await self.db.refresh(form)
        return form

    async def delete_existing_form(self, user_id: int):
        result = await self.db.execute(select(Form).where(user_id == Form.user_id))
        existing_form = result.scalar_one_or_none()

        if existing_form:
            await self.db.delete(existing_form)
            await self.db.flush()

        return True