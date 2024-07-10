import pandas as pd
from sklearn.feature_extraction import DictVectorizer


def vectorize_features(X_train, X_val):
    dv = DictVectorizer()
    dv.fit(X_train)

    X_train = dv.transform(X_train)
    X_val = dv.transform(X_val)

    return X_train, X_val, dv