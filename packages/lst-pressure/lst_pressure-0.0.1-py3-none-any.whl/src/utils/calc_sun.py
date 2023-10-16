from astral.sun import sun
from astral import LocationInfo
from .normalize_coordinates import normalize_coordinates
from .normalize_date import normalize_date


def calc_sun(latitude, longitude, yyyymmdd):
    latitude, longitude = normalize_coordinates(latitude, longitude)
    dt = normalize_date(yyyymmdd)
    location = LocationInfo(latitude=latitude, longitude=longitude)
    return sun(location.observer, date=dt)
