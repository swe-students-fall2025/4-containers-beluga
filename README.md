![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)
![Web App CI](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/web-app-ci.yml/badge.svg)

# Containerized App Exercise

Build a containerized app that uses machine learning. See [instructions](./instructions.md) for details.

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

- `MONGO_URI`: MongoDB connection string (default: `mongodb://localhost:27017/`)
- `DB_NAME`: Database name (default: `testdb`)
