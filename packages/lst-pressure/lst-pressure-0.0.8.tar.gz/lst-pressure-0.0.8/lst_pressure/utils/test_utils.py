import pytest
from datetime import date, datetime
from .normalize_date import normalize_date, normalize_iso_datetime
from .normalize_coordinates import normalize_coordinates
from .sun import calc_sun
from .time_conversions import lst_to_solar, solar_to_lst


test_data = [
    {
        "time_conversion": {
            "solar": "2022-06-17 05:03:23.350528+00:00",
            "base_solar_date": "20220617",
            "lst": 2.2676658757373573,
            "lat": "-30:42:39.8",
            "long": "21:26:38.0"
        },
        "yyyymmdd": ["20220617", date(2022, 6, 17)],
        "sunrise_sunset": {
            "dawn": "2022-06-17 05:03:23.350528+00:00",
            "sunrise": "2022-06-17 05:30:29.628263+00:00",
            "noon": "2022-06-17 10:35:03+00:00",
            "sunset": "2022-06-17 15:39:46.364401+00:00",
            "dusk": "2022-06-17 16:06:52.665164+00:00",
        },
        "lat": ["-30:42:39.8", -30.711055555555554],
        "long": ["21:26:38.0", 21.44388888888889],
    }
]

@pytest.mark.parametrize("test", test_data)
def test_normalize_iso_datetime(test):
    # This probably isn't required but is here for completeness
    pass

@pytest.mark.parametrize("test", test_data)
def test_lst_to_solar(test):
    time_conversion = test.get("time_conversion")
    solar_expected = normalize_iso_datetime(time_conversion.get("solar"))
    base_solar_date = time_conversion.get('base_solar_date')
    lst = time_conversion.get("lst")
    long = time_conversion.get('long')
    lat = time_conversion.get('lat')
    solar = lst_to_solar(lst,  base_solar_date, lat, long)
    assert(solar_expected.strftime("%Y-%m-%d %H:%M") == solar.strftime("%Y-%m-%d %H:%M"))

@pytest.mark.parametrize("test", test_data)
def test_solar_to_lst(test):
    time_conversion = test.get("time_conversion")
    solar = time_conversion.get("solar")
    lst_expected = time_conversion.get("lst")
    long = time_conversion.get('long')
    lat = time_conversion.get('lat')
    lst = solar_to_lst(solar, lat, long)
    assert lst == lst_expected


@pytest.mark.parametrize("test", test_data)
def test_normalize_date(test):
    d = test["yyyymmdd"]
    assert normalize_date(d[0]) == d[1]
    assert normalize_date(d[1]) == d[1]


@pytest.mark.parametrize("test", test_data)
def test_normalize_coordinates(test):
    lat = test["lat"]
    long = test["long"]

    # Conversion of DMS should work
    lat_, long_ = normalize_coordinates(lat[0], long[0])
    assert lat_ == lat[1]
    assert long_ == long[1]

    # Using decimal degrees directly should also work
    lat_, long_ = normalize_coordinates(lat[1], long[1])
    assert lat_ == lat[1]
    assert long_ == long[1]

    # Should not be possible to use both DEC and DMS
    with pytest.raises(ValueError):
        normalize_coordinates(lat[0], long[1])
    with pytest.raises(ValueError):
        normalize_coordinates(lat[1], long[0])


@pytest.mark.parametrize("test", test_data)
def test_calc_sun(test):
    lat = test.get("lat")[0]
    long = test.get("long")[0]
    yyyymmdd = test.get("yyyymmdd")[1]
    sunrise_sunset = test.get("sunrise_sunset")
    expected = {
        key: datetime.fromisoformat(value) for key, value in sunrise_sunset.items()
    }

    result = calc_sun(lat, long, yyyymmdd)
    assert all(result.get(key) == value for key, value in expected.items())
