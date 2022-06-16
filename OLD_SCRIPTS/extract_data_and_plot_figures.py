#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import HZ_kopparapu as HZ
import math as m
from matplotlib.lines import Line2D

pc_to_cm = 3.086e18
au_to_cm = 1.496e13
Rsol_cm = 6.957e10


def R_star(f_bol, Teff, distance):
    sb_con = 5.670e-8
    pc = 3.086e16
    R_sol = 6.955e8

    return (((10 ** f_bol) * 1e-3) / (sb_con * Teff ** 4)) ** (1 / 2) * distance * pc * 1 / R_sol


def L_conv(d, f_searched):
    return 4 * m.pi * (d * 3.086e18) ** 2 * 10 ** f_searched


def inc_flux(L_XUV, d_HZ):
    return (L_XUV / (4 * m.pi * (d_HZ * au_to_cm) ** 2)) / 5.6


##############################################################################
raw_1 = open("dataset_1_stelzer.dat", "r")
data_stelzer_1 = np.array([
    line.split("\t")
    for line in raw_1
])
raw_1.close()

raw_2 = open("dataset_2_stelzer.dat", "r")
data_stelzer_2 = np.array([
    line.split("\t")
    for line in raw_2
])
raw_2.close()

raw_nina = open("For_Simon_f_XUV_1_AU_new_radii.bin", "r")
data_nina = np.array([
    line.split() for line in raw_nina
])
data_nina = data_nina[1:]
raw_nina.close()

# Complete data sample from Stelzer (relevant values only)
data_stelzer_full = np.array([[
    data_stelzer_1[i][0], data_stelzer_1[i][2], data_stelzer_1[i][5],
    data_stelzer_1[i][6], data_stelzer_1[i][7], data_stelzer_2[i][7],
    data_stelzer_2[i][8]] for i in range(len(data_stelzer_2))
])

# Data sample consisting of upper limit only stars:
data_stelzer_upl_only = np.array([
    data_stelzer_full[i] for i in range(len(data_stelzer_full))
    if data_stelzer_full[i][-1] == "\n"
])

data_stelzer_rest = np.array([
    data_stelzer_full[i] for i in range(len(data_stelzer_full))
    if data_stelzer_full[i][-1] != "\n"
])

##############################################################################
# create appropriate dictionaries
a = len(data_stelzer_rest)
ph = data_stelzer_rest
stelzer_rest = {
    "ID": np.array([
        ph[i][0].strip()
        for i in range(a)
    ]),
    "d": np.array([
        float(ph[i][1])
        for i in range(a)
    ]),
    "SpT": np.array([
        ph[i][2].strip()
        for i in range(a)
    ]),
    "Teff": np.array([
        float(ph[i][3])
        for i in range(a)
    ]),
    "log(fbol)": np.array([
        -1 * float(ph[i][4].strip()[1:])
        for i in range(a)
    ]),
    "log(fx)": np.array([
        -1 * float(ph[i][5].strip()[1:])
        for i in range(a)
    ])
}
del a, ph

a = len(data_stelzer_upl_only)
ph = data_stelzer_upl_only
stelzer_upl = {
    "ID": np.array([
        ph[i][0].strip()
        for i in range(a)
    ]),
    "d": np.array([
        float(ph[i][1])
        for i in range(a)
    ]),
    "SpT": np.array([
        ph[i][2].strip()
        for i in range(a)
    ]),
    "Teff": np.array([
        float(ph[i][3])
        for i in range(a)
    ]),
    "log(fbol)": np.array([
        -1 * float(ph[i][4].strip()[1:])
        for i in range(a)
    ]),
    "log(fx)": np.array([
        -1 * float(ph[i][5].strip()[1:])
        for i in range(a)
    ])
}
del a, ph

