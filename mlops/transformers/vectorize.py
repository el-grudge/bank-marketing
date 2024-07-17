import pickle

from mlops.utils.data_preparation.encoders import vectorize_features

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer


@transformer
def transform(*args, **kwargs):
    with open('mlops/data/test/test.pkl', 'rb') as test, open('mlflow/artifacts/preprocessor.b', 'rb') as val:
        X, y = pickle.load(test)
        dv = pickle.load(val)

    # Process everything as sparse regardless of setting
    X = vectorize_features(dv, X)

    return X, y
