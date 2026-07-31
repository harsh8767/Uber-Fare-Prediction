from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="uber_fare_prediction")


def get_coordinates(address):
    """
    Convert an address into latitude and longitude.
    Searches only within New York City.
    """

    try:
        location = geolocator.geocode(
            f"{address}, New York City, New York, USA",
            exactly_one=True,
            timeout=10
        )

        if location:
            return (location.latitude, location.longitude)

        return None

    except Exception:
        return None