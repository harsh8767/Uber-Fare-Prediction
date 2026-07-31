"""
Uber Fare Prediction
--------------------
A Streamlit application for estimating Uber taxi fares
using a trained Random Forest Regression model.
"""

# ==========================================================
# Imports
# ==========================================================

from datetime import datetime

import folium
import streamlit as st
from streamlit_folium import st_folium

from utils.geocoder import get_coordinates
from utils.predictor import predict_fare


# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Uber Fare Prediction",
    page_icon="🚖",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==========================================================
# Helper Functions
# ==========================================================

def load_css(file_name):
    """
    Load and apply the custom CSS stylesheet.
    """

    with open(file_name) as css:
        st.markdown(
            f"<style>{css.read()}</style>",
            unsafe_allow_html=True
        )


def format_address(address):
    """
    Format addresses for a cleaner display.
    """

    if not address:
        return ""

    address = address.title()

    replacements = {
        "Jfk": "JFK",
        "Nyc": "NYC",
        "Usa": "USA"
    }

    for old, new in replacements.items():
        address = address.replace(old, new)

    return address


def estimate_trip_time(distance):
    """
    Estimate trip duration assuming an average
    driving speed of 45 km/h.
    """

    average_speed = 45

    minutes = max(
        1,
        round((distance / average_speed) * 60)
    )

    return minutes


# ==========================================================
# Load Custom Styling
# ==========================================================

load_css("assets/styles.css")


# ==========================================================
# Sidebar
# ==========================================================

with st.sidebar:

    st.title("🚖 Uber Fare Predictor")

    st.markdown("---")

    st.markdown("### 🌲 Model")

    st.success("Random Forest Regressor")

    st.markdown("### 📊 Performance")

    st.write("**R² Score:** 0.765")

    st.write("**RMSE:** 1.77")

    st.write("**MAE:** 1.25")

    st.markdown("---")

    st.markdown("### 📦 Dataset")

    st.write("177,026 Uber Trips")

    st.write("11 Engineered Features")

    st.markdown("---")

    st.caption(
        "Built using Streamlit,\nScikit-learn,\nFolium & OpenStreetMap."
    )


# ==========================================================
# Session State Initialization
# ==========================================================

default_values = {

    # Prediction Status
    "prediction_done": False,

    # Geographic Information
    "pickup": None,
    "dropoff": None,

    # User Inputs
    "pickup_address": "",
    "dropoff_address": "",
    "passenger_count": 1,
    "pickup_date": datetime.today().date(),
    "pickup_time": datetime.now().time(),

    # Prediction Results
    "predicted_fare": None,
    "distance": None,
    "trip_duration": None,

    # Prediction History
    "history": []
}

for key, value in default_values.items():

    if key not in st.session_state:

        st.session_state[key] = value


# ==========================================================
# Hero Section
# ==========================================================

st.markdown(
    """
<div class="hero">

<h1>🚖 Uber Fare Prediction</h1>

<p>
Estimate Uber taxi fares using Machine Learning,
Geospatial Analytics, and Interactive Mapping.
</p>


</div>
""",
    unsafe_allow_html=True
)


# ==========================================================
# Layout
# ==========================================================

left_col, right_col = st.columns(
    [1, 1.2],
    gap="large"
)


# ==========================================================
# Left Panel - Trip Details
# ==========================================================

with left_col:

    st.subheader("📍 Trip Details")

    # Pickup Address
    pickup_address = st.text_input(
        "Pickup Address",
        value=st.session_state.pickup_address,
        placeholder="Times Square, New York"
    )

    # Swap Button
    swap_col1, swap_col2, swap_col3 = st.columns([3, 1, 3])

    with swap_col2:

        swap_locations = st.button(
            "⇅",
            help="Swap pickup and dropoff locations",
            use_container_width=True
        )

    # Swap addresses when button is clicked
    if swap_locations:

        pickup_address, dropoff_address = (
            st.session_state.dropoff_address,
            st.session_state.pickup_address
        )

        st.session_state.pickup_address = pickup_address
        st.session_state.dropoff_address = dropoff_address

        st.rerun()

    # Dropoff Address
    dropoff_address = st.text_input(
        "Dropoff Address",
        value=st.session_state.dropoff_address,
        placeholder="JFK Airport"
    )

    st.divider()

    # Passenger Count
    passenger_count = st.number_input(
        "👥 Passenger Count",
        min_value=1,
        max_value=6,
        value=st.session_state.passenger_count,
        step=1
    )

    # Date & Time
    date_col, time_col = st.columns(2)

    with date_col:

        pickup_date = st.date_input(
            "📅 Pickup Date",
            value=st.session_state.pickup_date
        )

    with time_col:

        pickup_time = st.time_input(
            "🕒 Pickup Time",
            value=st.session_state.pickup_time
        )

    st.write("")

    # Predict Button
    predict_button = st.button(
        "🚖 Predict Fare",
        use_container_width=True
    )


