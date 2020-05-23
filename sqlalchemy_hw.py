import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from datetime import datetime

from flask import Flask, jsonify

# create engine
engine = create_engine("sqlite:///Resources_hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect = True)

# Save references to each table

Measure = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(bind=engine)

# Create our session (link) from Python to the DB

app = Flask(__name__)

@app.route("/")
def home():
    return (
        "Welcome to the Climate and Exploration API!<br/>"
        "Available routes: <br/>"
        "<br/>"
        "Precipitation Data <br/>"
        f"/api/v1.0/precipitation <br/>"
        "<br/>"
        "Stations <br/>"
        f"/api/v1.0/stations <br/>"
        "<br/>"
        "Temperature Observations <br/>"
        f"/api/v1.0/tobs <br/>"
        "<br/>"
        "Enter start date (YYYY-mm-dd) <br/>"
        f"/api/v1.0/<start> <br/>"
        "<br/>"
        "Enter start and end date (YYYY-mm-dd) <br/>"
        f"/api/v1.0/<start>/<end> <br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # session = Session(engine)
    query_prcp = session.query(Measure.date, Measure.prcp).all()
    prcp_list = [] #list of dictionaries
    for rain in query_prcp:
        date = rain[0]
        prcp = rain[1] 
        prcp_dict = {date : prcp}
        prcp_list.append(prcp_dict)
    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def stations():
    query_stations = session.query(Station.station, Station.name).all()
    station_list = [] #list of dictionaries
    for stat in query_stations:
        station_num = stat[0] 
        name = stat[1] 
        station_dict = {station_num : name}
        station_list.append(station_dict)
    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    query_tobs = session.query(Measure.station, func.count(Measure.station)).group_by(Measure.station).\
                order_by(func.count(Measure.station).desc()).all()
    for row in query_tobs[:1]:
        most_active = row[0]
    most_active_query = session.query(Measure.date, Measure.tobs).filter(Measure.station == most_active).\
                        filter(Measure.date.like('2017%')).all()
    tobs_list = []
    for station in most_active_query:
        date = station[0]
        tobs = station[1]
        date_tobs = {date:tobs}
        tobs_list.append(date_tobs)
    return jsonify(tobs_list)
        
@app.route("/api/v1.0/<start>")
def start(start):
    """takes start date from user and returns Tmin, Tavg, and Tmax for each date >= start date"""
    return jsonify(session.query(func.min(Measure.tobs), func.avg(Measure.tobs), func.max(Measure.tobs)).\
        filter(Measure.date >= start))
    
@app.route("/api/v1.0/<start>/<end>")
def start_end(start = None, end = None):
    """takes start and end date from user and return Tmin, Tavg, and Tmax"""
    return jsonify(session.query(func.min(Measure.tobs), func.avg(Measure.tobs), func.max(Measure.tobs)).\
        filter(Measure.date >= start).filter(Measure.date <= end))

# close session
session.close()

if __name__ == "__main__":
    app.run(debug=True)