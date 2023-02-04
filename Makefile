export PYTHONPATH := 'scr'
export PIPENV_VERBOSITY := -1

run:
	@pipenv run python src/app.py test.png

lint:
	@pipenv run black .
	@pipenv run isort .

qa:
	@pipenv run pytest