a = len(data_nina)
ph = data_nina
nina_full = {
    "ID": np.array([
        ph[i][0] + " " + ph[i][1]
        for i in range(a)
    ]),
    "Teff": np.array([
        float(ph[i][2])
        for i in range(a)
    ]),
    "Rstar": np.array([
        float(ph[i][3])
        for i in range(a)
    ]),
    "d": np.array([
        float(ph[i][4])
        for i in range(a)
    ]),
    "log(fbol)": np.array([
        -1 * float(ph[i][5].strip()[1:])
        for i in range(a)
    ]),
    "log(fx)": np.array([
        -1 * float(ph[i][6].strip()[1:])
        for i in range(a)
    ]),
    "fxuv1AU": np.array([
        # cgs-conversion
        1e3 * float(ph[i][-3])
        for i in range(a)
    ])
}

##############################################################################

# use plt.errorbar(x,y, yerr=error, fmt="o", uplims=True)

##############################################################################
# Add dictionary entries for L_bol, R_star and HZ-distance fluxes
stelzer_rest["Rstar"] = np.array(R_star(stelzer_rest["log(fbol)"], stelzer_rest["Teff"], stelzer_rest["d"]))
stelzer_rest["Lbol"] = L_conv(stelzer_rest["d"], stelzer_rest["log(fbol)"])
stelzer_rest["LXUV"] = 7 * (L_conv(stelzer_rest["d"], stelzer_rest["log(fx)"]))
stelzer_rest["inc_fxuv"] = {
    "ci": inc_flux(stelzer_rest["LXUV"],
                   HZ.conservative_inner(stelzer_rest["Teff"], stelzer_rest["Lbol"])),
    "co": inc_flux(stelzer_rest["LXUV"],
                   HZ.conservative_outer(stelzer_rest["Teff"], stelzer_rest["Lbol"])),
    "oi": inc_flux(stelzer_rest["LXUV"],
                   HZ.optimistic_inner(stelzer_rest["Teff"], stelzer_rest["Lbol"])),
    "oo": inc_flux(stelzer_rest["LXUV"],
                   HZ.optimistic_outer(stelzer_rest["Teff"], stelzer_rest["Lbol"]))
}

stelzer_upl["Rstar"] = np.array(R_star(stelzer_upl["log(fbol)"], stelzer_upl["Teff"], stelzer_upl["d"]))
stelzer_upl["Lbol"] = np.array(L_conv(stelzer_upl["d"], stelzer_upl["log(fbol)"]))
stelzer_upl["LXUV"] = 6 * (L_conv(stelzer_upl["d"], stelzer_upl["log(fx)"]))
stelzer_upl["inc_fxuv"] = {
    "ci": inc_flux(stelzer_upl["LXUV"], HZ.conservative_inner(
        stelzer_upl["Teff"], stelzer_upl["Lbol"])),
    "co": inc_flux(stelzer_upl["LXUV"], HZ.conservative_outer(
        stelzer_upl["Teff"], stelzer_upl["Lbol"])),
    "oi": inc_flux(stelzer_upl["LXUV"], HZ.optimistic_inner(
        stelzer_upl["Teff"], stelzer_upl["Lbol"])),
    "oo": inc_flux(stelzer_upl["LXUV"], HZ.optimistic_outer(
        stelzer_upl["Teff"], stelzer_upl["Lbol"]))
}

indices = []
for element in stelzer_rest["ID"]:
    for element2 in nina_full["ID"]:
        if element2 == element:
            indices.append(np.where(stelzer_rest["ID"] == element2)[0][0])
nina_full["log(fx)"] = np.array([])
for a in indices:
    nina_full["log(fx)"] = np.append(nina_full["log(fx)"], stelzer_rest["log(fx)"][a])
