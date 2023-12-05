import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from mpl_toolkits import axes_grid1

def findpeaks(x, y):
    k = max(y)
    idx_y, _ = find_peaks(y, height=k)
    peaks_y = y[idx_y]
    peaks_x = x[idx_y]
    print(f'Peak Lambda= {np.round(peaks_x, 3)}, Refl Max = {np.round(peaks_y, 3)}')
    
    return np.round(peaks_x, 3)

def FWHM(x,y):
    deltax = x[1] - x[0]
    half_max = max(y) / 2
    l = np.where(y > half_max, 1, 0)
    
    return np.around((np.sum(l) * deltax), 5)

def figure_basic(x, y, x_label, y_label):
    fig, ax = plt.subplots(figsize=[10,7])
    ax.plot(x, y, 'k', lw=2)
    ax.set_xlabel(f'{x_label}', fontsize=24, fontweight='bold')
    ax.set_ylabel(f'{y_label}', fontsize=24, fontweight='bold')
    ax.tick_params(axis='both', labelsize=22)  
    plt.tight_layout()

def figure_refl(x, y):
    fig, ax = plt.subplots(figsize=[10,7])
    ax.plot(x, y, 'k', lw=2, label='Reflection')
    ax.set_xlabel('Wavelength [nm]', fontsize=21, fontweight='bold')
    ax.set_ylabel('Reflection [%]', fontsize=22, fontweight='bold', color='k')
    ax.tick_params(axis='both', labelsize=22)
    ax.legend(frameon=True, loc='center right', prop={'size': 14})   
    plt.text(0.8, 0.85, f' Peak λ = {np.round(findpeaks(x, y)[0], 2)}', ha='center', va='center', 
             fontsize=18, fontweight='bold', color='red', transform=ax.transAxes) 
    plt.text(0.8, 0.75, f' FWHM = {np.round(FWHM(x, y), 2)}', ha='center', va='center', 
             fontsize=18, fontweight='bold', color='red', transform=ax.transAxes)
    plt.tight_layout()
    
def figure_refl_phase(x, y1, y2):
    fig, ax = plt.subplots(figsize=[10,7])
    ax.plot(x, y1, 'k', lw=2, label='Reflection')
    ax.set_xlabel('Wavelength [nm]', fontsize=21, fontweight='bold')
    ax.set_ylabel('Reflection [%]', fontsize=22, fontweight='bold', color='k')
    ax.tick_params(axis='both', labelsize=22)
    ax2 = ax.twinx()
    ax2.plot(x, y2, 'm', lw=2, label='Phase')
    ax2.set_ylabel('Phase [π rad]', fontsize=22, fontweight='bold', color = 'm', rotation = 270, labelpad=30)
    ax2.tick_params(axis='both', labelsize=22)
    # plt.axis([None, None, -1.1, 1.1])
    ax.legend(frameon=True, loc='upper right', prop={'size': 14})
    ax2.legend(frameon=True, loc='upper left', prop={'size': 14}) 
    plt.text(0.8, 0.85, f' Peak λ = {np.round(findpeaks(x, y1)[0], 2)}', ha='center', va='center', 
             fontsize=18, fontweight='bold', color='red', transform=ax.transAxes) 
    plt.text(0.8, 0.75, f' FWHM = {np.round(FWHM(x, y1), 2)}', ha='center', va='center', 
             fontsize=18, fontweight='bold', color='red', transform=ax.transAxes)
    plt.tight_layout()
    
def add_colorbar(im, aspect=20, pad_fraction=0.5, **kwargs):
    """Add a vertical color bar to an image plot."""
    divider = axes_grid1.make_axes_locatable(im.axes)
    width = axes_grid1.axes_size.AxesY(im.axes, aspect=1./aspect)
    pad = axes_grid1.axes_size.Fraction(pad_fraction, width)
    current_ax = plt.gca()
    cax = divider.append_axes("right", size=width, pad=pad)
    plt.sca(current_ax)
    return im.axes.figure.colorbar(im, cax=cax, **kwargs)
    
def figure_pixel_plot(cmap, data, xmin, xmax, zmin, zmax, x, z, data_eps):
    fig, ax = plt.subplots()
    mycmap1 = plt.get_cmap(f'cmap')
    k = ax.imshow((data)*(1), aspect='auto', 
              origin='lower', 
              extent=[xmin,xmax,zmin,zmax], 
              cmap=mycmap1)
    ax.contour(x, z, np.flipud(data_eps), 
           extent=[xmin,xmax,zmin,zmax], 
           colors=('k'))
    ax.set_xlabel('X Position [nm]', fontsize=16, fontweight='bold')
    ax.set_ylabel('Z Position [nm]', fontsize=16, fontweight='bold')
    ax.tick_params(axis='both', labelsize=14)

    # plt.title('TM Field - n_cover = 1.0', fontsize=18, fontweight='bold')
    add_colorbar(k)
    fig.tight_layout()
