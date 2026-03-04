# training-app

training-app is a networking workshop, designed to help you find mentors with relevant skills and knowdledge, and mentees with desire to learn something you eager to teach.

## How to start up?

1. Boot up Docker Desktop on your PC.
2. Open PyCharm and load training-app project.
3. Write the following commands into terminal (not python console):
```
cp .env.example .env
docker compose up --build -d
```
4. Wait for application to start
5. Check Docker Desktop. If you see training-app in "Containers" and all of his components are running (green dot next to name), then everything is setup correctly. If not, check logs in Docker Desktop for errors.

