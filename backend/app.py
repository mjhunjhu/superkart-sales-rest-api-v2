
# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
rental_price_predictor_api = Flask("Super Kart Sales Predictor")

# Load the trained machine learning model
model = joblib.load("deployment_files/superKart_prediction_model_v1_0.joblib")

# Define a route for the home page (GET request)
@rental_price_predictor_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the superkart sales Prediction API!"

# Define an endpoint for single property prediction (POST request)
@rental_price_predictor_api.post('/v1/sales')
def predict_rental_price():
    """
    This function handles POST requests to the '/v1/sales' endpoint.
    It expects a JSON payload containing property details and returns
    the predicted rental price as a JSON response.
    """
    # Get the JSON data from the request body
    property_data = request.get_json()

    # Extract relevant features from the JSON data
    sample = {
        'Product_Type': property_data['Product_Type'],
        'Store_Id': property_data['Store_Id'],
        'Store_Size': property_data['Store_Size'],
        'Store_Location_City_Type': property_data['Store_Location_City_Type'],
        'Store_Type': property_data['Store_Type'],
        'Product_Weight': property_data['Product_Weight'],
        'Product_Allocated_Area': property_data['Product_Allocated_Area'],
        'Product_MRP': property_data['Product_MRP']
    }

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    # Make prediction (get log_price)
    predicted_total_sale = model.predict(input_data)[0]

    # Calculate actual price
    predicted_sale = np.exp(predicted_total_sale)

    # Convert predicted_price to Python float
    predicted_sale = round(float(predicted_sale), 2)
    # The conversion above is needed as we convert the model prediction (log price) to actual price using np.exp, which returns predictions as NumPy float32 values.
    # When we send this value directly within a JSON response, Flask's jsonify function encounters a datatype error

    # Return the actual price
    return jsonify({'Predicted Sale (in dollars)': predicted_sale})


# Define an endpoint for batch prediction (POST request)
@rental_price_predictor_api.post('/v1/sales')
def predict_rental_price_batch():
    """
    This function handles POST requests to the '/v1/sales' endpoint.
    It expects a CSV file containing property details for multiple properties
    and returns the predicted rental prices as a dictionary in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for all properties in the DataFrame (get log_prices)
    predicted_total_sale = model.predict(input_data).tolist()

    # Calculate actual prices
    predicted_sale = [round(float(np.exp(log_price)), 2) for log_price in predicted_total_sale]

    # Create a dictionary of predictions with property IDs as keys
    property_ids = input_data['id'].tolist()  # Assuming 'id' is the property ID column
    output_dict = dict(zip(property_ids, predicted_sale))  # Use actual prices

    # Return the predictions dictionary as a JSON response
    return output_dict

# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    rental_price_predictor_api.run(debug=True)
