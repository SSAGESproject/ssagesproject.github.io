#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Flask
from flask import Flask,Response, redirect, request,make_response, render_template,jsonify

#Numpy imports
from numpy.linalg import inv
from numpy import arange,asarray,zeros

#Modules
import models.SLCT as SLCT
import models.VO as VO
from models.FH import *
from models.structurefactor import structure_factor,rpaPlot
import models.simpleA
import models.saftdemocode as saftdemocode
from models.general import flip

#For talking to chiSQL
import json
import urllib
#import MySQLdb

#Used to Debug
from flask_debugtoolbar import DebugToolbarExtension


#------------------ settings ----------------------#
#Settings to turn the DB on or off
DEBUG = 1 #Offline
if DEBUG == 0: #Online
        db = MySQLdb.connect(host="127.0.0.1", user="pppdb_prd_ro", db="pppdb_prd", passwd="jdUHGLqfuZJNYAB9Hr63b8", use_unicode=True, charset="utf8")
        cur = db.cursor()


#Initialize
app = Flask(__name__)

#redis queue, conn is the name of the redis connection as defined on worker
app.config['DEBUG'] =True
app.config['SECRET_KEY'] = 'use a better key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False




#------------------ general page routes ----------------------#
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/howto.html')
def howto():
	return render_template("howto.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#--------------------- database routes ------------------------#
#Query the DB for a specific polymer on the homepage
@app.route('/polymer', methods=['POST','GET'])
def polymer():
	if request.method == 'POST':
		poly = request.form.get('polymer')

		htmlpath = "/static/polymer.html?polymer="+poly
		return redirect(htmlpath)
		

# Get unique polymer names from db
@app.route('/polymers',methods=['GET'])
def polymers():
	if request.method == 'GET':
		if DEBUG == 0:
			query0 = "Select compound1, compound2 from reviewed_chis where type1='polymer' and type2='polymer'" 
			cur.execute(query0)
			db.commit()
		        results0 = cur.fetchall()
                        polymers = []

	    		for row0 in results0:
				polymers.append(row0[0])
				polymers.append(row0[1])
			unique_polymers	= list(set(polymers))
			polymers_str ='['
			for upol in unique_polymers:
				polymers_str = polymers_str + '"' + upol + '",'
			polymers_str = polymers_str.strip(',') + ']'
			return Response(json.dumps(polymers_str),  mimetype='application/json')

@app.route('/chis',methods=['POST','GET'])
def chis():
	if request.method == 'POST':
		if DEBUG == 0:
			tablecontent = []
			poly = request.get_json()
			poly = poly['polymer']
			query0 = "Select compound1, compound2, chinumber, chia, chib, chic, method, notes, doi , chimax, temperature, tempmax, tempunit, reference from reviewed_chis where (compound1 = '%s' or compound2='%s' )and type1='polymer' and type2='polymer'" % (poly, poly)
			cur.execute(query0)
			db.commit()
		        results0 = cur.fetchall()

			# Form table
	    		chi = u'\u03C7' 
                        polymers = []
	    		for row0 in results0:
				# Get link to paper from second table
				query1 = "select remotepath from papers where doi='%s'" % (row0[8])
				cur.execute(query1)
				db.commit()
				results1 = cur.fetchone()
				url = results1[0]
                                tablerow = {}	
				# Get other half of the polymer pair
				if row0[0].lower().find(poly) == -1:
					polymer = row0[0]
				else:
					polymer = row0[1]
				tablerow["polymer"] = polymer 
				tablerow["chi"] = str(row0[2]) 
				tablerow["chi_a"] = str(row0[3]) 
				tablerow["chi_b"] = str(row0[4]) 
				tablerow["chi_c"] = str(row0[5])
				tablerow["method"] = str(row0[6])
				
				tablerow["notes"] = row0[7]  # unicode decode?
				tablerow["doi"] = str(row0[8])
				tablerow["chimax"] = str(row0[9])
				tablerow["temperature"] = str(row0[10])
				tablerow["tempmax"] = str(row0[11])
				tablerow["tempunit"] = row0[12]
				tablerow["reference"] = str(row0[13])
				tablecontent.append(tablerow)
			print tablecontent
	   	else:
			tablecontent = [{'polymer': u'polystyrene', 'doi': '10.1021/ma401957s', 'chi_b': '0.0', 'chi_c': '0.0', 'reference': 'ISBN: 0-387-31235-8', 'chi_a': '0.0', 'chi': '0.047', 'notes': u'', 'chimax': '0.0', 'tempunit': u'C', 'tempmax': '0.0', 'method': '', 'temperature': '40.0'}, {'polymer': u'styrene', 'doi': '10.1021/ma3004136', 'chi_b': '0.0', 'chi_c': '0.0', 'reference': '', 'chi_a': '0.0', 'chi': '25.0', 'notes': u'X is given in terms of XN', 'chimax': '0.0', 'tempunit': u'K', 'tempmax': '0.0', 'method': 'scattering1', 'temperature': '298.0'}, {'polymer': u'polystyrene', 'doi': '10.1021/ma400533w', 'chi_b': '0.0', 'chi_c': '0.0', 'reference': 'DOI: 10.1021/ma011958x', 'chi_a': '0.0', 'chi': '0.05', 'notes': u'at 0 mol % C6F13H modifications', 'chimax': '0.0', 'tempunit': u'', 'tempmax': '0.0', 'method': 'scattering1', 'temperature': '0.0'}, {'polymer': u'polystyrene', 'doi': '10.1021/ma400533w', 'chi_b': '0.0', 'chi_c': '0.0', 'reference': 'DOI: 10.1021/ma011958x', 'chi_a': '0.0', 'chi': '0.75', 'notes': u'at 80 mol % C6F13H modification', 'chimax': '0.0', 'tempunit': u'', 'tempmax': '0.0', 'method': 'scattering1', 'temperature': '0.0'}, {'polymer': u'polystyrene', 'doi': '10.1021/ma500633b', 'chi_b': '0.0', 'chi_c': '0.0', 'reference': 'DOI: 10.1051/jp2:1997217 (http://dx.doi.org/10.1051/jp2:1997217)', 'chi_a': '0.0', 'chi': '0.0555', 'notes': u'Composition given in volume fractions. Temperature cited as room temperature, which is 23 degrees Celsius on average.', 'chimax': '0.0', 'tempunit': u'C', 'tempmax': '0.0', 'method': 'scattering1', 'temperature': '23.0'}, {'polymer': u'polystyrene', 'doi': '10.1021/ma202717p', 'chi_b': '0.0', 'chi_c': '0.0', 'reference': 'DOI: 10.1021/ma971309e', 'chi_a': '0.0', 'chi': '0.16', 'notes': u'', 'chimax': '0.0', 'tempunit': u'K', 'tempmax': '0.0', 'method': 'md_simulation', 'temperature': '298.0'}, {'polymer': u'polystyrene', 'doi': '10.1021/ma301487e', 'chi_b': '0.0', 'chi_c': '0.0', 'reference': 'DOI: 10.1021/ma00036a019', 'chi_a': '0.0', 'chi': '32.5', 'notes': u'', 'chimax': '0.0', 'tempunit': u'K', 'tempmax': '513.0', 'method': 'micro_phase_tri', 'temperature': '478.0'}] 
        	return Response(json.dumps(tablecontent),  mimetype='application/json')





#--------------------- saft routes ------------------------#
@app.route('/saftdemo.html',methods=['POST','GET'])
def saftdemo():
	return render_template("saftdemo.html")

#saft is currently a simple, demo version, full version still in progress
@app.route('/saftplot',methods=['POST','GET'])
def saftplot():
	if request.method == 'POST':
		#Call the function in saftdemocode.py
		pdid,pdjson,zipped2,critphi2,list_of_plots = saftdemocode.saft_plot()

		zipped2 = np.round(zipped2,4)
		critphi2= np.round(critphi2,4)

		return render_template("saftdemoplot.html",pdid=pdid,pdjson=pdjson,zipped=zipped2,critphi=critphi2,list_of_plots=list_of_plots)

#--------------------- voorn-overbeek routes ------------------------#

@app.route('/vorn.html',methods=['POST','GET'])
def vorn():
	return render_template("vorn.html")

@app.route('/vornplot', methods=['GET','POST'])	
def vornplot():
	if request.method == 'POST':
		#values
		N = float(request.form['N'])
		sigma = float(request.form['sigma'])
		psi = float(request.form['psi'])

		#run solver and plot
		critphi, list_of_plots, zipped = VO.vPlot(3.655,sigma,psi,N)
		return render_template("vornplot.html",critphi=critphi,list_of_plots=list_of_plots,zipped=zipped)



#----------------- simple lattice cluster theory routes ---------------------#
@app.route('/slct.html',methods=['POST','GET'])
def slct():
	return render_template("slct.html") 

@app.route('/slctplot', methods=['GET','POST'])	
def slctplot():
	if request.method == 'POST':
		na = float(request.form['NFA'])
		nb = float(request.form['NFB'])
		polya = request.form['polya']
		polyb = request.form['polyb']
		try:
			k1 = request.form['k1']
			k2 = request.form['k2']
		except:
			k1 = 0
			k2 = 0
		print polya,polyb
		actualname_a = SLCT.propername(polya,k1)
		actualname_b = SLCT.propername(polyb,k2)
		print actualname_b,actualname_a 

		#create url string to fetch data from site
		webstr = "http://chidb.ci.uchicago.edu/basic_api.php?polymera="
		#had to switch because values are symmetrical
		site_url = webstr + actualname_a+ "&polymerb=" + actualname_a

		#fetch db data
		response = urllib.urlopen(site_url)
		jsondata = json.load(response)

		#run and plot
		critphi, list_of_plots, zipped =SLCT.sPlot(polya,
					polyb,na,nb,jsondata)

		return render_template("slctplots.html",
				critphi=critphi,list_of_plots=list_of_plots,zipped=zipped)

#----------------- flory routes ---------------------#
@app.route('/flory.html',methods=['POST','GET'])
def flory():
	return render_template("flory.html")

@app.route('/floryplot', methods=['GET','POST'])	
def floryplot():
	#floryplot
	if request.method == 'POST':
		na = float(request.form['NFA'])
		nb = float(request.form['NFB'])
		v0 = float(request.form['v0'])

		#Talk to SQL
		#request the option selected from the dropdown
		polya = request.form['dropdowna']
		polyb = request.form['dropdownb']

		#create url string to fetch data from site
		webstr = "http://chidb.ci.uchicago.edu/basic_api.php?polymera="
		site_url = webstr + polya + "&polymerb=" + polyb

		#open the site and load into json
		response = urllib.urlopen(site_url)
		jsondata = json.load(response)
		jsondata,critvals,list_of_plots,zipped = fPlot(polya,polyb,na,nb,v0,jsondata)
			
		return render_template("floryplot.html",polya=polya,polyb=polyb,jsondata=jsondata,critphi=critvals,list_of_plots=list_of_plots,zipped=zipped)


#----------------- RPA structure factor routes ---------------------#
@app.route('/structurefactor.html',methods=['POST','GET'])
def structurefactor():
	return render_template("radiusgyration.html")

@app.route('/sfplot', methods=['GET','POST'])	
def sfplot():
	if request.method == 'POST':
		na = float(request.form['Na'])
		nb = float(request.form['Nb'])
		ba = float(request.form['Ba'])
		bb = float(request.form['Bb'])
		phi = float(request.form['phia'])
		chi = float(request.form['chi'])

		id, json01, zipped = rpaPlot(na,nb,ba,bb,phi,chi)
		return render_template("sfplot.html",id=id,json01=json01,zipped=zipped)

#------------------ extra ----------------------------#
def flip(a1,a2,b1,b2,c1,c2):
	return a2,a1,b2,b1,c2,c1




if __name__ == '__main__':
    app.run()








