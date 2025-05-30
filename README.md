WasFeines
=========

An amazing recipe storage application!

# Getting started

To set up local development of this application, install these prerequisites:

* Make sure `uv` is installed globally in your system. [Link](https://docs.astral.sh/uv/)
* Make sure `node` (version 22 LTS) and `npm` is installed globally in your system. [Link](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm).

Then, to start the backend:

* `cd api/` Go to the `api/` directory
* `uv run fastapi dev src/main.py` Run the FastAPI backend.

Then, to start the frontend:

* `cd frontend/` Go to the `frontend/` directory
* `npm install --legacy-peer-deps` Install frontend dependencies (only has to be done on initial setup or if dependencies change)
* `npm run dev` Run the `vite` development server.

Note that both `uv run fastapi dev` and `npm run dev` need to run at the same time (so maybe in separate terminal windows). During local development, the `vite` development server will reverse proxy to the fastapi backend.

An optional convenience script `./run.sh` is provided to start both frontend and backend.

## Testing

To run Backend tests, make sure you are in the `api/` directory, then run:

```bash
uv run pytest
```

## Frontend Typings

This project uses generated typings based on OpenAPI schemas in the frontend. You need to regenerate typings every time there is an API change in the Backend. To (re)generate frontend typings, first run the backend, then execute from the root folder of this project:

```bash
npx openapi-typescript http://localhost:8000/api/openapi.json -o frontend/src/api/schema.d.ts
```