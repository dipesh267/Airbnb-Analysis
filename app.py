import os

import pandas as pd
import numpy as np
import json

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#################################################
# Database Setup
#################################################

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Data/airbnb.sqlite"
# db = SQLAlchemy(app)
# # reflect an existing database into a new model
# Base = automap_base()
# # reflect the tables
# Base.prepare(db.engine, reflect=True)
# # Create our session (link) from Python to the DB
# Listings_table = Base.classes.listings
# Use Pandas to perform the sql query
engine = create_engine("sqlite:///Data/airbnb.sqlite", echo=False)

@app.route("/")
def welcome():
    return render_template('junk.html')

@app.route("/listingsall")
def listingsall():
    response = engine.execute('SELECT * FROM listings').fetchall()
    response_df = pd.DataFrame(response)
    header = ['id','listing_url','name','picture_url','host_name','host_response','host_is_superhost','host_has_profile_pic',
            'host_thumbnail_url','host_picture_url','neighbourhood','property_type','bedrooms','bathrooms','price',
            'weekly_price','monthly_price','availability_365','longitude','latitude','number_of_reviews','review_scores_rating',
            'reviews_per_month']
    response_df.columns = header
    returnjson = json.loads(response_df.to_json(orient='records'))
    
    return render_template('listings.html',data=returnjson)

@app.route("/coord-json")
def coord_json():
    response = engine.execute('SELECT * FROM listings').fetchall()
    response_df = pd.DataFrame(response)
    header = ['id','listing_url','name','picture_url','host_name','host_response','host_is_superhost','host_has_profile_pic',
            'host_thumbnail_url','host_picture_url','neighbourhood','property_type','bedrooms','bathrooms','price',
            'weekly_price','monthly_price','availability_365','longitude','latitude','number_of_reviews','review_scores_rating',
            'reviews_per_month']
    response_df.columns = header
    return_file = json.loads(response_df[["longitude","latitude","price"]].to_json(orient='records'))
    return jsonify(return_file)

@app.route("/coord")
def get_coord():
    response = engine.execute('SELECT * FROM listings').fetchall()
    response_df = pd.DataFrame(response)
    header = ['id','listing_url','name','picture_url','host_name','host_response','host_is_superhost','host_has_profile_pic',
            'host_thumbnail_url','host_picture_url','neighbourhood','property_type','bedrooms','bathrooms','price',
            'weekly_price','monthly_price','availability_365','longitude','latitude','number_of_reviews','review_scores_rating',
            'reviews_per_month']
    response_df.columns = header
    coord_df = response_df[["longitude","latitude","price","picture_url"]]
    
    return_file = json.loads(coord_df.to_json(orient='records'))
    
    return render_template('mapping.html',data=return_file)

if __name__ == "__main__":
    app.run()