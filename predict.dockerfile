FROM python:3.10-slim-bullseye

WORKDIR /app

RUN mkdir -p mlflow/artifacts/ \
&& chown -R root:root mlflow/artifacts/ \
    && chmod 755 mlflow/artifacts/
       
COPY [ "mlflow/artifacts/production_model.bin", "./mlflow/artifacts/" ]

COPY [ "requirements.txt", "./" ]

RUN pip install --no-cache-dir -r requirements.txt

COPY [ "predict.py", "./" ]

EXPOSE 9696

ENTRYPOINT [ "gunicorn", "--bind=0.0.0.0:9696", "predict:app" ]