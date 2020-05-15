#!/usr/bin/env python
# coding: utf-8
# CREATED BY ALI ABOU TAKA
# THIS PYTHON PROGRAM  HAS DIFFERENT FUNCTIONS THAT CAN BE USED
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

##################################################
# This Function will grab the energy at each cycle
##################################################
def GrabEnrg(directory):
    filenameL=[]
    filenameLL=[]
    x_keys =  []
    y_values= []
    markers=[4,5,6,7,'s','P', '^',"*",'X']
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
            x_keys.append(list(range(len(EnergyL))))
#                 print(x_keys)
            y_values.append(EnergyL)
            filenameLL.append(os.path.splitext(os.path.split(file)[1])[0])

        zipped_list= list(zip(x_keys,y_values,markers,filenameLL))
#         print(zipped3)
    for x,y,z,fn in zipped_list:
#         ax.plot(i,j, linestyle = '', marker=next(markers))
        plt.plot(x,y,label=fn,marker=z,linewidth=0.5)
        style.use('seaborn-talk')
        ax = plt.subplot(111)
        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + box.height * 0.1,
                         box.width, box.height * 0.9])
        ax.set_xlabel('Number of SCF iterations')
        ax.set_ylabel('Energy in (a.u.)')

        # Put a legend below current axis
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.4),
                  fancybox=True, shadow=True, ncol=5)
# UNCOMMENT the lines below if you wonna save a figure
    plt.savefig(os.path.join(directory,'EatEachSCF.png'),dpi=300,bbox_inches='tight')
    plt.close()



######################################################
# This Function will grab the DIIS Error at each cycle
######################################################
def GrabDIIS(directory):
    filenameL=[]
    filenameLL=[]
    x_keys =  []
    y_values= []
    markers=[4,5,6,7,'s','P', '^',"*",'X']
#
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
            x_keys.append(list(range(len(DIISL))))
#                 print(x_keys)
            y_values.append(DIISL)
            filenameLL.append(os.path.splitext(os.path.split(file)[1])[0])

        zipped_list= list(zip(x_keys,y_values,markers,filenameLL))
#         print(zipped3)
    for x,y,z,fn in zipped_list:
#         ax.plot(i,j, linestyle = '', marker=next(markers))
        plt.plot(x,y,label=fn,marker=z,linewidth=0.5)
        style.use('seaborn-talk')
        ax = plt.subplot(111)
        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + box.height * 0.1,
                         box.width, box.height * 0.9])
        ax.set_xlabel('Number of SCF iterations')
        ax.set_ylabel('DIIS Error in (a.u.)')

        # Put a legend below current axis
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.4),
                  fancybox=True, shadow=True, ncol=5)
# UNCOMMENT the lines below if you wonna save a figure
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
    filenameLL=[]
    x_keys =  []
    y_values= []
    markers=[4,5,6,7,'s','P', '^',"*",'X']
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
            x_keys.append(list(range(len(RMSDPL))))
#                 print(x_keys)
            y_values.append(RMSDPL)
            filenameLL.append(os.path.splitext(os.path.split(file)[1])[0])

#                 print(y_values)

#             print(RMSDPL)
        zipped_list= list(zip(x_keys,y_values,markers,filenameLL))
#         print(zipped_list)
    for x,y,z,fn in zipped_list:
#         ax.plot(i,j, linestyle = '', marker=next(markers))
        plt.plot(x,y,label=fn,marker=z,linewidth=0.5)
        style.use('seaborn-talk')
        ax = plt.subplot(111)
        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + box.height * 0.1,
                         box.width, box.height * 0.9])
        ax.set_xlabel('Number of SCF iterations')
        ax.set_ylabel('RMSDP in (a.u.)')

        # Put a legend below current axis
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.4),
                  fancybox=True, shadow=True, ncol=5)
# UNCOMMENT the lines below if you wonna save a figure
    plt.savefig(os.path.join(directory,'RMSDP.png'),dpi=300,bbox_inches='tight')
    plt.close()
#### RUNNING THE FUCNTIONS
#### REMEBER TO PROVIDE THE PATH IF THE CODE AND THE FILES ARE NOT IN THE SAME FOLDER
####
GrabEnrg(sys.argv[1])
#####

GrabDIIS(sys.argv[1])
#####

GrabRMSDP(sys.argv[1])
####

