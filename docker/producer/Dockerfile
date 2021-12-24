FROM python:3.6

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /home/producer

COPY . /home/producer/

# Install poetry and its dependencies
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev
