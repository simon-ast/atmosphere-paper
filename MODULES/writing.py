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
			        f'[{1e1 * data_set.HZ.con_in[i]:.2f},'
			        f'{1e1 * data_set.HZ.con_out[i]:.2f}] & '
			        f'[{1e1 * data_set.HZ.opt_in[i]:.2f},'
			        f'{1e1 * data_set.HZ.opt_out[i]:.2f}] & '
			        f'[{np.log10(data_set.incFXUV.con_in[i]):.2f},'
			        f'{np.log10(data_set.incFXUV.con_out[i]):.2f}] & '
			        f'[{np.log10(data_set.incFXUV.opt_in[i]):.2f},'
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

"""
\hline\hline
		%
		% TABLE HEADER
		\multicolumn{2}{c}{\multirow{2}{*}{Incident $f_{\mathrm{XUV}}$}} & \multicolumn{2}{c}{(1)} & \multicolumn{2}{c}{(2)} & \multicolumn{2}{c}{(3)} \\
		& & Inner & Outer & Inner & Outer & Inner & Outer \\
		\multicolumn{2}{c}{$\left[ f_{\mathrm{XUV}, \Earth} \right]$}&  \multicolumn{2}{c}{Edge} & \multicolumn{2}{c}{Edge} & \multicolumn{2}{c}{Edge} \\
		%
		%
		\hline
			\multirow{3}{*}{\rotatebox[origin=c]{90}{\textbf{Cons.}}}
			& 1 & 1.43 & 2.86 & 0.00 & 1.12 & 0.00 & 0.00 \\
			& 10 & 14.29 & 37.14 & 7.87 & 34.83 & 5.06 & 31.65 \\
			& 20 & 22.86 & 55.71 & 22.47 & 42.70 & 16.46 & 50.63 \\
		\hline
			\multirow{3}{*}{\rotatebox[origin=c]{90}{\textbf{Optim.}}} & 1 & 0.00 & 2.86 & 0.00 & 1.12 & 0.00 & 0.00  \\
			& 10 & 7.14 & 41.43 & 3.37 & 37.08 & 0.00 & 31.65 \\
			& 20 & 14.29 & 64.29 & 12.36 & 42.70 & 10.13 & 50.63 \\
		\hline

# 2) List of system percentage below certain threshold
r2 = open("r2.dat", "w")
r2.write(
    "\multicolumn{2}{c|}{Sample} & \multicolumn{3}{c|}{Conservative} & \multicolumn{3}{c}{Optimistic} " + "\\" * 2 + "\n"
)
r2.write("\hline \n" + "\hline \n")
r2.write('\multirow! & I & {:.2f} & {:.2f} & {:.2f} & {:.2f} & {:.2f} & {:.2f} '.format(n_st_upl_ci[0], n_st_upl_ci[1], n_st_upl_ci[2], n_st_upl_oi[0], n_st_upl_oi[1], n_st_upl_oi[2]) + '\\' * 2 + '\n')
r2.write('& O & {:.2f} & {:.2f} & {:.2f} & {:.2f} & {:.2f} & {:.2f} '.format(n_st_upl_co[0], n_st_upl_co[1], n_st_upl_co[2], n_st_upl_oo[0], n_st_upl_oo[1], n_st_upl_oo[2]) + "\\" * 2 + "\n")
r2.write("\hline \n")
r2.write('\multirow! & I & {:.2f} & {:.2f} & {:.2f} & {:.2f} & {:.2f} & {:.2f} '.format(n_st_rest_ci[0], n_st_rest_ci[1], n_st_rest_ci[2], n_st_rest_oi[0], n_st_rest_oi[1], n_st_rest_oi[2]) + '\\' * 2 + '\n')
r2.write('& O & {:.2f} & {:.2f} & {:.2f} & {:.2f} & {:.2f} & {:.2f} '.format(n_st_rest_co[0], n_st_rest_co[1], n_st_rest_co[2], n_st_rest_oo[0], n_st_rest_oo[1], n_st_rest_oo[2]) + "\\" * 2 + "\n")
r2.write("\hline \n")
r2.write('\multirow! & I & {:.2f} & {:.2f} & {:.2f} & {:.2f} & {:.2f} & {:.2f} '.format(n_n_ci[0], n_n_ci[1], n_n_ci[2], n_n_oi[0], n_n_oi[1], n_n_oi[2]) + '\\' * 2 + '\n')
r2.write('& O & {:.2f} & {:.2f} & {:.2f} & {:.2f} & {:.2f} & {:.2f} '.format(n_n_co[0], n_n_co[1], n_n_co[2], n_n_oo[0], n_n_oo[1], n_n_oo[2]) + "\\" * 2 + "\n")

r2.write("\hline \n")
r2.close()
"""