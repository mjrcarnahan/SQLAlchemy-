import numpy as np

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
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>` and `/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def rain():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Measurement.prcp, Measurement.date).all()

    session.close()

    session.close()

    # Create a dictionary from the row data and append to a list of rain fall and dates
    all_rain = []
    for prcp, date in results:
        rain_dict = {}
        rain_dict["date"] = date
        rain_dict["rainfall"] = prcp
        all_rain.append(rain_dict)

    return jsonify(all_rain)

@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all station names"""
    # Query all passengers
    results = session.query(Station.name, Station.station).all()

    session.close()

    return jsonify(results)

@app.route("/api/v1.0/tobs")
def temp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all station names"""
    # Query all passengers
    results = session.query(Measurement.tobs, Measurement.date).filter(Measurement.date >= '2016-01-01').filter(Measurement.date <= '2016-12-31').all()

    session.close()

    return jsonify(results)

@app.route("/api/v1.0/<start>")
def temp_stats_v1(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all station names"""
    # Query all passengers
    max_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start).scalar()
    min_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start).scalar()
    avg_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start).scalar()

    session.close()

    return jsonify(max_temp, min_temp, avg_temp)


@app.route("/api/v1.0/<start>/<end>")
def temp_stats_v2(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all station names"""
    # Query all passengers
    max_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).scalar()
    min_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).scalar()
    avg_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).scalar()

    session.close()

    return jsonify(max_temp, min_temp, avg_temp)

if __name__ == '__main__':
    app.run(debug=True)