nina_full["Lbol"] = np.array(L_conv(nina_full["d"], nina_full["log(fbol)"]))
nina_full["LXUV"] = 4 * m.pi * (1 * au_to_cm) ** 2 * nina_full["fxuv1AU"] * nina_full["Rstar"] ** 2
nina_full["LX"] = np.array(L_conv(nina_full["d"], nina_full["log(fx)"]))
nina_full["LEUV"] = nina_full["LXUV"] - nina_full["LX"]
nina_full["FXUV"] = nina_full["LXUV"] / (4 * m.pi * (nina_full["Rstar"] * Rsol_cm) ** 2)
nina_full["FX"] = nina_full["LX"] / (4 * m.pi * (nina_full["Rstar"] * Rsol_cm) ** 2)
nina_full["FEUV"] = nina_full["LEUV"] / (4 * m.pi * (nina_full["Rstar"] * Rsol_cm) ** 2)
nina_full["inc_fxuv"] = {
    "ci": inc_flux(nina_full["LXUV"], HZ.conservative_inner(
        nina_full["Teff"], nina_full["Lbol"])),
    "co": inc_flux(nina_full["LXUV"], HZ.conservative_outer(
        nina_full["Teff"], nina_full["Lbol"])),
    "oi": inc_flux(nina_full["LXUV"], HZ.optimistic_inner(
        nina_full["Teff"], nina_full["Lbol"])),
    "oo": inc_flux(nina_full["LXUV"], HZ.optimistic_outer(
        nina_full["Teff"], nina_full["Lbol"]))
}

##############################################################################
# 1st plots (surface fluxes F_EUV compared to F_X, L_EUV compared to L_X)
# plt.style.use("classic")
# fig = plt.figure(1)

# plot1 = fig.add_subplot(211)
# plot1.loglog(nina_full["FX"], nina_full["FEUV"], "o", c="grey")
# plt.xlabel("F$_X$ [erg/cm²/s]")
# plt.ylabel("F$_{EUV}$ [erg/cm²/s]")

# plot2 = fig.add_subplot(212)
# plot2.loglog(nina_full["LX"], nina_full["LEUV"], "o", c="red")
# plot2.plot([1e26, 1e30], [1e26, 1e30], c="grey", linestyle="--")
# plot2.text(x=1e27, y=1e29, s="L$_X$ < L$_{EUV}$", c="grey")
# plot2.text(x=1e29, y=1e27, s="L$_X$ > L$_{EUV}$", c="grey")
# plt.xlabel("L$_X$ [erg/s]")
# plt.ylabel("L$_{EUV}$ [erg/s]")
# plt.xlim(1e26, 1e30)

# plt.subplots_adjust(wspace=0.53, hspace=0)
# plt.tight_layout()
# plt.savefig("sF_and_L_comparison.eps")

##############################################################################
# 2nd plots (cons. edges with linear scaling above and ninas scaling below)
plt.style.use('classic')
fig = plt.figure(2)
fig.suptitle("Incident XUV-fluxes for conservative habitable zone")
# Set common labels
fig.text(0.5, 0.04, 'L$_{XUV}$ [erg/s]', ha='center', va='center')
# fig.text(0.06, 0.5, 'f$_{XUV}$ [f$_{XUV, Earth}$]', ha='center', va='center', rotation='vertical')

plot1 = fig.add_subplot(2, 2, 1)
error = [stelzer_upl["inc_fxuv"]["ci"] / 2, stelzer_upl["inc_fxuv"]["ci"] * 0]
plot1.loglog(stelzer_rest["LXUV"], stelzer_rest["inc_fxuv"]["ci"], "o",
             c="green", markersize=3, mec="black")
plot1.errorbar(stelzer_upl["LXUV"], stelzer_upl["inc_fxuv"]["ci"],
               yerr=error, fmt="o", markersize=3, uplims=True, c="red", ecolor="red", capsize=2.0)
plot1.axhline(y=20, c="grey", linestyle="--")/home/simon
plot1.text(x=1e30, y=20 + 0.15 * 22, s="20", c="grey")
plot1.axhline(y=1, c="grey", linestyle="--")
plot1.text(x=1e30, y=1 + 0.15 * 2, s="1", c="grey")
plt.ylabel("f$_{XUV}$ [f$_{XUV, Earth}$]")
plt.title("Inner Edge")

