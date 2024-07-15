import os
from mlops.utils.logging import register_model


if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data(data, *args, **kwargs):
     run_id, _, _ = data

     accuracy_score = 0.7
     
     register_model(run_id, accuracy_score)
