"""
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
"""