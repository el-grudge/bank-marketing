import pickle
import pandas as pd

from flask import Flask, request, jsonify


with open('mlflow/artifacts/production_model.bin', 'rb') as f_in:
    model, dv = pickle.load(f_in)

def cast_dataframe_types(df, num, cat):
    # Cast numeric columns
    for col in num:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Cast categorical columns
    for col in cat:
        df[col] = df[col].astype('category')

    return df    

def transform_data(data):
    df = pd.DataFrame([data])
    num = ['age', 'balance', 'day_of_week', 'campaign', 'pdays', 'previous']
    cat = ['job', 'housing', 'contact', 'month', 'poutcome']
    df = cast_dataframe_types(df, num, cat)
    features = num + cat
    df_transformed =  df[features].copy()

    # mapping pdays based on conditions
    df_transformed['pdays'] = df_transformed['pdays'].apply(lambda x: 
                                                            'never' if x == -1 
                                                            else ('plus 12 months' if x > 365 
                                                                  else ('plus 6 months' if 180 <= x <= 365 
                                                                        else '6 months'
                                                                       )
                                                                 )
                                                           )
    
    # mapping previous based on conditions
    df_transformed['previous'] = df_transformed['previous'].apply(lambda x: 
                                                                  'never' if x == 0 
                                                                  else ('more than 5' if x > 5 
                                                                        else 'less than 5'
                                                                       )
                                                                 )
    
    # mapping campaing based on conditions
    df_transformed['campaign'] = df_transformed['campaign'].apply(lambda x: 
                                                                  'once' if x == 1 
                                                                  else 'more than once'
                                                                 )

    # Consolidate categories of categorical features with many categories
    seasons = {
        'fall': ['sep','oct','nov'],
        'winter': ['dec','jan','feb'],
        'spring': ['mar','apr','may'],
        'summer': ['jun','jul','aug']
    }

    df_transformed['season'] = [season[0] for mon in df_transformed['month'] for season in list(seasons.items()) if mon in season[1]]
    
    job_category = {
        'cat_1': ['blue-collar','entrepreneur','housemaid'],
        'cat_2': ['retired','student','unemployed'],
        'cat_3': ['technician', 'admin.', 'management', 'services','unknown', 'self-employed']
    }

    df_transformed['job_category'] = [category[0] for job in df_transformed['job'] for category in list(job_category.items()) if job in category[1]]
    df_transformed = df_transformed.drop(['month','job'], axis=1).copy()
    df_transformed['contact'] = ['no' if contact == 'unknown' else 'yes' for contact in df_transformed['contact']]

    df_transformed['poutcome'] = [outcome if outcome in ['success', 'failure'] else 'other' for outcome in df_transformed['poutcome']]

    return dv.transform(df_transformed.to_dict(orient='records'))


app = Flask('predict-duration')

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    data = request.get_json()
    X_val = transform_data(data)
    y_pred = model.predict(X_val)
    
    return jsonify(y_pred.mean())

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)


