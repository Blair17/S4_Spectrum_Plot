import os
import numpy as np
import matplotlib.pyplot as plt
from Functions import figure_refl, figure_refl_phase

root = os.getcwd()

period = 368
dutycycle = 0.86
gratingindex = 2.0
gratingthickness = 150
ridgewidth = period * dutycycle
residual_layer_thickness = 100
alox_thickness = 50
film_thickness = residual_layer_thickness + gratingthickness

coverindex = 1.00
glassindex = 1.45
aloxindex = 1.6
loss = 0.0

nharm = 30
TEamp = 1
TMamp = 0

lambdain = 615
lambdafin = 655
npoints = 900;
deltalambda = (lambdafin - lambdain) / npoints

simulate = True
if simulate:
        args = (f'period = {period}; gratingthickness = {gratingthickness};'
                f'dutycycle = {dutycycle}; ridgewidth = {ridgewidth};'
                f'nharm = {nharm}; lambdain = {lambdain};lambdafin = {lambdafin};' 
                f'loss = {loss}; coverindex = {coverindex}; aloxindex = {aloxindex};' 
                f'deltalambda = {deltalambda}; gratingindex = {gratingindex};'
                f'glassindex = {glassindex}; TEamp = {TEamp}; TMamp = {TMamp};'
                f'residual_layer_thickness = {residual_layer_thickness};'
                f'film_thickness = {film_thickness}; alox_thickness = {alox_thickness};')

        lua_script = 'Standard_GMR.lua'
        os.system(f'S4 -a "{args}" {lua_script}')

datafilename = 'data.csv'
datafilepath = os.path.join(
    root,
    datafilename)
lam, spectrum, Ar, Ai = np.genfromtxt(
    fname=datafilepath,
    delimiter=",",
    skip_header=1,
    unpack=True)

epsfilename = 'eps.csv'
epsfilepath = os.path.join(
    root,
    epsfilename)
x, eps = np.genfromtxt(
    fname=epsfilepath,
    delimiter=",",
    skip_header=0,
    unpack=True) 

### Calculations ###
Aphi = np.arctan2(Ai,Ar)
phase1 = ( np.unwrap(Aphi, period=np.pi) ) / np.pi
phase = phase1 - min(phase1)
spectrum1 = spectrum*100

figure_refl(lam, spectrum1)

plt.title(f'P = {period}nm, FF = {dutycycle},' 
          f'T = {gratingthickness}nm, n_G = {gratingindex}, \n n_cover = {coverindex}, '
          f'n_sub = {glassindex}, Pedestal = {film_thickness}nm',
          fontsize=18, fontweight='bold')

plt.grid()
plt.xlim([lambdain,lambdafin])
plt.tight_layout()
plt.savefig('GMR_R.png')