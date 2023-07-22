FROM python:3.11

WORKDIR ./ 

RUN apt update && apt install -y make

COPY pyproject.toml poetry.lock Makefile ./

RUN curl -sSL https://install.python-poetry.org | python3 - &&  \
    mv /root/.local/bin/poetry /usr/local/bin/

RUN make install-deploy    

COPY . ./
