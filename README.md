# MESA_Python_Analysis
These are two python scripts to extract data from the 'history.data' file outputted by MESA simulations. Specifically for use in analysing x-ray burst frequency. They allow the user to retreive the Luminosity data, find the x-ray burst peaks, and determine their frequency. The frequency can then be saved to a file and in combination with other simulations, be used to build up a graph showing the data sets and a line of best fit using least squares regression.

You will need the python module 'mesa_reader' you can get it using pip install or by folling the instructions on their GitHub:
https://github.com/wmwolf/py_mesa_reader

It is worth noting that the code itself has a help option '-h' which has plenty of information. However, it's probably best to read through the code and figure out whats going on. The visualisation code doesn't have a help functionality and as such requires a little read through to make sure you get whats going on, plus you wil likely need to edit that code.

I know this is quite a terrible code & It was very much a 'botched toe' of a project, it did however work. I plugged the problems with trash - as medical advice recommends. [Dr. Toboggan, 2009]

Any problems that you can't figure out yourself, feel free to email me: df00177@surrey.ac.uk
