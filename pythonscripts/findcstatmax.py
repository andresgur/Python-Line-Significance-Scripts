#Script to find the maximum of delta C stat together with the corresponding energy. It will traverse all observation directories found in the working directory automatically and print the results for each of them.
# Author: Andres Gurpide Lasheras andres.gurpide@gmail.com

#imports
import os
   
#planck constant
h=4.135666733*pow(10,-15)
#speed of light
c=2.99792458*pow(10,8)
#velocity dispersions in km/s to be processed
velocity_dispersions = [0.0, 500, 1000]
#look for cstatlinescan.dat files inside the observation directories
working_directory=os.getcwd()
dirnames=os.listdir(working_directory)

for deltav in velocity_dispersions:
    print '#-------------------------------------#'
    print 'Velocity dispersion : %i  km/s' %deltav
    print '#-------------------------------------#\n'
    for directory in dirnames:
        filepath=directory+'/cstatlinescan_%i.dat' %deltav 
        if os.path.isfile(filepath):
            with open(filepath) as f:
                print 'Reading file: '+filepath
                lines = f.readlines()            
                print "Read %i lines from file %s " %(len(lines),filepath)    
                deltacstat =[]
#get energy column of the line 
                energy =[]
                expression= (line for line in lines if not line.startswith("\n"))
                for line in expression:
                    energy.append(float(line.split("\t")[3]))
                #norm of the line
                    norm=float(line.split("\t")[4])
                #change sign of delta according to the normalization to look for the minimum (absorption/emission lines)
                    delta=line.split("\t")[2]
                    if norm>= 0.0:
                        deltacstat.append(float(delta))
                    else:
                        deltacstat.append(-float(delta))
            #find maximum and minimum delta c stat
                max_cstat = max(deltacstat)
                max_index = deltacstat.index(max_cstat)
                max_energy = float(energy[max_index])
                min_cstat = min(deltacstat)
                min_index = deltacstat.index(min_cstat)
                min_energy = float(energy[min_index])
            #print results
                print "Max cstat at energy (keV): %.3f with c-stat %.2f, \n Min cstat at energy (keV): %.3f with c-stat %.2f" %(max_energy,max_cstat,min_energy,min_cstat)    
                print "Max cstat at energy (A): %.2f, \n Min cstat at energy (A): %.2f" %(10**7*c*h/max_energy,10**7*c*h/min_energy)
