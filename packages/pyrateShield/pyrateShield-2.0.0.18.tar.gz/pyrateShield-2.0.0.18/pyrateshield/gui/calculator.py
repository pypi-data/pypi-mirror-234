# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 11:25:57 2022

@author: Marcel
"""
from PyQt5.QtWidgets import (QPushButton, QLabel, 
                             QComboBox, QDoubleSpinBox, QApplication)
from PyQt5.QtGui import QIcon, QFont
import qtawesome                             

from pyrateshield.constants import CONSTANTS
from pyrateshield.model import DEFAULTS
from pyrateshield.model_sequences import Materials
from pyrateshield.labels import EMPTY_MATERIAL, MATERIALS

from pyrateshield.pyshield.calculator import attenuation_isotope, buildup_isotope, transmission_isotope, dose_rate
from pyrateshield.gui.item_views import EditValueWidget

from pyrateshield.radtracer.radtracer import TransmissionMCNP, MCNP_LOOKUP

class View(EditValueWidget):
    def create_widgets(self):
        
        bold_font = QFont()
        bold_font.setBold(True)

        self.isotope_list = QComboBox()
        self.material_list = QComboBox()
        self.thickness_value = QDoubleSpinBox() 

        self.pyshield_transmission = QLabel('')
        self.pyshield_attenuation = QLabel('')
        self.pyshield_buildup = QLabel('')
        
        self.pyshield_unshielded_doserate = QLabel('')
        self.radtracer_unshielded_doserate = QLabel('')
        
        self.pyshield_shielded_doserate = QLabel('')
        self.radtracer_shielded_doserate = QLabel('')
        
        self.radtracer_transmission = QLabel('')
        self.calculate_button = QPushButton('Calculate')
        self.close_button = QPushButton('Close')
    
    def create_layout(self):
        self.bold_font = QFont()
        self.bold_font.setBold(True)
        
        self.setWindowTitle('Calculator')
        icon = qtawesome.icon('mdi.calculator')
        self.setWindowIcon(QIcon(icon))
        
        row = 0
        
        self.layout.addWidget(QLabel('Isotope:'), row, 0)
        self.layout.addWidget(self.isotope_list, row, 1)
        
        row += 1
        
        self.layout.addWidget(QLabel('Material:'), row, 0)
        self.layout.addWidget(self.material_list, row, 1)
        
        row += 1
        
        self.layout.addWidget(QLabel('Thickness [cm]:'), row, 0)
        self.layout.addWidget(self.thickness_value, row, 1)
        
        row += 1
        label = QLabel('Unshielded h10 [uSv/h per MBq/m2]')
        label.setFont(self.bold_font)
        self.layout.addWidget(label, row, 0, 1, 2)    

        row += 1
        
        self.layout.addWidget(QLabel('Pyshield'))
        self.layout.addWidget(self.pyshield_unshielded_doserate, row, 1)
        
        row += 1
        
        self.layout.addWidget(QLabel('Radtracer'))
        self.layout.addWidget(self.radtracer_unshielded_doserate, row, 1)
        
        
        row += 1
        
        label = QLabel('Shielding')
        label.setFont(self.bold_font)
        self.layout.addWidget(label, row, 0, 1, 2)

        row += 1 
        
        self.layout.addWidget(QLabel('Pyshield Attenuation:'), row, 0)
        self.layout.addWidget(self.pyshield_attenuation, row, 1)
        
        row += 1 
        
        self.layout.addWidget(QLabel('Pyshield Buildup:'), row, 0)
        self.layout.addWidget(self.pyshield_buildup, row, 1)
        
        row += 1 
        
        self.layout.addWidget(QLabel('Pyshield Transmission:'), row, 0)
        self.layout.addWidget(self.pyshield_transmission, row, 1)
        
        row += 1
        
        self.layout.addWidget(QLabel('Radtracer Transmission:'), row, 0)
        self.layout.addWidget(self.radtracer_transmission, row, 1)

        row += 1
       
        label = QLabel('Shielded h10 [uSv/h per MBq/m2]')
        label.setFont(self.bold_font)
        self.layout.addWidget(label, row, 0, 1, 2)    

        row += 1
       
        self.layout.addWidget(QLabel('Pyshield'))
        self.layout.addWidget(self.pyshield_shielded_doserate, row, 1)
       
        row += 1
       
        self.layout.addWidget(QLabel('Radtracer'))
        self.layout.addWidget(self.radtracer_shielded_doserate, row, 1)
        
        row += 1
        
        self.layout.addWidget(self.calculate_button, row, 0)
        self.layout.addWidget(self.close_button, row, 1)
        
        
        
        
        

class Controller:
    DISP_FORMAT = "{:.2e}"
    
    def __init__(self):
        self.view = View()
        self.materials = Materials.from_list(DEFAULTS[MATERIALS])
        self.view.material_list.setModel(self.materials)
        self.view.isotope_list.addItems(CONSTANTS.get_isotope_name_list())
        
        self.view.calculate_button.clicked.connect(self.calculate)
        self.view.close_button.clicked.connect(self.view.close)
    
    def calculate(self):
        isotope = self.view.isotope_list.currentText()
        material = self.materials.itemByName(self.view.material_list.currentText())
        thickness = self.view.thickness_value.value()
        
        if material.name != EMPTY_MATERIAL:
            pyshield_attenuation = attenuation_isotope(isotope, material, thickness)
            pyshield_buildup = buildup_isotope(isotope, material, thickness)
            pyshield_transmission = transmission_isotope(isotope, material, thickness)
            radtracer_transmission = TransmissionMCNP(MCNP_LOOKUP[isotope]['None']).get(material.name, thickness)
        else:
            pyshield_attenuation = 1
            pyshield_buildup = 1
            pyshield_transmission = 1
            radtracer_transmission = 1
        
        pyshield_unshielded_doserate = dose_rate(isotope)
        pyshield_shielded_doserate = pyshield_unshielded_doserate * pyshield_transmission
            
        radtracer_unshielded_doserate = MCNP_LOOKUP[isotope]['None']["h(10) [uSv/h per MBq/m^2]"]
        radtracer_shielded_doserate = radtracer_unshielded_doserate * radtracer_transmission        
        
        self.view.pyshield_attenuation.setText(self.to_str(pyshield_attenuation))
        self.view.pyshield_buildup.setText(self.to_str(pyshield_buildup))
        self.view.pyshield_transmission.setText(self.to_str(pyshield_transmission))
        self.view.pyshield_unshielded_doserate.setText(self.to_str(pyshield_unshielded_doserate))
        self.view.pyshield_shielded_doserate.setText(self.to_str(pyshield_shielded_doserate))
        
        self.view.radtracer_unshielded_doserate.setText(self.to_str(radtracer_unshielded_doserate))
        self.view.radtracer_shielded_doserate.setText(self.to_str(radtracer_shielded_doserate))
        self.view.radtracer_transmission.setText(self.to_str(radtracer_transmission))
        
        
    def to_str(self, value):
        return self.DISP_FORMAT.format(value)
        

if __name__ == "__main__":
    app = QApplication([])
    
    controller = Controller()
    window = controller.view
    window.show()    
    app.exec_()
    
    
    
    
