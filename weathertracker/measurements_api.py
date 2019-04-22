from flask import request, jsonify
from flask.views import MethodView
from werkzeug.exceptions import abort
from weathertracker.utils.conversion import (
    convert_to_datetime,
    DatetimeConversionException,
)
from weathertracker.measurement_store import (
    add_measurement,
    get_measurement,
)

from .measurement import Measurement

class MeasurementsAPI(MethodView):

    # features/01-measurements/01-add-measurement.feature
    def post(self):
        """submit a new measurement with a timestamp and metrics
           with a status code of 201 and
           the path of Location header as "/measurements/timestamp"
        """
        json_data = request.get_json(force=True)
        
        #check if timestamp exist
        if not json_data or not 'timestamp' in json_data:
            abort(400)
        
        timestamp = json_data['timestamp']
        metrics = {}
        
        # create the object measurement
        measurement = Measurement( timestamp, metrics )
        
        # add the metrics to our measurement and check if the value are float
        for key in json_data:
            if key == 'timestamp':
                pass
            else:
                try:
                    float(json_data[key])
                    measurement.set_metric(key, json_data[key])
                except ValueError:
                    abort(400)
                    
        measurement = add_measurement(measurement)
        
        #retrun the 201 status code and define the correct location
        response = jsonify(measurement.metrics)
        response.status_code = 201
        response.headers['location'] = '/measurements/' + measurement.timestamp
        return response


    # features/01-measurements/02-get-measurement.feature
    def get(self, timestamp):
        """get a measurement for a specific 'timestamp'
           with a status code of 200
           And a response body with the timestamp and all metrics
        """
        try:
            timestamp = convert_to_datetime(timestamp)
        except DatetimeConversionException:
            return abort(400)
        
        
        measurement = get_measurement(timestamp)
        # add metrics and timestamp in the same list to display them together
        display_measurement = measurement.metrics
        display_measurement['timestamp'] = measurement.timestamp
        
        response = jsonify(display_measurement)
        response.status_code = 200
        response.headers['location'] = '/measurements/' + measurement.timestamp
        return response
        
        
