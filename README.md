[![Build Status](https://travis-ci.org/nobbynobbs/devman-async-python-3.svg?branch=master)](https://travis-ci.org/nobbynobbs/devman-async-python-3)

# Streamer

Module 3 of Devman's async Python [course](https://dvmn.org/modules/async-python)

## Run service

### With docker-compose
run service on port 8000
```bash
docker-compose up [-d]  # -d - run in detached mode
```

### With docker
```bash
# first build image
docker build -t streamer .
# run container
docker run --rm -it -p 8000:8080 streamer  # interactive with tty
docker run --rm -d -p 8000:8080 streamer  # detached 
```

## Where is requirements.txt?

It's not here, [poetry](https://poetry.eustace.io/) is used.

## Install dependencies

```bash
poetry install [--no-dev]
```
