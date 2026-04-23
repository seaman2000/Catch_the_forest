from math import radians, sin, cos, atan2, sqrt


def calculate_distance_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    earth_radius = 6371000
    return earth_radius * c


def is_within_radius(
    location_lat: float,
    location_lon: float,
    user_lat: float,
    user_lon: float,
    radius_m: int,
) -> tuple[bool, float]:
    distance = calculate_distance_m(location_lat, location_lon, user_lat, user_lon)
    return distance <= radius_m, distance