plot1.xaxis.get_major_ticks()[2].label1.set_visible(False)
plot1.xaxis.get_major_ticks()[-2].label1.set_visible(False)
plot1.yaxis.get_major_ticks()[1].label1.set_visible(False)
plot1.yaxis.get_major_ticks()[-2].label1.set_visible(False)

# -----------------------------------------------------------------------------

plot2 = fig.add_subplot(2, 2, 2, sharex=plot1, sharey=plot1)
error = [stelzer_upl["inc_fxuv"]["co"] / 2, stelzer_upl["inc_fxuv"]["co"] * 0]
plot2.loglog(stelzer_rest["LXUV"], stelzer_rest["inc_fxuv"]["co"], "o",
             c="green", markersize=3, mec="black")
plot2.errorbar(stelzer_upl["LXUV"], stelzer_upl["inc_fxuv"]["co"],
               yerr=error, fmt="o", markersize=3, uplims=True, c="red", capsize=2.0)
plot2.axhline(y=20, c="grey", linestyle="--")
plot2.axhline(y=1, c="grey", linestyle="--")
plt.title("Outer Edge")

plot2.xaxis.get_major_ticks()[2].label1.set_visible(False)
plot2.xaxis.get_major_ticks()[-2].label1.set_visible(False)
plt.setp(plot2.get_yticklabels(), visible=False)

# -----------------------------------------------------------------------------

plot3 = fig.add_subplot(2, 2, 3, sharex=plot1, sharey=plot1)
plot3.loglog(nina_full["LXUV"], nina_full["inc_fxuv"]["ci"], "o",
             c="black", markersize=3)
plot3.axhline(y=20, c="grey", linestyle="--")
plot3.text(x=1e30, y=20 + 0.15 * 20, s="20", c="grey")
plot3.axhline(y=1, c="grey", linestyle="--")
plot3.text(x=1e30, y=1 + 0.15 * 1, s="1", c="grey")
plt.ylabel("f$_{XUV}$ [f$_{XUV, Earth}$]")

plot3.xaxis.get_major_ticks()[2].label1.set_visible(False)
plot3.xaxis.get_major_ticks()[-2].label1.set_visible(False)
plot3.yaxis.get_major_ticks()[1].label1.set_visible(False)
plot3.yaxis.get_major_ticks()[-2].label1.set_visible(False)

# -----------------------------------------------------------------------------

plot4 = fig.add_subplot(2, 2, 4, sharex=plot1, sharey=plot1)
plot4.loglog(nina_full["LXUV"], nina_full["inc_fxuv"]["co"], "o",
             c="black", markersize=3)
plot4.axhline(y=20, c="grey", linestyle="--")
plot4.axhline(y=1, c="grey", linestyle="--")

plot4.xaxis.get_major_ticks()[2].label1.set_visible(False)
plot4.xaxis.get_major_ticks()[-2].label1.set_visible(False)
plt.setp(plot4.get_yticklabels(), visible=False)

# -----------------------------------------------------------------------------

plt.subplots_adjust(wspace=0)
plt.savefig("fluxes_cHZ.eps")

##############################################################################
# 3rd plots (opt. edges with linear scaling above and ninas scaling below)
# plt.style.use('classic')
fig = plt.figure(3)
fig.suptitle("Incident XUV-fluxes for optimistic habitable zone")
# Set common labels
fig.text(0.5, 0.04, 'L$_{XUV}$ [erg/s]', ha='center', va='center')
# fig.text(0.06, 0.5, 'f$_{XUV}$ [f$_{XUV, Earth}$]', ha='center', va='center', rotation='vertical')

plot1 = fig.add_subplot(2, 2, 1)
error = [stelzer_upl["inc_fxuv"]["oi"] / 2, stelzer_upl["inc_fxuv"]["oi"] * 0]
plot1.loglog(stelzer_rest["LXUV"], stelzer_rest["inc_fxuv"]["oi"], "o",
             c="green", markersize=3, mec="black")
