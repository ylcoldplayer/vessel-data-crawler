def percent_to_decimal(percent_string):
    decimal_value = float(percent_string.strip('%'))
    decimal_value /= 100
    return decimal_value