import os
import shutil
import pickle
from datetime import datetime
from mlops.utils.data_preparation.prepare_data import cleanup

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

@data_exporter
def export(data, *args, **kwargs):
    df, X, y, filename = data

    folder = 'mlops/data/monitor'
    
    cleanup(folder, 'reference.csv')
    df.to_csv(f'{folder}/reference.csv', index=False)
    
    folder = f'mlops/data/{filename}'
    # Save X and y using pickle
    cleanup(folder, f'{filename}.pkl')
    with open(f'{folder}/{filename}.pkl', 'wb') as f_out:
        pickle.dump((X, y), f_out)
