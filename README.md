# Guided mode resonance spectrum analysis
Python scripts for S4 RCWA simulations in Lua to model and plot the reflection spectrum and phase of a 1D guided mode resonance grating. Also included are is a script that iterates through given grating parameters (period, thickness etc.) and plots the corresponding reflection spectra.

## Features
The code works as follows:
* The python sript is used to run the Lua script by passing a dictionary with all the required parameters
* Thus, the Lua script sweeps wavelength, analytically solving the reflection spectrum
* The phase is computed using the complex amplitude of the reflected wave
* The reflection and phase data are read into the python script from csv files, where they are then plotted

Update: Spectra_field_extraction.py provides a more recent script that allows the user to toggle electric field simulations with a boolean flag.

## Requirements
These scripts were tested using Python 3.11, and S4 requires Lua 5.2.4.
