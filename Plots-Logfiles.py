#!/usr/bin/env python
# coding: utf-8
# CREATED BY ALI ABOU TAKA
# THIS PYTHON PROGRAM  HAS DIFFERENT FUNCTION THAT CAN BE USED
# TO EXTRACT DESIRED INFORMATION FOR LOG FILES
# BE CAREFULL WHAT FUNCTION YOU CALL AND WHAT PATH YOU PROVIDE. 

import warnings
warnings.filterwarnings(action='ignore')
import glob
import re
import numpy as np
from numpy import genfromtxt
import scipy
from scipy import stats, optimize, interpolate
import matplotlib
from matplotlib import pyplot as plt
import matplotlib.style as style
import os
import sys

####
if len(sys.argv) < 2 or  len(sys.argv) > 2 :
    print('You need  two arguments: name of the file and the path to the folder')
    sys.exit(0)
####    
##################################################
# This Function will grab the energy at each cycle
##################################################
def GrabEnrg(directory):
    filenameL=[]
    for filename in os.listdir(directory):      
        if filename.endswith(".log"):
            filenameL.append(filename)
    for file in filenameL:
        file=os.path.join(directory,file)
        EnergyL=[]
        with open (file,'r') as f:
            for line in f:
                if "E= " in line:
                    words = line.split()
                    if (words[0] =="E="):
                        energyval=float(words[1])
                        EnergyL.append(energyval)
        #     print (EnergyL)
        xEnergyL=list(range(len(EnergyL)))
        plt.plot(xEnergyL,EnergyL,label=os.path.splitext(os.path.split(file)[1])[0])     
#         style.use('seaborn-poster') #sets the size of the charts
        style.use('seaborn-talk')
#         style.use('ggplot')
        plt.xlabel('Number of SCF iterations')
        plt.ylabel('Energy in (a.u.)')
#       Making a small box under the plot for the legend
        ax = plt.subplot(111)   
        box = ax.get_position()    
        ax.set_position([box.x0, box.y0 + box.height * 0.1,
                       box.width, box.height * 0.9])

#       Put a legend below current axis
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.4),
                  fancybox=True, shadow=True, ncol=5)
#   Save the plot 
#    plt.show(block=False)
### TO BE ABLE TO ZOOM USING THE SCRIPT, MAKE SURE TO USE plt.show(), so you can
### SEE THE PLOT, ZOOM AND SAVE IT.
    plt.savefig(os.path.join(directory,'EatEachSCF.png'),dpi=300,bbox_inches='tight')
    plt.close()


######################################################
# This Function will grab the DIIS Error at each cycle
######################################################
def GrabDIIS(directory):
    filenameL=[]
    for filename in os.listdir(directory):
        if filename.endswith(".log"):
            filenameL.append(filename)
#     print (filenameL)
    for file in filenameL:
        file=os.path.join(directory,file)
        DIISL=[]
        with open (file,'r') as f:
            for line in f:
                if "DIIS: error=" in line:
                    line = line.replace("D","e")
                    words = line.split()
                    DIIS = float(words[2])
                    DIISL.append(DIIS) 
    #     print(DIISL)
        xDIISL=list(range(len(DIISL)))
        plt.plot(xDIISL,DIISL,label=os.path.splitext(os.path.split(file)[1])[0])
#         style.use('seaborn-ticks')
#         style.use('seaborn-poster') #sets the size of the charts
        style.use('seaborn-talk')
#         style.use('ggplot')
        plt.xlabel('Number of SCF iterations')
        plt.ylabel('DIIS Error in (a.u.)')
#       Making a small box under the plot for the legend
        ax = plt.subplot(111)
        box = ax.get_position()    
        ax.set_position([box.x0, box.y0 + box.height * 0.1,
                         box.width, box.height * 0.9])

        # Put a legend below current axis
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.4),
                  fancybox=True, shadow=True, ncol=5)
#    plt.show(block=False)
### TO BE ABLE TO ZOOM USING THE SCRIPT, MAKE SURE TO USE plt.show(), so you can
### SEE THE PLOT, ZOOM AND SAVE IT.
    plt.savefig(os.path.join(directory,'DIIS.png'),dpi=300,bbox_inches='tight')
    plt.close()

#################################################
# This Function will grab the RMSDP at each cycle
#################################################
def GrabRMSDP(directory):
    ref=(glob.glob('*ref.log'))
    ref1 = "" 
    for ele in ref:  
        ref1 += ele
    filenameL=[]
    for filename in os.listdir(directory):
        if filename.endswith(".log"):
            filenameL.append(filename)
#     print (filenameL)
    for file in filenameL:
        file=os.path.join(directory,file)
        if file == ref1:
            continue    
        RMSDPL=[]
        with open (file,'r') as f:
            for line in f:
                if "RMSDP" in line:
                    line = line.replace("="," ")
                    line = line.replace("D","e")
                    words = line.split()
                    RMSDP = float(words[1])
                    RMSDPL.append(RMSDP) 
#             print(RMSDPL)
        xRMSDPL=list(range(len(RMSDPL)))
        plt.plot(xRMSDPL,RMSDPL,label=os.path.splitext(os.path.split(file)[1])[0])    
#         style.use('seaborn-poster') #sets the size of the charts
        style.use('seaborn-talk')
#         style.use('ggplot'
        plt.xlabel('Number of SCF iterations')
        plt.ylabel('RMSDP in (a.u.)')
#       Making a small box under the plot for the legend
        ax = plt.subplot(111)    
        box = ax.get_position()    
        ax.set_position([box.x0, box.y0 + box.height * 0.1,
                         box.width, box.height * 0.9])

        # Put a legend below current axis
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.4),
                  fancybox=True, shadow=True, ncol=5)
# UNCOMMENT the lines below if you wonna save a figure
### TO BE ABLE TO ZOOM USING THE SCRIPT, MAKE SURE TO USE plt.show(), so you can
### SEE THE PLOT, ZOOM AND SAVE IT.
    plt.savefig(os.path.join(directory,'RMSDP.png'),dpi=300,bbox_inches='tight')
    plt.close()


#### RUNNING THE FUCNTIONS
#### REMEBER TO PROVIDE THE PATH IF THE CODE AND THE FILES ARE NOT IN THE SAME FOLDER
####
#if len(sys.argv) < 2 or  len(sys.argv) > 2 :
#    print('You need  two arguments: name of the file and the path to the folder')
#    sys.exit(0)
#elif len(sys.argv) == 2:

GrabEnrg(sys.argv[1])
#####

GrabDIIS(sys.argv[1])
#####

GrabRMSDP(sys.argv[1])
####



