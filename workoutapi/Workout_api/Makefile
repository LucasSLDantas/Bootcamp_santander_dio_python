run:
	@uvicorn Workout_api.main:app --reload

alembic_rota:
	@$env:PYTHONPATH = (Get-Location)
	@set PYTHONPATH=%cd%

alembic_files_creation:
	@alembic revision --autogenerate -m "ajusta FKs em atleta"

Update_tables:
	@alembic upgrade head