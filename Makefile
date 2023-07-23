install:
	poetry config virtualenvs.create false && poetry install --no-root

lint:
	ruff .
	mypy .

format:
	ruff --fix .

test:
	pytest --cov src --cov-report term-missing

startup:
	poetry shell
	poetry update

configure:
	cp local.def.env .env