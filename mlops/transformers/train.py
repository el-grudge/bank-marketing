from mlops.utils.logging import track_experiment
from mlops.utils.models.model_training import load_class, train_model

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer


@transformer
def training(
    model_info,
    training_set,
    *args,
    **kwargs,
): 
    # Specify your transformation logic here
    mlmodel_class = load_class(model_info)
    X_train, X_val, y_train, y_val = training_set['build']

    X_train, X_val, y_train, y_val = X_train[:100], X_val[:100], y_train[:100], y_val[:100]
  
    model, metrics, y_pred, run_id = train_model(
        mlmodel_class(),
        X_train,
        y_train,
        X_val,
        y_val,
        callback=lambda **opts: track_experiment(**{**opts, **kwargs}),
        random_state=42,
    )

    return run_id, model, metrics
    