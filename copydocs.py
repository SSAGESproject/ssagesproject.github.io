import os
import numpy as np
from shutil import copytree
from shutil import rmtree
from subprocess import call

#Path to SSAGES
ssages_path = "/home/cody/SSAGES"
ssages_site_path = "/home/cody/SSAGES-site"
build_ssages_path = ssages_path + "/build"
api_path = ssages_path + "/build/doc/API-doc/html/"
manual_path = ssages_path + "/build/doc/Manual"

#Switch to build directory, build SSAGES and docs
os.chdir(build_ssages_path)
print("Making SSAGES...")
call(["make"])
print("Making documentation...")
call(["make", "doc"])

#Copy API and refmanual
print("Copying API...")
if os.path.isdir(ssages_site_path + "/api"):
    rmtree(ssages_site_path + "/api")
copytree(api_path, ssages_site_path + "/api")
print("Copying Manual...")
if os.path.isdir(ssages_site_path + "/manual"):
    rmtree(ssages_site_path + "/manual")
copytree(manual_path, ssages_site_path + "/manual")
"""
#print(os.path.isdir("/home/el"))
#print(os.path.exists("/home/el/myfile.txt"))

###Inputs to change; set up range of inputs here###
parameters_changing = 2
sidewall_energy = np.linspace(-2.0, 2.0, 17)
template_CD = np.linspace(0.9, 2.3, 15)
periodicty = 1.8
template_CD = np.multiply(template_CD, periodicty)

#print(sidewall_energy)
#print(template_CD)

#Set up directories
dir_path = os.path.dirname(os.path.realpath(__file__))
for energy in sidewall_energy:
    energy_directory = "./" + str(energy)
    if not os.path.isdir(energy_directory):
        os.makedirs(energy_directory)
    os.chdir(energy_directory)
    for cd in template_CD:
        cd_directory = "./" + str(cd)
        if not os.path.isdir(cd_directory):
            os.makedirs(cd_directory)
        os.chdir(cd_directory)
        #In this directory should put an sbatch, symbolic link to ticg, and an Input file
        ticg_link = "../../../../../src/ticg"
        ticg_target = "./ticg"
        sbatch_link = dir_path + "/depablo.sbatch"
        sbatch_target = "./depablo.sbatch"
        input_link = dir_path + "/Input.dsa"
        input_target = "./Input.dsa"
        if not os.path.exists(ticg_target):
            os.symlink(ticg_link, ticg_target)
        #if not os.path.exists(sbatch_target):
        copyfile(sbatch_link, sbatch_target)
        copyfile(input_link, input_target)
        with open('Input.dsa', 'r') as file:
            data = file.readlines()
        templist = []
        line_counter = 0
        for line in data:
            if line_counter == 11:
                templist.append(str(cd) + "  Box dimension in X direction(Re)\n")
            elif line_counter == 12:
                templist.append(str(cd) + "  Box dimension in Y direction(Re)\n")
            elif line_counter == 46:
                templist.append(str(energy) + " Interaction strength of the stripe/sidewall with A\n")
            else:
                templist.append(data[line_counter])
            line_counter += 1
        with open('Input.dsa', 'w') as file:
            file.writelines(templist)
        sim_target = "./Simulation.log"
        if not os.path.exists(sim_target):
            #print("Would call sbatch")
            call(["sbatch", "depablo.sbatch"])
        else:
            #print("Simulation complete")
            1+1
        #print(data)
        #print(templist)
        os.chdir(dir_path)
        os.chdir(energy_directory)
    os.chdir(dir_path)
"""
