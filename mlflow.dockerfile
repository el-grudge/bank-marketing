FROM ghcr.io/mlflow/mlflow

# Install PostgreSQL client tools and development headers
RUN apt-get update && apt-get install -y libpq-dev gcc postgresql-client

# Install MLflow and psycopg2
RUN pip install mlflow==2.13.0 psycopg2==2.9.9

