# Python-Line-Significance-Scripts
Scripts to identify and asses emission lines
author: Andres Gurpide Lasheras; andres.gurpide@gmail.com


            findcstatmax.py


This script will go into every observation folder you have in the directory you run it from and find the maximum and minimum C-stat value of each cstatlinescan_deltav.dat, together with the energy and wavelength of corresponding to that delta C-stat. Deltav is the deltav used in the gaussian search scan of the line. The delta v are hardcoded for now in a list of deltav. The output is prompted in the command line.



            plotcstat.py


This script will go into every observation folder you have in the directory you run it from, and find every cstatlinescan_deltav.dat and create a plot with the delta C value vs energy, plotting all scans performed on every observation  together with the same delta v value. The plots are shown and stored.

            significance.py


This script computes the significance of a certain line at a certain energy. The user will be asked for the delta C value they want to test, the file with the c values of the simple model and the file with the c values of the complex model. It will compute the difference in delta C value between the fits of the two models and compute how many spectra gave an improvement higher than the delta C value the user introduced. Therefore the user needs to know the corresponding energy of that delta C value beforehand. Optionally the user can introduce a number of lines of the files to be read, if the entire file does not need to be processed.
