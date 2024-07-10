import os
import pickle
from typing import Dict, Optional, Tuple, Union

import mlflow
import mlflow.pyfunc
from mlflow import MlflowClient
from mlflow.sklearn import log_model as log_model_sklearn
from mlflow.xgboost import log_model as log_model_xgboost
from mlflow.entities import ViewType
import xgboost as xgb
from sklearn.base import BaseEstimator
from sklearn.feature_extraction import DictVectorizer


# setup experiment
DEFAULT_DEVELOPER = os.getenv('EXPERIMENTS_DEVELOPER', 'mager')
DEFAULT_EXPERIMENT_NAME = 'bank-marketing-mage'
DEFAULT_TRACKING_URI = os.getenv('MLFLOW_TRACKING_URI', "http://mlflow:5000")


def setup_experiment(experiment_name, tracking_uri):
    mlflow.set_tracking_uri(tracking_uri or DEFAULT_TRACKING_URI)
    experiment_name = experiment_name or DEFAULT_EXPERIMENT_NAME

    client = MlflowClient()
    experiment = client.get_experiment_by_name(experiment_name)

    if experiment:
        experiment_id = experiment.experiment_id
    else:
        experiment_id = client.create_experiment(experiment_name)
    
    mlflow.set_experiment(experiment_name)

    return client, experiment_id


def track_experiment(
    model: Optional[Union[BaseEstimator, xgb.Booster]] = None,
    preprocessor: Optional[DictVectorizer] = None,
    block_uuid: Optional[str] = None,
    partition: Optional[str] = None,
    pipeline_uuid: Optional[str] = None,
    run_name: Optional[str] = None,
    hyperparameters: Dict[str, Union[float, int, str]] = {},
    metrics: Dict[str, float] = {},
    **kwargs,
):
    experiment_name = DEFAULT_EXPERIMENT_NAME
    tracking_uri = DEFAULT_TRACKING_URI

    client, experiment_id = setup_experiment(experiment_name, tracking_uri)

    if not run_name:
        run_name = ':'.join(
            [str(s) for s in [pipeline_uuid, partition, block_uuid] if s]
        )

    run = client.create_run(experiment_id, run_name=run_name or None)
    run_id = run.info.run_id

    with mlflow.start_run():

        for key, value in [
            ('developer', DEFAULT_DEVELOPER),
            ('model', model.__class__.__name__),
        ]:
            if value is not None:
                client.set_tag(run_id, key, value)

        for key, value in [
            ('block_uuid', block_uuid),
            ('partition', partition),
            ('pipeline_uuid', pipeline_uuid),
        ]:
            if value is not None:
                client.log_param(run_id, key, value)

        for key, value in hyperparameters.items():
            client.log_param(run_id, key, value)
            print(f'Logged hyperparameter {key}: {value}.')

        for key, value in metrics.items():
            client.log_metric(run_id, key, value)
            print(f'Logged metric {key}: {value}.')

        if model:
            log_model = None

            if isinstance(model, BaseEstimator):
                log_model = log_model_sklearn
            elif isinstance(model, xgb.Booster):
                log_model = log_model_xgboost

            if log_model:
                opts = dict(artifact_path='models', input_example=None)

                log_model(model, **opts)
                print(f'Logged model {model.__class__.__name__}.')

    return run


def search_experiments(experiment_name, accuracy_score, max_results):
    client = MlflowClient()
    experiment = client.get_experiment_by_name(experiment_name)

    runs = client.search_runs(
        experiment_ids=experiment.experiment_id,
        filter_string=f'metrics.accuracy > {accuracy_score}',
        run_view_type=ViewType.ACTIVE_ONLY,
        max_results=max_results,
        order_by=["metrics.accuracy DESC"]
    )

    return runs
    

def register_model(run_id, model_name):
    model_uri = f"runs:/{run_id}/model"
    mlflow.register_model(model_uri=model_uri, name=model_name)
    print(f"Run ID {run_id} has been registered to model {model_name}")    


def find_model_in_stage(model_name):
    print(model_name)
    client = mlflow.tracking.MlflowClient()

    # Query for the latest version of the model in the staging stage
    latest_version_info = client.search_model_versions(f"name='{model_name}' and tags.stage='Staging'", order_by=["creation_timestamp DESC"], max_results=1)

    if latest_version_info:
        version = latest_version_info[0].version
    else:
        version = 1

    return version


def transition_stage(version, stage, model_name):
    client = MlflowClient()
    client.transition_model_version_stage(
        name=model_name,
        version=version,
        stage=stage,
        archive_existing_versions=False
    )

    # updating model version
    from datetime import datetime

    date = datetime.today().date()
    client.update_model_version(
        name=model_name,
        version=version,
        description=f"The model version {version} was transitioned to {stage} on {date}"
    )


def transition_models_to_staging():
    client = mlflow.tracking.MlflowClient()

    # List all registered models
    registered_models = client.search_registered_models()

    for model in registered_models:
        # Get the latest version for each registered model
        latest_version = client.get_latest_versions(model.name, stages=['None'])
        
        # Update the stage to 'staging'
        client.transition_model_version_stage(
            name=model.name,
            version=latest_version[0].version,
            stage='staging'
        )
        print(f"Model '{model.name}' version {latest_version[0].version} transitioned to 'staging' stage.")    


def transition_to_production(model_name, model_data):
    model, dv = model_data
    client = mlflow.tracking.MlflowClient()
    # List all registered models
    versions = client.search_model_versions(f"name='{model_name}'")
    
    staging_scores = []

    for version in versions:
        run_id = version.run_id
        run = client.get_run(run_id)
        if run:
            # Get the accuracy metric (adjust 'accuracy' as needed)
            accuracy = run.data.metrics.get('accuracy', None)
            
            if accuracy is not None:
                staging_scores.append({'version': version, 'run_id': run_id, 'accuracy_score': accuracy})
            else:
                print(f"Accuracy metric not found for run ID '{run_id}'. Skipping.")
        else:
            print(f"Run with ID '{run_id}' not found. Skipping.")
    
    best_score_entry = max(staging_scores, key=lambda x: x['accuracy_score'])
    
    # Update the stage to 'staging'
    client.transition_model_version_stage(
        name=model_name,
        version=best_score_entry['version'].version,
        stage='production',
        archive_existing_versions=True
    )
    client.set_model_version_tag(
        model_name, 
        key="v", 
        value="1", 
        stage='production'
        )
    print(f"Model '{model_name}' version {best_score_entry['version'].version} transitioned to 'production' stage.")    

    os.system("rm -f mlflow/artifacts/production_model.bin")
    with open("mlflow/artifacts/production_model.bin", "wb") as f_out:
        pickle.dump((model, dv), f_out)

    mlflow.log_artifact(local_path="mlflow/artifacts/production_model.bin", artifact_path="models", run_id=best_score_entry['version'].run_id)
    print(f"Artifact for run {best_score_entry['version'].run_id} has been created.")    


