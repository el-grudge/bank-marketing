import pandas as pd
from mlops.utils.data_preparation.prepare_data import drop_target
from mlops.utils.data_preparation.transform_data import transform_data


if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer


@transformer
def transform(data, *args, **kwargs):    
    key = data['name']

    X, y = drop_target(pd.DataFrame(data['data']))

    # transform data 
    X = transform_data(X)

    return X, y, key