![Lint-free](https://github.com/swe-students-fall2025/4-containers-beluga/actions/workflows/lint.yml/badge.svg)
![Web App CI](https://github.com/swe-students-fall2025/4-containers-beluga/actions/workflows/web-app-ci.yml/badge.svg)
![Machine Learning Client CI](https://github.com/swe-students-fall2025/4-containers-beluga/actions/workflows/machine-learning-client-ci.yml/badge.svg)

# Containerized App Exercise

This project is a fully containerized system that combines a Python-based web application, a machine‑learning inference client, and a MongoDB database. The webapp allows users to take a picture with a gesture, which will be identified by the ML Model. Then they can add their identified emotion to the whiteboard.

## Team Members
[JunHao Chen](https://github.com/JunHaoChen16)

[Xiaomin Liu](https://github.com/xl4624)

[YI-KAI Huang](https://github.com/DplayerXAX)

[Coco Liu](https://github.com/yiminliu2004)

[David](https://github.com/SnazzyBeatle115)


## Quick Start with Docker Compose
Works on all systems compatible with Docker Desktop. Make sure you have Docker Desktop installed.

Clone the repo:
```bash
git clone https://github.com/swe-students-fall2025/4-containers-beluga.git
cd 4-containers-beluga
```

To run all services together:

```bash
# Copy environment variables file
cp env.example .env

# Edit .env file with your configuration if needed
# You may keep the defaults for local development.

# Start all services
docker compose up --build

# Or run in detached mode
docker compose up -d --build
```

This will start:
- MongoDB database
- Web application
- Machine Learning client

You can access the webapp at `localhost:5000`, or whatever port you set in `.env`.

## MongoDB

Set up MongoDB as a replica set:

```bash
docker stop mongodb
docker rm mongodb
docker run --name mongodb -d -p 27017:27017 mongo --replSet rs0
docker exec -it mongodb mongosh --eval "rs.initiate({_id: 'rs0', members: [{_id: 0, host: 'localhost:27017'}]})"
```

## Web App

```bash
cd web-app
pipenv install
pipenv run python app.py
pipenv run black .              # Format code
pipenv run pylint **/*.py       # Lint code
pipenv run pytest --cov=. --cov-report=html  # Run tests with coverage
```

## Machine Learning Client

```bash
cd machine-learning-client
pipenv install
pipenv run python client.py
pipenv run black .              # Format code
pipenv run pylint **/*.py       # Lint code
pipenv run pytest --cov=. --cov-report=html  # Run tests with coverage
```

## Environment Variables
| Variable        | Default | Description                              |
|-----------------|---------|------------------------------------------|
| MONGO_USERNAME  | user    | MongoDB username for authentication      |
| MONGO_PASSWORD  | pass    | MongoDB password for authentication      |
| WEBAPP_PORT     | 5000    | Port exposed by the web application      |
| MLCLIENT_PORT   | 80      | Port exposed by the machine learning client |
| MONGODB_PORT    | 27017   | Port used by MongoDB                     |



