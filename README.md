# Cloud Storage Web Service Backend

## Features

- Fully async file management (upload/download/delete)
- File sharing with other users

## Run service

> Install Poetry first

```sh
poetry install && uvicorn app:app --reload
```

Service will be available on localhost:8000/docs