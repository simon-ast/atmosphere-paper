import numpy as np
from astropy.constants import sigma_sb

# GLOBAL CONSTANTS IN CGS
SIGMA_SB = sigma_sb.value


def R_star(f_bol, Teff, distance):
	"""DOC"""
	sb_con = 5.670e-8
	pc = 3.086e16
	R_sol = 6.955e8

	return (((10 ** f_bol) * 1e-3) / (sb_con * Teff ** 4)) ** (1 / 2) * distance * pc * 1 / R_sol


def L_conv(d, f_searched):
	"""DOC"""
	return 4 * m.pi * (d * 3.086e18) ** 2 * 10 ** f_searched


def inc_flux(L_XUV, d_HZ):
	"""DOC"""
	return (L_XUV / (4 * m.pi * (d_HZ * au_to_cm) ** 2)) / 5.6