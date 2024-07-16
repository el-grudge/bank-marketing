# LOAD MODELS
if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom


@custom
def models(*args, **kwargs):
    model_names = [
#        'sklearn.ensemble.RandomForestClassifier', 
#        'xgboost.XGBClassifier', 
#        #'lightgbm.LGBMClassifier', 
        'sklearn.linear_model.LogisticRegression', 
#        'sklearn.svm.SVC', 
        # 'sklearn.neural_network.MLPClassifier'
        ]
    metadata = [
        dict(block_uuid=model_name.split('.')[-1]) for model_name in model_names
    ]

    return model_names, metadata