import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd
import scienceplots

from Functions import figure_refl, FWHM, findpeaks, figure_refl_phase, phase_analysis, S4_run, add_colorbar, figure_pixel_plot, find_closest_value

plt.style.use(['science', 'nature', 'custom'])

def cm_to_inches(x):
    return x * 0.39

field = False

root = os.getcwd()

period = 530
dutycycle = 0.75
gratingindex = 1.9
gratingthickness = 150
accthickness = 1
coverindex = 1.34
glassindex = 1.45
accindex = 2.0
ridgewidth = period * dutycycle
loss = 0.0
total = 49
ITO_under = 5
TiO2thickness = total - ITO_under - accthickness

nharm = 30
TEamp = 1
TMamp = 0

zmin = -period/2 - 400
zmax = period/2 + gratingthickness + 400
xmin = -period
xmax = period

xstep = 1
zstep = 1

x = np.arange(xmin, xmax+1, xstep)
z = np.arange(zmin, zmax+1, zstep)

lambdain = 750
lambdafin = 850
npoints = 2000;
deltalambda = (lambdafin - lambdain) / npoints

args = (f'period = {period}; gratingthickness = {gratingthickness}; TiO2thickness = {TiO2thickness};'
            f'dutycycle = {dutycycle}; ridgewidth = {ridgewidth}; accthickness = {accthickness};'
            f'nharm = {nharm}; lambdain = {lambdain}; xstep = {xstep}; zstep = {zstep};' 
            f'lambdafin = {lambdafin}; loss = {loss}; coverindex = {coverindex};' 
            f'deltalambda = {deltalambda}; gratingindex = {gratingindex}; accindex = {accindex};'
            f'glassindex = {glassindex}; TEamp = {TEamp}; TMamp = {TMamp};'
            f'ITO_under = {ITO_under}; zmin = {zmin}; zmax = {zmax}; xmin = {xmin}; xmax = {xmax};')

S4_run(args, 'Standard_GMR.lua')     

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
eps_x, eps = np.genfromtxt(
    fname=epsfilepath,
    delimiter=",",
    skip_header=0,
    unpack=True) 

resmaxfilename = 'resmax.csv'
resmaxfilepath = os.path.join(
    root,
    resmaxfilename)
resmax = np.genfromtxt(
    fname=resmaxfilepath,
    delimiter=",",
    skip_header=0,
    unpack=True) 

phase = phase_analysis(Ai,Ar)
pparam = dict(xlabel='Wavelength (nm)', ylabel=r'Reflection (\%)')

fig, ax = plt.subplots()
ax.plot(lam, spectrum*100)
ax.legend()
ax.autoscale(tight=True)
ax.set(**pparam)
ax.set_ylim([1,100])
ax.set_xlim([lambdain,lambdafin])
fig.text(0.8, 0.75, f' FWHM = {np.round(FWHM(lam, spectrum*100), 2)}', ha='center', va='center', 
             fontsize=8, color='k', transform=ax.transAxes)
fig.text(0.8, 0.85, f' Peak = {np.round(findpeaks(lam, spectrum*100)[0], 2)}', ha='center', va='center', 
                 fontsize=8, color='k', transform=ax.transAxes) 
fig.savefig('GMR_RR.png', dpi=600)
plt.close()

fig, ax = plt.subplots(figsize=[5,4])
ax.plot(eps_x, eps, lw=2, color='mediumspringgreen')
ax.set_ylabel('Epsilon', fontsize=15, fontweight='bold')
ax.set_xlabel('X', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig('eps.png')

lambda1 = 0

fullwidth = FWHM(lam, spectrum*100)
qfac = resmax/fullwidth
print(qfac)

# mask_ITO = data2 > (3.3)
# data_eps = (data2 * mask_ITO)
# print(mask_ITO.shape)
# print(data2.shape)
# print(data_eps.shape)
# data_field = data * mask_ITO
# print(np.sum(np.abs(data_field)))

if field == True:
    lambda1 = int(resmax)
    args = (f'period = {period}; gratingthickness = {gratingthickness}; TiO2thickness = {TiO2thickness};'
            f'dutycycle = {dutycycle}; ridgewidth = {ridgewidth}; accindex = {accindex};'
            f'nharm = {nharm}; lambdain = {lambdain}; xstep = {xstep}; zstep = {zstep};' 
            f'lambdafin = {lambdafin}; loss = {loss}; coverindex = {coverindex}; accthickness = {accthickness};' 
            f'deltalambda = {deltalambda}; gratingindex = {gratingindex}; lambda1 = {lambda1};'
            f'glassindex = {glassindex}; TEamp = {TEamp}; TMamp = {TMamp}; resmax = {resmax};'
            f'ITO_under = {ITO_under}; zmin = {zmin}; zmax = {zmax}; xmin = {xmin}; xmax = {xmax};')

    S4_run(args, 'Field_extraction.lua')
    
    datafile = 'field.csv'
    field = np.genfromtxt(datafile, delimiter=',')
    
    field = field + abs(np.min(field))
    
    datafile = 'fieldeps.csv'
    epsfield = np.genfromtxt(datafile, delimiter=',')
    levels = np.linspace(-1,6,3)
    
    colors = ["white", "turquoise", "lightseagreen", "teal", "darkslategrey"]
    cmap = LinearSegmentedColormap.from_list("custom_cmap", colors)
    
    if TEamp == 1:
        figure_pixel_plot('jet', field, xmin, xmax, zmin, zmax, x, z, epsfield, levels)
    else:
        figure_pixel_plot('jet', field, xmin, xmax, zmin, zmax, x, z, epsfield, levels)
        
    print(f'Resonant Wavelength = {lambda1} nm \n'
          f'Max Field Strength = {np.round(np.max(field),2)} V/m')
