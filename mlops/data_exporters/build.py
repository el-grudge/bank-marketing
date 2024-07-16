import os
import shutil
import pickle
from datetime import datetime
from sklearn.feature_extraction import DictVectorizer

from mlops.utils.data_preparation.encoders import vectorize_features

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export(data, *args, **kwargs):
    X, y, filename = data

    folder_path = f'mlops/data/{filename}'

    if os.path.exists(folder_path) and os.listdir(folder_path):
        # Move files to archive folder with datetime suffix
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        destination = f'mlops/data/archive/{filename}/{filename}_{timestamp}.pkl'
        shutil.move(f'{folder_path}/{filename}.pkl', destination)

    # Save X and y using pickle
    with open(f'{folder_path}/{filename}.pkl', 'wb') as f:
        pickle.dump((X, y), f)
