import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


def split_data(df):
    # split the data into train/val/test with 80%/20%
    X_train, X_test = train_test_split(df, test_size=np.round(len(df)*.2).astype(int), random_state=42)
    
    y_train = X_train.y
    y_test = X_test.y

    del X_train['y']
    del X_test['y']

    return X_train, X_test, y_train, y_test


def prepare_data(df):
    # convert target var to numerical
    df.y = df.y.map({'yes':1,'no':0})

    # fill na
    df.fillna('unknown', inplace=True)

    # drop duration
    df.drop('duration', axis=1, inplace=True)

    return split_data(df)