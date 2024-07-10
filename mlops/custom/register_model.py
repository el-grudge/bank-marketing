import os
from mlops.utils.logging import search_experiments, register_model

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom


@custom
def transform_custom(model, *args, **kwargs):
    model, dv, _, _ = model
    experiment_name = os.getenv('MLFLOW_EXPERIMENT_NAME', 'bank-marketing-mage')
    runs = search_experiments(experiment_name, 0.7, 5)
    model_name = 'bank_marketing'

    for run in runs:
        register_model(run.info.run_id, model_name)

    return model_name, model, dv