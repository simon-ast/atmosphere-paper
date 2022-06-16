import numpy as np
import astropy.constants as c
import astropy.units as u

# GLOBAL CONSTANTS
SIGMA_SB = c.sigma_sb.value
PARSEC = c.pc.value
R_SUN = c.R_sun.value


def array_reduction(data_array: np.ndarray,
                    index_list: np.ndarray) -> np.ndarray:
	"""
	Reduction of an array by a list of indices.

	:param data_array: NDARRAY,
		Array that is to be reduced
	:param index_list: NDARRAY,
		List of indices that should be deleted
	:return: NDARRAY,
		The reduced array
	"""
	# Choose axis=0 to delete rows and not flatten the array
	reduced_array = np.delete(data_array, index_list, axis=0)

	return reduced_array


def radius_star(log_fbol: np.ndarray,
                T_eff: np.ndarray,
                distance: np.ndarray) -> np.ndarray:
	"""
	As described in Stelzer et al. (2013), synthetic surface fluxes have
	been converted to observed fluxes by a dilution factor:
	
				f_obs = (R_S / d)^2 * f_surf
	
	Rearranging this allows the re-calculation of the stellar radius:
	
				R_S = (f_obs / f_surf)^1/2 * d
	
				
	:param log_fbol: NDARRAY,
		Logarithmic f_bol in cgs units
	:param T_eff: NDARRAY,
		Temperature in Kelvin
	:param distance: NDARRAY,
		Distance in parsec
	:return: NDARRAY,
		Stellar radii in units of solar radius
	"""
	# See equation in doc-string, in units of [m]
	r_star = (10 ** log_fbol * 1e-3) / (SIGMA_SB * T_eff ** 4) * \
	         distance * PARSEC

	return r_star / R_SUN


def flux_to_luminosity(distance: np.ndarray,
                       log_flux: np.ndarray) -> np.ndarray:
	"""
	Simple calculation of luminosity from flux value, based in the CGS system.
	
	:param distance: NDARRAY,
		Distance in parsec
	:param log_flux: NDARRAY,
		Logarithmic flux value in CGS units
	:return: NDARRAY,
		Luminosity in CGS units
	"""
	
	return 4 * np.pi * (distance * c.pc.to(u.cm).value) ** 2 * 10 ** log_flux
