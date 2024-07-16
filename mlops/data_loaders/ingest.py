import shutil
from datetime import datetime

from mlops.utils.data_preparation.load_data import ingest_data
from mlops.utils.data_preparation.prepare_data import prepare_data

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader


@data_loader
def load_data(*args, **kwargs):
    source = 'mlops/data/test/dataset_1.csv'
    df = ingest_data(source)

    # move data/test/*csv to data/archive/test/*{datetime}.csv
    now = datetime.now().strftime('%Y%m%d_%H%M%S')
    destination = f'mlops/data/archive/test/dataset_{now}.csv'

    # Move the file
    shutil.move(source, destination)


    return dict(name='test', data=prepare_data(df))
