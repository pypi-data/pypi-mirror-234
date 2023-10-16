def normalize_coordinates(lat, long):
    def is_decimal(value):
        """Check if a value is already in decimal format"""
        try:
            float(value)
            return True
        except ValueError:
            return False

    def dms_str_to_dec(dms_str):
        """Convert DMS string to decimal value"""
        negative = dms_str.startswith("-")
        dms_str = dms_str.lstrip("-")
        degrees, minutes, seconds = map(float, dms_str.split(":"))
        decimal = degrees + (minutes / 60) + (seconds / 3600)
        return -decimal if negative else decimal

    if is_decimal(lat) or is_decimal(long):
        if not is_decimal(lat) and is_decimal(long):
            raise ValueError(
                "lat and long must both be in DMS or decimal format, not a mix of the two."
            )
        else:
            return float(lat), float(long)

    return dms_str_to_dec(lat), dms_str_to_dec(long)
