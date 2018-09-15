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

import geopandas as gpd

from decimal import *

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
engine = create_engine("sqlite:///db/airbnb.sqlite", echo=False)

@app.route("/")
def welcome():
    a = "<h1>These are the valid endpoints in this project</h1>"
    b = "<h3>/index</h3>"
    c = "<h3>/listingsall</h3>"
    d = "<h3>/listings-json</h3>"
    e = "<h3>/coord-json</h3>"
    f = "<h3>/pie-json</h3>"
    g = "<h3>/map-geojson</h3>"
    h = "<h3>/summary-json</h3>"

    return a+b+c+d+e+g

@app.route("/index")
def get_landing():
    response = engine.execute('SELECT * FROM listings').fetchall()
    response_df = pd.DataFrame(response)
    header = ['id','listing_url','name','picture_url','host_name','host_response','host_is_superhost','host_has_profile_pic',
            'host_thumbnail_url','host_picture_url','neighbourhood','property_type','bedrooms','bathrooms','price',
            'weekly_price','monthly_price','availability_365','longitude','latitude','number_of_reviews','review_scores_rating',
            'reviews_per_month']
    response_df.columns = header
    coord_df = response_df[["longitude","latitude","price","picture_url"]]
    
    return_file = json.loads(coord_df.to_json(orient='records'))
    
    return render_template('index.html',data=return_file)

@app.route("/bullet")
def bullet():
    return render_template('testbullet.html')

@app.route("/box")
def box():
    return render_template('testbox.html')

@app.route("/dash")
def dash():
    return render_template('dash.html')


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

@app.route("/listings-json")
def listings_json():
    response = engine.execute('SELECT * FROM listings').fetchall()
    response_df = pd.DataFrame(response)
    header = ['id','listing_url','name','picture_url','host_name','host_response','host_is_superhost','host_has_profile_pic',
            'host_thumbnail_url','host_picture_url','neighbourhood','property_type','bedrooms','bathrooms','price',
            'weekly_price','monthly_price','availability_365','longitude','latitude','number_of_reviews','review_scores_rating',
            'reviews_per_month']
    response_df.columns = header
    returnjson = json.loads(response_df.to_json(orient='records'))
    
    return jsonify(returnjson)

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

@app.route("/pie-json")
def pie_json():
    response = engine.execute('SELECT * FROM listings').fetchall()
    response_df = pd.DataFrame(response)
    header = ['id','listing_url','name','picture_url','host_name','host_response','host_is_superhost','host_has_profile_pic',
            'host_thumbnail_url','host_picture_url','neighbourhood','property_type','bedrooms','bathrooms','price',
            'weekly_price','monthly_price','availability_365','longitude','latitude','number_of_reviews','review_scores_rating',
            'reviews_per_month']
    response_df.columns = header
    return_file = json.loads(response_df[["neighbourhood","id"]].to_json(orient='records'))
    return jsonify(return_file)

@app.route("/map-geojson")
def get_mapdata():

   #01 Read in data
   path = "static/data/filtered_listings.csv"
   data = pd.read_csv(path)
   geodata =gpd.read_file('static/data/neighbourhoods.geojson')

   #02 Create the summmary stats and add to JSON file
   summarydata = data.groupby('neighbourhood').mean()
   summarydata.reset_index(inplace = True )
   geodata = pd.merge(geodata, summarydata, how = 'left', on = 'neighbourhood')

   # 03 Convert back to Dictionary and JSONIFY
   geodict = json.loads(geodata.to_json(na = 'null'))

   #04 Render to site
   return jsonify(geodict)

@app.route("/summary-json")
def get_summary():
    response = engine.execute('SELECT * FROM listings').fetchall()
    response_df = pd.DataFrame(response)
    header = ['id','listing_url','name','picture_url','host_name','host_response','host_is_superhost','host_has_profile_pic',
            'host_thumbnail_url','host_picture_url','neighbourhood','property_type','bedrooms','bathrooms','price',
            'weekly_price','monthly_price','availability_365','longitude','latitude','number_of_reviews','review_scores_rating',
            'reviews_per_month']
    response_df.columns = header
    price_df = response_df[["property_type","price"]]

    grouped_df = price_df.groupby('property_type', as_index=False).price.agg(['min','mean','max'])
    #grouped_df['mean'] = grouped_df['mean'].map('{:,.2f}'.format)
    grouped_df.reset_index(inplace = True )
    return_file = json.loads(grouped_df.to_json(orient='index'))
    #print(type(return_file))  #it's a string
    return jsonify(return_file)
    
if __name__ == "__main__":
    app.run()