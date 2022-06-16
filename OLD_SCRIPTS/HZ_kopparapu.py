#Python module to compute the distance of the habitable zone following the ansatz of Kopparapu et al. (2014)
#This model takes different planetary masses into account
#In this case it is valid for 1 M_earth

import numpy as np

#computation based on runaway greenhouse
def conservative_inner(T_eff, L):
    #Necessary parameters for computation, L_sun in erg/s
    L_sun = 3.828e33
    S_effsun = 1.107
    a = 1.332e-4
    b = 1.58e-8
    c = -8.308e-12
    d = -1.931e-15
    
    #Computing stellar incident flux
    T = T_eff - 5780
    S_eff = S_effsun + a*T + b*T**2 + c*T**3 + d*T**4
    
    #Computing distance in [au]
    distance = np.sqrt((L / L_sun) / S_eff)
    
    return distance

#Computation based on maximum greenhouse
def conservative_outer(T_eff, L):
    #Necessary parameters for computation
    L_sun = 3.828e33
    S_effsun = 0.356
    a = 6.171e-5
    b = 1.698e-9
    c = -3.198e-12
    d = -5.575e-16
    
    #Computing stellar incident flux
    T = T_eff - 5780
    S_eff = S_effsun + a*T + b*T**2 + c*T**3 + d*T**4
    
    #Computing distance in [au]
    distance = np.sqrt((L / L_sun) / S_eff)
    
    return distance


#Computation based on the recent venus criterion
def optimistic_inner(T_eff, L):
    #Necessary parameters for computation
    L_sun = 3.828e33
    S_effsun = 1.776
    a = 2.136e-4
    b = 2.533e-8
    c = -1.332e-11
    d = -3.097e-15
    
    #Computing stellar incident flux
    T = T_eff - 5780
    S_eff = S_effsun + a*T + b*T**2 + c*T**3 + d*T**4
    
    #Computing distance in [au], luminosity must be in solar values
    distance = np.sqrt((L / L_sun) / S_eff)
    
    return distance

#Computation based on early mars criterion
def optimistic_outer(T_eff, L):
    #Necessary parameters for computation
    L_sun = 3.828e33
    S_effsun = 0.32
    a = 5.547e-5
    b = 1.526e-9
    c = -2.874e-12
    d = -5.011e-16
    
    #Computing stellar incident flux
    T = T_eff - 5780
    S_eff = S_effsun + a*T + b*T**2 + c*T**3 + d*T**4
    
    #Computing distance in [au], luminosity must be in solar values
    distance = np.sqrt((L / L_sun) / S_eff)
    
    return distance