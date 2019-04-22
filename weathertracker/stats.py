from werkzeug.exceptions import abort
from weathertracker.measurement_store import query_measurements
from flask import jsonify
from werkzeug.exceptions import abort

def get_stats(stats, metrics, from_datetime, to_datetime):
    """this function give stats (the samalest, bigger and average value)
       of metrics (temperature, dewPoint, precipitation, ...) between a select begin and end 
       time period
    """
    all_display_stats = []
    query_measurement = query_measurements(from_datetime, to_datetime)
    for m in metrics:
        # create an array with metric values
        metric_val = metric_value(m, query_measurement)
        #if the array is empty return an empty array
        if len(metric_val) == 0:
            return jsonify(all_display_stats)
        #calculate the stats for every stat (min,max average) and add it into our final array
        for s in stats:
            if s == 'min':
                min_stats = min(metric_val)
                my_stat = creat_stat('min', m, min_stats)
                all_display_stats.append(my_stat)
            elif s == 'max':
                max_stats = max(metric_val)
                my_stat = creat_stat('max', m, max_stats)
                all_display_stats.append(my_stat)
            elif s == 'average':
                average_stats = float(sum(metric_val)) / float(len(metric_val))
                average_stats = round(average_stats, 1)
                my_stat = creat_stat('average', m, average_stats)
                all_display_stats.append(my_stat)
            else:
                return abort(400)
    return jsonify(all_display_stats)

def metric_value(metric, query):
    """check if the metric exist and 
       create an array with metric values 
    """
    metric_val = []
    for q in query:
        for qm in q.metrics:
            if metric == qm:
                metric_val.append(q.get_metric(metric))
            else:
                pass
    return metric_val
                

def creat_stat( stats_type, metric, value ):
    """create an element in the format requiered
    """
    display_stats = {}
    display_stats['metric'] = metric
    display_stats['stat'] = stats_type
    display_stats['value'] = value
    return display_stats

