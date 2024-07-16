import datetime
import time
import logging 
import pandas as pd
import psycopg2 as psycopg
import joblib
import calendar

import mlflow.pyfunc
from mlflow import MlflowClient

from evidently.report import Report
from evidently import ColumnMapping
from evidently.metrics import ColumnDriftMetric, DatasetDriftMetric, DatasetMissingValuesMetric

from mlops.utils.data_preparation.prepare_data import prepare_data, drop_target
from mlops.utils.data_preparation.transform_data import transform_data
from mlops.utils.data_preparation.encoders import vectorize_features

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

SEND_TIMEOUT = 10

create_table_statement = """
drop table if exists grafana.evidently_metrics;
create table grafana.evidently_metrics(
	month integer,
	prediction_drift float,
	num_drifted_columns integer,
	share_missing_values float
)
"""

def download_artifact(run_id, path):
	artifact_path = mlflow.artifacts.download_artifacts(run_id=run_id,artifact_path=path)
	return pd.read_csv(artifact_path)

# mlflow search + download setup
client = MlflowClient()
model_name = 'bank_marketing'
stage = 'production'
filter_string = f"name = '{model_name}' and tag.stage = '{stage}'"
mlmodel = client.search_model_versions(filter_string)

fileinfo = mlflow.artifacts.list_artifacts(run_id=mlmodel[0].run_id,artifact_path='data')
reference_features = download_artifact(mlmodel[0].run_id,fileinfo[0].path) # validation data
# reference_features = download_artifact(mlmodel[0].run_id,fileinfo[1].path) # validation data
reference_preds = download_artifact(mlmodel[0].run_id,fileinfo[2].path)
reference_data = pd.concat([reference_features, reference_preds], axis=1)

model_uri = mlmodel[0].source
model = mlflow.pyfunc.load_model(model_uri)

with open('mlflow/artifacts/preprocessor.b', 'rb') as f_in: # load production_model
	dv = joblib.load(f_in)

with open('mlflow/artifacts/production_model.bin', 'rb') as f_in: # load production_model
	model = joblib.load(f_in)

raw_data = pd.read_csv('mlops/data/test/dataset.csv') # test data
raw_data = prepare_data(raw_data)
raw_data, y = drop_target(raw_data)

num_features = ['age', 'balance', 'day_of_week', 'campaign', 'pdays', 'previous']
cat_features = ['job', 'housing', 'contact', 'month', 'poutcome']

column_mapping = ColumnMapping(
    prediction='prediction',
    numerical_features=num_features,
    categorical_features=cat_features,
    target=None
)

report = Report(metrics = [
    ColumnDriftMetric(column_name='prediction'),
    DatasetDriftMetric(),
    DatasetMissingValuesMetric()
])

def prep_db():
    conn = psycopg.connect(
        dbname='app_db',
        user='root',
        password='root',
        host='postgresdb',
    )
    conn.autocommit = True
    return conn.cursor()


@custom
def transform_custom(*args, **kwargs):
    cur = prep_db()

    # Execute a query
    cur.execute("SELECT 1 FROM pg_database WHERE datname='app_db'")

    res = cur.fetchall()

    if len(res) == 0:
        cur.execute("create database app_db;")

    cur.execute(create_table_statement)

    # Create a dictionary with month numerals as keys and 3-letter abbreviations as values
    months_dict = {i: calendar.month_abbr[i] for i in range(1, 13)}

    # Loop over the dictionary
    for month_num, month_abbr in months_dict.items():
        current_data = raw_data[raw_data.month == month_abbr.lower()]
        if not current_data.empty:
            X = vectorize_features(dv, transform_data(current_data))
    
            current_data['prediction'] = model.predict(X)
            
            report.run(reference_data = reference_data, current_data = current_data, column_mapping=column_mapping)

            result = report.as_dict()

            prediction_drift = result['metrics'][0]['result']['drift_score']
            num_drifted_columns = result['metrics'][1]['result']['number_of_drifted_columns']
            share_missing_values = result['metrics'][2]['result']['current']['share_of_missing_values']

            cur.execute(
                "insert into grafana.evidently_metrics(month, prediction_drift, num_drifted_columns, share_missing_values) values (%s, %s, %s, %s)",
                (month_num, prediction_drift, num_drifted_columns, share_missing_values)
            )
