#!/usr/bin/python
# coding: utf-8



# This program extract MO matrices from fchk or fmat files and calculate SVD




import math
import cmath
import numpy as np
from numpy import array
from numpy import diag
from numpy import dot
from numpy import zeros


# This function will grab NBasis 
def NBasGrab(filename):
    NBasis = 0
    with open(filename, 'r') as f:
        if filename.endswith('.fmat'):
            for line in f:
                if "NBasis" in line:
                    words = line.split()
                    for i in words:
    #                     print (words[3])
                        NBasis = int(words[3])
        elif filename.endswith('.fchk'):
            for line in f:
                if "Number of basis functions" in line:
                    words = line.split()
                    for i in words:
                        for letter in i:
                            if(letter.isdigit()):
                                NBasis = NBasis*10 + int(letter)
        else:
            print('The file extension is not supported. This script only supports fchk and fmat.')

    return NBasis


# This function will grab NBasis 
def MatGrab(filename,switch):
#   Get number of basis functions    
    NBasis=NBasGrab(filename)
#################################    
    with open(filename,'r') as f:
#       FMAT FILES
        if filename.endswith('.fmat'):
#           Initializing variables for fmat file    
            Exlines = int(math.ceil(NBasis/5))
            MOlines =int(Exlines+(NBasis*Exlines))
            MOrawa=[]
            MOrawb=[]
            MOFull=[]
            MOA=[]
            MOB=[]            
            if (switch == 1):                
#           Extract Alpha MO coefficient                
                for line  in f:
                    if  "ALPHA MO COEFFICIENTS" in line:
                        for m in range(0,MOlines):
                            nextline = next(f)
                            nextline = nextline.split()
                            MOrawa.append(nextline)       
#                       Clean header rows and columns
                        for n in range(0,len(MOrawa)-Exlines,NBasis):
                            del MOrawa[n] 
                        for n in range(len(MOrawa)):
                            del MOrawa[n][0]

#                       For NBasis > 5, the matrix is stored in chunks. temp is equal to the number chunks.
                        temp=int((len(MOrawa)/NBasis))
#        
#                       Create a copy of the first chunk of the matrix which is equal to NBasis.   
#                       Start filling the empty list "MOFull"                    
                        for i in range(0,NBasis):
                            MOFull.append(MOrawa[i])                            
#                         
#                       "Extend" the list "MOFull" by the chunks left to match the NBasis x NBasis matrix
                        for k in range(1,temp+1):
                            for j in range(0,NBasis):
                                for i in range(len(MOrawa)):
                                    if i==j+(NBasis*k):
                                        MOFull[j].extend(MOrawa[i])                    
#               Concatenate the list into one array    
                ConcMOFull = np.array(np.concatenate([np.array(i) for i in MOFull]))
#               Create another list to "float" all the elements 
                for item in ConcMOFull:
                    MOA.append(float(item))
#               Reshape the matrix into NBasis by NBasis           
                MOCoeffA = np.reshape(MOA,(NBasis,NBasis))
#               Return  MOCoeffA
                return MOCoeffA
        #
            elif (switch == -1):
#           Extract Beta MO coefficient                
                for line  in f:
                    if  "BETA MO COEFFICIENTS" in line:
                        for m in range(0,MOlines):
                            nextline = next(f)
                            nextline = nextline.split()
                            MOrawb.append(nextline)     
        #                   Clean header rows and columns                        
                        for n in range(0,len(MOrawb)-Exlines,NBasis):
                            del MOrawb[n] 
                        for n in range(len(MOrawb)):
                            del MOrawb[n][0]
        #                   For NBasis > 5, the matrix is stored in chunks. temp is equal to the number chunks.
                        temp=int((len(MOrawb)/NBasis))
        #    
        #                   Create a copy of the first chunk of the matrix which is equal to NBasis.   
        #                   Start filling the empty list "MOFull"                    
                        for i in range(0,NBasis):
                            MOFull.append(MOrawb[i])                            
        #            
        #                   "Extend" the list "MOFull" by the chunks left to match the NBasis x NBasis matrix
                        for k in range(1,temp+1):
                            for j in range(0,NBasis):
                                for i in range(len(MOrawb)):
                                    if i==j+(NBasis*k):
                                        MOFull[j].extend(MOrawb[i])                    
        #           Concatenate the list into one array    
                ConcMOFull = np.array(np.concatenate([np.array(i) for i in MOFull]))
        #           Create another list to "float" all the elements 
                for item in ConcMOFull:
                    MOB.append(float(item))
        #           Reshape the matrix into NBasis by NBasis           
                MOCoeffB = np.reshape(MOB,(NBasis,NBasis))
        #       
                return MOCoeffB
######################################################################################################################
######################################################################################################################
#       FCHK FILES
        elif filename.endswith('.fchk'):
