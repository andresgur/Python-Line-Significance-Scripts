#Script to account for the significance of a certain line with a given energy. The program reads the file of the fit with no line and the file of the
# fit with line contained in the specified folders in the working directory in the parameters. 
# - the simple model: no line
# - the complex model: with line
#the program substracts the C-stats that finds in both files and finally plots the C-stat probabily distribution for the given energy. Also 
#appends detection thresholds to the output_file_name
#if a Delta C value for that energy is provided, the program will also compute the significance of the line
# Author: Andres Gurpide Lasheras andres.gurpide@gmail.com
    #!/usr/bin/env python3
    # coding=utf-8
#input parameters: energy of the line to compute the distribution of the C value for. Optionally the DeltaC value of this line can be provided to 
#compute its significance and also how many spectra you want to compute the distribution with

#imports
import numpy as np
import sys
import matplotlib.pyplot    as plt
import os
from optparse import OptionParser

#Parameters
#------------------------------------------------------------------------------
output_file_name="detection_thresholds.txt"
simple_model_file="./FIT_NOLINE/10000.dat"
complex_model_file="./fitline_500/"
output_dir="lines"
compute_line_significance=1

#------------------------------------------------------------------------------

#Read script arguments
#------------------------------------------------------------------------------
parser = OptionParser()

parser.add_option("-n", "--nspectra",dest="nspectra",
                  help="Number of spectra to be processed (optional)",default=-1, type='int')
parser.add_option("-E", "--energy",dest="energy",default="",
                  help="Energy of the line to be analysed")  
parser.add_option("-C", "--Cstat",dest="cstat",default=-1,
                  help="Cstat value of the line in the original spectrum", type='float') 

(options, args) = parser.parse_args()
#set the number of spectra to be read to infinite
nspectra=options.nspectra
energy_line=options.energy
delta_c=options.cstat

if energy_line=="":
    print "Error: Energy line not provided"
    sys.exit()

#------------------------------------------------------------------------------

#find complex model for the specified energy
complex_model_file=complex_model_file+energy_line+"_10000.dat"

#case where the document has to be fully read i.e. no number of spectra was provided
if nspectra==-1:
    #read simple model
    with open(simple_model_file) as f:
        lines = f.readlines()    
        c_simple = [float(line.split(" ")[1]) for line in lines if not line.startswith("\n")]
        print "Number of lines in %s %i" %(simple_model_file,len(c_simple))
    #read complex model
    with open(complex_model_file) as f:
        lines = f.readlines()    
        c_complex = [float(line.split(" ")[1]) for line in lines if not line.startswith("\n")]
        print "Number of lines in %s %i" %(complex_model_file,len(c_complex))
    #exit program if the length of the monte carlo simulations is not the same
    if len(c_complex)!=len(c_simple):
        print "Length of both files is not the same: %i vs %i, exiting program" %(len(c_simple),len(c_complex))
        sys.exit()

 
            
#case where the user has set some number of spectra to be read
else:
     print "Processing only %i spectra" %nspectra
     #read simple model
     c_simple=[]
     i=0
     with open(simple_model_file) as f:
             for line in f:
                 if not line.startswith("\n"):
                     c_simple.append(float(line.split(" ")[1]))
                     i+=1
                     if i>=nspectra:break
                     
               
     #read complex model
     c_complex=[]
     i=0
     with open(complex_model_file) as f:
            for line in f:
                if not line.startswith("\n"):
                     c_complex.append(float(line.split(" ")[1]))
                     i+=1
                     if i>=nspectra:break
                     

#set the number of processed spectra, taking into account skipped spectra
nspectra = len(c_simple)     

#warn the user if DeltaC of the line was not provided
if delta_c==-1:
    compute_line_significance=0
    print "Warning! Delta C for the line not provided -> significance of the line will not be computed"

#compute differences and account for the significance of the line
differences =[]
nhigher=0
nnegative=0

#traverse every spectrum
for s in range(nspectra):

#get the difference in C between the simple and the complex model (complex must have lower C, otherwise warn the user)
    difference = float(c_simple[s]-c_complex[s])

    if difference<0.0:
        #warn the user that a negative delta C-stat value has been found
        print "Warning! Spectrum %i has negative delta-c = %.3f" %(s,difference)
        nnegative+=1
        continue
    differences.append(difference)
   # print "Differences: %.3f for spectrum: %i" %(difference,s)

    #if a higher difference is found record it
    if compute_line_significance==1:
        if difference>delta_c:
            nhigher+=1
            print "Spectrum %i has higher delta-c = %.3f" %(s,difference)

#substract the number of negative cstat simulations to the total to avoid accounting them
totalsimulations = len(differences) 

#compute significance of the line
significance=100.0*(1-nhigher/float(totalsimulations))

#compute 3 sigma value
three_sigma_delta_c = np.percentile(differences,99.7);

#compute 2 sigma value
two_sigma_delta_c = np.percentile(differences,95.4);

#log process
if nnegative!=0: 
    print "Skipped %i spectra for negative delta c" %nnegative
    
print "Threshold delta C value for detection at " +energy_line + ": %.3f" %three_sigma_delta_c
if compute_line_significance==1:
    print "Found %i spectra with higher delta c" %nhigher
    print "Significance of the line: %.3f" %significance
    print "Detection above threshold: %r " %(three_sigma_delta_c<delta_c)
#save outputs

#create output directory if it does not exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

#if it does not exist, create and append the header
if not os.path.isfile(output_dir+'/'+output_file_name):
    print "Creating output file "+ output_file_name 
    f = open(output_dir+"/"+output_file_name, 'a+')
    print >> f, "#E(keV)\t C_stat (99.7%)\t C_stat (95.4%) \t #simulations "
    
#if it exist append the output
else:
    f = open(output_dir+"/"+output_file_name, 'a')  
#append sigma detection thresholds to the file
print >> f, energy_line + "\t %.3f \t %.3f \t %i"  %(three_sigma_delta_c,two_sigma_delta_c,totalsimulations)


#save plot distribution
plot_directory=output_dir+"/"+ energy_line
if not os.path.exists(plot_directory):
    os.makedirs(plot_directory)

plt.figure(figsize=(16.0, 10.0))


#add vertical line for the cstat we are testing against
if compute_line_significance==1:
    plt.axvline(x=delta_c, color='black') 
    #place label next to it
    plt.text(float(delta_c) + 0.05,10,"%.2f %%" %(significance) ,fontsize=18)

#detection thresholds vertical lines
#plot three sigma value
plt.text(float(three_sigma_delta_c)-1,120,"99.7%", color='red',fontsize=18)
plt.axvline(x=three_sigma_delta_c, color='red') 

#plot two sigma value
plt.text(float(two_sigma_delta_c)-1,120,"95.4%", color='green',fontsize=18)
plt.axvline(x=two_sigma_delta_c, color='green') 
#create histogram bins of delta C, from 0 to 20 and size of the  bin
bins = np.arange(0, max(differences), 0.2)

#plot the result
plt.hist(differences, bins=bins, normed=False,log=True)
plt.title('%i simulations'%totalsimulations)
plt.ylim(0.1,2500)
plt.xlim(0,14)
plt.xlabel('$\Delta$ C-stat bin')
plt.ylabel('# spectra')

#label sizes
plt.rc('font', size=24)

#save plot
outputfile=plot_directory +"/%i_simulations.pdf" %(totalsimulations)
plt.savefig(outputfile,bbox_inches='tight')
print "Plot generated and saved to "+outputfile
#plt.show()


