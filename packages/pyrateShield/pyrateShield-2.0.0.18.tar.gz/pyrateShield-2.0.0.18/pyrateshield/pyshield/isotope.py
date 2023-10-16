# -*- coding: utf-8 -*-
"""
Isotope calculations for pyshield package

Last Updated 05-02-2016
"""
import numpy as np
import scipy.interpolate as si

from pyrateshield.pyshield import tables
from scipy.interpolate import RegularGridInterpolator

class AttenuationHelper:
    _interpolators = {}
    
    @classmethod
    def _get_interpolator(cls, material, energy_keV):
       
        key = (material.attenuation_table, energy_keV)
        
        if key in cls._interpolators.keys():
            return cls._interpolators[key]
        
        table       = tables.ATTENUATION_TABLES[material.attenuation_table]
        
        MeV = np.array(table[tables.ENERGY_MeV])
        mu_p = np.array(table[tables.MASS_ATTENUATION])
        
        interp_fcn = si.interp1d(MeV, mu_p)
  
        cls._interpolators[key] = interp_fcn
        return interp_fcn
    
    @classmethod
    def ulinear(cls, material,  energy_keV):
        umass = cls._get_interpolator(material, energy_keV)(energy_keV/1000) 
        return umass * material.density
    
    @classmethod
    def calculate(cls, material,  energy_keV, thickness):
        return np.exp(-cls.ulinear(material, energy_keV) * thickness)
    
    @classmethod
    def number_mean_free_path(cls, material, energy_keV, thickness):
        return cls.ulinear(material,  energy_keV) *thickness
       
        


class BuildupHelper:
    _interpolators = {}
    _cache = {}
    
    @classmethod
    def _get_interpolator(cls, material, energy_keV):
       
        key = (material.buildup_table, energy_keV)
        
        if key in cls._interpolators.keys():
            return cls._interpolators[key]

        table       = tables.BUILDUP_TABLES[material.buildup_table]
        
        n_mfp       = np.asarray(table[tables.MFP], 'float64')
        
        table       = table.drop(tables.MFP, axis=1) 
        factors     = np.asarray(table, 'float64')
        energies    = np.asarray(table.columns, dtype='float64')
        
        interp_fcn = RegularGridInterpolator((n_mfp,energies), factors,
                                             method='linear', 
                                             bounds_error=False)
        #xi = np.arange(0, 100.1, 0.1)
        xi = n_mfp
        points = [(ii, energy_keV/1000) for ii in xi]
        buildup_keV = interp_fcn(points)
        
        
        interp_fcn = si.interp1d(xi, buildup_keV, kind='linear')
   
        
        # interpolator = si.interp2d(energies, n_mfp, factors)
        # interp_fcn = lambda x, y: cls.interpolant(x, y, interpolator)
        cls._interpolators[key] = interp_fcn
        return interp_fcn
        
        
    @classmethod
    def calculate(cls, material, energy_keV,  thickness):
        
        interpolator = cls._get_interpolator(material, energy_keV)

        n_mfpi = AttenuationHelper.number_mean_free_path(material,energy_keV,  thickness)
        
        if isinstance(n_mfpi, np.ndarray):
            n_mfpi[n_mfpi>100] = 100
        else:
            n_mfpi = min(100, n_mfpi)
        
        value = interpolator(n_mfpi)
        
        return value
    
  