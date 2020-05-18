# This is a code to read the Mass frequency values out of a file produced 
# by XRayFreq.py, calculate the line of best fit using least squares 
# regression and then plot the data and the fit onto a graph which is 
# saved.  
# Written by: Daniel Foulds-Holt 11/05/2020

import csv 
import matplotlib.pyplot as plt
import numpy as np
import sys

def GetData(filename):
	Mass = []
	Freq = []
	TimP = []
	NoPk = []   
	Aver = []
	APL = []
	AVL = []
	ART = []
	AFT = []

	# Average Peak Luminosity   = Averages_In[0] 
	# Average Valley Luminosity = Averages_In[1]
	# Average Rise Time = Averages_In[2] 
	# Average Fall Time = Averages_In[3]
	with open(filename) as csvfile:
		readCSV = csv.reader(csvfile, delimiter=',')
		for row in readCSV:
			Mass.append(float(row[0]))
			Freq.append(float(row[1]))
			TimP.append(float(row[2]))
			NoPk.append(float(row[3]))
			APL.append(float(row[4]))
			AVL.append(float(row[5]))
			ART.append(float(row[6]))
			AFT.append(float(row[7]))

	#return Mass, Freq, TimP, NoPk, APL, AVL, ART, AFT 

	res = [Mass, Freq, TimP, NoPk, APL, AVL, ART, AFT] 
	return res

def FitData(x, y):
	x_fit = np.array(x)
	y_fit = np.array(y)

	#Z is the coefficiants cov is the covarient matrix
	cov = []
	z, cov = np.polyfit(x_fit, y_fit, 1, cov=True)
	
	#Standard deviation as the sqrt of the variance
	StDev = []
	StDev.append(np.sqrt(cov[0][0]))
	StDev.append(np.sqrt(cov[1][1]))

	correlation = np.corrcoef(x, y)[0,1]
	rsq = correlation**2

	print "y = ", z[0], " (+/- ", StDev[0], " ) x + ", z[1], " (+/- ", StDev[1], " )"
	print "R^2 = ", rsq
	return z, rsq, StDev

def DrawData(Mass, Freq):	
	plt.rcParams['font.serif'] = "Times New Roman"
	plt.rcParams['font.family'] = "serif"
	plt.rcParams['font.weight'] = "normal"
	plt.rcParams['font.size'] = 14

	plt.figure(figsize=(8, 6))
	plt.xlabel("Star Mass, " r"$[ M\ /\ M_{\odot} ]$" , fontsize=18)  
	plt.ylabel("X-Ray Burst Frequency, " r" $[ 1\ /\ \mathrm{Hrs} ]$", fontsize=18)
	plt.rc('xtick', labelsize=16) 
	plt.rc('ytick', labelsize=16)
	plt.xlim(1.1,1.8)

	plt.plot(Mass, Freq,"rD", label="X-Ray burst data", ms=5)

	#StDev is unused as I dont want it in the graph.
	z, rsq, StDev = FitData(Mass, Freq)
	axes = plt.gca()
	x_vals = np.array(axes.get_xlim())
	y_vals = z[1] + z[0] * x_vals
	#sting = "y = %:.2f x + %:.2f : Rsq = %:.3f",z[0], z[1], rsq
	sting = "y = " + str(round(z[0],2)) + " x + " + str(round(z[1],2)) + " : Rsq = " + str(round(rsq,3))
	plt.plot(x_vals, y_vals, '--', color="Black", label=sting)

	#xfit = []
	#yfit = []
	#xfit.append(1.3)
	#yfit.append(z[0] * 1.3 + z[1])
	#xfit.append(1.6)
	#yfit.append(z[0] * 1.6 + z[1])
	#plt.plot(xfit, yfit, "g--", label=f"y = {z[0]}x + {z[1]}")

	plt.legend(loc="upper right")

	plt.savefig('MassFrequency.png', format='png')
	print ""
	print "------------------------------------------------"
	print "The graph has been saved to 'MassFrequency.png'."
	print "------------------------------------------------"
	print ""

	plt.show()

