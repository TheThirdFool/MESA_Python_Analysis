#Draw Roche.
import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import ticker, cm

def Roche(x, y, M1, M2, A):

	q = M2 / M1
	r1 = math.sqrt((x + (A/2))**2.0 + y**2.0)
	r2 = math.sqrt((x - (A/2))**2.0 + y**2.0)

	if r1 == 0 or r2 == 0:
		return 0

	a1 = 2 / (1 + q) * 1 / r1
	a2 = 2 * q / (1 + q) * 1 / r2
	a3 = (x  - (q / (q+1)))**2.0 + y**2.0

	res = a1 + a2 + a3

#	Max = 10000
#	if res > Max:
#		res = Max

	return res

def COM(M1, M2, A):
	return ((M2 * A/2) - (M1 * A/2))/(M1+M2), 0


def GenerateData():
	plt.rcParams['font.serif'] = "Times New Roman"
	plt.rcParams['font.family'] = "serif"
	plt.rcParams['font.weight'] = "light"
	plt.rcParams['font.size'] = 14
	plt.rcParams['mathtext.fontset'] = 'cm'
	plt.rcParams['mathtext.rm'] = 'serif'


	M1 = 10
	M2 = 3

	A = 0.75

	comx, comy = COM(M1, M2, A)
	temp = Roche(comx, comy, M1, M2, A)
	print("COM (", comx, ",", comy, ") = ", temp)

	cblabel = "Gravitational Potential " r"$\Phi$" 
 
	Factor = 1
	steps = 1000
	bound = 1
	#lines = [0, 2, 5, 6,7, 10, 50, 75, 100, 150, 200, 250, 300, 400, 500]
	lines = 1000

	xlist = np.linspace(-bound, bound, steps)
	ylist = np.linspace(-bound, bound, steps)
	x, y = np.meshgrid(xlist, ylist)
	z = [[0 for k in range(steps)] for l in range(steps)]

	i = 0
	while i < steps:		
		j = 0 
		while j < steps:
			z[i][j] = (Factor * Roche(xlist[i],ylist[j],M1,M2,A))
			if (z[i][j] - 0)**2 < 3:
				print("0 = (", xlist[i], ", ", ylist[j], ") ")
			j = j + 1
		i = i + 1

	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.set_aspect("equal")
	cp = plt.contourf(y, x, z, lines, cmap=plt.cm.bone, locator=ticker.LogLocator(base=10.0, subs="all"), vmax=100)
	cb = fig.colorbar(cp, ticks=[1,10,100, 1000], label=cblabel)

	ax.text(A/2-0.06, -0.26, r"$\mathbf{M_2}$", color='White', fontsize=14, fontweight='bold')
	ax.text(-A/2-0.05, -0.26, r"$\mathbf{M_1}$", color='White', fontsize=14, fontweight='bold')

	#cp2 = plt.contour(cp, levels=[5.667865], colors='r')
	#cp3 = plt.contour(cp, levels=[5.66555], colors='r')
	cp4 = plt.contour(cp, levels=[4.9281], colors='r')

	plt.plot([A/2], [0], "o", color="Yellow", markersize=6*(M2/(M1+M2)))
	plt.plot([-A/2], [0], "o",color="Yellow", markersize=6*(M1/(M1+M2)))
	plt.axis('off')
#	plt.legend(loc="best")
	plt.savefig("RocheLobe.png", format='png', dpi=1200)
	plt.show()
	
	return x, y, z


def Main():
	x, y, z = GenerateData()


Main()
