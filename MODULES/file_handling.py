import numpy as np
import copy as cp
import astropy.units as u

# NECESSARY GLOBAL: CGS FLUX UNIT
FLUX_CGS = u.erg / u.cm / u.cm / u.s


def read_data(filename):
	"""Read-in data file in string format"""
	with open(filename, "r") as f:
		data = [line.split("\t") for line in f]
	
	# Cut the first 4 lines (header)
	data = np.array(data[4:])
	
	return data


def assign_data(filename):
	"""DOC"""
	# Create raw data array
	raw_data = read_data(filename)
	
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


class DataSet:
	def __init__(self, filename):
		"""DOC"""
		# First instantiate data array and determine length
		assigned_data = assign_data(filename)
		sample_size = len(assigned_data)
		
		# ASSIGN DATA TO IDENTIFIERS
		self.id = assigned_data[:, 0]
		self.dist = assigned_data[:, 3].astype(float)
		self.teff = assigned_data[:, 5].astype(float)
		self.LOGfbolE = assigned_data[:, 6].astype(float)
		self.LOGfx = assigned_data[:, 12].astype(float)
		
		# Determine if full case or upper-limit only
		identifier = assigned_data[:, -1]
		signal = " N/A\n"
		self.limit_case = np.where(identifier == signal)[0]

'''
READ IN THE COMBINED DATA TABLE
RETURN MATRIX WITH VALUES AND UNITS
'''

