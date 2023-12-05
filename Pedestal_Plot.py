import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob

def FWHM(x,spectrum1):
    deltax = x[1] - x[0]
    half_max = max(spectrum1) / 2
    l = np.where(spectrum1 > half_max, 1, 0)
    
    return np.sum(l) * deltax

def last_9chars(x):
    return(x[1:])

root = os.getcwd()
    

ptrange = [0, 200, 400, 600, 800, 1000]

period = 396 # 572
gratingthickness = 127
# pedestal_thickness = 200
dutycycle = 0.6
gratingindex = 1.63

loss = 0.00
subindex = 1.49
nharm = 20
TEamp = 1
TMamp = 0
z_field = 450

eps_r = gratingindex**2 - loss**2
eps_i = 2 * gratingindex * loss

lambdain = 575
lambdafin = 675
npoints = 900;
deltalambda = (lambdafin - lambdain) / npoints

simulate = True

grooves_array = []

for pedestal_thickness in ptrange:
    ridgewidth = period * dutycycle
    groove = period - ridgewidth
    print(pedestal_thickness)
    if simulate:
                args = (f'period = {period}; gratingthickness = {gratingthickness};'
                        f'dutycycle = {dutycycle}; ridgewidth = {ridgewidth};'
                        f'nharm = {nharm}; lambdain = {lambdain};' 
                        f'lambdafin = {lambdafin}; loss = {loss};'
                        f'z_field= {z_field}; pedestal_thickness = {pedestal_thickness};' 
                        f'deltalambda = {deltalambda}; gratingindex = {gratingindex};'
                        f'subindex = {subindex}; TEamp = {TEamp}; TMamp = {TMamp};' 
                        f'eps_r = {eps_r}; eps_i = {eps_i};')

                lua_script = 'Pedestal.lua'
                os.system(f'S4 -a "{args}" {lua_script}')

    datafilename = 'data.csv'
    datafilepath = os.path.join(
        root,
        datafilename)
    lam, spectrum = np.genfromtxt(
        fname=datafilepath,
        delimiter=",",
        skip_header=1,
        unpack=True)

    df = pd.DataFrame({'Wavelength': lam, 'Reflection': spectrum})
    df.to_csv(f'data/{np.round(pedestal_thickness,2)}.csv', index=False)
    
    grooves_array.append(groove)

files = glob.glob('data/*.csv')
sorted_array = sorted(files, key = last_9chars)  

l_array = []
r_array = []

for file in sorted_array:
    datafilename = file
    datafilepath = os.path.join(
        root,
        datafilename)
    l, r = np.genfromtxt(
        fname=datafilepath,
        delimiter=",",
        skip_header=1,
        unpack=True)
    l_array.append(l)
    r_array.append(r)   
    
labels = []

for f, g in zip(ptrange, grooves_array):
    labels.append([np.round(f,2)])

fig, ax = plt.subplots(figsize=[10,7])
for index, l in enumerate(l_array):
    ax.plot(l,r_array[index], label=[x[0] for x in labels][index], lw=2)
    ax.set_xlabel('Wavelength [nm]', fontsize=16, fontweight='bold')
    ax.set_ylabel('Reflection', fontsize=16, fontweight='bold')
    ax.tick_params(axis='both', labelsize=14)
    ax.legend(frameon=True, loc='upper right', ncol=2, prop={'size': 12})

plt.tight_layout()
plt.savefig('test.png')