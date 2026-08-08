
!pip install streamlit -q
import streamlit as st
import pandas as pd
import joblib

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"


st.set_page_config(
    page_title="SuperKart Sales Predictor",
    page_icon="🛒",
    layout="centered"
)

st.title("🛒 SuperKart Sales Prediction")
st.write(
    "Enter the product and store details below to predict "
    "Product Store Sales Total."
)

# ---------------------------------
# Product information
# ---------------------------------
st.subheader("Product Information")

product_id = st.selectbox(
    "Product Category",
    ["FD", "NC", "DR"]
)

product_weight = st.number_input(
    "Product Weight",
    min_value=0.0,
    value=10.0
)

sugar_content = st.selectbox(
    "Product Sugar Content",
    ["Low Sugar", "Regular", "No Sugar"]
)

allocated_area = st.number_input(
    "Product Allocated Area",
    min_value=0.0,
    value=0.05,
    format="%.3f"
)

product_type = st.selectbox(
    "Product Type",
    [
        "Fruits and Vegetables",
        "Snack Foods",
        "Frozen Foods",
        "Dairy",
        "Household",
        "Baking Goods",
        "Canned",
        "Health and Hygiene",
        "Meat",
        "Soft Drinks",
        "Breads",
        "Hard Drinks",
        "Others",
        "Starchy Foods",
        "Breakfast",
        "Seafood"
    ]
)

product_mrp = st.number_input(
    "Product MRP",
    min_value=0.0,
    value=100.0
)

# ---------------------------------
# Store information
# ---------------------------------
st.subheader("Store Information")

store_id = st.selectbox(
    "Store ID",
    ["OUT001", "OUT002", "OUT003", "OUT004"]
)

store_size = st.selectbox(
    "Store Size",
    ["Small", "Medium", "High"]
)

city_type = st.selectbox(
    "Store Location City Type",
    ["Tier 1", "Tier 2", "Tier 3"]
)

store_type = st.selectbox(
    "Store Type",
    [
        "Supermarket Type1",
        "Supermarket Type2",
        "Departmental Store",
        "Food Mart"
    ]
)

store_age = st.number_input(
    "Store Age",
    min_value=0,
    value=10
)

# ---------------------------------
# Prediction
# ---------------------------------
if st.button("Predict Sales"):

    input_data = pd.DataFrame({
        "Product_Id": [product_id],
        "Product_Weight": [product_weight],
        "Product_Sugar_Content": [sugar_content],
        "Product_Allocated_Area": [allocated_area],
        "Product_Type": [product_type],
        "Product_MRP": [product_mrp],
        "Store_Id": [store_id],
        "Store_Size": [store_size],
        "Store_Location_City_Type": [city_type],
        "Store_Type": [store_type],
        "Store_Age": [store_age]
    })

   # Make prediction when the "Predict" button is clicked
if st.button("Predict", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/sales", json=input_data.to_dict(orient='records')[0])  # Send data to Flask API
    if response.status_code == 200:
        prediction = response.json()['Predicted sales (in dollars)']
        st.success(f"Predicted sales (in dollars): {prediction}")
    else:
        st.error("Unable to connect to the prediction API.")

# Section for batch prediction
st.subheader("Batch Prediction")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/sales", files={"file": uploaded_file})  # Send file to Flask API
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")
            st.write(predictions)  # Display the predictions
        else:
            st.error("Unable to connect to the prediction API.")
