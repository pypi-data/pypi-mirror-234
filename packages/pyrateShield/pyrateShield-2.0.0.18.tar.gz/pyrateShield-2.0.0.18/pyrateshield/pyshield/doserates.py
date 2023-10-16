#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 11:35:41 2016

@author: Marcel
"""
from scipy.interpolate import CubicSpline
import numpy as np

def attenuation(isotope, material=None, thickness=None):
    unshielded = H10()
    
    
    
    
def ratio_H10_air_kerma(energy_keV):
    # Emperical function proposed by ICRU 47
    # 
    E0 = 9.85
    xi = np.log(energy_keV / E0)

    r = xi / (1.465 * xi**2 - 4.414 * xi + 4.789) \
        + 0.7006 * np.arctan(0.6519 * xi)
    return r

def H10(energy_keV, abundance = 1, add = True):
    """
    Calculates the h10 in uSv/h per MBq/m^2 for given photon energy or
    multiple energies.
    Args:
      energy_keV: photon energy(ies)
      abundance:  abundance for each photon energy
      add:        sum dose rates for all energies (default = True)
    Returns:
      dose rate in uSv/h per MBq/m^2
    """
    # convert tuple and list to numpy
    energy_keV = np.array(energy_keV)
    abundance = np.array(abundance)

    #ratio = np.interp(energy_keV, energies_keV, Hp10_ka)
    ratio = ratio_H10_air_kerma(energy_keV)

    h10 = ratio * kerma_air_rate(energy_keV, abundance, add = False)

    if add:
        h10 = np.sum(h10)
    return h10

def kerma_air_rate(energy_keV, abundance=1, add = True):
    """
    Calculates the air kerma in uGy/h per MBq/m^2 for given photon energy or
    multiple energies.
    Args:
      energy_keV: photon energy(ies)
      abundance:  abundance for each photon energy
      add:        sum dose rates for all energies (default = True)
    Returns:
      kerma in uGy/h per MBq/m^2
    """
    # air kerma : dKair/dt = A/(4*pi*l^2) * uk/p * E
    energy_keV = np.array(energy_keV, dtype=np.float64)
                          
    abundance = np.array(abundance, dtype=np.float64)

    # kerma rate at 1m for 1 Bq (A=1, l=1)
    Joule_per_eV = 1.60217662e-19

    energy_J = Joule_per_eV * energy_keV * 1000

    energy_absorption_coeff = linear_energy_absorption_coeff_air(energy_keV)

    # s^-1 --> h^-1 Gy--> uGy Bq --> MBq
    energy_absorption_coeff *= 3600 * 1e12

    # kerma in uGy/h per MBq/m^2
    kerma = abundance * energy_absorption_coeff * energy_J / (4 * np.pi)

    if add:
        kerma = np.sum(kerma)
    return kerma

def linear_energy_absorption_coeff_air(energy_keV):
    """
    Calculates the linear energy transfer coefficients by interpolation.
    Source data is obtained from the NIST XCOM database.
    https://physics.nist.gov/PhysRefData/XrayMassCoef/ComTab/air.html
    Args:
      energy_keV: photon energy(ies) in keV
    Returns:
      linear energy tranfer rate(s)
    """

    energy_keV = np.array(energy_keV)
    # source data (cut off at 15 keV)
    Energy_MeV =  [ 1.50E-02,
                    2.00E-02,
                    3.00E-02,
                    4.00E-02,
                    5.00E-02,
                    6.00E-02,
                    8.00E-02,
                    1.00E-01,
                    1.50E-01,
                    2.00E-01,
                    3.00E-01,
                    4.00E-01,
                    5.00E-01,
                    6.00E-01,
                    8.00E-01,
                    1.00E+00,
                    1.25E+00,
                    1.50E+00,
                    2.00E+00,
                    3.00E+00,
                    4.00E+00,
                    5.00E+00,
                    6.00E+00,
                    8.00E+00,
                    1.00E+01,
                    1.50E+01,
                    2.00E+01]

    u_en_p = [  1.3340E+00,
                5.3890E-01,
                1.5370E-01,
                6.8330E-02,
                4.0980E-02,
                3.0410E-02,
                2.4070E-02,
                2.3250E-02,
                2.4960E-02,
                2.6720E-02,
                2.8720E-02,
                2.9490E-02,
                2.9660E-02,
                2.9530E-02,
                2.8820E-02,
                2.7890E-02,
                2.6660E-02,
                2.5470E-02,
                2.3450E-02,
                2.0570E-02,
                1.8700E-02,
                1.7400E-02,
                1.6470E-02,
                1.5250E-02,
                1.4500E-02,
                1.3530E-02,
                1.3110E-02]

    
    interpolator = CubicSpline(Energy_MeV, u_en_p)
    
    #coeff = np.interp(np.log10(energy_keV/1e3), np.log10(Energy_MeV), u_en_p) # Units cm^2 per g
    coeff = interpolator(energy_keV/1e3)
    
    
    # plt.plot(Energy_MeV, u_en_p, 'd')
    # x = np.arange(0.015, 20, 0.001 )
    # plt.plot(x, interpolator(x), '-')
    
    
    coeff /= 10 # cm^2/g --> m^2/kg
    return coeff




