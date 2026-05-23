# Airflow Learning Guide

This project now includes a Docker-based Airflow setup for learning, integrated with our FastAPI application and SQLite database.

## Prerequisites
- Docker Desktop installed and running on your Windows machine.

## Architecture
The pipeline consists of three tasks:
1.  **`generate_random_data`**: Generates 5 random numbers.
2.  **`process_data_via_api`**: Sends data to FastAPI for NumPy-based calculations.
3.  **`save_data_to_db`**: Saves the resulting metrics into the shared `database.db`.

## Setup Instructions

1.  **Initialize the Environment**:
    Open your terminal in the project root and run:
    ```powershell
    # Ensure database and airflow files exist locally
    New-Item -ItemType file airflow.db -Force
    New-Item -ItemType file database.db -Force
    
    # Start Airflow
    docker-compose up -d
    ```

2.  **Start FastAPI**:
    Airflow needs the API to be active. Run this in a separate terminal:
    ```powershell
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ```

3.  **Access Airflow UI**:
    Go to [http://localhost:8080](http://localhost:8080) (Login: `airflow` / `airflow`).

4.  **Configure Connection**:
    - Go to **Admin -> Connections**.
    - Edit `http_default`.
    - Set **Connection Type** to `HTTP`.
    - Set **Host** to `host.docker.internal`.
    - Set **Port** to `8000`.

5.  **Run the DAG**:
    - Unpause `learning_data_pipeline` and trigger it.
    - The results will be saved to the `processed_data` table in `database.db`.

## Why Shared SQLite?
We are mounting `database.db` into the Airflow container. This allows Airflow to write results directly to the same database FastAPI uses, making it easy to query the processed results later via an API endpoint.
