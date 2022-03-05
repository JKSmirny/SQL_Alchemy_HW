import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify

# Database Setup
engine = create_engine('sqlite:///Resources/hawaii.sqlite', connect_args={'check_same_thread': False}, echo=True)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup
app = Flask(__name__)

# Flask Routes
#List all routes that are available
@app.route("/")
def welcome():

     return (
         f"/api/v1.0/precipitation<br/>"
         f"/api/v1.0/stations<br/>"
         f"/api/v1.0/tobs<br/>"
         f"/api/v1.0/start<br/>"
         f"/api/v1.0/startYYYY-MM-DD&endYYYY-MM-DD<br/>"
     )


@app.route("/api/v1.0/precipitation")
def precip():
    # Calculate the date 1 year ago from the last data point in the database
    year_end = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]

    #find date 12 months before
    year_start = dt.datetime.strptime(year_end, "%Y-%m-%d") - dt.timedelta(days=366)

    # Perform a query to retrieve the data and precipitation scores
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= year_start).all()

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

    #create dictionary for JSON
    station_list = []
    for name, station, elevation in station_data:
        data = {}
        data['name'] = name
        data['station'] = station
        data['elevation'] = elevation
        station_list.append(data)
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def temperature_tobs():
    active_tobs = session.query(Station.name, Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= "2017-05-01", Measurement.date <= "2017-09-01").\
        all()

    #use dictionary, create json
    tobs_list = []
    for name, date, tobs in active_tobs:
        data = {}
        data["name"] = name
        data["date"] = date
        data["tobs"] = tobs
        tobs_list.append(data)

    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>")
def start(start=None):
    
    start_date = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs),
                               func.max(Measurement.tobs)).filter(Measurement.date == start).group_by(
        Measurement.date).all()
    start_date_list = list(start_date)
    #return jsonify(start_date_list)

    start_query = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs),
                                  func.max(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()
    start_query_list = list(start_query)
    #return jsonify(start_date_list)
    return jsonify(start_query_list)

@app.route("/api/v1.0/<start>&<end>")
def end_date(end=None):
    
    end_date = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs),
                               func.max(Measurement.tobs)).filter(Measurement.date >= end).group_by(
        Measurement.date).all()
    end_date_list = list(end_date)
    
    end_query = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs),
                                  func.max(Measurement.tobs)).filter(Measurement.date >= end).filter(
        Measurement.date <= end).group_by(Measurement.date).all()
    end_query_list = list(end_query)
    #return jsonify(end_date_list)
    return jsonify(end_query_list)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
