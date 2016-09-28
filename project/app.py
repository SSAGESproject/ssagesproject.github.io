#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Flask
from flask import Flask,Response, redirect, request,make_response, render_template,jsonify
from flask_flatpages import FlatPages
from flask_frozen import Freezer

#Initialize
app = Flask(__name__)
app.config.from_pyfile('settings.py')
pages = FlatPages(app)
freezer = Freezer(app)

