#Import libraries
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#Database Connection
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Map database
Base = automap_base()
Base.prepare(engine, reflect = True)

#Reference known tables
measurement = Base.classes.measurement
station = Base.classes.station

#Set up flask
app = Flask(__name__)

#Flask Routes
@app.route("/")
def home():
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[enter start date: yyyy-mm-dd] <br/>"
        f"/api/v1.0/[enter start date: yyyy-mm-dd]/[enter end date: yyyy-mm-dd]"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    #Create session & query
    session = Session(engine)
    results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date > "2016-08-23").all()
    session.close()

    #Create dictionary and append to list
    prcp_list = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp
        prcp_list.append(prcp_dict)

    #Return json
    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def stations():
    #Create session & query
    session = Session(engine)
    stations = session.query(station.station).all()
    station_list = list(np.ravel(stations))
    session.close()

    #Return json
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    #Create session & query
    session = Session(engine)
    tobs_results = session.query(measurement.station, measurement.date, measurement.tobs).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date >'2016-08-23').all()
    session.close()

    #Create dictionary and append to list
    tobs_list = []
    for station, date, tobs in tobs_results:
        tobs_dict = {}
        tobs_dict['station'] = station
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs
        tobs_list.append(tobs_dict)

    #Return json
    return jsonify(tobs_list) 

@app.route("/api/v1.0/<start_date>")
def Start_date(start_date):
    #Create session & query
    session = Session(engine)
    start_results = session.query( func.avg(measurement.tobs), func.max(measurement.tobs), func.min(measurement.tobs)).\
        filter(measurement.date >= start_date)
    session.close()

    #Create dictionary and append to list
    tobs_start_list = []
    for avg, max, min in start_results:
        start_dict = {}
        start_dict['avg'] = avg
        start_dict['max'] = max
        start_dict['min'] = min
        tobs_start_list.append(start_dict)

    #Return json
    return jsonify(tobs_start_list)

@app.route("/api/v1.0/<start_date>/<end_date>")
def Start_end_date(start_date, end_date):
    #Create session & query
    session = Session(engine)
    start_results = session.query( func.avg(measurement.tobs), func.max(measurement.tobs), func.min(measurement.tobs)).\
        filter(measurement.date >= start_date).\
        filter(measurement.date <= end_date)
    session.close()

    #Create dictionary and append to list
    tobs_start_end_list = []
    for avg, max, min in start_results:
        start_end_dict = {}
        start_end_dict['avg'] = avg
        start_end_dict['max'] = max
        start_end_dict['min'] = min
        tobs_start_end_list.append(start_end_dict)

    #Return json
    return jsonify(tobs_start_end_list)

if __name__ == '__main__':
    app.run(debug=True)