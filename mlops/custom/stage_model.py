from mlops.utils.logging import find_model_in_stage, transition_stage, transition_models_to_staging


if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom


@custom
def transform_custom(model_data, *args, **kwargs):
    model_name, model, dv = model_data
    transition_models_to_staging()

    return model_name, model, dv
