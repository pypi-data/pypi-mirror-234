import os
import yaml
from pyrateshield import labels
from pyrateshield.modelitem import ModelItem



CONSTANTS_FILE = "constants.yml"
ISOTOPES_FILE = "isotopes.yml"

class Isotope(ModelItem):
    _attr_dct = {
        "name": labels.NAME,
        "half_life": labels.HALF_LIFE,
        "self_shielding_options": labels.SELF_SHIELDING_OPTIONS,
    }
    spectrum = None
    
    def __eq__(self, other):
        return self.name == other.name
    
    def mass_number(self):
        mass_number = self.name.split('-')[1]
        try:
            mass_number = int(mass_number)
        except ValueError:
            # Cut off the m for Tc-99m
            mass_number = int(mass_number[:-1])
        return mass_number
    
    def __gt__(self, other):
        return self.mass_number() > other.mass_number()
    
    def __lt__(self, other):
        return self.mass_number() < other.mass_number()
    
    def __ge__(self, other):
        return self.mass_number() >= other.mass_number()
    
    def __le__(self, other):
        return self.mass_number() <= other.mass_number()
        

class ArcherParamsCT(ModelItem):
    _attr_dct = {
        "kvp": labels.KVP,
        "archer": labels.ARCHER,
        "scatter_fraction_body": labels.CT_SCATTER_FRACTION_BODY,
        "scatter_fraction_head": labels.CT_SCATTER_FRACTION_HEAD,
    }

class ArcherParamsXray(ModelItem):
    _attr_dct = {
        "kvp": labels.KVP,
        "archer": labels.ARCHER,
        "scatter_fraction": labels.XRAY_SCATTER_FRACTION,
    }



class Constants:
    _isotopes = None
    _ct = None
    _xray = None
    _wdir = None
    _constants_yml = None
    _isotope_yml = None
   
    def __init__(self):
        self.base_materials = [labels.EMPTY_TABLE] + self.constants_yml[labels.BASE_MATERIALS]
        self.buildup_materials = [labels.EMPTY_TABLE] + self.constants_yml[labels.BUILDUP_MATERIALS]
        self.CT_body_part_options = self.constants_yml[labels.CT_BODY_PART_OPTIONS]
        self.self_shielding_pyshield = self.constants_yml[labels.SELF_SHIELDING_PYSHIELD]
        self.self_shielding_options = [labels.SELF_SHIELDING_NONE,
                                       labels.SELF_SHIELDING_BODY, 
                                       labels.SELF_SHIELDING_FACTOR]
     
        self.decay_chains = self.isotope_yml[labels.DECAY_CHAINS]
        
        supported_isotopes = self.isotope_yml[labels.SUPPORTED_ISOTOPES]
        self.radtracer_supported_isotopes = supported_isotopes[labels.RADTRACER]
        self.pyshield_supported_isotopes = supported_isotopes[labels.PYSHIELD]
        self.isotope_spectra = self.isotope_yml[labels.ISOTOPE_SPECTRA]
        
    @property
    def wdir(self):
        if self._wdir is None:
            try:
                wdir = os.path.split(__file__)[0] 
            except:
                wdir = os.getcwd()
            self._wdir = wdir
        return self._wdir
    
    @property
    def constants_yml(self):
        if self._constants_yml is None:
            with open(os.path.join(self.wdir, CONSTANTS_FILE)) as f:
                constants_yml = yaml.safe_load(f)
            self._constants_yml = constants_yml
        return self._constants_yml
    
    @property
    def isotope_yml(self):
        if self._isotope_yml is None:
            with open(os.path.join(self.wdir, ISOTOPES_FILE)) as f:
               self._isotope_yml = (yaml.safe_load(f))    
        return self._isotope_yml
            
    @property
    def ct(self):
        if self._ct is None:
            self._ct = [ArcherParamsCT.from_dict(item)\
                        for item in self.constants_yml[labels.CT_PARAMETERS]]
        return self._ct
    @property
    def xray(self):
        if self._xray is None:
            self._xray = [ArcherParamsXray.from_dict(item)\
                          for item in self.constants_yml[labels.XRAY_PARAMETERS]]
        return self._xray
    
    
   
    
    @property
    def isotopes(self):
        if self._isotopes is None:

            isotopes = [Isotope.from_dict(item)\
                        for item in self.isotope_yml[labels.ISOTOPES]]
                
            # sort isotopes by mass number
            isotopes = sorted(isotopes)
        
            for isotope in isotopes:
                spectrum = list(self.isotope_spectra[isotope.name])
                spectrum_with_parent = [(isotope.name, energy, intensity)\
                                        for energy, intensity in spectrum]
                for daughter, abundance in self.decay_chains.get(isotope.name, []):
                    for energy, intensity in self.isotope_spectra[daughter]:
                        spectrum.append([energy, intensity*abundance])
                        spectrum_with_parent.append([daughter, energy, intensity*abundance])
                isotope.spectrum = spectrum
                isotope.spectrum_with_parent = spectrum_with_parent
            self._isotopes = isotopes
        return self._isotopes
    
    def get_isotope_name_list(self):
        return [item.name for item in self.isotopes]
        

    def get_isotope_by_name(self, name):
       
       isotope = [x for x in self.isotopes if x.name == name]
       if len(isotope) == 0:
           raise KeyError(f'No isotope with name {name}')
       return isotope[0]
    
  
    
CONSTANTS = Constants()
