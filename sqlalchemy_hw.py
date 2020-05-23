from flask import Flask, jsonify

import numpy as np

import pandas as pd

import datetime as dt

from datetime import datetime
#Reflect Tables into SQLAlchemy ORM

# Python SQL toolkit and Object Relational Mapper

import sqlalchemy

from sqlalchemy.ext.automap import automap_base

from sqlalchemy.orm import Session

from sqlalchemy import create_engine, func, inspect

engine = create_engine("sqlite:///hawaii (2).sqlite")


# reflect an existing database into a new model

Base = automap_base()

# reflect the tables

Base.prepare(engine, reflect = True)

# We can view all of the classes that automap found

#Base.classes.keys()
#['measurement', 'station']

# Save references to each table

Measure = Base.classes.measurement

Station = Base.classes.station
# Create our session (link) from Python to the DB
# session = Session(engine)

# Create our session (link) from Python to the DB

#session = Session(bind=engine)
app = Flask(__name__)

@app.route("/")
def home():
    return (
        "Welcome to the Climate and Exploration API!<br/>"
        "Available routes: <br/>"
        "/api/v1.0/precipitation <br/>"
        "/api/v1.0/stations <br/>"
        "/api/v1.0/tobs <br/>"
        f"/api/v1.0/<start> <br/>"
        f"/api/v1.0/<start>/<end> <br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    query_prcp = session.query(Measure.date, Measure.prcp).all()
    session.close()
    prcp = []
    for date, prcp in query_prcp:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp.append(prcp_dict)
        return jsonify(prcp)

# @app.route("/api/v1.0/stations")
# def stations():
#     query_stations = session.query(Measure.station).all()
#     stations = []
#     for row in query_stations:
#         if row not in stations:
#             stations.append(row)
#     station_dict = {'stations' : stations}
#     return jsonify(stations_dict)


# @app.route("/api/v1.0/tobs")
# def tobs():
#     query_tobs = session.query(Measure.station, func.count(Measure.station)).group_by(Measure.station).\
#                 order_by(func.count(Measure.station).desc()).all()
#     for row in query_tobs[:1]:
#         most_active = row[0]
#     most_active_query = session.query(Measure.date, Measure.tobs).filter(Measure.station == most_active).\
#                         filter(Measure.date.like('2017%'))
#     for station in most_active_query:
#         date = station[0]
#         tobs = station[1]
#         date_tobs = {date:tobs}
#         return jsonify(date_tobs)
        
# @app.route("/api/v1.0/<start>")
# def start(start):
#     """takes start date from user and returns Tmin, Tavg, and Tmax for each date >= start date"""
#     return jsonify(session.query(func.min(Measure.tobs), func.avg(Measure.tobs), func.max(Measure.tobs)).\
#         filter(Measure.date >= start))
    
# @app.route("/api/v1.0/<start>/<end>")
# def start_end(start = None, end = None):
#     """takes start and end date from user and return Tmin, Tavg, and Tmax"""
#     return jsonify(session.query(func.min(Measure.tobs), func.avg(Measure.tobs), func.max(Measure.tobs)).\
#         filter(Measure.date >= start).filter(Measure.date <= end))

if __name__ == "__main__":
    app.run()