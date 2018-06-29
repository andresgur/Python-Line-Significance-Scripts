#Same as plotcstat.py but all observations for a given source together. All the obsid_directories for the observations with the 
#line scan files inside them have to be in the working obsid_directory
# Author: Andres Gurpide Lasheras  andres.gurpide@gmail.com
    #!/usr/bin/env python3
    # coding=utf-8

#imports
import numpy as np
import matplotlib.pyplot as plt
import os


#line colors; add more if needed
colors=['b','green','orange','red','deepskyblue','orange']
#velocity dispersions in km/s to be processed
velocity_dispersions = [500,1000,2000]

#planck constant
h=4.135666733*pow(10,-15)
#speed of light
c=2.99792458*pow(10,8)
#detection thresholds path
detection_thresholds_path='/lines/detection_thresholds.txt'
#line scan folders
line_scan_folders='linescan'

#output dir for the plot
outputdir="linescanplots"

#get current working obsid_directory
working_obsid_directory=os.getcwd()


#create output dir if it does not exist
if not os.path.exists(outputdir):
    os.makedirs(outputdir)


obsid_directories=os.listdir(working_obsid_directory)

#sort observations by date (id)
obsid_directories.sort()

#traverse each delta v
for deltav in velocity_dispersions:
    print 'Looking for files with velocity %i' %deltav
    #Prepare plot
    fig = plt.figure(figsize=(16.0, 10.0))
    #set figure labels
    ax1 = fig.add_subplot(111)
    ax1.set_xlabel('Energy (keV)')
    ax1.set_ylabel('$\Delta$ C-stat (rescaled)')
    #ax1.set_title('HolmbergXII',y=1.08) 

    #set second axis with wavelength
    ax2 = ax1.twiny() 
    ax2.set_xlabel('$\lambda$ ($\AA$)')  
        
    #create each window for each figure
    plt.rc('font', size=24)     
    
    #reset variables for new plot
    colorindex=0
    theshold_colors_index=0
    energy_points =[]
    #initial y axis position
    y_axis_shift=-50
    y_shift=25

    #traverse the observation directories
    for obsid_directory in obsid_directories:
        print "Processing obs: " + obsid_directory

        #traverse each obsid_line scan file
        cstatlinescan_file=obsid_directory+ "/" + line_scan_folders + '/cstatlinescan_%i.dat' %deltav
        
        y = []
        energy_points = []        
        
        if os.path.isfile(cstatlinescan_file):
            with open(cstatlinescan_file) as f:
                print 'Reading file: '+cstatlinescan_file
                lines = f.readlines()            
                print "Read %i lines from file %s " %(len(lines),cstatlinescan_file)    
                
                #skip lines starting with new line character
                expression= (line for line in lines if not line.startswith("\n"))
                
                for line in expression:
                    delta=float(line.split("\t")[2])
                    #skip negative delta C
                    if delta<0.0:
                        print "Warning! Found " +line +" with negative delta C %.3f" %delta
                        continue
                    #retrieve energy
                    energy =float(line.split("\t")[3])
                    energy_points.append(energy)
                    #norm of the line
                    norm=float(line.split("\t")[4])
                    #change sign of delta according to the normalization for plotting purposes (absorption/emission lines)
                    if norm>= 0.0:
                        y.append(delta)
                    else:
                        y.append(-float(delta))

                    #horizontal line at Delta C 0 value for each data set
                plt.axhline(y=y_axis_shift, color='black') 
                #get a difference color for each line   
                #shift the y axis level for each observation       
                ax1.plot(energy_points,[a+y_axis_shift for a in y] , c=colors[colorindex], label=obsid_directory,linewidth=2)
                colorindex=colorindex+1
                
                y_axis_shift=y_axis_shift+y_shift
               
                #ax1.scatter(energy_points,y, c=colors[colorindex], label="Sampling")                            
                                                    
        #check if any file was found, that is if x is empty or not
        if energy_points:
    
         
           # plt.axhline(y=25, color='black')                                                            
           # plt.axhline(y=0, color='black') 
           # plt.axhline(y=-25, color='black') 
           # plt.axhline(y=-50, color='black') 
            #vertical line to highlight a particular energy
            #plt.axvline(x=0.583, color='black',linestyle='--',linewidth=1)
            #plt.axvline(x=0.972, color='black',linestyle='--',linewidth=1)
            #plt.axvline(x=0.870, color='black',linestyle='--',linewidth=1)
            #plt.axvline(x=0.565, color='black',linestyle='--',linewidth=1)
            #plt.axvline(x=0.848, color='black',linestyle='--',linewidth=1)
            #plt.axvline(x=0.867, color='black',linestyle='--',linewidth=1)
            #plt.axvline(x=0.554, color='black',linestyle='--',linewidth=1)
            
    
            #add ionic species of each of the identified lines
            # plt.text(0.570, 37, 'O VII', fontsize=15)    
            # plt.text(0.853, -67, 'Fe XVIII', fontsize=15)
            # plt.text(0.54, -65, 'O VII', fontsize=15)    
            # plt.text(0.78, -19, 'Fe XVII/Fe XVIII', fontsize=15)
            # plt.text(0.854, -15, 'Fe XVIII', fontsize=15)
            # plt.text(0.960, -13, 'Fe XXI', fontsize=15)
            # plt.text(0.550, 21, 'O VII', fontsize=15)
        
            #format x axis 
            max_energy=max(energy_points)
            min_energy=min(energy_points)
            ax1.set_xticks(np.arange(min_energy,max_energy, 0.1))
            ax1.set_xlim(min_energy,max_energy)
        
            #y axis, tick at each 0 C value level
            #ax1.set_yticks(np.arange(-50,50,y_shift))
            
            #add wavelength x axis                                                       
            xticks = ax1.get_xticks()
            x2labels = ['{:01.2f}'.format(w) for w in 10**7*h*c/xticks]
            ax2.set_xticks(xticks)
            ax2.set_xticklabels(x2labels)
            ax2.set_xlim(ax1.get_xlim())
    
            #put legend inside the plot
            leg = ax1.legend(bbox_to_anchor=(0.9,0.58), prop={'size': 14}, bbox_transform=plt.gcf().transFigure) 
        
            #save figure
            plt.savefig(outputdir+'/energydeltacstat_multiple_%i.pdf' %deltav,bbox_inches='tight')
                                                        
        else:
            print "No cstat scan line files were found for velocity dispersion for %s: %i" %(obsid_directory,deltav)
                                                                                                                        
    plt.show()
                                                                        