#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Flask
from flask import Flask,Response, redirect, request,make_response, render_template,jsonify

#Numpy imports
from numpy.linalg import inv
from numpy import arange,asarray,zeros

#Modules

#Used to Debug
from flask_debugtoolbar import DebugToolbarExtension


#------------------ settings ----------------------#
#Settings to turn the DB on or off
DEBUG = 1 #For testing locally
#DEBUG = 0 #For deploying online


#Initialize
app = Flask(__name__)

#redis queue, conn is the name of the redis connection as defined on worker
app.config['DEBUG'] =True
app.config['SECRET_KEY'] = 'use a better key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

#------------------ general page routes ----------------------#
@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/features')
def features():
	return render_template("features.html")

@app.route('/team')
def team():
	return render_template("team.html")

@app.route('/download')
def download():
    return render_template("download.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()
