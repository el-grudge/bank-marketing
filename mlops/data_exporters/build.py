import pickle
from mlops.utils.data_preparation.prepare_data import cleanup

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

@data_exporter
def export(data, *args, **kwargs):
    df, X, y, filename = data

    folder = 'mlops/data/monitor'
    features_filename = f'reference_features_{filename}.csv'
    
    cleanup(folder, features_filename)
    df.to_csv(f'{folder}/{features_filename}', index=False)
    
    # Save X and y using pickle
    folder = f'mlops/data/{filename}'
    cleanup(folder, f'{filename}.pkl')
    with open(f'{folder}/{filename}.pkl', 'wb') as f_out:
        pickle.dump((X, y), f_out)
