import os
import sys
import numpy
import numpy as np

OLD_DATA_DIR = f"{sys.path[0]}/original"
FILE_NAME = "stelzer_tables_combined.dat"


def main():
	# Create file and insert comment + header
	start_file()
	
	# Read in both old data files. It is important to note here that the
	# arrangement of both tables is identically done by NAME
	stelzer_1 = read_old_data(f"{OLD_DATA_DIR}/dataset_1_stelzer.dat")
	stelzer_2 = read_old_data(f"{OLD_DATA_DIR}/dataset_2_stelzer.dat")
	
	# SANITY CHECK: Both arrays have to have same length
	assert len(stelzer_1) == len(stelzer_2), \
		f"SAMPLE SIZE NOT THE SAME!"
	sample_size = len(stelzer_1)
	
	# Write iteratively
	for i in range(sample_size):
		write_line(stelzer_1[i], stelzer_2[i], FILE_NAME)
		
	
def start_file():
	"""Start new file with header"""
	with open(FILE_NAME, "w") as f:
		f.write("COMBINED TABLES 1 AND 2 FROM STELZER (2013) APPENDIX.\n"
		        "ALL FLUX VALUES ARE IN ERG/CM2/S!\n\n")
		f.write(f"NAME\t Gl/GJ\t d [pc]\t d_unc [pc]\t SpT\t T_eff [K]\t "
		        f"log f_bol,E \t v sin(i) [km/s]\t "
		        f"log f_NUV\t log f_NUV_bound\t "
		        f"log f_FUV\t log_f_FUV_bound\t "
		        f"log f_X\t log f_X_bound\n")


def write_line(data_s1, data_s2, filename):
	"""
	Write one line into combined data table from old singular ones. Both
	arguments represent slices of the individual old Stelzer tables.
	"""
	# SANITY CHECK: Both table slices must represent the same star
	assert data_s1[0].strip() == data_s2[0].strip(), \
		f"{data_s1[0].strip()} IS NOT THE SAME AS {data_s2[0].strip()}!"
	
	# Set up the data to write correctly
	keys = ["name", "opt_name", "dist", "dist_unc", "spt", "teff",
	        "fbe", "vsini", "fnuv", "fnuvb", "ffuv", "ffuvb",
	        "fx", "fxb"]
	values = [data_s1[0].strip(), data_s1[1].strip(),
	          float(data_s1[2]), float(data_s1[4]),
	          data_s1[5].strip(), float(data_s1[6]),
	          data_s1[7].strip(), data_s1[8].strip("\n"),
	          data_s2[1].strip(), data_s2[2].strip(),
	          data_s2[4].strip(), data_s2[5].strip(),
	          data_s2[7].strip(), data_s2[8].strip()]
	
	# Replace empty values with the string "N/A"
	for i in range(len(values)):
		if values[i] == "":
			values[i] = "N/A"

	# Create dictionary for readability
	data_line = dict(zip(keys, values))
	
	# Append to file according to the header
	with open(filename, "a") as f:
		f.write(f"{data_line['name']}\t "
		        f"{data_line['opt_name']}\t "
		        f"{data_line['dist']}\t "
		        f"{data_line['dist_unc']}\t "
		        f"{data_line['spt']}\t "
		        f"{data_line['teff']}\t "
		        f"{data_line['fbe']}\t "
		        f"{data_line['vsini']}\t "
		        f"{data_line['fnuv']}\t "
		        f"{data_line['fnuvb']}\t "
		        f"{data_line['ffuv']}\t "
		        f"{data_line['ffuvb']}\t "
		        f"{data_line['fx']}\t "
		        f"{data_line['fxb']}\n")


def read_old_data(filename):
	"""Read-in old Stelzer data files"""
	with open(filename, "r") as f:
		data = np.array([
			line.split("\t") for line in f
		])
	
	return data


if __name__ == "__main__":
	main()
