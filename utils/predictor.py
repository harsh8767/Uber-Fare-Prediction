"""
Prediction utilities for Uber Fare Prediction.
"""

from pathlib import Path
import joblib
import pandas as pd

from utils.distance import haversine_distance

BASE_DIR = Path(__file__).resolve().parent.parent

model = joblib.load(
    BASE_DIR / "models" / "random_forest_model.pkl"
)

model_features = joblib.load(
    BASE_DIR / "models" / "model_features.pkl"
)

def prepare_features(
    pickup_lat,
    pickup_lon,
    dropoff_lat,
    dropoff_lon,
    passenger_count,
    pickup_datetime
):
    """
    Prepare model input features.
    """

    distance = haversine_distance(
        pickup_lat,
        pickup_lon,
        dropoff_lat,
        dropoff_lon
    )

    input_data = {
    "pickup_longitude": pickup_lon,
    "pickup_latitude": pickup_lat,
    "dropoff_longitude": dropoff_lon,
    "dropoff_latitude": dropoff_lat,
    "passenger_count": passenger_count,
    "year": pickup_datetime.year,
    "month": pickup_datetime.month,
    "day": pickup_datetime.day,
    "hour": pickup_datetime.hour,
    "day_of_week": pickup_datetime.weekday(),
    "distance_km": distance
}

    return pd.DataFrame([input_data])[model_features], distance


def predict_fare(
    pickup_lat,
    pickup_lon,
    dropoff_lat,
    dropoff_lon,
    passenger_count,
    pickup_datetime
):
    """
    Predict Uber fare.

    Returns
    -------
    tuple
        (predicted_fare, distance_km)
    """

    features, distance = prepare_features(
        pickup_lat,
        pickup_lon,
        dropoff_lat,
        dropoff_lon,
        passenger_count,
        pickup_datetime
    )

    prediction = model.predict(features)[0]

    return round(prediction, 2), round(distance, 2)

