#%%
#Import dependencies
import datetime as dt
import numpy as np
import pandas as pd

# %%
# Import SQLAlchemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# %%
# import the dependencies for Flask
from flask import Flask, jsonify

# %%
# Set Up the Database
engine = create_engine("sqlite:///hawaii.sqlite")

# %%
# Reflect the database into our classes.
Base = automap_base()

# %%
# Reflect the database
Base.prepare(engine, reflect=True)

# %%
# Create a variable for each of the classes so that we can reference them later
Measurement = Base.classes.measurement
Station = Base.classes.station

# %%
# Create a session link from Python to our database
session = Session(engine)
# %%
# Create a Flask application
app = Flask(__name__)
# Definie the welcome route
@app.route('/')
# Create a function welcome() with a return statement
def welcome():
    return(
    #Add the precipitation, stations, tobs, and temp routes that we’ll need into our return statement
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# %%
# Create the route for the percipitation analysis
@app.route("/api/v1.0/precipitation")
# Create the precipitation() function.
def precipitation():
    # Calculates the date one year ago from the most recent date in the database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Write a query to get the date and precipitation for the previous year
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    # Use jsonify() to format our results into a JSON structured file.
    return jsonify(precip)

# %%
#Create the route for the stations
@app.route("/api/v1.0/stations/")
# Create the stations() function.
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# %%
#Create the route for the tobs
@app.route("/api/v1.0/tobs")
#Create the tobs() function.
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# %%
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date <= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
    results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)


# %%
