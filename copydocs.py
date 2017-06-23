import os
import numpy as np
from shutil import copytree
from shutil import rmtree
from subprocess import call

#Path to SSAGES
ssages_path = "/home/cody/SSAGES"
ssages_site_path = "/home/cody/SSAGES-site"
ssages_site_project_path = "/home/cody/SSAGES-site/project/templates"
build_ssages_path = ssages_path + "/build"
api_path = ssages_path + "/build/doc/API-doc/html/"
manual_path = ssages_path + "/build/doc/Manual"

#Switch to build directory, build SSAGES and docs
os.chdir(build_ssages_path)
print("Making SSAGES...")
call(["make"])
print("Making documentation...")
call(["make", "doc"])

#Copy API and refmanual to project
print("Copying API to project...")
if os.path.isdir(ssages_site_project_path + "/api"):
    rmtree(ssages_site_project_path + "/api")
copytree(api_path, ssages_site_project_path + "/api")
print("Copying Manual to project...")
if os.path.isdir(ssages_site_project_path + "/manual"):
    rmtree(ssages_site_project_path + "/manual")
copytree(manual_path, ssages_site_project_path + "/manual")

#Copy API and refmanual
print("Copying API...")
if os.path.isdir(ssages_site_path + "/api"):
    rmtree(ssages_site_path + "/api")
copytree(api_path, ssages_site_path + "/api")
print("Copying Manual...")
if os.path.isdir(ssages_site_path + "/manual"):
    rmtree(ssages_site_path + "/manual")
copytree(manual_path, ssages_site_path + "/manual")
