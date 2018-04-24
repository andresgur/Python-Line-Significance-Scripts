#Script to account for the significance of a certain line. The program asks for the delta C-stat of the line you want to study and two files:
# - the simple model: no line
# - the complex model: with line
#the program substracts the C-stats that finds in both files and finally plots the C-stat probabily distribution of the data together with the C-stat provided with its significance
# Author: Andres Gurpide Lasheras andres.gurpide@gmail.com
import numpy as np
import os
import sys
import matplotlib.pyplot as plt   

delta_c= float(raw_input("Type delta C you want to test against: \n"))

simple_model_file = raw_input("Type data file for the 'simple' model: \n")
complex_model_file = raw_input("Type data file for the 'complex' model: \n")

#read simple model
with open(simple_model_file) as f:
	lines = f.readlines()	
	c_simple = [float(line.split(" ")[1]) for line in lines]
	print "Number of lines in %s %i" %(simple_model_file,len(c_simple))
#read simple model
with open(complex_model_file) as f:
	lines = f.readlines()	
	c_complex = [float(line.split(" ")[1]) for line in lines]
	print "Number of lines in %s %i" %(complex_model_file,len(c_complex))

#exit program if the length of the monte carlo simulations is not the same
if len(c_complex)!=len(c_simple):
	print "Length of both files is not the same: %i vs %i, exiting program" %(len(c_simple),len(c_complex))
	sys.exit()

#compute differences and account for the significance of the line
differences =[]
nhigher=0
nnegative=0

#get number of simulations from the files
nsimulations=len(c_simple)

#traverse every spectrum
for i in range(nsimulations):

#get the difference in C between the simple and the complex model (complex should have lower C as it is a better fit usually)
	difference = float(c_simple[i]-c_complex[i])

	if difference<0.0:
#warn the user that a negative delta C-stat value has been found
		print "Warning! Spectrum %i has negative delta-c = %.3f" %(i,difference)
		nnegative+=1
		continue
	differences.append(difference)
	#print "Differences: %.3f for spectrum: %i" %(difference,i)

#if a higher difference is found record it
	if difference>delta_c:
		nhigher+=1
		print "Spectrum %i has higher delta-c = %.3f" %(i,difference)

#substract the number of negative cstat simulations to the total to avoi accounting them
totalsimulations = nsimulations-nnegative

#compute significance of the line
significance=100.0*(1-nhigher/float(totalsimulations))

#log process
print "Skipped %i spectra for negative delta c" %nnegative
print "Found %i spectra with higher delta c" %nhigher
print "Significance of the line: %.3f" %significance

plt.figure(figsize=(16.0, 10.0))
#vertical line for the cstat we are testing against
plt.axvline(x=delta_c, color='black') 
#place label next to it
plt.text(float(delta_c) + 0.1,125,"%.2f %%" %(100*float(nhigher)/totalsimulations) ,rotation=0)
#create histogram bins of delta C, from 0 to 20 and size of the  bin
bins = np.arange(0, 20, 0.1)

#plot the result

plt.hist(differences, bins=bins, normed=False)
plt.title('Delta C-stat distribution')
plt.xlabel('Delta C-stat bin')
plt.ylabel('# spectra')
plt.savefig("distribution_%.2f.pdf" %delta_c,bbox_inches='tight')
plt.show()


