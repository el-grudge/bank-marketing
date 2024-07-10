from typing import Tuple
from pandas import DataFrame, Series
from sklearn.feature_extraction import DictVectorizer

from mlops.utils.data_preparation.encoders import vectorize_features

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export(data: Tuple[DataFrame, DataFrame, Series, Series], *args, **kwargs):
    X_train, X_val, y_train, y_val = data
    
    # Process everything as sparse regardless of setting
    dv = DictVectorizer()
    dv.fit(X_train)

    X_train, X_val = vectorize_features(dv, X_train),  vectorize_features(dv, X_val)
    
    return X_train, X_val, y_train, y_val, dv