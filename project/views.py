import os
from flask import render_template
from app import app, pages
from flask import send_from_directory

#------------------ general page routes ----------------------#
@app.route('/')
@app.route('/SSAGES-site/index.html')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/SSAGES-site/features.html')
@app.route('/features.html')
def features():
	return render_template("features.html")

@app.route('/SSAGES-site/team.html')
@app.route('/team.html')
def team():
	return render_template("team.html")

@app.route('/SSAGES-site/download.html')
@app.route('/download.html')
def download():
    return render_template("download.html")

@app.route('/SSAGES-site/papers.html')
@app.route('/papers.html')
def papers():
    return render_template("papers.html")

@app.route('/SSAGES-site/validation.html')
@app.route('/validation.html')
def validation():
    return render_template("validation.html")

@app.route('/SSAGES-site/tutorials.html')
@app.route('/tutorials.html')
def tutorials():
    return render_template("tutorials.html")

@app.route('/SSAGES-site/docs.html')
@app.route('/docs.html')
def docs():
	return render_template("docs.html")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("%s" % path)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

