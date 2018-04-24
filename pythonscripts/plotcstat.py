#Script to plot the delta C-stat vs energy for a line scan throughout a spectrum. The program will traverse each directory looking for the cstatlinescan.dat file and finally will plot all the observations found together
# Author: Andres Gurpide Lasheras  andres.gurpide@gmail.com
import numpy as np
import matplotlib.pyplot as plt
import os

#line colors; add more if needed
colors=['b','olivedrab','r','magenta','deepskyblue','orange']

#planck constant
h=4.135666733*pow(10,-15)
#speed of light
c=2.99792458*pow(10,8)

#velocity dispersions in km/s to be processed
velocity_dispersions = [0,500,1000]

#get current working directory
working_directory=os.getcwd()

dirnames=os.listdir(working_directory)
#traverse each delta v
for deltav in velocity_dispersions:
    #create each window for each figure
#specify size of the window
   
    fig = plt.figure(figsize=(16.0, 10.0))
     #set figure labels
    ax1 = fig.add_subplot(111)
    ax1.set_xlabel('lambda (Angstrom)')
    ax1.set_ylabel('deltaC-stat')
    ax1.set_title('HolmbergXII, velocity dispersion: %i km/s' %deltav,y=1.08) 
    ax2 = ax1.twiny() 
    ax2.set_xlabel('Energy (keV)')
    colorindex=0
#traverse each directory
    for directory in dirnames:
        filepath=directory+'/cstatlinescan_%i.dat' %deltav
#find each output file from a cstat line scan
        if os.path.isfile(filepath):
            with open(filepath) as f:
                print 'Reading file: '+filepath
                lines = f.readlines()            
                print "Read %i lines from file %s " %(len(lines),filepath)    
                #convert energy to wavelength
                expression= (line for line in lines if not line.startswith("\n"))
                y = []
                wavelength = []
                for line in expression:
                    delta=float(line.split("\t")[2])
                    #skip negative delta C
                    if delta<0.0:
                        continue
                    energy =float(line.split("\t")[3])
                    wavelength.append( 10**7*h*c/energy)
                #x = [float(line.split("\t")[3]) for line in lines]
                #norm of the line
                    norm=float(line.split("\t")[4])
                #change sign of delta according to the normalization for plotting purposes (absorption/emission lines)
                   
                    
                    if norm>= 0.0:
                        y.append(delta)
                    else:
                        y.append(-float(delta))
    #get a difference color for each line
                ax1.plot(wavelength,y, c=colors[colorindex], label=directory)
                colorindex=colorindex+1
      
        else:
            continue
      
               
#check if any file was found, that is if x is empty or not
    if wavelength:
    #horizontal line    
        horizontal_line= np.array([0 for i in xrange(len(wavelength))])
        plt.axhline(y=0, color='black') 
        ax1.set_xticks(np.arange(8.0,25, 1.0))
        ax1.set_xlim(8.0,25)
        ax2.set_xlim(1.5,0.5)
    #put legend outside the plot
        leg = ax1.legend(bbox_to_anchor=(1,1), prop={'size': 7.5}, bbox_transform=plt.gcf().transFigure) 
    #save figure
        plt.savefig('energydeltacstat_%i.pdf' %deltav,bbox_inches='tight')       

    else:
        print "No cstat scan line files were found for velocity dispersion: %i" %deltav
   
plt.show()
        
