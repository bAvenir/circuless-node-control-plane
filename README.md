# circuless-node-control-plane
Control plane for managing circuless remote data infrastructures

## Requirements

## Run development mode

### Install python environment

python -m venv .venv
source .venv/bin/activate

### Libraries
pip install "fastapi[standard]"
pip freeze > ./app/requirements.txt

### Start dev env (Only app)
fastapi run app/src/main.py --port 3000

## Configuration
Create .env file

```
DATABASE_URL=postgresql+asyncpg://bavenir:bavenir@localhost:5432/circdb
```

## Run with docker
Copy .env to app directory and replace URLs for Docker DNS names (i.e. localhost --> Postgres)

### Build
docker compose up --build

### Run
docker compose up -d

### Stop
docker compose down



