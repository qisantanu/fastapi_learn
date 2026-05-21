## FastAPI from Python3

This repository is where I grab the knowledge of a framework for API development only named FastAPI renowned for web development.


- [FastAPI from Python3](#fastapi-from-python3)
- [Pre-requisites](#pre-requisites)
  - [Setting up](#setting-up)
    - [Steps to follow](#steps-to-follow)
- [Additional informations](#additional-informations)
  - [Environment variables](#environment-variables)


## Pre-requisites

The following software is required to work with the repository.

Development:

1. python3
2. sqlite3

This project currently works with:

![Python version](https://img.shields.io/static/v1?label=Python&message=3.10.12&color=red&&style=for-the-badge)
![FastAPI](https://img.shields.io/static/v1?label=FastAPI&message=0.116.1&color=9C312A&&style=for-the-badge)
![pip](https://img.shields.io/static/v1?label=pip&message=22.0.2&color=f77b07&&style=for-the-badge)
![Sqlite3](https://img.shields.io/static/v1?label=Sqlite3&message=3.37.2&color=2f5d8d&style=for-the-badge)

### Setting up

#### Linux/Ubuntu

It is recommended to use a virtual environment to isolate dependencies:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Windows (PowerShell)

```powershell
pip install -r requirements.txt
```

#### Steps to follow

-  [ ] Clone from repository
-  [ ] Create and activate virtual environment (Linux) or skip (Windows)
-  [ ] Run bundler `pip install -r requirements.txt`
-  [ ] Database migration `alembic upgrade head`
-  [ ] Run the application server: `uvicorn main:app --reload --log-config=log_conf.yml`
-  [ ] Start Celery worker: `./start_celery.sh` or manually:
   - Start Redis: `redis-server`
   - Start worker: `celery -A celery_app worker --loglevel=info`
   - Start beat scheduler: `celery -A celery_app beat --loglevel=info`
-  [ ] Access the APIDOCS by opening your application in http://localhost:8000/apidocs


## Additional informations
### Environment variables

| Key                       | Sample Value                               |
| ------------------------- | ------------------------------------------ |
| WEATHER_API_KEY          | 23aec9ae09052892422dac0403931879                                 |
