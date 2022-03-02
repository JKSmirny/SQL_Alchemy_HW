import csv
import datetime as dt
import json as json
import os
import pandas as pd
import time
import matplotlib.pyplot as plt
%matplotlib inline
from matplotlib.ticker import StrMethodFormatter
import numpy as np
import scipy.stats as st
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, inspect
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
engine = create_engine('postgresql://postgres:Ben&LizzyA2@localhost:5433/SQLAlchemy_db')
engine=create_engine('sqlite:///Resources/hawaii.sqlite')
conn = engine.connect()
engine=create_engine('sqlite:///./Resources/hawaii.sqlite')
Base = automap_base()
Base.prepare(engine, reflect=True)
 # Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
from sqlalchemy.orm import Session
session = Session(engine)
Hawaii_station = [Measurement.station, Measurement.date, Measurement.prcp, Measurement.tobs, Station.station, Station.name]
Hawaii = session.query(*Hawaii_station).filter(Measurement.station == Station.station).limit(10).all()
#Use Flask to create your routes.
#import Flask
from flask import Flask
from flask import jsonify
@app.route("/")
def welcome():
        return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )
date_count = session.query(func.count(Measurement.date)).all()
earliest_date = session.query(Measurement.date).order_by(Measurement.date.asc()).first()[0]
print(earliest_date)
latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
@app.route("/api/v1.0/precipitation")
def precipitation():
    year_ago = dt.datetime.strptime(latest_date, "%Y-%m-%d") - dt.timedelta(days=366)
precipitation_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= year_ago).all()
    precipitation_dict = []
for date, prcp in precipitation_data:
    data = {}
    data['date'] = date
    data['prcp'] = prcp
    precipitation_dict.append(data)
    return jsonify(precipitation_dict)
@app.route("/api/v1.0/stations")
def stations():
    station_data = session.query(Station.name, Station.station, Station.elevation).all()
station_list = []
for data in station_data:
    row = {}
    row['name'] = data[0]
    row['station'] = data[1]
    row['elevation'] = data[2]
    station_list.append(row)
    return jsonify(station_list)
active_tobs = session.query(Station.name, Measurement.date , Measurement.tobs).\
filter(Measurement.date > '2016-08-23').\
group_by(Station.name).order_by(func.count(Station.name).desc()).all()
tobs_dict = []
for name,date,tobs in active_tobs:
    data = {}
    data['name'] = name
    data['date'] = date
    data['tobs'] = tobs
    tobs_dict.append(data)
    return jsonify(tobs_dict)
@app.route("/api/v1.0/<start>")
def start():
       start_date = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs),
                               func.max(Measurement.tobs)).filter(Measurement.date == earliest_date).all()
start_date_list = list(start_date)
return jsonify(start_date_list)  
@app.route("/api/v1.0/<start>/<end>")
def end_date():
    end_date = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs),
                               func.max(Measurement.tobs)).filter(Measurement.date == latest_date).all()
end_date_list = list(end_date)
return jsonify(end_date_list) 
start_query = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs),
                               func.max(Measurement.tobs)).filter(Measurement.date >= earliest_date).group_by(
        Measurement.date).all() 
full_data_query = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs),
                            func.max(Measurement.tobs)).filter(Measurement.date >= earliest_date).filter(
        Measurement.date <= latest_date).group_by(Measurement.date).all()
measurements = session.query(Measurement.station, Measurement.date, Measurement.prcp, Measurement.tobs).all()
measurements_df = pd.DataFrame(measurements)
measurements_df.columns =['station', 'date', 'prcp', 'tobs']
from datetime import datetime, date 
measurements_df['date'] = measurements_df['date'].astype('datetime64[ns]')
from sqlalchemy.orm import Session
session = Session(engine)
measurements_df['month'] = pd.to_datetime(measurements_df['date']).dt.month
measurements_jun = measurements_df[measurements_df['month']==6]
measurements_jun = round(measurements_df.groupby(["station"]).mean()["tobs"],2)
tobs_jun_mean = pd.DataFrame(measurements_jun)
tobs_jun_mean = tobs_jun_mean.rename(columns={'tobs': 'avg.temp in June'})
#Selecting data for month of december
# Identify the average temperature in June at all stations across all available years in the dataset. 
measurements_dec = measurements_df[measurements_df['month']==12]
# Identify the average temperature in December at all stations across all available years in the dataset. 
measurements_dec = round(measurements_df.groupby(["station"]).mean()["tobs"],2)
tobs_dec_mean = pd.DataFrame(measurements_dec)
tobs_dec_mean = tobs_dec_mean.rename(columns={'tobs': 'avg.temp in Dec'})
jun_dec_tobs = pd.merge(tobs_jun_mean, tobs_dec_mean, how="left", on=["station"])
from scipy import stats
from scipy import mean
jun_list = []
for temp in tobs_jun_mean:
    if type(tobs_jun_mean.tobs) == int:
        jun_list.append(tobs_jun_mean.tobs)        
dec_list = []
for temp in tobs_dec_mean:
    if type(tobs_dec_mean.tobs) == int:
        dec_list.append(tobs_dec_mean.tobs)
stats.ttest_rel('tobs_jun_mean'[0:200], 'tobs_dec_mean'[0:200])



