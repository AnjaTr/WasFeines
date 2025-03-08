WasFeines
=========

An amazing recipe storage application!

# Getting started

To set up local development of this application, install these prerequisites:

* Make sure `uv` is installed globally in your system. [Link](https://docs.astral.sh/uv/)
* Make sure `node` (version 22 LTS) and `npm` is installed globally in your system. [Link](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm).

Then, to start the backend:

* `cd api/` Go to the `api/` directory
* `uv install` Install backend dependencies (only has to be done on initial setup or if dependencies change)
* `uv run fastapi dev` Run the FastAPI backend.

Then, to start the frontend:

* `cd frontend/` Go to the `frontend/` directory
* `npm install` Install frontend dependencies (only has to be done on initial setup or if dependencies change)
* `npm run dev` Run the `vite` development server.

Note that both `uv run fastapi dev` and `npm run dev` need to run at the same time (so maybe in separate terminal windows). During local development, the `vite` development server will reverse proxy to the fastapi backend.