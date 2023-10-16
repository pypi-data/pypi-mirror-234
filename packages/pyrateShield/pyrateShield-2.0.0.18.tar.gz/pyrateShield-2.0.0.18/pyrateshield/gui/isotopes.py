import qtawesome                             
import pandas as pd

from PyQt5.QtWidgets import QLabel, QTableView,  QComboBox, QApplication                            
from PyQt5.QtGui import QIcon


from pyrateshield.constants import CONSTANTS
from pyrateshield.labels import ENERGY_KEV, ABUNDANCE, PARENT, ISOTOPES
from pyrateshield.gui.item_views import EditValueWidget
from pyrateshield.gui.critical_point_controller import PandasModel

INFO_LABEL =('Isotopes can not be added by the user at the moment. '
             'To request a new isotope send an e-mail to the developers '
             ' of pyrateshield.'
             '\n'
             'For some isotopes daughters are included. For daughter nuclei '
             'the abundance is corrected for the branching ratio.'
             '\n'
             'Pyshield neglects gamma rays with energies smaller than 30 keV '
             'because no buildup data is available for these energies.')


class View(EditValueWidget):
    explanation = INFO_LABEL
    def create_widgets(self):
        self.isotope_combo = QComboBox()
        self.isotope_label = QLabel()
        self.table_view = QTableView()
        
    def create_layout(self):
        self.setWindowTitle(ISOTOPES)
        icon = qtawesome.icon('mdi.atom')
        self.setWindowIcon(QIcon(icon))
        self.layout.addWidget(self.isotope_combo, 0, 0)
        self.layout.addWidget(self.table_view, 1, 0)

    def set_stretch(self):
        
        
        
        if hasattr(self, 'explanation'):
            label = QLabel(self.explanation)
            label.setWordWrap(True)
            self.layout.addWidget(label)
            
        self.setLayout(self.layout)
        
    @property
    def isotope(self):
        return self.isotope_combo.currentText()

class Controller:
    def __init__(self, view=None):
        if view is None:
            view = View()
        
        self.view = view
        
        
        self.add_callbacks()
        
        
        self.view.isotope_combo.addItems(self.isotopes)
        
    @property
    def model(self):
        return PandasModel(self.data)
        
    @property
    def data(self):
        data = []
        if self.view.isotope != '':
            isotope = CONSTANTS.get_isotope_by_name(self.view.isotope)
            for parent, keV, abundance in isotope.spectrum_with_parent:
                entry = {PARENT: parent, ENERGY_KEV: keV, ABUNDANCE: abundance}
                data += [entry]
        return pd.DataFrame(data)
        
    def add_callbacks(self):
        self.view.isotope_combo.currentIndexChanged.connect(self.update_isotope)
        
    @property
    def isotopes(self):
        return [item.name for item in CONSTANTS.isotopes]
    
    def update_isotope(self):
        self.view.table_view.setModel(self.model)

        
if __name__ == "__main__":
    app = QApplication([])
    
    controller = Controller()
    window = controller.view
    window.show()    
    app.exec_()