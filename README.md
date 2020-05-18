# MESA_Python_Analysis
These are two python scripts to extract data from the 'history.data' file outputted by MESA simulations. Specifically for use in analysing x-ray burst frequency. They allow the user to retreive the Luminosity data, find the x-ray burst peaks, and determine their frequency. The frequency can then be saved to a file and in combination with other simulations, be used to build up a graph showing the data sets and a line of best fit using least squares regression.

You will need the python module 'mesa_reader' you can get it using pip install or by folling the instructions on their GitHub:
https://github.com/wmwolf/py_mesa_reader

It is worth noting that the code itself has a help option '-h' which has plenty of information. However, it's probably best to read through the code and figure out whats going on. The visualisation code doesn't have a help functionality and as such requires a little read through to make sure you get whats going on, plus you wil likely need to edit that code.

I know this is quite a terrible code & It was very much a 'botched toe' of a project, it did however work. I plugged the problems with trash - as medical advice recommends. [Dr. Toboggan, 2009]

Any problems that you can't figure out yourself, feel free to email me: df00177@surrey.ac.uk

===========================

In order to change the variable being plotted in 'VisualiseXRay_Freq.py' head to the bottom of the code [line 311] and edit these lines to what you need:

	title  = "FileTitle.png" # "None" for no print
	ytitle = "X-Ray Burst Frequency, " r" $[1\ /\ \mathrm{Hrs}]$"
	xtitle = "Star Mass, " r"$[ M\ /\ M_{\odot} ]$"
	ylow   = 0.0
	yhigh  = -1 # -1 for default
	var    = 1
	lloc   = "best"

The variable 'var' determines the variable plotted on the y-axis. This corresponds to:

	Res = [Mass, Freq, TimP, NoPk, APL, AVL, ART, AFT]
	        0  ,  1  ,  2  ,  3  ,  4 ,  5 ,  6 ,  7 
  
Or:

	0 = NS Mass
	1 = X-ray burst frequency
	2 = X-ray burst time period
	3 = Number of peaks analysed
	4 = Average peak luminosity
	5 = Average valley luminosity
	6 = Average rise time
	7 = Average fall time
  
