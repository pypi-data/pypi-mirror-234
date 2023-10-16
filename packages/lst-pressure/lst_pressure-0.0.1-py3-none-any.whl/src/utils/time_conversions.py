import ephem
from .normalize_coordinates import normalize_coordinates
from .normalize_date import normalize_iso_datetime
from datetime import datetime, timedelta


def lst_to_solar(target_lst, base_solar_date_yyyymmdd, lat, long):
    lat, long = normalize_coordinates(lat, long)
    observer = ephem.Observer()
    observer.lat = lat
    observer.lon = long

    # Start with a guessed solar time (midnight)
    guessed_date = datetime.strptime(base_solar_date_yyyymmdd, "%Y%m%d")
    delta = timedelta(minutes=1)  # increment by minutes for approximation
    best_difference = float('inf')
    best_date = None

    # Iterate over the 24 hours of the day
    for _ in range(24*60):  # 24 hours * 60 minutes
        observer.date = guessed_date.strftime("%Y-%m-%d %H:%M:%S")
        current_lst = observer.sidereal_time()
        difference = abs(current_lst - target_lst)

        if difference < best_difference:
            best_difference = difference
            best_date = guessed_date

        guessed_date += delta

    return best_date


def solar_to_lst(iso_date, lat, long):
    lat, long = normalize_coordinates(lat, long)
    observer = ephem.Observer()
    observer.date = normalize_iso_datetime(iso_date).strftime("%Y-%m-%d %H:%M:%S")
    observer.lon = long
    lst = observer.sidereal_time()
    return lst