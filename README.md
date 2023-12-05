# Guided mode resonance spectrum analysis
Python script for an S4 RCWA simulation in Lua to model and plot the reflection spectrum and phase of a 1D guided mode resonance grating.

## Features
The code works as follows:
* The python sript is used to run the Lua script by passing a dictionary with all the required parameters
* Thus, the Lua script sweeps wavelength, analytically solving the reflection spectrum
* The phase is computed using the complex amplitude of the reflected wave
* The reflection and phase data are read into the python script from csv files, where they are then plotted

## Requirements
These scripts were tested using Python 3.11, and S4 requires Lua 5.2.4.