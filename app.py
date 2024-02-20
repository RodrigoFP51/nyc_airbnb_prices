from flask import Flask, jsonify, request
import pandas as pd 
import joblib

def prep_data(data):
    data = data.drop(['id','host_id','host_name'],axis=1)
    data['price'] = data['price'].astype("float64")
    
    for col in data.select_dtypes(include='object').columns[1:]:
        data[col] = data[col].astype("category")
    
    data['last_review'] = pd.to_datetime(data['last_review'])
    
    data['year'] = data.last_review.dt.year
    data['month'] = data.last_review.dt.month
    del data['last_review']
    
    return data

app = Flask(__name__)

@app.route('/', methoods=['POST'])

model = joblib.load('models/best_lgbm.pkl')
data = pd.read_csv('Data/airbnb_imputed.csv')
data = prep_data(data)

model.predict(data.drop(['price'],axis=1).sample(20))


