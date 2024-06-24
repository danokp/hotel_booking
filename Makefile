start:
	uvicorn app.main:app --reload

makemigrations:
	alembic init migrations
	alembic revision --autogenerate -m "Initial migration"

migrate:
	alembic upgrade head

revert_migration:
	alembic downgrade -1

start_celery:
	celery -A app.tasks.celery_app:celery_app worker --loglevel=INFO

start_celery_beat:
	celery --app=app.tasks.celery_app:celery_app worker -l INFO -B

start_flower:
	celery -A app.tasks.celery_app:celery_app flower

linter:
	ruff check --fix # add to see suggested changes --diff

formater:
	ruff format # add to see suggested changes --check --diff
