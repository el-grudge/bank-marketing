from mlops.utils.data_preparation.prepare_data import split_data

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer


@transformer
def transform(data, *args, **kwargs):
    # dynamic block
    df = data['data']
    data = []
    metadata = []

    datasets = split_data(df)
    names = ['train','val']

    for dataset, name in zip(datasets, names):
        data.append(dict(name=name, data=dataset))
        metadata.append(dict(block_uuid=name))

    return [
        data,
        metadata, # optional
    ]