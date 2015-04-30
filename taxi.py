#!/usr/bin/env python

import pandas as pd
import numpy as np
from math import radians, sin, cos, atan2, sqrt

def credit_fraction(data):
    credit_data = data[data['payment_type'] == 'CRD']
    return float(len(credit_data.index)) / len(data.index)

def haversine(longitude1, latitude1, longitude2, latitude2):
    R_earth = 3959
    longitude1 = radians(longitude1)
    longitude2 = radians(longitude2)
    latitude1 = radians(latitude1)
    latitude2 = radians(latitude2)
    dlongitude = longitude2 - longitude1
    dlatitude = latitude2 - latitude1
    a = (sin(dlatitude/2))**2 + cos(latitude1) * cos(latitude2) * (sin(dlongitude/2))**2
    c = 2 * atan2( sqrt(a), sqrt(1-a) )
    d = R_earth * c
    return d
if __name__ == '__main__':
    row_count = 10000
    # data = pd.read_csv('trip_data_3.csv', skipinitialspace=True, na_values=[0], nrows=row_count)
    # fare = pd.read_csv('trip_fare_3.csv', skipinitialspace=True, nrows=row_count)
    data = pd.read_csv('trip_data_3.csv', skipinitialspace=True, na_values=[0])
    fare = pd.read_csv('trip_fare_3.csv', skipinitialspace=True)
    print data.columns.values
    print fare.columns.values
    data = pd.merge(data, fare, on=['medallion', 'hack_license', 'vendor_id', 'pickup_datetime'])
    data['pickup_datetime'] = pd.to_datetime(data['pickup_datetime'])
    data['dropoff_datetime'] = pd.to_datetime(data['dropoff_datetime'])
    payments_5 = data[data['total_amount'] < 5]
    print 'credit_fraction(payments_5) =', credit_fraction(payments_5)
    payments_50 = data[data['total_amount'] > 50]
    print 'credit_fraction(payments_50) =', credit_fraction(payments_50)
    data['fare_per_minute'] =  data['fare_amount'] / (data['trip_time_in_secs'] / 60.)
    print 'fare_per_minute =', data['fare_per_minute'].mean()
    data['fare_per_mile'] = data['fare_amount'] / data['trip_distance']
    print 'fare_per_mile =', data['fare_per_mile'].median()
    data['speed'] = data['trip_distance'] / (data['trip_time_in_secs'] / 60. /60.)
    print '95%_speed =', data['speed'].quantile(.95)
    data['great_circle_distance'] = [haversine(row['pickup_latitude'], row['pickup_longitude'],
                  row['dropoff_latitude'], row['dropoff_longitude']) for index, row in data.iterrows()]
    data['ratio'] = data['great_circle_distance'] / data['trip_distance']
    print 'data[ratio].mean() =', data['ratio'].mean()
    JFK_longitude_min = -73.808319
    JFK_longitude_max = -73.776448
    JFK_latitude_min = 40.641140
    JFK_latitude_max = 40.666486
    is_from_JFK = ((data['pickup_longitude'] < JFK_longitude_max) & (data['pickup_longitude'] > JFK_longitude_min) &
                   (data['pickup_latitude'] < JFK_latitude_max) & (data['pickup_latitude'] > JFK_latitude_min))
    print 'data[is_from_JFK][tip_amount].mean() =', data[is_from_JFK]['tip_amount'].mean()
    is_march = pd.DatetimeIndex(data['pickup_datetime']).month == 3
    revenue_march = data[is_march][['hack_license', 'total_amount']].groupby('hack_license').aggregate(sum)
    print 'revenue_march.median() =', revenue_march['total_amount'].median()
