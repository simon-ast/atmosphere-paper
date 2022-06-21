# Atmosphere Paper - Data Evaluation and Calculations

The `main.py`-file collects all subroutines and subsequently executes them. The main parts are:

1. Reading in the original data set from [Stelzer et al (2013)](https://ui.adsabs.harvard.edu/abs/2013MNRAS.431.2063S/abstract "Stelzer et al (2013)") and the re-calculated values from Nina Nemec
	a. The raw data is stored in the DATA directory
	
2. Using this data to generate the necessary plots
	a. These plots are saved as `.eps`-files in the PLOT directory and its substructre

3. Writing the final data products into text files with the appropriate LaTeX formatting to simply put them in a LaTeX document
	a. These text files are saved into the main directory of the repository

### Selected Substructures

#### MODULES
The scripts contained in this provide the main functionality of the calculation routine:

- **`file_handling.py`**: All functions and object classes necessary to generate data set objects for both data sources
- **`kopparapu_hz.py`**: All functions necessary to convert effective temperatures and bolometric luminosities of stars into habitable zone distances and, together with XUV luminosities, into incident XUV flux values. This follows the paper of [Kopparapu et al. (2013)](https://ui.adsabs.harvard.edu/abs/2013ApJ...765..131K/abstract "Kopparapu et al. (2013)") (Please note that there is an [Erratum](https://ui.adsabs.harvard.edu/abs/2013ApJ...770...82K/abstract "Erratum") to the coefficients from that paper!)
- **`plotting.py`**: Routines for plots placed in the paper
- **`writing.py`**: Same as above, but for tables in the paper
-**`miscellanous.py`**: Collection of functions not placed in other files (e.g. array reduction based on list of indices)


#### OLD
A collection of my previous scripts, basically serving the same function. Please don't open any of the files in here if you do not want to be blinded by gruesome displays of uncommented, non-PEP8 formatted code.