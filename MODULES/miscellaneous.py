import numpy as np
import astropy.constants as c
import astropy.units as u
from . import file_handling as fh

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


def perc_below_XUV(input_array, limit):
	"""
	Simple calculation of input array fraction below some limiting value
	"""
	total = len(input_array)
	number = np.where(input_array <= limit)
	
	return len(number[0]) / total * 100


def total_sample_eval(data_nemec, data_stel_full, data_stel_upl):
	"""DOC"""
	# We know that the Nemec sample is a reduced form of the Stelzer_FLL
	# sample and does not contain stars from the Stelzer_UPL sample. We
	# therefore want to find an index list of stars NOT in the Nemec
	# sample
	# STELZER-NEMEC OVERLAPPING INDICES
	sui = fh.find_index_comparison(data_stel_full.id, data_nemec.id)
	
	# PRINT A SANITY CHECK FOR SAMPLE SIZE
	print(f"NEMEC SAMPLE SIZE = {len(data_nemec.id)}\n"
	      f"REMAINING STELZER SAMPLE SIZE = {len(sui)}\n"
	      f"STELZER UPL SAMPLE SIZE = {len(data_stel_upl.id)}\n"
	      f"TOTAL SAMPLE = "
	      f"{len(data_stel_full.id) + len(data_stel_upl.id)}\n\n")
	
	for limit in [1, 10, 20]:
		print(f"BELOW LIMIT = {limit} fXUV_E\n")
		write_compiled_limits(limit, data_nemec, data_stel_full, sui,
		                      data_stel_upl)
		print("\n")


def write_compiled_limits(limit, nemec, stelzer_fll, stelzer_ui, stelzer_upl):
	"""DOC"""
	print("Optimistic inner edge:")
	print_sample_eval(limit, nemec, stelzer_fll, stelzer_ui, stelzer_upl,
	                  "opt_in")
	
	print("Conservative inner edge:")
	print_sample_eval(limit, nemec, stelzer_fll, stelzer_ui, stelzer_upl,
	                  "con_in")
	
	print("Conservative outer edge:")
	print_sample_eval(limit, nemec, stelzer_fll, stelzer_ui, stelzer_upl,
	                  "con_out")
	
	print("Optimistic outer edge:")
	print_sample_eval(limit, nemec, stelzer_fll, stelzer_ui, stelzer_upl,
	                  "opt_out")


def print_sample_eval(limit, nemec, stelzer_fll, stelzer_ui, stelzer_upl, ind):
	"""DOC"""
	nemec_flux = getattr(nemec.incFXUV, ind)
	stel_fll_red = array_reduction(
		getattr(stelzer_fll.incFXUV, ind), stelzer_ui)
	stel_upl = getattr(stelzer_upl.incFXUV, ind)
	
	nem_num = len(np.where(nemec_flux <= limit)[0])
	rs_fll_num = len(np.where(stel_fll_red <= limit)[0])
	s_upl_num = len(np.where(stel_upl <= limit)[0])
	combined_num = nem_num + rs_fll_num + s_upl_num
	total_sample_size = len(nemec_flux) + len(stel_fll_red) + len(stel_upl)
	
	print(f"NEMEC:\t {nem_num} of {len(nemec_flux)} STARS")
	print(f"RS_FLL:\t {rs_fll_num} of {len(stel_fll_red)} STARS")
	print(f"S_UPL:\t {s_upl_num} of {len(stel_upl)} STARS")
	print(f"COMBINED PERCENTAGE of {combined_num} "
	      f"out of {total_sample_size} STARS:\t "
	      f"{combined_num / total_sample_size * 100:.2f} %\n")
	
