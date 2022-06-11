import sys
import numpy as np
from MODULES import file_handling as fh

DATA_FILE = f"{sys.path[0]}/DATA/stelzer_tables_combined.dat"


def main():
	# Read in the total dataset from Stelzer (2013)
	# This covers lines 30 - 70 of the old script
	stelzer_full = fh.DataSet(DATA_FILE)
	
	print(stelzer_full.limit_case)
	

if __name__ == "__main__":
	main()