# ==========================================================
# Prediction Logic
# ==========================================================

if predict_button:

    # ------------------------------------------------------
    # Validate User Input
    # ------------------------------------------------------

    if not pickup_address.strip() or not dropoff_address.strip():

        st.error(
            "Please enter both pickup and dropoff addresses."
        )

    else:

        with st.spinner(
            "Calculating the best fare estimate..."
        ):

            # ----------------------------------------------
            # Convert addresses into coordinates
            # ----------------------------------------------

            pickup = get_coordinates(
                pickup_address
            )

            dropoff = get_coordinates(
                dropoff_address
            )

            # ----------------------------------------------
            # Validate Coordinates
            # ----------------------------------------------

            if pickup is None or dropoff is None:

                st.error(
                    "Unable to locate one or both addresses."
                )

            else:

                # ------------------------------------------
                # Create Pickup Datetime
                # ------------------------------------------

                pickup_datetime = datetime.combine(
                    pickup_date,
                    pickup_time
                )

                # ------------------------------------------
                # Predict Fare
                # ------------------------------------------

                predicted_fare, distance = predict_fare(
                    pickup[0],
                    pickup[1],
                    dropoff[0],
                    dropoff[1],
                    passenger_count,
                    pickup_datetime
                )

                # ------------------------------------------
                # Estimate Trip Duration
                # ------------------------------------------

                trip_duration = estimate_trip_time(
                    distance
                )

                # ------------------------------------------
                # Store Prediction Results
                # ------------------------------------------

                st.session_state.pickup = pickup
                st.session_state.dropoff = dropoff

                st.session_state.pickup_address = (
                    pickup_address
                )

                st.session_state.dropoff_address = (
                    dropoff_address
                )

                st.session_state.passenger_count = (
                    passenger_count
                )

                st.session_state.pickup_date = (
                    pickup_date
                )

                st.session_state.pickup_time = (
                    pickup_time
                )

                st.session_state.predicted_fare = (
                    predicted_fare
                )

                st.session_state.distance = (
                    distance
                )

                st.session_state.trip_duration = (
                    trip_duration
                )

                st.session_state.prediction_done = True

                # ------------------------------------------
                # Save Prediction History
                # ------------------------------------------

                st.session_state.history.insert(
                    0,
                    {
                        "pickup": format_address(
                            pickup_address
                        ),
                        "dropoff": format_address(
                            dropoff_address
                        ),
                        "fare": predicted_fare,
                        "distance": distance,
                        "duration": trip_duration
                    }
                )

                # Keep only the latest five trips

                st.session_state.history = (
                    st.session_state.history[:5]
                )

                st.success(
                    "Fare prediction completed successfully!"
                )


# ==========================================================
# Right Panel - Interactive Route Map
# ==========================================================

with right_col:

    st.subheader("🗺️ Route Preview")

    # ------------------------------------------------------
    # Display Default Map
    # ------------------------------------------------------

    if not st.session_state.prediction_done:

        route_map = folium.Map(
            location=[40.7128, -74.0060],
            zoom_start=11,
            tiles="CartoDB Positron"
        )

    # ------------------------------------------------------
    # Display Predicted Route
    # ------------------------------------------------------

    else:

        pickup = st.session_state.pickup
        dropoff = st.session_state.dropoff

        # Center map between pickup and destination
        center_lat = (
            pickup[0] + dropoff[0]
        ) / 2

        center_lon = (
            pickup[1] + dropoff[1]
        ) / 2

        route_map = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=12,
            tiles="CartoDB Positron"
        )

        # --------------------------------------------------
        # Pickup Marker
        # --------------------------------------------------

        folium.Marker(
            location=pickup,
            tooltip="Pickup Location",
            popup="Pickup",
            icon=folium.Icon(
                color="green",
                icon="play"
            )
        ).add_to(route_map)

        # --------------------------------------------------
        # Dropoff Marker
        # --------------------------------------------------

        folium.Marker(
            location=dropoff,
            tooltip="Destination",
            popup="Dropoff",
            icon=folium.Icon(
                color="red",
                icon="flag"
            )
        ).add_to(route_map)

        # --------------------------------------------------
        # Route Line
        # --------------------------------------------------

        folium.PolyLine(
            locations=[
                pickup,
                dropoff
            ],
            color="#1E88E5",
            weight=7,
            opacity=0.8
        ).add_to(route_map)

        # --------------------------------------------------
        # Automatically Fit Both Locations
        # --------------------------------------------------

        route_map.fit_bounds(
            [
                pickup,
                dropoff
            ]
        )

    # ------------------------------------------------------
    # Render Interactive Map
    # ------------------------------------------------------

    st_folium(
        route_map,
        width=700,
        height=550
    )


