import json

from fastapi import HTTPException
from sqlalchemy.testing.pickleable import User

from app.dto.form import FormDTO
from app.dto.skill import SkillDTO
from app.dto.user import UserDTO
from app.enums.user import UserType
from app.redis_db import redis_db
from app.repository.form import FormRepository
from app.repository.form import SkillRepository
from app.repository.token import SECONDS_IN_DAY
from app.schemas.form import FormCreate, FormOut, ScoredForm
from app.schemas.skill import SkillOut


class FormService:
    def __init__(self, form_repository: FormRepository, skill_repository: SkillRepository):
        self.form_repository = form_repository
        self.skill_repository = skill_repository

    async def create_form(self, user: UserDTO, form_data: FormCreate) -> FormOut:
        await self.form_repository.delete_existing_form(user.id)

        new_form = await self.form_repository.create_form(form_data.model_dump(exclude={"skills"}), user.id)

        skills_dicts = [skill.model_dump() for skill in form_data.skills]
        created_skills = await self.skill_repository.create_skills(new_form.id, skills_dicts)

        return FormOut(
            id=new_form.id,
            description=new_form.description,
            user_id=new_form.user_id,
            status=new_form.status,
            skills=[
                SkillOut.model_validate(i) for i in created_skills
            ]
        )

    async def update_form_status(self, form_id, new_form_status, current_user):
        if current_user.access_level != UserType.MODERATOR:
            raise HTTPException(status_code=403, detail="Forbidden. You don't have access to this action.")

        form = await self.form_repository.update_form_status(form_id, new_form_status)

        return form

    async def find_suitable_forms(self, user_id: int) -> list[ScoredForm]:
        form = await self.form_repository.get_form_by_id(user_id)
        skills = await self.skill_repository.get_skills_by_form(form)
        suitable_forms = await self.skill_repository.get_suitable_forms(skills, user_id)

        if suitable_forms:
            await redis_db.setex(
                user_id,
                SECONDS_IN_DAY,
                json.dumps([form.model_dump() for form in suitable_forms]),
            )

        return suitable_forms

    async def reject_form(self, user_id: int, rejected_form_id: int):
        await self.form_repository.add_rejected_to_db(user_id, rejected_form_id)
        await self.form_repository.reject_form(user_id, rejected_form_id)