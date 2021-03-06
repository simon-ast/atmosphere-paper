import sys
import matplotlib as mpl
import matplotlib.pyplot as plt

# GLOBAL: Save directory path
PLOT_SAVE_DIR = f"{sys.path[0]}/PLOTS"


def rc_setup():
	"""Generalized plot attributes"""
	mpl.rcParams["xtick.direction"] = "in"
	mpl.rcParams["xtick.labelsize"] = "large"
	mpl.rcParams["xtick.major.width"] = 1.5
	mpl.rcParams["xtick.minor.width"] = 1.5
	mpl.rcParams["xtick.minor.visible"] = "True"
	mpl.rcParams["xtick.top"] = "True"
	
	mpl.rcParams["ytick.direction"] = "in"
	mpl.rcParams["ytick.labelsize"] = "large"
	mpl.rcParams["ytick.major.width"] = 1.5
	mpl.rcParams["ytick.minor.width"] = 1.5
	mpl.rcParams["ytick.minor.visible"] = "True"
	mpl.rcParams["ytick.right"] = "True"
	
	mpl.rcParams["axes.grid"] = "True"
	mpl.rcParams["axes.linewidth"] = 1.5
	mpl.rcParams["axes.labelsize"] = "large"


def fluxes_HZ(stelzer_com, stelzer_upl, nemec_data, bound_ind):
	"""DOC"""
	# GENERAL FIGURE SETUP
	fig, ax = plt.subplots(2, 2, figsize=(10, 7),
	                       sharex=True, sharey=True)
	
	# Title for whole figure, might not be necessary
	# fig.suptitle("Incident XUV-fluxes for conservative habitable zone")
	
	# Upper left plot: Conservative Inner boundary, linear scaling
	ax_linci = ax[0][0]
	fill_stelzer_plot(ax_linci, stelzer_com, stelzer_upl, f"{bound_ind}_in")
	
	# Upper right plot: Conservative Outer boundary, linear scaling
	ax_linco = ax[0][1]
	fill_stelzer_plot(ax_linco, stelzer_com, stelzer_upl, f"{bound_ind}_out")
	
	# Lower left plot: Conservative Inner boundary, Calculated scaling
	ax_nemci = ax[1][0]
	fill_nemec_plot(ax_nemci, nemec_data, f"{bound_ind}_in")
	
	# Lower right plot: Conservative Outer boundary, Calculated scaling
	ax_nemco = ax[1][1]
	fill_nemec_plot(ax_nemco, nemec_data, f"{bound_ind}_out")
	
	# Finishing touches
	finish_2x2_plots(ax, fig)
	
	# Save the plot
	plt.savefig(f"{PLOT_SAVE_DIR}/fluxes_{bound_ind}HZ.eps")
	plt.close()


def fluxes_HZ_reduced(stelzer_com, stelzer_upl, nemec_data, bound_ind):
	"""DOC"""
	# GENERAL FIGURE SETUP
	fig, ax = plt.subplots(2, 1, figsize=(5, 7),
	                       sharex=True, sharey=True)
	
	# Title for whole figure, might not be necessary
	# fig.suptitle("Incident XUV-fluxes for conservative habitable zone")
	
	# Upper left plot: Conservative Inner boundary, linear scaling
	ax_linci = ax[0]
	fill_stelzer_plot(ax_linci, stelzer_com, stelzer_upl, f"{bound_ind}_in")
	
	# Lower left plot: Conservative Inner boundary, Calculated scaling
	ax_nemci = ax[1]
	fill_nemec_plot(ax_nemci, nemec_data, f"{bound_ind}_in")
	
	# Finishing touches
	finish_1x2_plots(ax, fig)
	
	# Save the plot
	plt.savefig(f"{PLOT_SAVE_DIR}/fluxes_{bound_ind}HZ_reduced.eps")
	plt.close()


def finish_2x2_plots(axes_list, figure_pointer):
	"""To finish and clean up the plots"""
	# Common axes labels
	figure_pointer.supxlabel('L$_{XUV}$ [erg s$^{-1}]$',
	                         fontsize="xx-large")
	figure_pointer.supylabel('f$_{XUV}$ [f$_{XUV, Earth}$]',
	                         fontsize="xx-large")
	
	for ax_row in axes_list:
		for axis in ax_row:
			# Plot the fXUV = 1 and fXUV = 20 marker in all plots
			axis.grid(color="lightgrey")
			axes_XUV_indicators(axis)
	
	# Adjust tick visibility for subplots
	subplot_tick_adjustment(axes_list)
	
	# Space out subplots
	plt.tight_layout()


