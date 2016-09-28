from flask import render_template
from app import app, pages

#------------------ general page routes ----------------------#
@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/SSAGES-site/features.html')
def features():
	return render_template("features.html")

@app.route('/SSAGES-site/team.html')
def team():
	return render_template("team.html")

@app.route('/SSAGES-site/download.html')
def download():
    return render_template("download.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

