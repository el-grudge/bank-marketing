from mlops.utils.logging import transition_to_production

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom


@custom
def transform_custom(model_data, *args, **kwargs):
    model_name, model, dv = model_data
    transition_to_production(model_name, (model, dv))