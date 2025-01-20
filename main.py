import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Database Setup
#database_path = "/Users/marylarson/Desktop/Data_Analytics/sqlalchemy-challenge/hawaii.sqlite"
engine = create_engine("sqlite:///hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
# Save reference to the tables
measurement = Base.classes.measurement
station = Base.classes.station

# Flask Setup
app = Flask(__name__)


# Step 1
# Flask Routes
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

# Step 2
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
# Convert the query results from your precipitation analysis 
# (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
    results = session.query(measurement.date, measurement.prcp).all
    session.close()
    precipitation_analysis = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation_analysis.append(precipitation_dict)

# Return the JSON representation of your dictionary.
    return jsonify(precipitation_analysis)

# Step 3
# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    
    rows = session.query(station)
    return jsonify(stations)


# Step 4
# Query the dates and temperature observations of the most-active station for the previous year of data.
# Return a JSON list of temperature observations for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

most_active = session.query(measurement.station, measurement.tobs).\
    filter(measurement.station == 'USC00519281').\
    order_by(measurement.station).all()
most_active

lowest = session.query(func.min(measurement.tobs)).scalar()
print(lowest)
highest = session.query(func.max(measurement.tobs)).scalar()
print(highest)
average = session.query(func.avg(measurement.tobs)).scalar()
print(average)

# Step 5
# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
# For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
# For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
@app.route("/api/v1.0/<start>")
def start():
    session = Session(engine)
    lowest = session.query(func.min(measurement.tobs)).scalar()
    print(lowest)
    highest = session.query(func.max(measurement.tobs)).scalar()
    print(highest)
    average = session.query(func.avg(measurement.tobs)).scalar()
    print(average)
    return jsonify(start)

















if __name__ == '__main__':
    app.run(debug=True)