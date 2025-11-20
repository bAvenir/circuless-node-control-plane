# circuless-node-control-plane
Control plane for managing circuless remote data infrastructures

## Requirements

Python installed if you plan to run locally

Docker and docker compose

Production: POSTGRES, APISIX*, ETCD*

Development: (Testing whole stack) POSTGRES, APISIX*, ETCD*, ZIPKIN, FLUENT-BIT

* APISIX not enabled in v0.0.1

## Run production with Docker

1. Copy environments/.env.docker in the root folder (Update if needed)

2. Add your certificate.pem at the root folder. Obtain with support from bAvenir. (Without it you can start in development mode only)

3. Build the application: docker compose up -d --build

4. Initialize DB:

Run 'docker ps' and get container ID of circuless-node. In the example output from docker ps below, take e2a1564620f7.

>    
    CONTAINER ID   IMAGE                              COMMAND                  CREATED              STATUS                        PORTS                                         NAMES
    e2a1564620f7   circuless-node-control-plane-app   "uvicorn main:app --…"   About a minute ago   Up About a minute (healthy)   0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp   circuless-node

Run docker exec -it CONTAINER_ID python init_db.py

5. DONE

## Run development mode

1. Install python environment

python -m venv .venv
source .venv/bin/activate

2. Install libraries
Install from requirements.txt

3. Copy environment settings

Copy environments/.env.local to root

4. Init dB

Run python src/init_db.py

5. Start
fastapi run src/main.py --port 3000

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

## Who to contact
Jozef.Ziduliak@bavenir.eu