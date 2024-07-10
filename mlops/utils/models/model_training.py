import importlib
from sklearn.metrics import accuracy_score
from typing import Callable, Optional


def load_class(full_class_string):
    module_path, class_name = full_class_string.rsplit('.', 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


def train_model(
    model,
    preprocessor,
    X_train,
    y_train,
    X_val,
    y_val,
    callback: Optional[Callable[..., None]] = None,
    **kwargs,
):
    model.fit(X_train, y_train)

    metrics = None
    y_pred = model.predict(X_val)

    accuracy = accuracy_score(y_val, y_pred)
    metrics = {'accuracy': accuracy}

    if callback:
        callback(
            hyperparameters=model.get_params(),
            metrics=metrics,
            model=model,
            preprocessor=preprocessor
        )

    return model, metrics, y_pred