#!/usr/bin/env python3
# coding=utf-8
"""
Created on Tue May 29 12:56:51 2018

@author: gurpide
"""

import numpy as np
import matplotlib.pyplot as plt
import os
from optparse import OptionParser


#line colors; add more if needed
colors=['b','green','orange','','deepskyblue','orange']
theshold_colors=["red", "aqua"]

#planck constant
h=4.135666733*pow(10,-15)
#speed of light
c=2.99792458*pow(10,8)
#detection thresholds path
detection_thresholds_path='/lines/detection_thresholds.txt'



#output dir for the plot
outputdir="linescanplots"
#velocity dispersions in km/s to be processed
velocity_dispersions = [500,1000,2000]

#read arguments
parser = OptionParser()
parser.add_option("-E", "--energy",dest="max_energy",
                  help="Last energy to be processed",default=1.5, type='float')

(options, args) = parser.parse_args()
#set the number of spectra to be read to infinite
max_energy=options.max_energy
#get current working directory
working_directory=os.getcwd()

   
fig = plt.figure(figsize=(16.0, 10.0))
     #set figure labels
ax1 = fig.add_subplot(111)
ax1.set_xlabel('Energy (keV)')
ax1.set_ylabel('$\Delta$ C-stat')
#ax1.set_title('HolmbergXII',y=1.08) 
ax2 = ax1.twiny() 
ax2.set_xlabel('$\lambda$ ($\AA$)')
colorindex=0
theshold_colors_index=0
energy_points =[]
#traverse each delta v
for deltav in velocity_dispersions:
    #create each window for each figure
 plt.rc('font', size=24)     
#traverse each directory
 cstatlinescan_file=working_directory+'/linescan/cstatlinescan_%i.dat' %deltav
#find each output file from a cstat line scan
 if os.path.isfile(cstatlinescan_file):
            with open(cstatlinescan_file) as f:
                print 'Reading file: '+cstatlinescan_file
                lines = f.readlines()            
                print "Read %i lines from file %s " %(len(lines),cstatlinescan_file)    
                #convert energy to wavelength
                expression= (line for line in lines if not line.startswith("\n"))
                y = []
                energy_points = []
                
                for line in expression:
                    delta=float(line.split("\t")[2])
                    #skip negative delta C
                    if delta<0.0:
                        print "Warning! Found " +line +" with negative delta C %.3f" %delta
                        continue
                    energy =float(line.split("\t")[3])
                
                    energy_points.append(energy)
                #norm of the line
                    norm=float(line.split("\t")[4])
                #change sign of delta according to the normalization for plotting purposes (absorption/emission lines)
                   
                    
                    if norm>= 0.0:
                        y.append(delta)
                    else:
                        y.append(-float(delta))
                      #process the file only until desired energy
                    if energy>max_energy:
                        print "Maximum energy %.3f reached. Closing file..." %max_energy
                        break;
    #get a difference color for each line
                ax1.plot(energy_points,y, c=colors[colorindex], label="%i km/s"%deltav,linewidth=2)
             #   ax1.scatter(energy_points,y, c=colors[colorindex], label="Sampling")
               
                
                if deltav==500:
                    #read detection thresholds file to plot the 3 sigma detection threshold
                    detection_thresholds_full_path=working_directory+""+detection_thresholds_path
                    if os.path.isfile(detection_thresholds_full_path):
                        print 'Found detection thresholds file: '+detection_thresholds_full_path
                        with open(detection_thresholds_full_path) as thresholds_file:
                        #skip the # symbol for the header
                            thresholds = thresholds_file.readlines()  
                            expression= (line for line in thresholds if not line.startswith("#"))
                            energy_thresholds = []
                            three_sigma_deltaC = []
                            three_sigma_negative_deltaC=[]
                            for line in expression:
                                     print line.split("\t")[0]
                                     energy_thresholds.append(float(line.split("\t")[0]))
                                     three_sigma_deltaC.append(float(line.split("\t")[1]))
                                     three_sigma_negative_deltaC.append(-float(line.split("\t")[1]))
                        ax1.plot(energy_thresholds,three_sigma_deltaC, theshold_colors[theshold_colors_index], label="3$\sigma$",marker="^")  
                        ax1.plot(energy_thresholds,three_sigma_negative_deltaC, theshold_colors[theshold_colors_index], label="3$\sigma$",marker="^")           
                        theshold_colors_index=theshold_colors_index+1         
                colorindex=colorindex+1
                
          
 else:
            continue
      
               
#check if any file was found, that is if x is empty or not
 if energy_points:
    #horizontal line    
 
        plt.axhline(y=0, color='black') 
        #line to highlight a particular energy
       # plt.axvline(x=0.972, color='red',linestyle='--',linewidth=1)
        ax1.set_xticks(np.arange(0.5,1.5, 0.1))
    
        ax1.set_xlim(0.5,1.5)
        #ax1.set_ylim(-10,13)
 
        xticks = ax1.get_xticks()
        x2labels = ['{:01.2f}'.format(w) for w in 10**7*h*c/xticks]
        ax2.set_xticks(xticks)
        ax2.set_xticklabels(x2labels)
        ax2.set_xlim(ax1.get_xlim())
        ax1.set_xlim(0.5,1.5)
    #put legend inside the plot
        leg = ax1.legend(bbox_to_anchor=(0.9,0.9), prop={'size': 17}, bbox_transform=plt.gcf().transFigure) 
    #save figure
        plt.savefig(outputdir+'/energydeltacstat_multiple_%.3f.pdf' %max_energy,bbox_inches='tight')       

 else:
        print "No cstat scan line files were found for velocity dispersion: %i" %deltav

            
#plt.show()
        