import pickle
from sklearn.feature_extraction import DictVectorizer

from mlops.utils.data_preparation.encoders import vectorize_features

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader


@data_loader
def load_data(*args, **kwargs):
    with open('mlops/data/train/train.pkl', 'rb') as train, open('mlops/data/val/val.pkl', 'rb') as val:
        X_train, y_train = pickle.load(train)
        X_val, y_val = pickle.load(val)

    # Process everything as sparse regardless of setting
    dv = DictVectorizer()
    dv.fit(X_train)
    
    X_train, X_val = vectorize_features(dv, X_train),  vectorize_features(dv, X_val)

    with open('mlflow/artifacts/preprocessor.b', 'wb') as f_out:
        pickle.dump(dv, f_out)
    
    return X_train, X_val, y_train, y_val
