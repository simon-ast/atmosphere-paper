import sys
import copy
from MODULES import file_handling as fh
from MODULES import plotting
from MODULES import writing
from MODULES import miscellaneous as misc

DATA_FILE_ST = f"{sys.path[0]}/DATA/stelzer_tables_combined.dat"
DATA_FILE_NE = f"{sys.path[0]}/DATA/nemec_fXUV_1AU.bin"
TABLE_SAVE_DIR = f"{sys.path[0]}"


def main():
	# Read in the total dataset from Stelzer (2013) and separate.
	# This covers lines 30 - 128 of the old script.
	stelzer_ALL = fh.DataSetStelzer(DATA_FILE_ST)
	
	# CONTAINS DATA WITH UPPER LIMITS ONLY
	stelzer_UPL = copy.deepcopy(stelzer_ALL)
	stelzer_UPL.slice_dataset("upper_limits")
	
	# CONTAINS "COMPLETE" DATA
	stelzer_FLL = copy.deepcopy(stelzer_ALL)
	stelzer_FLL.slice_dataset("bound_avail")
	
	# Read in the total dataset from Nina Nemec and separate.
	nemec_FLL = fh.DataSetNemec(DATA_FILE_NE)
	nemec_FLL.fill_data(stelzer_ALL)
	
	misc.total_sample_eval(nemec_FLL, stelzer_FLL, stelzer_UPL)
	exit()
	
	# CALL ON PLOTTING ROUTINES
	# 2 x 2 conservative boundary plots
	plotting.fluxes_HZ(stelzer_FLL, stelzer_UPL, nemec_FLL, "con")
	# 2 x 2 optimistic boundary plots
	plotting.fluxes_HZ(stelzer_FLL, stelzer_UPL, nemec_FLL, "opt")
	# DOC
	plotting.fluxes_HZ_reduced(stelzer_FLL, stelzer_UPL, nemec_FLL, "con")
	# DOC
	plotting.flux_lum_comparison(nemec_FLL)
	
	# Write results into text document with LaTeX formatting
	writing.write_full_table(nemec_FLL, TABLE_SAVE_DIR)
	writing.write_perc_table(stelzer_UPL, stelzer_FLL, nemec_FLL,
	                         TABLE_SAVE_DIR)
	
	
if __name__ == "__main__":
	# Set global parameters for plots
	plotting.rc_setup()
	
	main()
