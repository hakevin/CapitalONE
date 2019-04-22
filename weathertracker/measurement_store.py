from .measurement import Measurement
from werkzeug.exceptions import abort
from weathertracker.utils.conversion import (
    convert_to_datetime,
    DatetimeConversionException,
)

measurements = []

def add_measurement(measurement):
    """ add the measurement to the list,
    """
    measurements.append(measurement)
    return measurement

def get_measurement(date):
    """get the right measurement for the selected timestamp
    """
    for measurement in measurements:
        try:
            timestamp = convert_to_datetime(measurement.timestamp)
            if timestamp == date:
                return measurement
        except DatetimeConversionException:
            return abort(400)
    return abort(404)

def query_measurements(start_date, end_date):
    """get a list of measurements between start_date and end_date
    """
    selected_measurements = []
    for measurement in measurements:
        try:
            timestamp = convert_to_datetime(measurement.timestamp)
            if start_date <= timestamp < end_date:
                selected_measurements.append(measurement)
        except DatetimeConversionException:
            return abort(400)
    return selected_measurements
            
