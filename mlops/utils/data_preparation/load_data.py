import pandas as pd

def ingest_data(url):
    # load the data
    df = pd.read_csv(url)
    return df