# ==========================================================
# Prediction Results
# ==========================================================

if st.session_state.prediction_done:

    st.markdown("---")

    st.subheader("📊 Prediction Results")

    card1, card2, card3 = st.columns(3)

    # ------------------------------------------------------
    # Estimated Fare
    # ------------------------------------------------------

    with card1:

        st.markdown(
            f"""
<div class="metric-card">

<h3>💰 Estimated Fare</h3>

<h1>${st.session_state.predicted_fare:.2f}</h1>

</div>
""",
            unsafe_allow_html=True
        )

    # ------------------------------------------------------
    # Distance
    # ------------------------------------------------------

    with card2:

        st.markdown(
            f"""
<div class="metric-card">

<h3>📏 Distance</h3>

<h1>{st.session_state.distance:.2f} km</h1>

</div>
""",
            unsafe_allow_html=True
        )

    # ------------------------------------------------------
    # Trip Duration
    # ------------------------------------------------------

    with card3:

        st.markdown(
            f"""
<div class="metric-card">

<h3>⏱ Estimated Time</h3>

<h1>{st.session_state.trip_duration} min</h1>

</div>
""",
            unsafe_allow_html=True
        )

    st.markdown("---")

    # ======================================================
    # Trip Summary
    # ======================================================

    st.subheader("📋 Trip Summary")

    summary1, summary2 = st.columns(2)

    with summary1:

        st.markdown(
            f"""
<div class="history-card">

**📍 Pickup**

{format_address(st.session_state.pickup_address)}

<br>

**👥 Passengers**

{st.session_state.passenger_count}

<br>

**📅 Date**

{st.session_state.pickup_date.strftime('%d %B %Y')}

</div>
""",
            unsafe_allow_html=True
        )

    with summary2:

        st.markdown(
            f"""
<div class="history-card">

**🏁 Dropoff**

{format_address(st.session_state.dropoff_address)}

<br>

**📏 Distance**

{st.session_state.distance:.2f} km

<br>

**🕒 Time**

{st.session_state.pickup_time.strftime('%I:%M %p')}

</div>
""",
            unsafe_allow_html=True
        )

    st.markdown("---")

    # ======================================================
    # Prediction History
    # ======================================================

    st.subheader("🕒 Recent Predictions")

    if st.session_state.history:

        for trip in st.session_state.history:

            st.markdown(
                f"""
<div class="summary">

**{trip["pickup"]}**

➡️

**{trip["dropoff"]}**

<br>

💰 **${trip["fare"]:.2f}**

&nbsp;&nbsp;&nbsp;&nbsp;

📏 **{trip["distance"]:.2f} km**

&nbsp;&nbsp;&nbsp;&nbsp;

⏱ **{trip["duration"]} min**

</div>
""",
                unsafe_allow_html=True
            )

    st.markdown("---")

    # ======================================================
    # About Project
    # ======================================================

    with st.expander("ℹ️ About This Project"):

        st.markdown(
            """
This application predicts Uber taxi fares using a **Random Forest Regression** model trained on more than **177,000 Uber trips**.

### Prediction Pipeline

- 📍 Address Geocoding using OpenStreetMap Nominatim
- 📏 Haversine Distance Calculation
- 📅 Date & Time Feature Engineering
- 🌲 Random Forest Regression
- 🗺️ Interactive Route Visualization using Folium

This project demonstrates the integration of **Machine Learning**, **Geospatial Analytics**, and **Interactive Web Applications** using Streamlit.
"""
        )

    st.markdown("---")

    st.caption(
        "🚖 Built with Streamlit • Scikit-learn • Folium • OpenStreetMap"
    )