plot1.errorbar(stelzer_upl["LXUV"], stelzer_upl["inc_fxuv"]["oi"],
               yerr=error, fmt="o", markersize=3, uplims=True, c="red", capsize=2.0)
plot1.axhline(y=20, c="grey", linestyle="--")
plot1.text(x=1e30, y=20 + 0.15 * 20, s="20", c="grey")
plot1.axhline(y=1, c="grey", linestyle="--")
plot1.text(x=1e30, y=1 + 0.15 * 1, s="1", c="grey")
plt.ylabel("f$_{XUV}$ [f$_{XUV, Earth}$]")
plt.title("Inner Edge")

plot1.xaxis.get_major_ticks()[2].label1.set_visible(False)
plot1.xaxis.get_major_ticks()[-2].label1.set_visible(False)
plot1.yaxis.get_major_ticks()[1].label1.set_visible(False)
plot1.yaxis.get_major_ticks()[-2].label1.set_visible(False)

plot2 = fig.add_subplot(2, 2, 2, sharex=plot1, sharey=plot1)
error = [stelzer_upl["inc_fxuv"]["oo"] / 2, stelzer_upl["inc_fxuv"]["oo"] * 0]
plot2.loglog(stelzer_rest["LXUV"], stelzer_rest["inc_fxuv"]["oo"], "o",
             c="green", markersize=3, mec="black")
plot2.errorbar(stelzer_upl["LXUV"], stelzer_upl["inc_fxuv"]["oo"],
               yerr=error, fmt="o", markersize=3, uplims=True, c="red", capsize=2.0)
plot2.axhline(y=20, c="grey", linestyle="--")
plot2.axhline(y=1, c="grey", linestyle="--")
plt.title("Outer Edge")

plot2.xaxis.get_major_ticks()[2].label1.set_visible(False)
plot2.xaxis.get_major_ticks()[-2].label1.set_visible(False)
plt.setp(plot2.get_yticklabels(), visible=False)

plot3 = fig.add_subplot(2, 2, 3, sharex=plot1, sharey=plot1)
plot3.loglog(nina_full["LXUV"], nina_full["inc_fxuv"]["oi"], "o",
             c="black", markersize=3)
plt.ylabel("f$_{XUV}$ [f$_{XUV, Earth}$]")
plot3.axhline(y=20, c="grey", linestyle="--")
plot3.text(x=1e30, y=20 + 0.15 * 20, s="20", c="grey")
plot3.axhline(y=1, c="grey", linestyle="--")
plot3.text(x=1e30, y=1 + 0.15 * 1, s="1", c="grey")

plot3.xaxis.get_major_ticks()[2].label1.set_visible(False)
plot3.xaxis.get_major_ticks()[-2].label1.set_visible(False)
plot3.yaxis.get_major_ticks()[1].label1.set_visible(False)
plot3.yaxis.get_major_ticks()[-2].label1.set_visible(False)

plot4 = fig.add_subplot(2, 2, 4, sharex=plot1, sharey=plot1)
plot4.loglog(nina_full["LXUV"], nina_full["inc_fxuv"]["oo"], "o",
             c="black", markersize=3)
plt.setp(plot4.get_yticklabels(), visible=False)
plot4.axhline(y=20, c="grey", linestyle="--")
plot4.axhline(y=1, c="grey", linestyle="--")

plot4.xaxis.get_major_ticks()[2].label1.set_visible(False)
plot4.xaxis.get_major_ticks()[-2].label1.set_visible(False)
plt.setp(plot4.get_yticklabels(), visible=False)

plt.subplots_adjust(wspace=0)
plt.savefig("fluxes_oHZ.eps")


#######################################################################################################################
# Create a bar chart that represents systems with a maximum of 1, 10 or 20 XUV in their habitable zone. Will need
# four different charts: optimistic and conservative inner and outer edges.

def perc_XUV_lim(lim, array):
    result = []
    for element in array:
        if element <= lim:
            result += [element]
    return len(result) / len(array) * 100


