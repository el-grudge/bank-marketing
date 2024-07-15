import subprocess

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


source = '/home/src/mlops/payloads/templates/dockerfile_template.txt'
destination = '/home/src/mlops/payloads/predict.dockerfile'

@data_exporter
def export_data(data, *args, **kwargs):
    with open(source, 'r') as f, open(destination, 'w') as w: 
        contents = f.read()
        w.write(contents)
