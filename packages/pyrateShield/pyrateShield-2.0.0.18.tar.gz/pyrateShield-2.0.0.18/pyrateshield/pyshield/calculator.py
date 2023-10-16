from pyrateshield.constants import CONSTANTS
from pyrateshield.model import DEFAULTS
from pyrateshield.pyshield.doserates import H10
from pyrateshield.pyshield.isotope import AttenuationHelper, BuildupHelper

def get_material_by_name(name):
    return [material for material in DEFAULTS.materials if material.name==name][0]

def dose_rate(isotope_name):
    isotope = CONSTANTS.get_isotope_by_name(isotope_name)
    
    energy_keV, abundance = list(zip(*isotope.spectrum))
    
    abundance = [ai / 100 for ai in abundance] #% to fraction
    
    return H10(energy_keV, abundance)


def attenuation_isotope(isotope_name, material, thickness):
   
    
    isotope = CONSTANTS.get_isotope_by_name(isotope_name)
    
    energy_keV, abundance = list(zip(*isotope.spectrum))
    
    abundance = [ai / 100 for ai in abundance] #% to fraction
    
    att = [AttenuationHelper.calculate(material, ei,thickness) for ei in energy_keV]
    
    unshielded_dose_rate = H10(energy_keV, abundance)
    
    shielded_abundance = [ai * atti for ai, atti in zip(abundance, att)]
    
    shielded_dose_rate = H10(energy_keV, shielded_abundance)
    
    return shielded_dose_rate / unshielded_dose_rate


def buildup_isotope(isotope_name, material, thickness):
    
    
    isotope = CONSTANTS.get_isotope_by_name(isotope_name)
    
    energy_keV, abundance = list(zip(*isotope.spectrum))

    abundance = [ai / 100 for ai in abundance] #% to fraction
    
    bup = [BuildupHelper.calculate(material, ei, thickness) for ei in energy_keV]
    
    unshielded_dose_rate = H10(energy_keV, abundance)
    
    shielded_abundance = [ai * atti for ai, atti in zip(abundance, bup)]
    
    shielded_dose_rate = H10(energy_keV, shielded_abundance)
    
    return shielded_dose_rate / unshielded_dose_rate


def transmission_isotope(isotope_name, material, thickness):
    
    
    isotope = CONSTANTS.get_isotope_by_name(isotope_name)

    energy_keV, abundance = list(zip(*isotope.spectrum))
    
    abundance = [ai / 100 for ai in abundance] #% to fraction
    
    bup = [BuildupHelper.calculate(material, ei, thickness) for ei in energy_keV]
    
    att = [AttenuationHelper.calculate(material, ei, thickness) for ei in energy_keV]
    
    trans = [ai * atti * bupi for ai, atti, bupi in zip(abundance, att, bup)]
    
    shielded_dose_rate = H10(energy_keV, trans)
    
    unshielded_dose_rate = H10(energy_keV, abundance)
    
    return shielded_dose_rate / unshielded_dose_rate


if __name__ == "__main__":
    pass
