lint:
	ruff .
	mypy .

format:
	ruff --fix .

test:
	pytest --cov back --cov-report term-missing
