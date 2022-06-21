import numpy as np
import astropy.units as u
import astropy.constants as c
from . import miscellaneous as misc
from . import kopparapu_hz as khz

# NECESSARY GLOBAL: CGS FLUX UNIT
FLUX_CGS = u.erg / u.cm / u.cm / u.s
AU_CM = c.au.cgs.value
RSOL_CM = c.R_sun.cgs.value


class DataSetStelzer:
	"""DOC"""
	def __init__(self, filename):
		# First instantiate data array
		assigned_data = assign_data_stelzer(filename)
		
		# ASSIGN DATA TO IDENTIFIERS
		self.id = assigned_data[:, 0]
		self.dist = assigned_data[:, 2].astype(float)
		self.teff = assigned_data[:, 5].astype(float)
		self.LOGfbolE = assigned_data[:, 6].astype(float)
		self.LOGfx = assigned_data[:, 12].astype(float)
		
		# Determine if full case or upper-limit only
		identifier = assigned_data[:, -1]
		signal = " N/A\n"
		
		# Lists indices where only upper limit is valid
		self.limit_case = np.where(identifier == signal)[0]
		
		# Instantiate future attributes
		self.incFXUV = None
		self.HZ = None
		self.Lxuv = None
		self.Lbol = None
		self.radius = None
	
	def slice_dataset(self, case_ident):
		"""DOC"""
		full_index_array = np.arange(len(self.id))
		
		# For explanation, see comment below
		if case_ident == "upper_limits":
			index_array = misc.array_reduction(full_index_array,
			                                   self.limit_case)
		else:
			index_array = self.limit_case
		
		# The call "array_reduction()" excludes all indices from the list
		# passed as an argument. Therefore, the case "upper_limits" lists all
		# indices where NOT ONLY upper limits are given!
		self.id = misc.array_reduction(self.id, index_array)
		self.dist = misc.array_reduction(self.dist, index_array)
		self.teff = misc.array_reduction(self.teff, index_array)
		self.LOGfbolE = misc.array_reduction(self.LOGfbolE, index_array)
		self.LOGfx = misc.array_reduction(self.LOGfx, index_array)
		self.limit_case = case_ident
		
		# ADDITIONAL ATTRIBUTES WITH EXTERNAL CALCULATIONS
		# Stellar radius [R_sol]
		self.radius = misc.radius_star(self.LOGfbolE, self.teff, self.dist)
		
		# Stellar bolometric luminosity [cgs]
		self.Lbol = misc.flux_to_luminosity(self.dist, self.LOGfbolE)
		
		# Simple scaling of X-ray luminosity to XUV luminosity
		# by a factor of 7
		self.Lxuv = 7 * misc.flux_to_luminosity(self.dist, self.LOGfx)
		
		# Habitable zone distances [au] as sub-class
		self.HZ = khz.KopparapuHZs(self.teff, self.Lbol)
		
		# Relative incident XUV fluxes [scaled to current Earth value]
		self.incFXUV = khz.HZincidenXUVflux(self.Lxuv, self.HZ)


def read_data(filename, separator):
	"""Read-in data file in string format"""
	with open(filename, "r") as f:
		data = [line.split(separator) for line in f]
	
	return data


def assign_data_stelzer(filename):
	"""DOC"""
	# Create raw data array and cut header
	raw_data_header = read_data(filename, "\t")
	raw_data = np.array(raw_data_header[4:])
	
	# CONVERT NECESSARY STRINGS TO FLOATS
	for i in range(len(raw_data)):
		
		# 3rd entry is distance in parsec
		raw_data[i][2] = float(raw_data[i][2])
		
		# 4th entry is distance uncertainty in parsec
		raw_data[i][3] = float(raw_data[i][3])
		
		# 6th entry is effective temperature in Kelvin
		raw_data[i][5] = float(raw_data[i][5])
		
		# 7th entry is logarithmic bolometric flux at 1 AU in FLUX_CGS
		raw_data[i][6] = -1 * float(raw_data[i][6].strip().strip("−"))
		
		# 13th entry is logarithmic X-ray flux in FLUX_CGS
		raw_data[i][12] = -1 * float(raw_data[i][12].strip().strip("−"))
	
	return raw_data
		

class DataSetNemec:
	"""DOC"""
	def __init__(self, filename):
		# First instantiate data array
		assigned_data = assign_data_nemec(filename)
		
		# ASSIGN DATA TO IDENTIFIERS
		# Stellar ID "PM XXX"
		self.id = assigned_data[:, 0]
		
		# Effective temperature
		self.teff = assigned_data[:, 1].astype(float)
		
		# Stellar radius (previously calculated) in Rsol
		self.radius = assigned_data[:, 2].astype(float)
		
		# Distance in parsec
		self.dist = assigned_data[:, 3].astype(float)
		
		# Logarithmic bolometric luminosity
		self.LOGfbol = assigned_data[:, 4].astype(float)
		
		# XUV flux @ 1 AU (converted to cgs)
		self.fxuvE = assigned_data[:, 8].astype(float) * 1e3
		
		# ADDITIONAL ATTRIBUTES WITH EXTERNAL CALCULATIONS
		# Stellar bolometric luminosity [cgs]
		self.Lbol = misc.flux_to_luminosity(self.dist, self.LOGfbol)
		
		# XUV luminosity as calculated by Nina's model
		self.Lxuv = 4 * np.pi * AU_CM ** 2 * self.fxuvE * self.radius ** 2
		
		# Habitable zone distances [au] as sub-class
		self.HZ = khz.KopparapuHZs(self.teff, self.Lbol)
		
		# Relative incident XUV fluxes [scaled to current Earth value]
		self.incFXUV = khz.HZincidenXUVflux(self.Lxuv, self.HZ)
		
		# Instantiate future attributes
		self.Feuv = None
		self.Fx = None
		self.Fxuv = None
		self.Leuv = None
		self.Lx = None
		self.LOGfx = None
		
	def fill_data(self, stelzer_data):
		"""Generate additional data with the help of old data set"""
		# Logarithmic X-ray flux from Stelzer-Data
		non_ident_id = misc.array_reduction(
			np.arange(len(stelzer_data.id)),
			find_index_comparison(stelzer_data.id, self.id)
		)
		self.LOGfx = misc.array_reduction(stelzer_data.LOGfx, non_ident_id)
		
		# X-ray luminosity from X-ray flux
		self.Lx = misc.flux_to_luminosity(self.dist, self.LOGfx)
		
		# EUV luminosity
		self.Leuv = self.Lxuv - self.Lx
		
		# Surface flux values (XUV, X-ray, EUV)
		self.Fxuv = self.Lxuv / (4 * np.pi * (self.radius * RSOL_CM) ** 2)
		self.Fx = self.Lx / (4 * np.pi * (self.radius * RSOL_CM) ** 2)
		self.Feuv = self.Leuv / (4 * np.pi * (self.radius * RSOL_CM) ** 2)


def assign_data_nemec(filename):
	"""DOC"""
	# File entries are separated by 4 whitespaces
	raw_data_header = read_data(filename, "    ")
	raw_data = np.array(raw_data_header[1:])
	
	return raw_data


def find_index_comparison(stelzer_id, nemec_id):
	"""
	Find indices of Stelzer et al. (2013) array corresponding to data
	provided by Nina Nemec.
	"""
	indices = []
	for name_1 in stelzer_id:
		for name_2 in nemec_id:
			if name_1 == name_2:
				# WHY IS THIS SO NESTED?
				indices.append(np.where(stelzer_id == name_1)[0][0])
	
	return np.array(indices)

