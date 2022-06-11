import numpy as np
import astropy.units as u
from astropy.constants import L_sun


# NECESSARY GLOBAL CONSTANT IN CGS
L_SUN = L_sun.cgs


def habitable_zone_distance(T_eff, L, est_ident):
	"""DOC"""
	# Determine valid indicators
	valid_ind = ["oi", "ci", "co", "oo"]
	est_indices = dict(zip(valid_ind, range(4)))
	
	# SANITY CHECK: indicator for estimate must exist
	assert est_ident.lower() in ["oi", "ci", "co", "oo"], \
		f"INDICATOR {est_ident} FOR ESTIMATION METHOD NOT RECOGNIZED!"
	
	# Parameter matrix organized by oi, ci, co, oo estimates
	param = np.array([
		[2.136e-4, 2.533e-8, -1.332e-11, -3.097e-15],
		[1.332e-4, 1.580e-8, -8.308e-12, -1.931e-15],
		[6.171e-5, 1.698e-9, -3.198e-12, -5.575e-16],
		[5.547e-5, 1.526e-9, -2.874e-12, -5.011e-16],
	])
	
	# Set correct param-subindex according to est_ident
	est_index = est_indices[est_ident]
	
	# Call the S_eff calculation function with correct parameters
	S_eff = effective_flux(param[est_index], T_eff)
	
	# Calculate distance
	distance = np.sqrt((L / L_sun.cgs) / S_eff)
	
	return distance
	
	
def effective_flux(param_list, T_eff):
	"""Intermediate step in HZ calculation"""
	S_effsun = 1.107
	
	# Temperature array consisting of powers 1 to 4
	temp = np.array(
		[(T_eff - 5780) ** (i + 1) for i in range(4)]
	)
	
	return S_effsun + np.sum(param_list * temp)
