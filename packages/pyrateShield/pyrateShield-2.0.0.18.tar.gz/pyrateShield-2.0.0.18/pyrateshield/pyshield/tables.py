import os
import pandas as pd
import numpy as np
from pyrateshield import labels

#ENERGY_keV = 'Energy [keV]'
MFP = 'mfp'
MASS_ATTENUATION = 'mu/p [cm^2/g]'
ENERGY_MeV = 'Energy [MeV]'

folder = os.path.dirname(__file__)

file = os.path.join(folder, 'buildup.xls')
BUILDUP_TABLES = pd.read_excel(os.path.join(folder, file), sheet_name=None)

file = os.path.join(folder, 'attenuation.xls')
ATTENUATION_TABLES = pd.read_excel(os.path.join(folder, file), sheet_name=None)

ATTENUATION = {}


# for material, table in ATTENUATION_TABLES.items():
#     if material == 'References':
#         continue
    
#     ATTENUATION[material] = {}
#     ATTENUATION[material][ENERGY_MeV] = np.array(table[ENERGY_MeV])
#     ATTENUATION[material][MASS_ATTENUATION] = np.array(table[MASS_ATTENUATION])


# BUILDUP = {}

# for material, table in ATTENUATION_TABLES.items():
#     if material == 'References':
#         continue
    
#     ATTENUATION[material] = {}
#     ATTENUATION[material][ENERGY_MeV] = np.array(table[ENERGY_MeV])
#     ATTENUATION[material][MASS_ATTENUATION] = np.array(table[MASS_ATTENUATION])
    
    

        




  