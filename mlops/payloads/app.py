import streamlit as st
import requests

st.title("Customer Prediction Dashboard")

# Define the input fields for the customer dictionary
age = st.text_input("Age", value="30")
job = st.text_input("Job", value="admin.")
balance = st.text_input("Balance", value="2443")
housing = st.text_input("Housing", value="yes")
contact = st.text_input("Contact", value="NaN")
day_of_week = st.text_input("Day of Week", value="5")
month = st.text_input("Month", value="may")
campaign = st.text_input("Campaign", value="1")
pdays = st.text_input("Pdays", value="-1")
previous = st.text_input("Previous", value="0")
poutcome = st.text_input("Poutcome", value="NaN")

# URL of the Flask API endpoint
url = 'http://localhost:9696/predict'

# Create a button to send the POST request
if st.button("Predict"):
    customer = {
        'age': age,
        'job': job,
        'balance': balance,
        'housing': housing,
        'contact': contact,
        'day_of_week': day_of_week,
        'month': month,
        'campaign': campaign,
        'pdays': pdays,
        'previous': previous,
        'poutcome': poutcome,
    }
    
    # Send the POST request
    response = requests.post(url, json=customer).json()
    
    # Display the response
    st.write("Response:", response)
