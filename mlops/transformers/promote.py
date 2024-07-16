# from mlops.utils.logging import transition_to_staging, transition_to_production
from mlops.utils.logging import promote_model

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer


@transformer
def transform(*args, **kwargs):
    promote_model('staging', 'registered', 3)
    promote_model('production', 'staging', 1, True)