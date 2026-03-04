from app.models.form import FormStatus
from app.repository.form import FormRepository
from app.repository.form import SkillRepository
from app.schemas.form import FormCreate, FormOut
from app.schemas.skill import SkillOut
from app.schemas.user import UserOut


class FormService:
    def __init__(self, form_repository: FormRepository, skill_repository: SkillRepository):
        self.form_repository = form_repository
        self.skill_repository = skill_repository

    async def create_form(self, user: UserOut, form_data: FormCreate) -> FormOut:
        existing_form = await self.form_repository.get_form_by_user_id(user.id)

        if existing_form is not None:
            await self.form_repository.delete_form(existing_form)
            await self.form_repository.db.flush()

        form_dict = {
            "description": form_data.description,
            "user_id": user.id,
            "status": FormStatus.PENDING
        }

        new_form = await self.form_repository.create_form(form_dict)

        skills_dicts = [skill.model_dump() for skill in form_data.skills]
        created_skills = await self.skill_repository.create_skills(new_form.id, skills_dicts)

        form_out = {"id": new_form.id, "user_id": new_form.user_id, "description": new_form.description,
                    "status": new_form.status, "skills": [SkillOut.model_validate(skill) for skill in created_skills]}
        return FormOut.model_validate(form_out)