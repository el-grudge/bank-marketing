from mlops.utils.data_preparation.load_data import ingest_data
from mlops.utils.data_preparation.prepare_data import prepare_data


if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader


@data_loader
def load_data(*args, **kwargs):
    url = 'https://archive.ics.uci.edu/static/public/222/data.csv'
    df = ingest_data(url)

    return prepare_data(df)