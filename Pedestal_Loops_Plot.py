import os
import numpy as np
import matplotlib.pyplot as plt
import glob

def last_9chars(x):
    return(x[1:])

root = os.getcwd()
files = glob.glob('FFs/*.csv')
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

labels = ['0.5', '0.6', '0.7', '0.8', '0.9']

fig, ax = plt.subplots(figsize=[10,7])
for index, l in enumerate(l_array):
        ax.plot(l,r_array[index], label=[x for x in labels][index])
        ax.set_xlabel('Wavelength [nm]', fontsize=16, fontweight='bold')
        ax.set_ylabel('Reflection', fontsize=16, fontweight='bold')
        ax.tick_params(axis='both', labelsize=14)
        ax.legend(frameon=True, loc=0, ncol=2, prop={'size': 12})

plt.tight_layout()
plt.savefig('FF_Sweep_Plot.png')