FROM python:3.11

WORKDIR ./ 

RUN pip install  poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root
COPY . ./
