install-deploy:
	poetry config virtualenvs.create false \
    && poetry install --no-root --only main --no-interaction --no-ansi

install:
	poetry config virtualenvs.create false && poetry install --no-root

lint:
	mypy .
	ruff .

format:
	ruff --fix .

test:
	pytest --cov src --cov-report term-missing

startup:
	poetry shell
	poetry update

configure:
	cp local.def.env .env
