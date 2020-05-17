# This is a code to extract Luminosity and time values from a 'history.data' file as
# outputted from a MESA simulation. The code then tries to find the peaks caused by 
# X-Ray bursts and determine their frequency. The code has many capabilities as 
# described by the help option.
# Written by: Daniel Foulds-Holt 11/05/2020

import numpy as np
import matplotlib.pyplot as plt
import sys
# mesa_reader allows to get the data from the "./LOGS/" folder files easily
import mesa_reader as mr

def DrawData(x, y, py, px, vy, vx, opt):
	plt.rcParams['font.serif'] = "Times New Roman"
	plt.rcParams['font.family'] = "serif"
	plt.rcParams['font.size'] = 14

	#Labels
	#plt.xlabel("Star age, "r"$\displaystyle \tau$ [hr]")
	#plt.ylabel("Luminosity, $\log L/L_{\odot}$");
	plt.xlabel("Star age, " r"$\tau$ [hr]", fontsize=20)  
	plt.ylabel("Luminosity, " r" $\log\ L\ /\ L_{\odot}$", fontsize=20)

	plt.rc('xtick', labelsize=16) 
	plt.rc('ytick', labelsize=16)

	#Plot
	plt.plot(x, y)
	#plot peak positions
	plt.plot(px, py, "rD", markersize=5, label="X-Ray burst peaks")
	plt.plot(vx, vy, "bD", markersize=5, label="X-Ray burst valleys")
	

	plt.legend(loc="upper left")
	# Save it on a png that can be reused later
	plt.savefig('XRayFrequency.png', format='png')
	print "------------------------------------------------"
	print "The graph has been saved to 'XRayFrequency.png'."
	print "------------------------------------------------"
	print ""

	if (opt == "draw"):
		plt.show()

def DrawTemp(x, y, py, px, vy, vx, opt):
	plt.rcParams['font.serif'] = "Times New Roman"
	plt.rcParams['font.family'] = "serif"
	plt.rcParams['font.size'] = 14

	#Labels
	#plt.xlabel("Star age, "r"$\displaystyle \tau$ [hr]")
	#plt.ylabel("Luminosity, $\log L/L_{\odot}$");
	plt.xlabel("Star age, " r"$\tau$ [hr]", fontsize=20)  
	plt.ylabel("Temperature, " r" $\log\ T_{\mathrm{Eff}}$", fontsize=20)

	plt.rc('xtick', labelsize=16) 
	plt.rc('ytick', labelsize=16)

	#Plot
	plt.plot(x, y)
	#plot peak positions
	plt.plot(px, py, "rD", markersize=5, label="X-Ray burst peaks")
	plt.plot(vx, vy, "bD", markersize=5, label="X-Ray burst valleys")
	

	plt.legend(loc="upper left")
	# Save it on a png that can be reused later
	plt.savefig('XRayFrequencyTEMP.png', format='png')
	print "------------------------------------------------"
	print "The graph has been saved to 'XRayFrequencyTEMP.png'."
	print "------------------------------------------------"
	print ""

	if (opt == "draw"):
		plt.show()

def FindPeaks(y, x):	
	peaks = []
	peak_times = []

	valleys = []
	valley_times = []

	APL = 0 #Average Peak Luminosity
	AVL = 0 #Average Valley Luminosity 
	ART = 0 #Average Rise Time
	AFT = 0 #Average Fall Time
	A_counter = 0

	#This is the tolerence - it only counts a peak if the peak is followed by 
	# </ tolerence /> data points that decrease from the peak. Each time a data
	# point is higher than the one previous, the count goes to 0.
	# ============
	tolerence = 25
	tolerence2 = 25
	# ============

	#This is the machinary to find the peaks.
	i = 0
	count = 0
	previous = 0
	first = False
	newprev = False
	last = 0
	possible_min = 0
	count2 = 0
	firstmin = True
	while i < len(y) - 1:
		if y[i] > y[previous]:
			previous = i
			count = 0
			first = True
		if y[i] < y[previous]:
			count = count + 1
			#print "p = ", x[previous]
		if y[i] < y[previous] and count == tolerence and first:
			peaks.append(y[previous])
			peak_times.append(x[previous])
			APL = APL + y[previous]
			if possible_min != 0:
				ART = ART + x[previous] - x[possible_min]
			newprev = True
