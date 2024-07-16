import shutil
from datetime import datetime

from mlops.utils.data_preparation.prepare_data import ingest_data, prepare_data, cleanup

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader


@data_loader
def load_data(*args, **kwargs):
    folder = 'mlops/data/test'
    filename = 'dataset.csv'
    source = f'{folder}/{filename}'

    df = ingest_data(source)
    cleanup(folder, filename)

    return dict(name='test', data=prepare_data(df))
