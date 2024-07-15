import os
import pickle
from typing import Dict, Optional, Tuple, Union

import mlflow
import mlflow.pyfunc
from mlflow import MlflowClient
from mlflow.sklearn import log_model as log_model_sklearn
from mlflow.xgboost import log_model as log_model_xgboost
from mlflow.sklearn import save_model as save_model_sklearn
from mlflow.xgboost import save_model as save_model_xgboost
from mlflow.entities import ViewType
import xgboost as xgb
from sklearn.base import BaseEstimator


# setup experiment
DEFAULT_DEVELOPER = os.getenv('EXPERIMENTS_DEVELOPER', 'mager')
DEFAULT_EXPERIMENT_NAME = 'bank-marketing-mage'
DEFAULT_TRACKING_URI = os.getenv('MLFLOW_TRACKING_URI', "http://mlflow:5000")
model_name = 'bank_marketing'

client = MlflowClient()


def setup_experiment(experiment_name, tracking_uri):
    mlflow.set_tracking_uri(tracking_uri or DEFAULT_TRACKING_URI)
    experiment_name = experiment_name or DEFAULT_EXPERIMENT_NAME

    experiment = client.get_experiment_by_name(experiment_name)

    if experiment:
        experiment_id = experiment.experiment_id
    else:
        experiment_id = client.create_experiment(experiment_name)
    
    mlflow.set_experiment(experiment_name)

    return client, experiment_id


def track_experiment(
    model: Optional[Union[BaseEstimator, xgb.Booster]] = None,
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

    with mlflow.start_run(run_name=run_name, nested=True):

        filter_string = f"name = '{experiment_name}'"
        experiment_id = client.search_experiments(filter_string=filter_string)[0].experiment_id[0]
        run_id = client.search_runs(experiment_id)[0].info.run_id    
        
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
                # log_model = save_model_sklearn
            elif isinstance(model, xgb.Booster):
                log_model = log_model_xgboost
                # log_model = save_model_xgboost

            if log_model:
                opts = dict(artifact_path='model', input_example=None)
                # opts = dict(f'models/{run_id}', input_example=None)

                model_info = log_model(model, **opts)
                print(model_info.model_uri)
                # model_info = log_model(model, f'models/{run_id}')
                print(f'Logged model {model.__class__.__name__} at {model_info.model_uri}. Model uuid is {model_info.model_uuid}, and run_id is {model_info.run_id}')

    return run_id
    
    
def register_model(run_id, accuracy_score=0.5, model_name=model_name):
    run_score = client.get_metric_history(run_id, 'accuracy')[0].value
    
    if run_score >= accuracy_score:
        model_uri = f"runs:/{run_id}/model"
        mlflow.register_model(model_uri=model_uri, name=model_name, tags={'stage': 'registered'})


def get_model_by_run_id(model_uri, artifact_path="model"):
    # Load the model using the model URI
    model = mlflow.pyfunc.load_model(model_uri)
    
    return model


def get_top_n(mlmodels, n=3, asc=True):
    staging_scores = []

    for mlmodel in mlmodels:
        run_id = mlmodel.run_id
        run = client.get_run(run_id)
        if run:
            # Get the accuracy metric (adjust 'accuracy' as needed)
            accuracy = run.data.metrics.get('accuracy', None)
            
            if accuracy is not None:
                staging_scores.append({'mlmodel': mlmodel, 'run_id': run_id, 'accuracy_score': accuracy})
            else:
                print(f"Accuracy metric not found for run ID '{run_id}'. Skipping.")
        else:
            print(f"Run with ID '{run_id}' not found. Skipping.")

    return sorted(staging_scores, key=lambda mv: mv['accuracy_score'], reverse=asc)[:n]


def promote_model(new_stage, current_stage=None, n=3, log_artifacts=False, model_name=model_name):
    filter_string = f"name = '{model_name}' and tag.stage != '{new_stage}'"
    mlmodels = client.search_model_versions(filter_string)

    top_n = get_top_n(mlmodels, n, True)

    for model in top_n:
        model['mlmodel'].tags['stage'] = ''
        print(model['mlmodel'].tags) 
        # client.delete_tag(model['mlmodel'], "stage")
        # Update the stage to 'staging'
        client.transition_model_version_stage(
            name=model['mlmodel'].name,
            version=model['mlmodel'].version,
            stage=new_stage,
            archive_existing_versions=True
        )
        client.set_model_version_tag(
            name=model['mlmodel'].name,
            version=model['mlmodel'].version,
            key='stage', 
            value=new_stage
            )
        print(f"Model '{model['mlmodel'].name}' version {model['mlmodel'].version} transitioned to '{new_stage}' stage.")

        if log_artifacts:
            model = get_model_by_run_id(model['mlmodel'].source)

        with open('mlflow/artifacts/production_model.bin', 'wb') as f_out:
            pickle.dump(model, f_out)