#			print "newPrev true ", x[i], " peak at = ", x[previous]
		if y[i] > y[last] and newprev:
			count2 = count2 + 1
#			print "I = ", x[i] , " > ",x[last], " : ", count2
			if firstmin:
#				print "FirstMin^^^"
				possible_min = last
				firstmin = False
		if count2 == tolerence2:
			AFT = AFT + x[possible_min] - x[previous]
			AVL = AVL + y[possible_min]
			A_counter = A_counter + 1
			previous = possible_min
			valleys.append(y[possible_min])
			valley_times.append(x[possible_min])
			firstmin = True
#			print "Previous = ", x[previous]
			newprev = False
			count2 = 0
#=============================================================
# Somethimes there is incomplete data and the algorithm must
# cut off before it gets messy. When uncommented, this stops
# the peak finder after 'x' number of valleys.
#=============================================================
#		if len(valleys) == 5:
#			break
#=============================================================

		last = i
		i = i + 1

	Averages_Out = []
	Averages_Out.append(APL/len(peaks))
	Averages_Out.append(AVL/len(valleys))
	Averages_Out.append(ART/len(valleys))
	Averages_Out.append(AFT/len(valleys))

	return peaks, peak_times, valleys, valley_times, Averages_Out

def FindPeakFrequency(px):
	total  = 0
	i = 1
	last_time = px[0]
	while i < len(px):
		total = total + (px[i] - last_time)
		last_time = px[i]
		i = i + 1
	
	average = total / (len(px) - 1)
	return average 

def SaveData(time, lumi, Peak_Times, Peaks):
	f = open("LuminosityData.txt","w+")
	co = 0
	while co < len(lumi):
		f.write(str(time[co]) + ", " + str(lumi[co]) + "\n")
		co = co + 1
	f.close()

	print ""
	print "The luminosity data has been saved to the file 'LuminosityData.txt'."

	f = open("PeakData.txt","w+")
	co = 0
	while co < len(Peaks):
		f.write(str(Peak_Times[co]) + ", " + str(Peaks[co]) + "\n")
		co = co + 1
	f.close()

	print "The peak positions have been saved to the file 'PeakData.txt'."
	print ""

def SaveFreqs(freq, timp, noPeaks, SMass, AVI, name):
	f = open(name ,"a")
	f.write(str(SMass[0]) + ", " + str(freq) + ", " + str(timp) + ", " + str(noPeaks) + ", " + str(AVI[0]) + ", " + str(AVI[1]) + ", " + str(AVI[2]) + ", " + str(AVI[3]) + "\n")
	f.close()

	# Average Peak Luminosity   = Averages_In[0] 
	# Average Valley Luminosity = Averages_In[1]
	# Average Rise Time = Averages_In[2] 
	# Average Fall Time = Averages_In[3]

	print ""
	print "The data has been saved to the file '", name, "'."
	print ""

def DoTemp(Temp, time, mass):
	Peaks = []
	Peak_Times = []
	Valleys = []
	Valley_Times = []
	Averages_In = []

	Peaks, Peak_Times, Valleys, Valley_Times, Averages_In = FindPeaks(Temp, time)
	DrawTemp(time, Temp, Peaks, Peak_Times, Valleys, Valley_Times, "draw")

	print "========= TEMP ========="
	print "Average Peak Temperature   = ", Averages_In[0] 
	print "Average Valley Temperature = ", Averages_In[1]
	print "Average Rise Time = ", Averages_In[2] 
	print "Average Fall Time = ", Averages_In[3]
	print "========================"
	print ""
	time_period = FindPeakFrequency(Peak_Times)

	frequency = 1 / time_period	
	SaveFreqs(frequency, time_period, len(Peaks), mass, Averages_In, "TemperatureData.txt")

