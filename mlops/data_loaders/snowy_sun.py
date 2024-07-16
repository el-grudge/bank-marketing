import pickle

from mlops.utils.data_preparation.encoders import vectorize_features

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader


@data_loader
def load_data(*args, **kwargs):
    with open('mlops/data/test/test.pkl', 'rb') as test, open('mlflow/artifacts/preprocessor.b', 'rb') as dv:
        X, y = pickle.load(test)
        dv = pickle.load(dv)

    X = vectorize_features(dv, X)
    
    return X, y