#           Initializing variables for fchk file
            MOElements = NBasis * NBasis
            MOlines = int(MOElements/5) + 1
            p = 0
            r = 0
            AOE = 0
            MOrawa = np.zeros(NBasis*NBasis)
            MOrawb = np.zeros(NBasis*NBasis)            
            if (NBasis%5 == 0):
                MOlines = MOlines - 1
#           Extract Alpha MO coefficient  
            if (switch == 1):
                with open(filename,'r') as origin:
                    for i, line  in enumerate(origin):
                        if "Alpha Orbital Energies" in line:
                            AOE = i
                        if  "Alpha MO coefficients" in line:
                            i=i+1
                            AMO=i
                            j=i+MOlines-1
                            for m in range(0,j-i+1):
                                nextline = next(origin)
                                nextline = nextline.split()
                                for p in range(p,len(nextline)):
                                    MOrawa[r] = nextline[p]
                                    r = r+1
                                p = 0
                # Reshape the array into NBasis by NBasis matrix                        
                MOCoeffA = np.reshape(np.array(MOrawa),(NBasis,NBasis),order='F')
                return MOCoeffA
            if (switch == -1):
#           Extract Beta MO coefficient                
                with open(filename,'r') as origin:
                    for i, line  in enumerate(origin):
                        if "Beta Orbital Energies" in line:
                                BOE = i
                        if  "Beta MO coefficients" in line:
                            i=i+1
                            BMO=i
                            j=i+MOlines-1
                            for m in range(0,j-i+1):
                                nextline = next(origin)
                                nextline = nextline.split()
                                for p in range(p,len(nextline)):
                                    MOrawb[r] = nextline[p]
                                    r = r+1
                                p = 0
#               Reshape the array into NBasis by NBasis matrix
                MOCoeffB = np.reshape(np.array(MOrawb),(NBasis,NBasis),order='F')
                return MOCoeffB
        else:
            print('The file extension is not supported. This script only supports fchk and fmat.')
########################

#######################
##### AO OVERLAP ######
#######################
def FrmAOOverlap(A):
    CInv = np.linalg.inv(A)
    S = np.dot(np.transpose(CInv),CInv)
    return S


AOOverlap=FrmAOOverlap(MatGrab("H2O.fmat",1))
print(AOOverlap)


AOOverlapfc=FrmAOOverlap(MatGrab("h2o.fchk",-1))
print(AOOverlapfc)



#######################
#####Sanity Checks#####
#######################
MOCoeff =(MatGrab('H2O.fmat',1))
MOCoeffT=np.transpose(MOCoeff)
print ("MOCoeff")
print (MOCoeff)
print ("AO Overlap")
print (AOOverlap)
# You should get IDENTITY matrix 
print ("CT.AOS.C")
print((np.matmul(np.matmul((MOCoeffT),AOOverlapfc),MOCoeff)))

#########################################
######## EXAMPLE on H2 MOLECULE #########
#########################################
#
# Pulling the Coeff. from the first file
filename ='h2.fchk'
# you can hhave different files, but they should have same dimensions
filename2 = 'h2.fchk'
switch = 1
MOCoeff1 = MatGrab(filename,1)
#
# Pulling the Coeff. from the Second file
MOCoeff2 = MatGrab(filename2,1)
#
# Printing the coeff 
print(" MOCoeff. of ",filename)
print(MOCoeff1)
print("")
print(" MOCoeff. of ",filename2)
print(MOCoeff2)


# Calculate the overlap between the two MOCoeffs. with and without the AO overlap
MOOverlap  = np.matmul(np.transpose(MOCoeff1),MOCoeff2)
MOOverlapS = np.matmul(np.matmul((MOCoeffT),AOOverlapfc),MOCoeff)
#
# Optional printing - uncomment it if needed
# print" MO Overlap is ", MOOverlap

######################################
###########CALCULATING SVD############
######################################

#      A = U * SIGMA * VT
#      VT = transpose(V)
#      where SIGMA is an M-by-N  diagonal matrix i.e is zero except for its
#      min(m,n) diagonal elements, U is an M-by-M orthogonal matrix, and
#      V is an N-by-N orthogonal matrix.  The diagonal elements of SIGMA
#      are the singular values of A; they are real and non-negative, and
#      are returned in descending order.  The first min(m,n) columns of
#      U and V are the left and right singular vectors of A.
# SVD

U, s, VT = np.linalg.svd(MOOverlap)
print("U is ",(U))
print("SIGMA is ",(s))
print("V-Transpose is ",(VT))
print("V is ",(np.transpose(VT)))



# We can also reconstruct the matrix using the diagonal matrix
# First, form the diagonal matrix from s
Sigma = diag(s)
print("sigma" ,Sigma)



# Reconstruct the initial matrix
Reconstructed_MOOverlap = U.dot(Sigma.dot(VT))


print("Reconstructed_AAOverlap", Reconstructed_MOOverlap)
print(" ")
print("MOOverlap is", MOOverlap)