def DrawData3(Mass1, Freq1, Mass2, Freq2, Mass3, Freq3, xtitle, ytitle, ylow, yhigh, title, lloc):	
	plt.rcParams['font.serif'] = "Times New Roman"
	plt.rcParams['font.family'] = "serif"
	plt.rcParams['font.weight'] = "normal"
	plt.rcParams['font.size'] = 14

	plt.figure(figsize=(16, 8))
#	plt.xlabel("Star Mass, " r"$[ M\ /\ M_{\odot} ]$" , fontsize=18)  
#	plt.ylabel("X-Ray Burst Frequency, " r" $[ 1\ /\ \mathrm{Hrs} ]$", fontsize=18)
#	plt.ylabel("Number of X-Ray Bursts", fontsize=18)
	plt.xlabel(xtitle, fontsize=18)  
	plt.ylabel(ytitle, fontsize=18)
	plt.rc('xtick', labelsize=16) 
	plt.rc('ytick', labelsize=16)
	plt.xlim(1.1,1.8)
#	plt.ylim(0.7,2.2)
	if yhigh != -1:
		plt.ylim(ylow,yhigh)

	#=========================================================================================================================
	plt.plot(Mass1, Freq1,"rD", label="X-Ray burst data - " r"$ \dot{\mathrm{M}}\ /\ \mathrm{M}_{\odot} = 1 \times 10^{-9} $", ms=5)
	plt.plot(Mass2, Freq2,"gD", label="X-Ray burst data - " r"$ \dot{\mathrm{M}}\ /\ \mathrm{M}_{\odot} = 2.5 \times 10^{-9} $", ms=5)
	plt.plot(Mass3, Freq3,"bD", label="X-Ray burst data - " r"$ \dot{\mathrm{M}}\ /\ \mathrm{M}_{\odot} = 5 \times 10^{-9} $", ms=5)
	#=========================================================================================================================

	#=========================================================================================================================
	#StDev is unused as I dont want it in the graph.
	z1, rsq1, StDev1 = FitData(Mass1, Freq1)
	axes = plt.gca()
	x_vals1 = np.array(axes.get_xlim())
	y_vals1 = z1[1] + z1[0] * x_vals1
	#sting = "y = %:.2f x + %:.2f : Rsq = %:.3f",z[0], z[1], rsq
	sting = "y = " + str(round(z1[0],2)) + " x + " + str(round(z1[1],2)) + " : Rsq = " + str(round(rsq1,3))
	plt.plot(x_vals1, y_vals1, '--', color="maroon")#, label=sting)
	#=========================================================================================================================

	#=========================================================================================================================
	#StDev is unused as I dont want it in the graph.
	z2, rsq2, StDev2 = FitData(Mass2, Freq2)
	axes = plt.gca()
	x_vals2 = np.array(axes.get_xlim())
	y_vals2 = z2[1] + z2[0] * x_vals2
	#sting = "y = %:.2f x + %:.2f : Rsq = %:.3f",z[0], z[1], rsq
	sting = "y = " + str(round(z2[0],2)) + " x + " + str(round(z2[1],2)) + " : Rsq = " + str(round(rsq2,3))
	plt.plot(x_vals2, y_vals2, '--', color="darkgreen")#, label=sting)
	#=========================================================================================================================

	#=========================================================================================================================
	#StDev is unused as I dont want it in the graph.
	z3, rsq3, StDev3 = FitData(Mass3, Freq3)
	axes = plt.gca()
	x_vals3 = np.array(axes.get_xlim())
	y_vals3 = z3[1] + z3[0] * x_vals3
	#sting = "y = %:.2f x + %:.2f : Rsq = %:.3f",z[0], z[1], rsq
	sting = "y = " + str(round(z3[0],2)) + " x + " + str(round(z3[1],2)) + " : Rsq = " + str(round(rsq3,3))
	plt.plot(x_vals3, y_vals3, '--', color="midnightblue")#, label=sting)
	#=========================================================================================================================


	#xfit = []
	#yfit = []
	#xfit.append(1.3)
	#yfit.append(z[0] * 1.3 + z[1])
	#xfit.append(1.6)
	#yfit.append(z[0] * 1.6 + z[1])
	#plt.plot(xfit, yfit, "g--", label=f"y = {z[0]}x + {z[1]}")

