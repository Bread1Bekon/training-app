from fastapi import HTTPException

from app.dto.form import FormDTO
from app.dto.user import UserDTO
from app.models.form import FormStatus
from app.repository.form import FormRepository
from app.repository.form import SkillRepository
from app.schemas.form import FormCreate, FormOut, FormStatusEnum
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
        if current_user.access_level != "moderator":
            raise HTTPException(status_code=403, detail="Forbidden. You don't have access to this action.")

        form = await self.form_repository.update_form_status(form_id, new_form_status)

        return form