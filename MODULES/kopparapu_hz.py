import numpy as np
import astropy.constants as c


# NECESSARY GLOBAL CONSTANT IN CGS
L_SUN = c.L_sun.cgs.value
AU_CGS = c.au.cgs.value
CURRENT_XUV_EARTH = 5.6


class KopparapuHZs:
	"""
	This instantiates a class object with 4 attributes, pointing to
	habitable zone distances from Kopparapu et al. (2013) and the
	addendum in Kopparapu et al. (2014).
	"""
	def __init__(self, temperature, luminosity) -> None:
		self.opt_in = habitable_zone_distance(temperature, luminosity, "oi")
		self.con_in = habitable_zone_distance(temperature, luminosity, "ci")
		self.con_out = habitable_zone_distance(temperature, luminosity, "co")
		self.opt_out = habitable_zone_distance(temperature, luminosity, "oo")


class HZincidenXUVflux:
	"""Converts XUV luminosity and distance to incident flux"""
	def __init__(self, l_xuv, HZclass) -> None:
		self.opt_in = relative_incident_flux(l_xuv, HZclass.opt_in)
		self.con_in = relative_incident_flux(l_xuv, HZclass.con_in)
		self.con_out = relative_incident_flux(l_xuv, HZclass.con_out)
		self.opt_out = relative_incident_flux(l_xuv, HZclass.opt_out)


def habitable_zone_distance(T_eff, L, est_ident):
	"""
	HZ estimation from Kopparapu et al. (2013, 2014).
	
	:param T_eff: NDARRAY,
		Stellar temperature in Kelvin
	:param L: NDARRAY,
		Stellar bolometric luminosity in CGS units
	:param est_ident: STR,
		Identifier for the estimation boundary
	:return: NDARRAY,
		HZ distance in AU
	"""
	# Determine valid indicators
	valid_ind = ["oi", "ci", "co", "oo"]
	est_indices = dict(zip(valid_ind, range(4)))
	
	# SANITY CHECK: indicator for estimate must exist
	assert est_ident.lower() in ["oi", "ci", "co", "oo"], \
		f"INDICATOR {est_ident} FOR ESTIMATION METHOD NOT RECOGNIZED!"
	
	# Parameter matrix organized by oi, ci, co, oo estimates
	# PLEASE NOTE THE ERRATUM TO THE ORIGINAL KOPPARAPU (2013) PAPER!
	param = np.array([
		[1.4335e-4, 3.3954e-9, -7.6364e-12, -1.1950e-15],
		[1.2456e-4, 1.4612e-8, -7.6345e-12, -1.7511e-15],
		[5.9578e-5, 1.6707e-9, -3.0058e-12, -5.1925e-16],
		[5.4471e-5, 1.5275e-9, -2.1709e-12, -3.8282e-16],
	])
	
	# Set correct param-subindex according to est_ident
	est_index = est_indices[est_ident]
	
	# Call the S_eff calculation function with correct parameters
	S_eff = effective_flux(param[est_index], T_eff, est_index)
	
	# Calculate distance
	distance = np.sqrt((L / L_SUN) / S_eff)
	
	return distance
	
	
def effective_flux(param_list, T_eff, estimation_index):
	"""Intermediate step in HZ calculation"""
	S_effsun = [1.7763, 1.0385, 0.3507, 0.3207]
	
	# Temperature array consisting of powers 1 to 4
	temp = np.array(
		[(T_eff - 5780) ** (i + 1) for i in range(4)]
	)
	
	# Transpose the temperature-power array to have each row be a list
	# of Temp ** 1 to Temp ** 4, and then calculate the dot-product
	# with the parameter list vector
	return S_effsun[estimation_index] + temp.T @ param_list


def relative_incident_flux(l_xuv: np.ndarray,
                           hz_distance: np.ndarray):
	"""
	Calculates the incident XUV-flux levels at a given distance (HZ
	boundaries) and returns the value scaled to the current incident
	XUV flux on Earth.
	
	:param l_xuv: NDARRAY,
		XUV luminosity in CGS units
	:param hz_distance: NDARRAY,
		Distance value in AU
	:return: NDARRAY,
		Scaled incident XUV flux
	"""
	
	inc_fxuv = l_xuv / (4 * np.pi * (hz_distance * AU_CGS) ** 2)
	
	return inc_fxuv / CURRENT_XUV_EARTH