def finish_1x2_plots(axes_list, figure_pointer):
	"""To finish and clean up the plots"""
	# Common axes labels
	figure_pointer.supylabel('f$_{XUV}$ [f$_{XUV, Earth}$]')
	axes_list[1].set(xlabel='L$_{XUV}$ [erg s$^{-1}]$')
	
	for axis in axes_list:
		# Plot the fXUV = 1 and fXUV = 20 marker in all plots
		axes_XUV_indicators(axis)
		axis.grid(color="lightgrey")
	
	# Adjust tick visibility for subplots
	plt.setp(axes_list[0].get_xticklabels(), visible=False)
	
	# Space out subplots
	plt.tight_layout()


def axes_XUV_indicators(axis):
	"""
	To hide extensive loops in the plotting examples and reduce redundancy.
	Draws dashed lines at 1 and 20 times f_XUV levels with text in all
	subplots.
	"""
	axis.axhline(y=20, c="grey", linestyle="--", zorder=3)
	axis.text(x=1e30, y=20 + 0.15 * 22,
	          fontsize="xx-large",
	          s="20", c="grey", zorder=3)
	axis.axhline(y=1, c="grey", linestyle="--", zorder=3)
	axis.text(x=1e30, y=1 + 0.15 * 2,
	          fontsize="xx-large",
	          s="1", c="grey", zorder=3)


def subplot_tick_adjustment(axes_list):
	"""
	To hide extensive loops in the plotting examples and reduce redundancy.
	Adjust tick visibility in a 4x4 subplot arrangement.
	"""
	
	upper_left = axes_list[0][0]
	plt.setp(upper_left.get_xticklabels(), visible=False)
	
	upper_right = axes_list[0][1]
	plt.setp(upper_right.get_xticklabels(), visible=False)
	plt.setp(upper_right.get_yticklabels(), visible=False)
	
	lower_left = axes_list[1][0]
	
	lower_right = axes_list[1][1]
	plt.setp(lower_right.get_yticklabels(), visible=False)


def fill_stelzer_plot(axis, data_set_f, data_set_u, hz_key):
	"""DOC"""
	# "Complete" data as scatter plot
	axis.loglog(data_set_f.Lxuv,
	            getattr(data_set_f.incFXUV, hz_key),
	            "o", markersize=4,
	            c="forestgreen", mec="darkgreen",
	            zorder=4)
	
	# "Upper limit only" as scatter with arrow downwards
	error = [getattr(data_set_u.incFXUV, hz_key) / 2,
	         getattr(data_set_u.incFXUV, hz_key) * 0]
	
	axis.errorbar(data_set_u.Lxuv,
	              getattr(data_set_u.incFXUV, hz_key),
	              yerr=error,
	              fmt="o", markersize=4, capsize=2.0,
	              c="red", mec="darkred",
	              uplims=True, zorder=5)


def fill_nemec_plot(axis, data_set, hz_key):
	"""DOC"""
	# Sample with XUV flux from Nina as scatter plot
	axis.loglog(data_set.Lxuv,
	            getattr(data_set.incFXUV, hz_key),
	            "o", markersize=4,
	            c="black", mec="black",
	            zorder=4)


def flux_lum_comparison(data_set):
	"""DOC"""
	# GENERAL FIGURE SETUP
	fig, ax = plt.subplots(2, 1, figsize=(5, 9))
	
	# DESCR
	ax[0].loglog(data_set.Fx,
	             data_set.Feuv,
	             "o", markersize=6,
	             c="grey", mec="black",
	             zorder=4)
	ax[0].set(xlabel="F$_X$ [erg cm$^{-2}$ s$^{-1}$]",
	          ylabel="F$_{EUV}$ [erg cm$^{-2}$ s$^{-1}$]")
	ax[0].grid(color="lightgrey", zorder=0)
	
	# DESCR
	ax[1].loglog(data_set.Lx, data_set.Leuv,
	             "o", markersize=6,
	             c="red", mec="black",
	             zorder=4)
	ax[1].plot([1e26, 1e30], [1e26, 1e30], c="grey", linestyle="--", zorder=3)
	
	ax[1].text(x=3e26, y=2e29, s="L$_X$ < L$_{EUV}$", c="grey",
	           fontsize="xx-large", zorder=3)
	ax[1].text(x=3e28, y=2e26, s="L$_X$ > L$_{EUV}$", c="grey",
	           fontsize="xx-large", zorder=3)
	
	ax[1].set(xlabel="L$_X$ [erg s$^{-1}$]", xlim=(1e26, 1e30),
	          ylabel="L$_{EUV}$ [erg s$^{-1}$]")
	ax[1].grid(color="lightgrey", zorder=0)
	
	plt.subplots_adjust(wspace=0.53, hspace=0)
	plt.tight_layout()
	plt.savefig(f"{PLOT_SAVE_DIR}/sFLUX_LUM_comp.eps")