def PrintHelp():
	print ""
	print "XRayFreq.py Help:"
	print "================="
	print ""
	print "Basic usage:"
	print "  python XRayFreq.py path/to/history.data"
	print ""
	print " python XRayFreq.py history.data -d : Draw & print graph."
	print "                                 -p : Print graph only."
	print "                                 -s : Save data only."
	print "                                 -f : Save frequency data."
	print "                                 -t : Analyse temperature data."
	print "                                 -h : Help."
	print ""
	print "This code is to read data from the '.data' files outputted by MESA."
	print "It then scans through the luminosity data to find peaks produced by"
	print "X-Ray bursts. These peaks are located and the time period and frequency"
	print "are calculated and printed to the screen. It can also draw the luminosity"
	print "graph with peak positions marked. This graph will be saved as"
	print "'XRayFrequency.png' in the working directory. The data can be saved also"
	print "outputting to 'LuminosityData.txt' and 'PeakData.txt' or 'FrequencyData.txt'."
	print ""
	print "Further plotting and analysis can be done using 'VisualiseXRay_Freq.py'."
	print ""

def Main():

	if(len(sys.argv) == 1):
		print ""
		print "Please include the 'history.data' file:"
		print "  python XRayFreq.py history.data"
		print ""
		print "python XRayFreq.py -h : Help."
		print ""
		return

	if  (sys.argv[1] == "-h"):
		PrintHelp()
		return

	print ""
	print "Getting the MESA data..."
	print ""

	# Load the "history.data" file and store it in "h" using Mesa_reader capabilities
	h = mr.MesaData(sys.argv[1])

	# Retrieve the star age (in hours) and save it in "time" array
	time=h.data('star_age_hr');

	# Retrieve the luminosity 
	lumi=h.data('log_L');
#	lumi=h.data('net_energy');

	if(len(sys.argv) == 3) and (sys.argv[2] == "-t"):
		DoTemp(h.data('log_Teff'), time, h.data('star_mass'))
		return

	#Find the peaks
	Peaks = []
	Peak_Times = []
	Valleys = []
	Valley_Times = []
	Averages_In = []

	Peaks, Peak_Times, Valleys, Valley_Times, Averages_In = FindPeaks(lumi, time)

	if(len(sys.argv) == 3) and (sys.argv[2] == "-d"):
		DrawData(time, lumi, Peaks, Peak_Times, Valleys, Valley_Times, "draw")
	
	if(len(sys.argv) == 3) and (sys.argv[2] == "-p"):
		DrawData(time, lumi, Peaks, Peak_Times, Valleys, Valley_Times, "print")


	#Peak_Times = Peak_Times[0:4]
	print "Number of peaks = ", len(Peak_Times)
	print "Peak times [hr]:"
	print Peak_Times
	print "Average Peak Luminosity   = ", Averages_In[0] 
	print "Average Valley Luminosity = ", Averages_In[1]
	print "Average Rise Time = ", Averages_In[2] 
	print "Average Fall Time = ", Averages_In[3]
	
	time_period = FindPeakFrequency(Peak_Times)

	frequency = 1 / time_period	
	
	print ""
	print "Time period = ", time_period, " [hr]"
	print "Frequency   = ", frequency, " [1 / hr]"  
	print ""

	if(len(sys.argv) == 3) and (sys.argv[2] == "-s"):
		SaveData(time, lumi, Peak_Times, Peaks)

	if(len(sys.argv) == 3) and (sys.argv[2] == "-f"):
		SaveFreqs(frequency, time_period, len(Peaks), h.data('star_mass'), Averages_In, "FrequencyData.txt")
# Main
Main()

