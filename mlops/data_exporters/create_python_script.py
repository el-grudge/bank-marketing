if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


source_1 = '/home/src/mlops/payloads/templates/python_header.txt'
source_2 = '/home/src/mlops/utils/data_preparation/transform_data.py'
source_3 = '/home/src/mlops/payloads/templates/python_footer.txt'
destination = '/home/src/mlops/payloads/predict.py'

@data_exporter
def export_data(data, *args, **kwargs):
    with open(source_1, 'r') as f_1, open(source_2, 'r') as f_2, open(source_3, 'r') as f_3, open(destination, 'w') as w: 
        contents = f_1.read()
        w.write(contents)
        contents = f_2.read()
        w.write(contents)
        contents = f_3.read()
        w.write(contents)