# sample size and XUV-limits
s = 159
l = np.array([1, 10, 20])

# Data for optimistic inner edge
n_st_upl_oi = np.array([perc_XUV_lim(1, stelzer_upl["inc_fxuv"]["oi"]), perc_XUV_lim(10, stelzer_upl["inc_fxuv"]["oi"]),
                        perc_XUV_lim(20, stelzer_upl["inc_fxuv"]["oi"])])
n_st_rest_oi = np.array(
    [perc_XUV_lim(1, stelzer_rest["inc_fxuv"]["oi"]), perc_XUV_lim(10, stelzer_rest["inc_fxuv"]["oi"]),
     perc_XUV_lim(20, stelzer_rest["inc_fxuv"]["oi"])])
n_n_oi = np.array([perc_XUV_lim(1, nina_full["inc_fxuv"]["oi"]), perc_XUV_lim(10, nina_full["inc_fxuv"]["oi"]),
                   perc_XUV_lim(20, nina_full["inc_fxuv"]["oi"])])

# Data for optimistic outer edge
n_st_upl_oo = np.array([perc_XUV_lim(1, stelzer_upl["inc_fxuv"]["oo"]), perc_XUV_lim(10, stelzer_upl["inc_fxuv"]["oo"]),
                        perc_XUV_lim(20, stelzer_upl["inc_fxuv"]["oo"])])
n_st_rest_oo = np.array(
    [perc_XUV_lim(1, stelzer_rest["inc_fxuv"]["oo"]), perc_XUV_lim(10, stelzer_rest["inc_fxuv"]["oo"]),
     perc_XUV_lim(20, stelzer_rest["inc_fxuv"]["oo"])])
n_n_oo = np.array([perc_XUV_lim(1, nina_full["inc_fxuv"]["oo"]), perc_XUV_lim(10, nina_full["inc_fxuv"]["oo"]),
                   perc_XUV_lim(20, nina_full["inc_fxuv"]["oo"])])

# Data for conservative inner edge
n_st_upl_ci = np.array([perc_XUV_lim(1, stelzer_upl["inc_fxuv"]["ci"]), perc_XUV_lim(10, stelzer_upl["inc_fxuv"]["ci"]),
                        perc_XUV_lim(20, stelzer_upl["inc_fxuv"]["ci"])])
n_st_rest_ci = np.array(
    [perc_XUV_lim(1, stelzer_rest["inc_fxuv"]["ci"]), perc_XUV_lim(10, stelzer_rest["inc_fxuv"]["ci"]),
     perc_XUV_lim(20, stelzer_rest["inc_fxuv"]["ci"])])
n_n_ci = np.array([perc_XUV_lim(1, nina_full["inc_fxuv"]["ci"]), perc_XUV_lim(10, nina_full["inc_fxuv"]["ci"]),
                   perc_XUV_lim(20, nina_full["inc_fxuv"]["ci"])])

# Data for conservative outer edge
n_st_upl_co = np.array([perc_XUV_lim(1, stelzer_upl["inc_fxuv"]["co"]), perc_XUV_lim(10, stelzer_upl["inc_fxuv"]["co"]),
                        perc_XUV_lim(20, stelzer_upl["inc_fxuv"]["co"])])
n_st_rest_co = np.array(
    [perc_XUV_lim(1, stelzer_rest["inc_fxuv"]["co"]), perc_XUV_lim(10, stelzer_rest["inc_fxuv"]["co"]),
     perc_XUV_lim(20, stelzer_rest["inc_fxuv"]["co"])])
n_n_co = np.array([perc_XUV_lim(1, nina_full["inc_fxuv"]["co"]), perc_XUV_lim(10, nina_full["inc_fxuv"]["co"]),
                   perc_XUV_lim(20, nina_full["inc_fxuv"]["co"])])

# Plot bar chart for the results
bar_width = 2

fig = plt.figure(4)
fig.text(0.5, 0.03, 'f$_{XUV}$ [f$_{XUV, Earth}$]', ha='center', va='center')
fig.text(0.04, 0.5, '% of System below limit', ha='center', va='center', rotation=90)

