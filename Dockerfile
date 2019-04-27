FROM python:3.7-alpine
RUN apk add --no-cache zip=3.0-r7 \
  && pip install poetry==0.12.12 \
  && poetry config settings.virtualenvs.create false
WORKDIR /opt
ENV PYTHONPATH=/opt
COPY poetry.lock /opt/poetry.lock
COPY pyproject.toml /opt/pyproject.toml
RUN poetry install --no-dev
COPY streamer /opt/streamer
WORKDIR /opt/streamer
EXPOSE 8080
CMD ["python", "main.py"]
