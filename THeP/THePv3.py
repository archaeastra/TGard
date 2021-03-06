#Tidal Heating Plot, by Lyan I.A. Guez.
#A script to plot the tidal heat in a Monte Carlo VSpace run.
#Thanks to Dr. David Fleming, whose code I based this script on for VPlanet compatibility.

import matplotlib as mpl
mpl.use('Agg')
#Used when plotting without a screen.
import matplotlib.pyplot as plt
import numpy as np
import math
import sys
import os
import re

# Check correct number of arguments
if (len(sys.argv) != 2):
    print('ERROR: Incorrect number of arguments.')
    print('Usage: '+sys.argv[0]+' <pdf | png>')
    exit(1)
if (sys.argv[1] != 'pdf' and sys.argv[1] != 'png'):
    print('ERROR: Unknown file format: '+sys.argv[1])
    print('Options are: pdf, png')
    exit(1)

#Can also hard code the addresses.
#InputDir = input("Input Directory:")
InputDir = "./Canari1K_AGES"


#Definitions
def Strip(pattern):      
    result = re.findall("\d+.\d+.+", pattern)
    result = float(result[0])
    return (result)
def Seek(log, pattern):
    for line in log:
        result = re.findall(pattern, line)
        if len(result) != 0:
            return(result)
def Find(log, pattern):
    for line in log:
        result = re.findall(pattern, line)
        #print(result)       
        if len(result) != 0:
            result = Strip(line)
            return (result)
def Degrees(list):
    for index in range(0,len(list)):
        list[index] = np.array(list[index], dtype=float)
        list[index] = math.degrees(list[index])
    return list

def Repair(list):
    for index in range(0,len(list)):
        #print(str(type(list[index])))
        if str(type(list[index])) == "<class 'NoneType'>":
            list[index] = int(0)
            print("Empty Index Zeroed")
            #print(list[index])
            return(list)


#Arrays for sorting the values. 
BInit=[]
CInit=[]
BFin=[]
CFin=[]

#Create an output file

#OTFL = input("Create output file? y/n:")
OTFL = "n"
csl = sys.stdout
if OTFL == 'y':
    out = open("THePv2.log", 'w+')
    sys.stdout = out
    print("Log File of Tidal Heats found")
else: 
    print("No Output File Created, proceeding to console...")
#>The output prints the values THeP finds to a text file: THeP.log, so they can be checked and/or used.

#Collection of b log files:
for root, dirs, files in os.walk(InputDir, topdown=False):
    for name in files:
        if name == "TGard.log":
            LogName = str(os.path.join(root, name))
            with open (LogName, 'rt') as log: 
                #Finding initial obs
                Seek(log,"----\sINITIAL\sSYSTEM\sPROPERTIES\s----")
                Seek(log, "-----\sBODY:\sTGb\s----") 
                obb = Find(log, "\(SurfEnFluxTotal\)")
                BInit.append(obb)
                Seek(log, "-----\sBODY:\sTGc\s----") 
                obc = Find(log, "\(SurfEnFluxTotal\)")
                CInit.append(obc)
                if OTFL == 'y':
                    print("----FILE:" + os.path.join(root, name))
                    print("--INITIAL--")
                    print("BODY-b:"+str(obb))
                    print ("BODY-c:"+str(obc))
            with open (LogName, 'rt') as log: 
                #Finding final obs
                Seek(log,"----\sFINAL\sSYSTEM\sPROPERTIES\s----") 
                Seek(log, "-----\sBODY:\sTGb\s----") 
                obb = Find(log, "\(SurfEnFluxTotal\)")
                BFin.append(obb)
                Seek(log, "-----\sBODY:\sTGc\s----") 
                obc = Find(log, "\(SurfEnFluxTotal\)")
                CFin.append(obc)
                if OTFL == 'y':
                    print("----FILE:" + os.path.join(root, name))
                    print("--FINAL--") 
                    print("BODY-b:"+str(obb))
                    print ("BODY-c:"+str(obc))                    

sys.stdout = csl

print ("Files Found")

#Math:
for list in BInit, CInit, BFin, CFin:
    Repair(list)
    Degrees(list)

#Plotting:

fig, ax = plt.subplots(2,2, sharex=False);                                  
fig.set_size_inches(8,6);                                                 
#fig.suptitle("Tidal Heating Plot", fontsize=12);
fig.tight_layout(pad=2, w_pad=1.5);      

ax[0,0].hist(BInit, bins=50, facecolor='DimGray');
ax[0,0].set_xlabel('Initial Surface Flux of b (MW/m$^{2}$)', fontsize=10);
ax[0,0].set_ylabel('Number', fontsize=10);
ax[0,0].set_xticklabels(["0", "1", "2"]);
ax[0,0].set_xticks([0, 1000000, 2000000]);
ax[0,0].set_xlim(0,2000000);
#ax[0,0].set_xscale('log')

ax[0,1].hist(CInit, bins=75, facecolor='Gray');
ax[0,1].set_xlabel('Initial Surface Flux of c (kW/m$^{2}$)', fontsize=10);
ax[0,1].set_xticklabels(["0", "3", "6", "10"]);
ax[0,1].set_xticks([0, 3000, 6000, 10000]);
ax[0,1].set_xlim(0,10000);
#ax[0,1].set_xscale('log');


ax[1,0].hist(BFin, bins=25, facecolor='DimGray');
ax[1,0].set_xlabel('Final Surface Flux of b (W/m$^{2}$)', fontsize=10);
ax[1,0].set_ylabel('Number', fontsize=10);
#ax[1,0].set_xticklabels(["0", "1", "2", "3"]);
#ax[1,0].set_xticks([0, 1, 2, 3]);
#ax[1,0].set_xlim(0,3);
#ax[1,0].set_yscale('log');
ax[1,0].set_xscale('log');


ax[1,1].hist(CFin, bins=25, facecolor='Gray');
ax[1,1].set_xlabel('Final Surface Flux of c (W/m$^{2}$)', fontsize=10);
#ax[1,1].set_xticklabels(["0", "0.1", "0.2", "0.5", "1"]);
#ax[1,1].set_xticks([0, 0.1, 0.2, 0.5, 1]);
ax[1,1].set_xscale('log');
ax[1,1].set_yscale('log');

plt.show()

if (sys.argv[1] == 'pdf'):
    fig.savefig("THeP.pdf", bbox_inches="tight", dpi=600)
if (sys.argv[1] == 'png'):
    fig.savefig("THeP.png", bbox_inches="tight", dpi=600)
