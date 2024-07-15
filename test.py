#!/usr/bin/env python
# coding: utf-8

import requests


url = 'http://localhost:9696/predict'


customer_id = 'xyz-123'
customer = {
    'age': '30',
    'job': 'admin.',
    'balance': '2443',
    'housing': 'yes',
    'contact': 'NaN',
    'day_of_week': '5',
    'month': 'may',
    'campaign': '1',
    'pdays': '-1',
    'previous': '0',
    'poutcome': 'NaN',
}


response = requests.post(url, json=customer).json()
print(response)