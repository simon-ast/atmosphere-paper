import numpy as np
from MODULES.miscellaneous import perc_below_XUV as pbXUV


def write_full_table(data_set, save_directory):
	"""DOC"""
	sample_len = len(data_set.id)
	
	with open(f"{save_directory}/LONG_TABLE.dat", "w") as f:
		# HEADER AND LOGGING INFO
		f.write(f"SAMPLE SIZE = {sample_len}\n\n")
		
		for i in range(sample_len):
			f.write(f'{data_set.id[i]} & {data_set.radius[i]:.2f} & '
			        f'{np.log10(data_set.Lxuv[i]):.2f} & '
			        f'[{1e1 * data_set.HZ.con_in[i]:.2f}, '
			        f'{1e1 * data_set.HZ.con_out[i]:.2f}] & '
			        f'[{1e1 * data_set.HZ.opt_in[i]:.2f}, '
			        f'{1e1 * data_set.HZ.opt_out[i]:.2f}] & '
			        f'[{np.log10(data_set.incFXUV.con_in[i]):.2f}, '
			        f'{np.log10(data_set.incFXUV.con_out[i]):.2f}] & '
			        f'[{np.log10(data_set.incFXUV.opt_in[i]):.2f}, '
			        f'{np.log10(data_set.incFXUV.opt_out[i]):.2f}] ' +
			        f'\\' * 2 + f'\n')


def write_perc_table(dssul, dssfl, dsn, save_directory):
	"""DOC"""
	with open(f"{save_directory}/PERC_TABLE.dat", "w") as f:
		# PRELIM. INFORMATION
		f.write(f"STELZER UPPER LIMITS: \t {len(dssul.id)}\n"
		        f"STELZER FULL SAMPLE:\t {len(dssfl.id)}\n"
		        f"NINA CALCULATED SAMPLE:\t {len(dsn.id)}\n\n\n")
		
		# TABLE FORMATTING
		# Header
		f.write("\multicolumn{2}{c}{\multirow{2}{*}{Incident "
		        "$f_{\mathrm{XUV}}$}} & \multicolumn{2}{c}{(1)} & "
		        "\multicolumn{2}{c}{(2)} & \multicolumn{2}{c}{(3)}"
				+ "\\" * 2 + "\n" +
				" & & Inner & Outer & Inner & Outer & Inner & Outer "
				+ "\\" * 2 + "\n" +
		        "\multicolumn{2}{c}{$\left[ f_{\mathrm{XUV}, \Earth} "
		        "\\right]$}&  \multicolumn{2}{c}{Edge} & "
		        "\multicolumn{2}{c}{Edge} & \multicolumn{2}{c}{Edge} "
				+ "\\" * 2 + "\n" +
		        "\hline \n")
		
		# Conservative percentages for all data sets
		f.write(
			"\t\multirow{3}{*}{\\rotatebox[origin=c]{90}{\\textbf{Cons.}}}" +
			f" & {1} & "
			f"{pbXUV(dssul.incFXUV.con_in, 1):.2f} & "
			f"{pbXUV(dssul.incFXUV.con_out, 1):.2f} & "
			f"{pbXUV(dssfl.incFXUV.con_in, 1):.2f} & "
			f"{pbXUV(dssfl.incFXUV.con_out, 1):.2f} & "
			f"{pbXUV(dsn.incFXUV.con_in, 1):.2f} & "
			f"{pbXUV(dsn.incFXUV.con_out, 1):.2f} "
			+ "\\" * 2 + "\n"
		)
		
		for limit in [10, 20]:
			f.write(
				f"\t & {limit} & "
		        f"{pbXUV(dssul.incFXUV.con_in, limit):.2f} & "
		        f"{pbXUV(dssul.incFXUV.con_out, limit):.2f} & "
		        f"{pbXUV(dssfl.incFXUV.con_in, limit):.2f} & "
		        f"{pbXUV(dssfl.incFXUV.con_out, limit):.2f} & "
		        f"{pbXUV(dsn.incFXUV.con_in, limit):.2f} & "
		        f"{pbXUV(dsn.incFXUV.con_out, limit):.2f} "
		        + "\\" * 2 + "\n"
			)
		
		# Separator between conservative and optimistic
		f.write("\hline \n")
		
		# Optimistic percentages percentages for all data sets
		f.write(
			"\t\multirow{3}{*}{\\rotatebox[origin=c]{90}{\\textbf{Optim.}}}"
			+ f" & {1} & "
			  f"{pbXUV(dssul.incFXUV.opt_in, 1):.2f} & "
			  f"{pbXUV(dssul.incFXUV.opt_out, 1):.2f} & "
			  f"{pbXUV(dssfl.incFXUV.opt_in, 1):.2f} & "
			  f"{pbXUV(dssfl.incFXUV.opt_out, 1):.2f} & "
			  f"{pbXUV(dsn.incFXUV.opt_in, 1):.2f} & "
			  f"{pbXUV(dsn.incFXUV.opt_out, 1):.2f} "
			+ "\\" * 2 + "\n")
		
		for limit in [10, 20]:
			f.write(
				f"\t & {limit} & "
		        f"{pbXUV(dssul.incFXUV.opt_in, limit):.2f} & "
		        f"{pbXUV(dssul.incFXUV.opt_out, limit):.2f} & "
		        f"{pbXUV(dssfl.incFXUV.opt_in, limit):.2f} & "
		        f"{pbXUV(dssfl.incFXUV.opt_out, limit):.2f} & "
		        f"{pbXUV(dsn.incFXUV.opt_in, limit):.2f} & "
		        f"{pbXUV(dsn.incFXUV.opt_out, limit):.2f} "
		        + "\\" * 2 + "\n")
			
		# Separator at the end
		f.write("\hline \n")
