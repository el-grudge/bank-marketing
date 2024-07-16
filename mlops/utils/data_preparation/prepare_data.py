import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


def split_data(df):
    # split the data into train/val/test with 80%/20%
    return list(train_test_split(df, test_size=np.round(len(df)*.2).astype(int), random_state=42))
    

def drop_target(df):
    y = df.y
    del df['y']

    X = df
    return X, y


def prepare_data(df):
    # convert target var to numerical
    df.y = df.y.map({'yes':1,'no':0})

    # fill na
    df.fillna('unknown', inplace=True)

    # drop duration
    df.drop('duration', axis=1, inplace=True)

    return df