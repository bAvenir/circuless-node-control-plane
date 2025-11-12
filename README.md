# circuless-node-control-plane
Control plane for managing circuless remote data infrastructures

## Requirements

APISIX, POSTGRES, ETCD, VALKEY


## Configuration
Create .env file

```
DATABASE_URL=postgresql+asyncpg://bavenir:bavenir@localhost:5432/circdb
```

## Run development mode

### Install python environment

python -m venv .venv
source .venv/bin/activate

### Libraries
Install from requirements.txt

### Start dev env (Only app)

Copy .env to root, use localhost to connect to postgres

APISIX will be skipped

fastapi run app/src/main.py --port 3000

## Run with docker
Copy .env to app directory and replace URLs for Docker DNS names (i.e. localhost --> Postgres)

### Build
docker compose up --build

### Run
docker compose up -d

### Stop
docker compose down

## DB management

Using SQLAlchemy and alembic

### DB initialization

Inside folder sources

    python init_db.py

### Other alembic commands

#### Create new migration after model changes
alembic revision --autogenerate -m "What changed in the table"

#### Apply all pending migrations
alembic upgrade head

#### Rollback one migration
alembic downgrade -1

#### Check current database version
alembic current

#### View migration history
alembic history --verbose

