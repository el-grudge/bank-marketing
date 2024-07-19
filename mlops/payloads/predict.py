import pickle

from flask import Flask, request, jsonify
import pandas as pd


num = ['age', 'balance', 'day_of_week', 'campaign', 'pdays', 'previous']
cat = ['job', 'housing', 'contact', 'month', 'poutcome']


def cast_dataframe_types(df, num, cat):
    # Cast numeric columns
    for col in num:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Cast categorical columns
    for col in cat:
        df[col] = df[col].astype('category')

    return df


def mapping_pdays(col):
    return col.apply(lambda x:
                    'never' if x == -1 
                    else ('plus 12 months' if x > 365 
                          else ('plus 6 months' if 180 <= x <= 365 
                                else '6 months'
                               )
                         )
                   )


def mapping_previous(col):
    return col.apply(lambda x:
                     'never' if x == 0 
                     else ('more than 5' if x > 5 
                           else 'less than 5'
                           )
                     )


def mapping_campaign(col):
    return col.apply(lambda x: 'once' if x == 1 else 'more than once')


def create_season_column(df):
    seasons = {
        'fall': ['sep','oct','nov'],
        'winter': ['dec','jan','feb'],
        'spring': ['mar','apr','may'],
        'summer': ['jun','jul','aug']
    }

    df['season'] = [season[0] for mon in df['month'] for season in list(seasons.items()) if mon in season[1]]
    return df.drop(['month'], axis=1)


def create_job_categories(df):
    job_category = {
        'cat_1': ['blue-collar','entrepreneur','housemaid'],
        'cat_2': ['retired','student','unemployed'],
        'cat_3': ['technician', 'admin.', 'management', 'services','unknown', 'self-employed']
    }

    df['job_category'] = [category[0] for job in df['job'] for category in list(job_category.items()) if job in category[1]]
    return df.drop(['job'], axis=1)


def transform_contact(col):
    return ['no' if c == 'unknown' else 'yes' for c in col]


def transform_poutcome(col):
    return [o if o in ['success', 'failure'] else 'other' for o in col]


def transform_data(df):
    df = cast_dataframe_types(df, num, cat)
    # mapping pdays based on conditions
    df['pdays'] = mapping_pdays(df['pdays'])

    # mapping previous based on conditions
    df['previous'] = mapping_previous(df['previous']) 

    # mapping campaign based on conditions
    df['campaign'] = mapping_campaign(df['campaign'])

    # create seasons column 
    df = create_season_column(df)

    # create job categories
    df = create_job_categories(df)

    # transfrom contact column
    df['contact'] = transform_contact(df['contact'])

    # transform poutcome
    df['poutcome'] = transform_poutcome(df['poutcome'])
    
    return df.to_dict(orient='records')


def vectorize_features(dv, X):
    return dv.transform(X)


def load_pickle(filename):
    with open(f'{filename}', 'rb') as f_in:
        payload = pickle.load(f_in)
    return payload


dv = load_pickle('/home/src/mlflow/artifacts/preprocessor.b')
model = load_pickle('/home/src/mlflow/artifacts/production_model.bin')

app = Flask('predict-response')

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    data = request.get_json()
    data = pd.DataFrame([data])
    
    # preprocess
    data = transform_data(data)
    X = vectorize_features(dv, data)
    
    # predict
    y_pred = model.predict(X)
    
    return jsonify(y_pred.mean())

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)