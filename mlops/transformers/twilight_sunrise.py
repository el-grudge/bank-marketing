import mlflow.pyfunc
from mlflow import MlflowClient
from sklearn.metrics import accuracy_score

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer


client = MlflowClient()


@transformer
def transform(data, *args, **kwargs):
    model_name = 'bank_marketing'
    stage = 'production'
    filter_string = f"name = '{model_name}' and tag.stage = '{stage}'"
    mlmodel = client.search_model_versions(filter_string)
    # promote_model('production', 'staging', 1, True)
    model_uri = mlmodel[0].source
    model = mlflow.pyfunc.load_model(model_uri)
    X, y = data
    y_pred = model.predict(X)
    accuracy = accuracy_score(y, y_pred)
    metrics = {'accuracy': accuracy}
    print(accuracy)
    return metrics
