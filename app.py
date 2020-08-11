# import dependencies
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

################################
session = Session(engine)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home_page():
    "List all routes that are available."
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )
@app.route('/api/v1.0/<start>')
def def_start(start):
    query_start = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()

    dict_start = []
    for min, avg, max in query_start:
        dictionary = {}
        dictionary["Minimum"] = min
        dictionary["Average"] = avg
        dictionary["Maximum"] = max
        dict_start.append(dictionary)
    
    return jsonify(dict_start)

@app.route('/api/v1.0/<start>/<end>')
def start_end(start, end):
    query_start_end = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    session.close()
    
    dict_start_end = []
    for min, avg, max in query_start_end:
        dictionary = {}
        dictionary["Minimum"] = min
        dictionary["Average"] = avg
        dictionary["Maximum"] = max
        dict_start_end.append(dictionary)
    
    return jsonify(dict_start_end)
    


@app.route('/api/v1.0/precipitation')
def precipitation():
    sel = [Measurement.date, Measurement.prcp]
    query_prcp = session.query(*sel).all()
    
    session.close()

    dict_prcp =[]
    for date, prcp in query_prcp:
        dictionary = {}
        dictionary["Date"] = date
        dictionary["Precipitation"] = prcp
        dict_prcp.append(dictionary)

    return jsonify(dict_prcp)

@app.route('/api/v1.0/stations')
def stations():
    sel = [Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation]
    query_station = session.query(*sel).all()

    session.close()

    dict_station = []
    for station, name, lat, long, elevation in query_station:
        dictionary = {}
        dictionary["Station"] = station
        dictionary["Name"] = name
        dictionary["Latitude"] = lat
        dictionary["Longitude"] = long
        dictionary["Elevation"] = elevation
        dict_station.append(dictionary)
          
    return jsonify(dict_station)

@app.route('/api/v1.0/tobs')
def tobs():
    sel = [Measurement.date, Measurement.tobs]
    query_tobs = session.query(*sel).filter(Measurement.date >= '2016-08-23').all()

    session.close()
    
    dict_tobs = []
    for date, tobs in query_tobs:
        dictionary = {}
        dictionary["Date"] = date
        dictionary["Temperature"] = tobs
        dict_tobs.append(dictionary)

    return jsonify(dict_tobs)



if __name__ == "__main__":
    app.run(debug=True)