# Optimistic inner edge
plot1 = fig.add_subplot(221)
plot1.bar(l, n_st_upl_oi, bar_width, label="(1)", color="red")
plot1.bar(l + bar_width, n_st_rest_oi, bar_width, label="(2)", color="green")
plot1.bar(l + 2 * bar_width, n_n_oi, bar_width, label="(3)", color="blue")
plt.title("Inner Edge")
plt.ylabel("Opt.")
plot1.yaxis.get_major_ticks()[0].label1.set_visible(False)

plt.xticks(l + bar_width, (1, 10, 20))
plt.tick_params(axis='x', length=0)

# Optimistic outer edge
plot2 = fig.add_subplot(222)
plot2.bar(l, n_st_upl_oo, bar_width, color="red")
plot2.bar(l + bar_width, n_st_rest_oo, bar_width, color="green")
plot2.bar(l + 2 * bar_width, n_n_oo, bar_width, color="blue")
plt.title("Outer Edge")
plot2.yaxis.get_major_ticks()[0].label1.set_visible(False)

plt.xticks(l + bar_width, (1, 10, 20))
plt.tick_params(axis='x', length=0)

# conservative inner edge
plot3 = fig.add_subplot(223)
plot3.bar(l, n_st_upl_ci, bar_width, color="red")
plot3.bar(l + bar_width, n_st_rest_ci, bar_width, color="green")
plot3.bar(l + 2 * bar_width, n_n_ci, bar_width, color="blue")
plt.ylabel("Cons.")
plot3.yaxis.get_major_ticks()[0].label1.set_visible(False)

plt.xticks(l + bar_width, (1, 10, 20))
plt.tick_params(axis='x', length=0)

# conservative co edge
plot4 = fig.add_subplot(224)
plot4.bar(l, n_st_upl_co, bar_width, color="red")
plot4.bar(l + bar_width, n_st_rest_co, bar_width, color="green")
plot4.bar(l + 2 * bar_width, n_n_co, bar_width, color="blue")
plot4.yaxis.get_major_ticks()[0].label1.set_visible(False)

plt.xticks(l + bar_width, (1, 10, 20))
plt.tick_params(axis='x', length=0)

plt.savefig("perc_below_limits.eps")

#plt.show()

print(len(stelzer_upl["inc_fxuv"]["oi"]), len(stelzer_rest["inc_fxuv"]["oi"]), len(nina_full["inc_fxuv"]["oi"]))

#######################################################################################################################
# Print the results in text documents, ready to put in a TeX-Document!
# 1) List of resulting XUV-flux values
nina_HZdist = [1e1*HZ.conservative_inner(nina_full["Teff"], nina_full["Lbol"]), 1e1*HZ.conservative_outer(nina_full["Teff"], nina_full["Lbol"]),
               1e1*HZ.optimistic_inner(nina_full["Teff"], nina_full["Lbol"]), 1e1*HZ.optimistic_outer(nina_full["Teff"], nina_full["Lbol"])]
r1 = open("r1.dat", "w")
for i in range(len(nina_full["ID"])):
    r1.write('\t {} & {:.2f} & [{:.2f},{:.2f}] & [{:.2f},{:.2f}] & [{:.2f},{:.2f}] & [{:.2f},{:.2f}]'.format(nina_full["ID"][i], np.log10(nina_full["LXUV"][i]), nina_HZdist[0][i], nina_HZdist[1][i], nina_HZdist[2][i], nina_HZdist[3][i],
                                                                                                          np.log10(nina_full["inc_fxuv"]["ci"][i]), np.log10(nina_full["inc_fxuv"]["co"][i]), np.log10(nina_full["inc_fxuv"]["oi"][i]),
                                                                                                             np.log10(nina_full["inc_fxuv"]["oo"][i]))
             + '\\'*2 + '\n'
)
r1.close()

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
