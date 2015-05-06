# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 16:54:30 2015

@author: Yancheng Liu
"""

import os
import glob
import numpy as np
from StringIO import StringIO

path = "C:\Users\Liu\Desktop\Screen_Plate_Analysis\Samples\\" ## change file path here

out_file = open(path+"summary.txt", "a")
out_file.write("Barcode,Perimeter,Center,Difference,Edge_effect,Average,StDev,CoV,Z-factor\n")

for file_name in glob.glob(os.path.join(path, '*.csv')):
    data_string = ''
    barcode=''
    
    #load data
    my_file = open(file_name, "r")
    for i in range(10):
        if i == 2:
            barcode = my_file.readline().split(",")[2]
        else:
            my_file.readline()
    for i in range(16):
        data_string += my_file.readline()
    my_file.close()
    
    data = np.genfromtxt(StringIO(data_string),
        delimiter=","
        )
    
    data = data[:, 1:25]
    sample_data = data[:,1:23]
    
    #statistical analysis
    perimeter = (sum(data[0,:]) + sum(data[15,:]) + sum(data[1:15,0]) + sum(data[1:15, 23]))/76
    center = np.mean(data[1:15,1:23])
    difference = perimeter - center
    #print difference
    
    edge_effect = round(difference/perimeter * 100, 1)
    #print edge_effect
    
    average = np.mean(sample_data)
    #print average
    
    stDev = np.std(sample_data, ddof=1)
    #print stDev
    
    coV = stDev/average
    #print coV
    
    z=1-(np.std(data[:,23], ddof=1)*3 + np.std(data[:8,22], ddof=1)*3)/abs(np.mean(data[:,23])-np.mean(data[:8,22]))
    #print z
    
    # output analysis
    out_file.write(barcode+','+str(perimeter)+','+str(center)+','+str(difference)+','+str(edge_effect)+\
    ','+str(average)+','+str(stDev)+','+str(coV)+','+str(z)+'\n')

out_file.close()
