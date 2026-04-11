from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

geolocator = Nominatim(user_agent="satellitevision-pro")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

def get_coordinates(city, country=None):
    try:
        query = f"{city}, {country}" if country else city
        location = geocode(query)

        if location is None:
            return None, None

        return location.latitude, location.longitude

    except Exception as e:
        return None, None