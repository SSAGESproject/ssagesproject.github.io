#!/usr/bin/env python
import subprocess
import os
import time

def hello_world():
	redis_url = os.getenv('REDISTOGO_URL','redis://localhost:6379')

	if redis_url == 'redis://localhost:6379':
		# This line is for local only
		output = subprocess.call(['./LOCAL_rscft','37','3','6','3','3','outfile1','outfile2','infile','1.78'])
		
	
	else:

		#These 3 lines are for remote
		os.chdir('/app/models/SCFT_real')
		subprocess.call(['make'])
		output = subprocess.call(['./rscft','37','3','6','3','3','outfile1','outfile2','infile','1.78'])

		output = str(output)


	return output

def wait1min():
	time.sleep(10)
	return "done!"