#	plt.legend(loc="upper right")
	plt.legend(loc=lloc)

	if title != "None":
		plt.savefig(title, format='png', dpi=600)
		print ""
		print "------------------------------------------------"
		print "The graph has been saved to '", title, "'."
		print "------------------------------------------------"
		print ""

	plt.show()

def DrawGeneral(Mass, Freq, xTitle, yTitle, name):	
	plt.rcParams['font.serif'] = "Times New Roman"
	plt.rcParams['font.family'] = "serif"
	plt.rcParams['font.weight'] = "normal"
	plt.rcParams['font.size'] = 14

	plt.figure(figsize=(8, 6))
	plt.xlabel(xTitle, fontsize=18)  
	plt.ylabel(yTitle, fontsize=18)
	plt.rc('xtick', labelsize=16) 
	plt.rc('ytick', labelsize=16)
	#plt.xlim(1.1,1.8)

	plt.plot(Mass, Freq,"rD", label="X-Ray burst data", ms=5)

	#StDev is unused as I dont want it in the graph.
	z, rsq, StDev = FitData(Mass, Freq)
	axes = plt.gca()
	x_vals = np.array(axes.get_xlim())
	y_vals = z[1] + z[0] * x_vals
	#sting = "y = %:.2f x + %:.2f : Rsq = %:.3f",z[0], z[1], rsq
	sting = "y = " + str(round(z[0],2)) + " x + " + str(round(z[1],2)) + " : Rsq = " + str(round(rsq,3))
	plt.plot(x_vals, y_vals, '--', color="Black", label=sting)

	#xfit = []
	#yfit = []
	#xfit.append(1.3)
	#yfit.append(z[0] * 1.3 + z[1])
	#xfit.append(1.6)
	#yfit.append(z[0] * 1.6 + z[1])
	#plt.plot(xfit, yfit, "g--", label=f"y = {z[0]}x + {z[1]}")

	plt.legend(loc="best")

	plt.savefig(name, format='png')
	print ""
	print "------------------------------------------------"
	print "The graph has been saved to '", name, "'."
	print "------------------------------------------------"
	print ""

	plt.show()

def DrawLum(Res):
	DrawGeneral(Res[0], Res[4], "Star Mass, " r"$[ M\ /\ M_{\odot} ]$", "Average Peak Luminosity " r"$[\log{ L\ /\ L_{\odot}} ]$", "Mass_APL_L.png")	
	DrawGeneral(Res[0], Res[5], "Star Mass, " r"$[ M\ /\ M_{\odot} ]$", "Average Valley Luminosity " r"$[\log{ L\ /\ L_{\odot}} ]$", "Mass_AVL_L.png")	
	DrawGeneral(Res[0], Res[6], "Star Mass, " r"$[ M\ /\ M_{\odot} ]$", "Average Rise Time (Lum) " r"$[\mathrm{Hrs}]$", "Mass_ART_L.png")	
	DrawGeneral(Res[0], Res[7], "Star Mass, " r"$[ M\ /\ M_{\odot} ]$", "Average Fall Time (Lum) " r"$[\mathrm{Hrs}]$", "Mass_AFT_L.png")	

