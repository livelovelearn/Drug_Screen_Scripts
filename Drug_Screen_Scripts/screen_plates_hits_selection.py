# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 16:54:30 2015

@author: Yancheng Liu
"""

import os
import glob
import numpy as np
from StringIO import StringIO

path = "C:\Users\Liu\Desktop\Screen_Plate_Analysis\Samples\\" ## change file path here

out_file1 = open(path+"inhibitor_hits.txt", "a")
out_file1.write("Barcode,Location,Value\n")
out_file2 = open(path+"enhancer_hits.txt", "a")
out_file2.write("Barcode,Location,Value\n")
out_file3 = open(path+"inhibitor_hits_by_percent_inhibition.txt", "a")
out_file3.write("Barcode,Location,Value,%inhibition\n")

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
    
    all_data = data[:, 1:25]
    sample_data = data[:,1:23]   # use this or all_data for calculation? 
    
    #statistical analysis    
    average = np.mean(sample_data)
    stDev = np.std(sample_data, ddof=1)
    lower_bound = average - 3*stDev
    upper_bound = average + 3*stDev
    DMSO = np.mean(all_data[:,23])
    RIF_high = np.mean(all_data[:8,22])
    RIF_inhibition = DMSO - RIF_high
    
    
    #select the hits
    rowName = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P']
    inhibitors = ""
    enhancers = ""
    inhibitors_by_percent_inhibition = ""
    
    for row in range (16):
        for col in range (22):
            if sample_data[row][col] < lower_bound:
                inhibitors += rowName[row]+str(col+1)+","+str(sample_data[row][col])+","
            if sample_data[row][col] > upper_bound:
                enhancers += rowName[row]+str(col+1)+","+str(sample_data[row][col])+","
            if (DMSO-sample_data[row][col])/(RIF_inhibition) > 0.7:
                inhibitors_by_percent_inhibition += rowName[row]+str(col+1)+","+str(sample_data[row][col])+\
                ","+ str((DMSO-sample_data[row][col])/(RIF_inhibition)*100)+","
    
    # output analysis
    out_file1.write(barcode+','+inhibitors+'\n')
    out_file2.write(barcode+','+enhancers+'\n')
    out_file3.write(barcode+','+inhibitors_by_percent_inhibition+'\n')
    
out_file1.close()
out_file2.close()
out_file3.close()