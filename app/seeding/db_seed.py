import random

from faker import Faker
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.db import engine
from app.models.base import Base
from app.models.form import Form
from app.models.user import UserDB
from app.models.skill import Skill
from app.enums.form import FormStatus
from app.enums.user import UserType
from app.enums.skill import SkillType


fake = Faker()

# Sample data pools (optional)
SKILL_NAMES = [
    "Python Basics", "Git & GitHub", "Python", "Git", "Data Science", "Machine Learning", "Web Development", "SQL",
    "Docker", "REST APIs", "PostgreSQL"
]

DESCRIPTIONS = {
    "Python": "Learn Python programming from scratch to advanced.",
    "Data Science": "Data analysis, visualization, and ML basics.",
    "Machine Learning": "Supervised and unsupervised learning.",
    "Web Development": "HTML, CSS, JavaScript, React.",
    "SQL": "Querying and managing relational databases.",
    "Python Basics": "Teach core Python syntax and data structures.",
    "Git & GitHub": "Version control and collaboration.",
    "Docker": "Containerization and orchestration basics.",
    "REST APIs": "Design and build RESTful APIs.",
    "PostgreSQL": "Advanced SQL and database design.",
}


async def seed_postgres(session: AsyncSession, num_users: int = 10):
    users = []
    forms = []

    for _ in range(num_users):
        user = UserDB(
            name=fake.unique.name(),
            email=fake.unique.email(),
            password=fake.password(length=12),
            access_level=UserType.ORDINARY
        )
        users.append(user)
        session.add(user)
        await session.flush()

        form_status = random.choice(list(FormStatus))
        form = Form(
            description=fake.sentence(nb_words=10),
            user_id=user.id,
            status=form_status,
        )
        forms.append(form)
        session.add(form)
        await session.flush()

    for form in forms:
        num_skills = random.randint(1, 5)
        selected_skills = random.sample(SKILL_NAMES, k=min(num_skills, len(SKILL_NAMES)))
        for name in selected_skills:
            skill_type = random.choice([SkillType.LEARN, SkillType.TEACH])
            description = DESCRIPTIONS.get(name, fake.text(max_nb_chars=200))

            skill = Skill(
                form_id=form.id,
                name=name,
                description=description,
                type=skill_type,
            )
            session.add(skill)

    await session.commit()