def DrawTemp(Res):
	DrawGeneral(Res[0], Res[4], "Star Mass, " r"$[ M\ /\ M_{\odot} ]$", "Average Peak Temperature " r"$[T_{\mathrm{Eff}}]$", "Mass_APL_T.png")	
	DrawGeneral(Res[0], Res[5], "Star Mass, " r"$[ M\ /\ M_{\odot} ]$", "Average Valley Temperature " r"$[T_{\mathrm{Eff}}]$", "Mass_AVL_T.png")	
	DrawGeneral(Res[0], Res[6], "Star Mass, " r"$[ M\ /\ M_{\odot} ]$", "Average Rise Time (Temp) " r"$[\mathrm{Hrs}]$", "Mass_ART_T.png")	
	DrawGeneral(Res[0], Res[7], "Star Mass, " r"$[ M\ /\ M_{\odot} ]$", "Average Fall Time (Temp)" r"$[\mathrm{Hrs}]$", "Mass_AFT_T.png")	

def PrintHelp():
	print ""
	print "VisualiseXRay_Freq.py - Help"
	print "============================"
	print ""
	print "This is a python script to visualise the data outputted"
	print "by the 'XRayFreq.py' code for MESA analysis."
	print ""
	print "Usage:"
	print ""
	print "python VisualiseXRay_Freq.py FrequencyData.txt    : This will plot the NS Mass against frequency."
	print "                             FrequencyData.txt -l : This will plot all graphs associated with Luminosity."
	print "                             FrequencyData.txt -t : This will plot all graphs associated with Temperature."
	print "                             FD_1 FD_2 FD_3       : This will plot the NS Mass against frequency for all"
	print "                                                    three files on one plot."
	print ""
	print "These four usages allow for all the data to be plotted"
	print "for either one file, or plot three files data together"
	print "on one graph. The temprature setting is to be used with"
	print "the 'TemperatureData.txt' file outputted by 'XRayFreq.py'."
	print ""
	print "Enjoy!"
	print ""


def Main():

	#Res structure:
	#
	#Res = [Mass, Freq, TimP, NoPk, APL, AVL, ART, AFT]
	#        0  ,  1  ,  2  ,  3  ,  4 ,  5 ,  6 ,  7 
	#
	#DrawGeneral(Mass, VAR, "xTitle", "yTitle", "FileName.png"):	
	#

	if len(sys.argv) == 1:
		print "For usage and more help:"
		print "python VisualiseXRay_Freq.py -h"
		print ""
		return

	if sys.argv[1] == "-h":
		PrintHelp()
		return

	if len(sys.argv) < 4:
		Res = GetData(sys.argv[1])
		DrawData(Res[0], Res[1])	
		if len(sys.argv) == 3:
			if sys.argv[2] == '-l':
				DrawLum(Res)
				return
			elif sys.argv[2] == '-t':
				DrawTemp(Res)
				return
			else:
				print "Unknown command!"
				print "Help : python VisualiseXRay_Freq.py -h"
				print ""
				return
		return

	if len(sys.argv) == 4:
		Res1 = GetData(sys.argv[1])
		Res2 = GetData(sys.argv[2])
		Res3 = GetData(sys.argv[3])
	#	DrawData3(Res1[0],Res1[1],Res2[0],Res2[1],Res3[0],Res3[1],"Star Mass, " r"$[ M\ /\ M_{\odot} ]$","X-Ray Burst Frequency, " r" $[1\ /\ \mathrm{Hrs}]$",0.7,2.2,"MassFrequency_ALL.png","upper right")
	#	DrawData3(Res1[0],Res1[3],Res2[0],Res2[3],Res3[0],Res3[3],"Star Mass, " r"$[ M\ /\ M_{\odot} ]$","Number of X-Ray Bursts", 0,15, "MassPkNo_ALL.png", "upper left")

		title  = "None" # "None" for no print
		ytitle = "Average Fall Time [hrs]$"
		xtitle = "Star Mass, " r"$[ M\ /\ M_{\odot} ]$"
		ylow   = 0.0
		yhigh  = -1 # -1 for default
		var    = 6
		lloc   = "best"

		DrawData3(Res1[0],Res1[var],Res2[0],Res2[var],Res3[0],Res3[var],xtitle,ytitle,ylow,yhigh,title,lloc)

		return

Main()



