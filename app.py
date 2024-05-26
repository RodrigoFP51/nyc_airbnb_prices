import pandas as pd
from numpy import exp
import streamlit as st
import joblib
import os
    
model = joblib.load(open('models/best_lgbm.pkl','rb'))

data = pd.read_csv('https://raw.githubusercontent.com/RodrigoFP51/nyc_ayrbnb_prices/main/Data/airbnb_imputed.csv')
neigh_groups = data['neighbourhood_group'].unique()
room_type = data['room_type'].unique()
neighbourhood = data['neighbourhood'].unique()

# model.feature_names_in_

st.markdown(
"""
<style>
button {
    height: 30px;
    border: 1px solid black;
}
</style>
""",
    unsafe_allow_html=True,
)

st.title('Predict Airbnb Rent Cost')
col1, col2 = st.columns([1,1])

with col1:
    
    min_nights = st.number_input(
        "Minimum Nights", step=1
    )
    
    num_reviews = st.number_input(
        "Number of Reviews", step=1
    )
    
    reviews_per_month = st.number_input(
        "Reviews per Month", step=1
    )
    
    calculated_host_listings_count = st.number_input(
        "Listing Count", step=1
    )
    
    availability_365 = st.number_input(
        "Availability", step=1
    )
    
with col2:
    description = st.text_input("Description")
    
    neighbourhood_group = st.selectbox(
        "Neighbourhood Group",
        options=neigh_groups
    )

    neighbourhood = st.selectbox(
        "Neighbourhood",
        options=neighbourhood
    )
    
    room_type = st.selectbox(
        "Room Type",
        options=room_type
    )
    
    last_review = st.date_input(
        "Last Review"
    )
    
st.write("\n\n")
if st.button("Predict Rent"):

    client_data = pd.DataFrame({
        "minimum_nights": [min_nights],
        "number_of_reviews": [num_reviews],
        "reviews_per_month": [reviews_per_month],
        "calculated_host_listings_count": [calculated_host_listings_count],
        "availability_365": [availability_365], 
        "name": [description],
        "neighbourhood_group": [neighbourhood_group],
        "neighbourhood": [neighbourhood],
        "room_type": [room_type],
        "last_review": [last_review]
    })

    st.dataframe(client_data)

    pred_value = model.predict(client_data)
    pred_value = exp(pred_value)
    st.markdown(f"## Valor do aluguel previsto: US$ {round(float(pred_value), 2)}")
