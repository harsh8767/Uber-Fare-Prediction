"""
Utility functions for geographical distance calculations.
"""

from math import radians, sin, cos, sqrt, atan2


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two locations
    using the Haversine formula.

    Parameters
    ----------
    lat1, lon1 : float
        Pickup latitude and longitude

    lat2, lon2 : float
        Dropoff latitude and longitude

    Returns
    -------
    float
        Distance in kilometers.
    """

    earth_radius = 6371  # Radius of Earth (km)

    lat1, lon1, lat2, lon2 = map(
        radians,
        [lat1, lon1, lat2, lon2]
    )

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1)
        * cos(lat2)
        * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return earth_radius * c