import qtawesome as qta


from PyQt5.QtWidgets import QApplication

from PyQt5.QtWidgets import (QWidget, QCheckBox, QPushButton, 
                             QLineEdit, QSpinBox, QGridLayout, QLabel, 
                             QComboBox, QDoubleSpinBox, QColorDialog, 
                             QScrollBar, QMainWindow, QRadioButton)
                             
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSignal


from pyrateshield.model import Model
from pyrateshield import labels
from pyrateshield.constants import CONSTANTS



MAX_VALUE = float('inf')
MAX_INT_VALUE = 99999999



def safe_get_value_from_widget(widget):
    if isinstance(widget, (EditValueWidget, QDoubleSpinBox, QSpinBox)):
        value = widget.value()
    elif isinstance(widget, (QCheckBox, QRadioButton)):
        value = widget.isChecked()
    elif isinstance(widget, QComboBox):
        value = widget.currentText()
    elif isinstance(widget, (QLineEdit, QLabel)):
         value = widget.text()
         
    else:
        raise TypeError(type(widget))
    return value

def safe_clear(widget):
    if isinstance(widget, (EditValueWidget, QDoubleSpinBox, QSpinBox, QLineEdit)):
        widget.clear()
    elif isinstance(widget, (QRadioButton, QCheckBox)):
        widget.setChecked(False)
    elif isinstance(widget, QComboBox):
        if widget.count() > 0:
            widget.setCurrentIndex(0)
        else:
            widget.setCurrentText('')
        
    elif isinstance(widget, EditValueWidget):
        widget.clear()


def safe_to_int(value):
    if value == '':
        value = 0
    else:
        value = int(round(float(value)))
    return value

def safe_to_float(value):
    if value == '':
        value = 0
    else:
        value = float(value)
    return value

def safe_set_value_to_widget(widget, value):
    # Set widget to a specified value
    # do not set when value equals current value
    # will not generate events when changed
    
    if isinstance(widget, QSpinBox):
        if widget.value() != safe_to_int(value):
            widget.setValue(safe_to_int(value))
    elif isinstance(widget, QDoubleSpinBox):
        if widget.value() != safe_to_float(value):
            widget.setValue(safe_to_float(value))
    elif isinstance(widget, (QLineEdit, QLabel)):
        if widget.text() != str(value):
            widget.setText(str(value))
    elif isinstance(widget, (QRadioButton, QCheckBox)):
        if widget.isChecked() != value:
            widget.setChecked(value)
    elif isinstance(widget, QScrollBar):
        if widget.value() != safe_to_int(value):
            widget.setValue(safe_to_int(value))
    elif isinstance(widget, QComboBox):
        if value is None:
            value = ''
        if isinstance(value, str):
            value = widget.findText(str(value))        
        if widget.currentIndex != safe_to_int(value):
            widget.setCurrentIndex(safe_to_int(value))
    elif isinstance(widget, EditValueWidget):
        widget.setValue(value)
            
    else:
        raise TypeError(f'Unsupported widget type {type(widget)}')
        
class BlockValueChangedSignal:
    def __init__(self, view=None):
        self.view = view
        
    def __enter__(self):
        self.old_value = self.view.valueChangedIsBlocked()
        self.view.setValueChangedBlocked(True)
        
    def __exit__(self, *args):
        self.view.setValueChangedBlocked(self.old_value)
        
class QDoubleSpinBoxInfinite(QDoubleSpinBox):

    def __init__(self, *args, **kwargs):
        super(QDoubleSpinBox, self).__init__(*args, **kwargs)

        self.setMinimum(float('-inf'))
        self.setMaximum(float('inf'))

    def keyPressEvent(self, e: QtGui.QKeyEvent):
        if e.key() == QtCore.Qt.Key_End:
            self.setValue(self.maximum())
        elif e.key() == QtCore.Qt.Key_Home:
            self.setValue(self.minimum())
        else:
            super(QDoubleSpinBox, self).keyPressEvent(e)

class EditValueWidget(QWidget):
    valueChanged = pyqtSignal(object)
    
    def __init__(self, parent=None):

        QWidget.__init__(self, parent=parent)
        self.layout = QGridLayout()
        self.create_widgets()
        self.create_layout()
        self.set_callbacks()
        self.setLayout(self.layout)
    
    def create_widgets(self):
        pass
    
    def set_callbacks(self):
        pass
    
    def value_changed(self):
        if not self.parent().valueChangedIsBlocked():
            self.valueChanged.emit(self.value())
        
    def create_layout(self):
        pass
    
    def value(self):
        pass
    
    def setValue(self):
        pass
   
    
class PositionWidget(EditValueWidget):
    _position_x_text = "X [{unit}]:"
    _position_y_text = "Y [{unit}]:"
    
    def __init__(self, *args, unit='cm', header=labels.POSITION, **kwargs):
        self.unit = unit
        self.header = header
        super().__init__(*args, **kwargs)
    
    def set_callbacks(self):          
        self.x.valueChanged.connect(self.value_changed)
        self.y.valueChanged.connect(self.value_changed)
    
    
    def create_widgets(self):
        x = QDoubleSpinBox(decimals=1)
        x.setRange(-MAX_VALUE, MAX_VALUE)
    
        y = QDoubleSpinBox(decimals=1)
        y.setRange(-MAX_VALUE, MAX_VALUE)
        
        self.x = x
        self.y = y
        self.position_label = QLabel(self.header)
        self.position_label.setStyleSheet('font-weight: bold')
        self.position_x_label = QLabel(self._position_x_text.format(unit=self.unit))
        self.position_y_label = QLabel(self._position_y_text.format(unit=self.unit))
        
    def setValue(self, value):
        safe_set_value_to_widget(self.x, value[0])
        safe_set_value_to_widget(self.y, value[1])
        
    def value(self):
        return [self.x.value(), self.y.value()]
    
    def create_layout(self):
        self.layout.addWidget(self.position_label, 0, 0, 1, 2)

        self.layout.addWidget(self.position_x_label, 1, 0)
        self.layout.addWidget(self.x, 1, 1)
     
        self.layout.addWidget(self.position_y_label, 2, 0)
        self.layout.addWidget(self.y, 2, 1)
        # row += 1
        # self.layout.addWidget(self.position_button, row, 0, 1, 2)
        
    def clear(self):
        safe_clear(self.x)
        safe_clear(self.y)


class VerticesWidget(EditValueWidget):
   
    
    def __init__(self, *args, unit='cm', **kwargs):
        self.unit = unit
        super().__init__(*args, **kwargs)
        
    def set_callbacks(self):          
        self.x1.valueChanged.connect(self.value_changed)
        self.y1.valueChanged.connect(self.value_changed)
        self.x2.valueChanged.connect(self.value_changed)
        self.y2.valueChanged.connect(self.value_changed)
    
        
    def create_widgets(self):
        self.x1 = QDoubleSpinBox(decimals=1)
        self.x1.setRange(-MAX_VALUE, MAX_VALUE)
    
        self.y1 = QDoubleSpinBox(decimals=1)
        self.y1.setRange(-MAX_VALUE, MAX_VALUE)
        
        self.x2 = QDoubleSpinBox(decimals=1)
        self.x2.setRange(-MAX_VALUE, MAX_VALUE)
    
        self.y2 = QDoubleSpinBox(decimals=1)
        self.y2.setRange(-MAX_VALUE, MAX_VALUE)
        
        
        self.label = QLabel(labels.VERTICES)
        self.label.setStyleSheet('font-weight: bold')
        
        position_x1_text = f'X1 [{self.unit}]:'
        position_y1_text = f'Y1 [{self.unit}]:'
        position_x2_text = f'X2 [{self.unit}]:'
        position_y2_text = f'Y2 [{self.unit}]:'
        
        self.position_x1_label = QLabel(position_x1_text)
        self.position_y1_label = QLabel(position_y1_text)
        self.position_x2_label = QLabel(position_x2_text)
        self.position_y2_label = QLabel(position_y2_text)
        
    def setValue(self, value):
   
        safe_set_value_to_widget(self.x1, value[0][0])
        safe_set_value_to_widget(self.y1, value[0][1])
        safe_set_value_to_widget(self.x2, value[1][0])
        safe_set_value_to_widget(self.y2, value[1][1])
        
    def value(self):
        vertices = [[self.x1.value(), self.y1.value()],
                    [self.x2.value(), self.y2.value()]]
       
        return vertices
    
    def create_layout(self):
        self.layout.addWidget(self.label, 0, 0, 1, 2)

        self.layout.addWidget(self.position_x1_label, 1, 0)
        self.layout.addWidget(self.x1, 1, 1)
     
        self.layout.addWidget(self.position_y1_label, 2, 0)
        self.layout.addWidget(self.y1, 2, 1)
        
        self.layout.addWidget(self.position_x2_label, 3, 0)
        self.layout.addWidget(self.x2, 3, 1)
     
        self.layout.addWidget(self.position_y2_label, 4, 0)
        self.layout.addWidget(self.y2, 4, 1)
        # row += 1
        # self.layout.addWidget(self.position_button, row, 0, 1, 2)
        
    def clear(self):
        for widget in self.x1, self.x2, self.y1, self.y2:
            safe_clear(widget)
        
     
class IsotopeWidget(EditValueWidget):
  
    def create_layout(self):        
        self.layout.addWidget(self.isotope_label, 0, 0)
        self.layout.addWidget(self.isotope_input, 0, 1)
        self.layout.addWidget(self.halflife_label, 1, 0)
        self.layout.addWidget(self.halflife_value, 1, 1)
    
        
    def create_widgets(self):
        self.isotope_input = QComboBox()
        self.isotope_input.addItems(CONSTANTS.get_isotope_name_list())
        self.isotope_label = QLabel(labels.ISOTOPE)
        self.halflife_label = QLabel(labels.HALF_LIFE)
        self.halflife_value = QLabel('empty')
        
    def set_callbacks(self):
        callback = self.value_changed
        self.isotope_input.currentTextChanged.connect(callback)
        
    def update_halflife_label(self):
        isotope = CONSTANTS.get_isotope_by_name(self.value())
     
        safe_set_value_to_widget(self.halflife_value, isotope.half_life)
    
    def value_changed(self):
        self.update_halflife_label()
        
        self.valueChanged.emit(self.value())
        
    def value(self):
        return self.isotope_input.currentText()
    
    def setValue(self, value):
        self.isotope_input.setCurrentText(value) 
        self.update_halflife_label()
        
    def clear(self):
        for widget in self.isotope_input, self.halflife_value:
            safe_clear(widget)
        



class SelfShieldingWidget(EditValueWidget):
    def create_widgets(self):    
        self.self_shielding_list = QComboBox()
        self.self_shielding_list.addItems(CONSTANTS.self_shielding_options)
        self.self_shielding_label = QLabel(labels.SELF_SHIELDING)
        self.self_shielding_factor_label = QLabel(labels.SELF_SHIELDING_FACTOR)
        self.self_shielding_factor_input = QDoubleSpinBox()
        self.self_shielding_factor_input.setSingleStep(0.01)
        self.self_shielding_factor_input.setRange(0, MAX_VALUE)
        self.self_shielding_factor_input.setDecimals(6)
        self.self_shielding_factor_input.setValue(1.0)     
    
    def create_layout(self):
        self.layout = QGridLayout()
        self.layout.addWidget(self.self_shielding_label, 0, 0)
        self.layout.addWidget(self.self_shielding_list, 0, 1)
        self.layout.addWidget(self.self_shielding_factor_label, 1, 0)
        self.layout.addWidget(self.self_shielding_factor_input, 1, 1)
        
    def set_callbacks(self):
       
        callback = self.value_changed
        
        self.self_shielding_list.currentTextChanged.connect(callback)        
        self.self_shielding_factor_input.valueChanged.connect(callback)
        
    def value_changed(self):
        self.valueChanged.emit(self.value())
        if isinstance(self.value(), str):
            enabled = False
        else:
            enabled = True
            
        self.self_shielding_factor_label.setEnabled(enabled)
        self.self_shielding_factor_input.setEnabled(enabled)
        
        
    def value(self):
        list_value = self.self_shielding_list.currentText()
        if list_value == labels.SELF_SHIELDING_FACTOR:
            return self.self_shielding_factor_input.value()
        else:
            return list_value
        
    def setValue(self, value):
        if isinstance(value, str):
            self.self_shielding_list.setCurrentText(value)
        else:
            self.self_shielding_list.setCurrentText(labels.SELF_SHIELDING_FACTOR)
            safe_set_value_to_widget(self.self_shielding_factor_input, value)            
            
    def clear(self):
        for widget in self.self_shielding_factor_input, self.self_shielding_list:
            safe_clear(widget)
            
class MaterialsWidget(EditValueWidget):
    def create_widgets(self):
        self.material1_label = QLabel(labels.MATERIAL + ' 1')
        self.material1_list = QComboBox()
    
        self.thickness1_label = QLabel(labels.THICKNESS)
        self.thickness1_input = QDoubleSpinBox(decimals=3)
    
        self.material2_label = QLabel(labels.MATERIAL + ' 2')
        self.material2_list = QComboBox()
        
        self.thickness2_label = QLabel(labels.THICKNESS)
        self.thickness2_input = QDoubleSpinBox(decimals=3)
    
    def create_layout(self):
        row = 0
        self.layout.addWidget(self.material1_label, row, 0)
        self.layout.addWidget(self.material1_list, row, 1)
        row += 1
        self.layout.addWidget(self.thickness1_label, row, 0)
        self.layout.addWidget(self.thickness1_input, row, 1)
        row += 1
        self.layout.addWidget(self.material2_label, row, 0)
        self.layout.addWidget(self.material2_list, row, 1)
        row += 1
        self.layout.addWidget(self.thickness2_label, row, 0)
        self.layout.addWidget(self.thickness2_input, row, 1)
        
    def set_callbacks(self):
        
        callback = self.value_changed
        
        self.material1_list.currentTextChanged.connect(callback)
        self.material2_list.currentTextChanged.connect(callback)
        self.thickness1_input.valueChanged.connect(callback)
        self.thickness2_input.valueChanged.connect(callback)
    
    def value(self):
        materials1 = safe_get_value_from_widget(self.material1_list)
        thickness1 = safe_get_value_from_widget(self.thickness1_input)
        thickness2 = safe_get_value_from_widget(self.thickness2_input)
        materials2 = safe_get_value_from_widget(self.material2_list)
        
        # if thickness1 == 0:
        #     materials1 = None
        # if thickness2 == 0:
        #     materials2 = None
                    
        return [[materials1, thickness1], [materials2, thickness2]]
    
    def setValue(self, value):

        materials1 = value[0][0]
        thickness1 = value[0][1]
        
        if len(value) == 2:
            materials2 = value[1][0]
            thickness2 = value[1][1]
        else:
            materials2 = labels.EMPTY_MATERIAL
            thickness2 = 0
            
             
        safe_set_value_to_widget(self.material1_list, materials1)
        safe_set_value_to_widget(self.thickness1_input, thickness1)
        
        
        
        if len(value) == 2:
            
            safe_set_value_to_widget(self.material2_list, materials2)
            safe_set_value_to_widget(self.thickness2_input, thickness2 )
        else:
            safe_set_value_to_widget(self.material2_list, labels.EMPTY_MATERIAL)
            safe_set_value_to_widget(self.thickness2_input, 0)
            
    def clear(self):
        for widget in (self.material1_list, self. material2_list,
                       self.thickness1_input, self.thickness2_input):
            safe_clear(widget)
    
            
class ModelItemsWidget(EditValueWidget):
    _name_text = "Name:"
    _value_widgets = None
    enabled = None
    name_input = None
    list = None
    valueChanged = pyqtSignal(str, object)
    
    _signal_blocked = False
    
    def __init__(self, *args, parent=None, **kwargs):
        super().__init__(*args, parent=parent, **kwargs)
        self.layout.setRowStretch(self.layout.rowCount(), 1)
    
    def setValueChangedBlocked(self, block=True):
        self._signal_blocked = block
        
    def valueChangedIsBlocked(self):
        return self._signal_blocked
    
    def add_list(self):
        self.list = QComboBox()
        row = self.layout.rowCount()
        self.layout.addWidget(self.list, row, 0, 1, 2)
        
    def add_enabled(self):
        self.enabled = QCheckBox('Enabled')
        row = self.layout.rowCount()
        self.layout.addWidget(self.enabled, row, 0, 1, 2)
    
    def add_name(self):
        self.name_label = QLabel(self._name_text)
        self.name_input = QLineEdit()
        
        row = self.layout.rowCount()
        
        self.layout.addWidget(self.name_label, row, 0)
        self.layout.addWidget(self.name_input, row, 1)
        
    def value_widgets(self):
        if self._value_widgets is None:
            self._value_widgets = {}
            if self.enabled is not None:
                self._value_widgets[labels.ENABLED] = self.enabled
            if self.name_input is not None:
                self._value_widgets[labels.NAME] = self.name_input
        return self._value_widgets
    
    def clear(self):
        with BlockValueChangedSignal(self):
            for widget in self.value_widgets().values():
                safe_clear(widget)
            if hasattr(self, 'list'):
                safe_clear(self.list)
           
    
    def value_changed(self, label): 
        if not self._signal_blocked:
            self.valueChanged.emit(label, self.value(label))
     
            
    def value(self, label):       
        widget = self.value_widgets()[label]
        value = safe_get_value_from_widget(widget)
        if label == labels.KVP:
            value = int(value)
        return value
    
    def setValue(self, label, value):
        if label == labels.KVP:
            value = str(value)
            
        widget = self.value_widgets()[label]
        
        safe_set_value_to_widget(widget, value)
        
        if label == labels.NAME:            
            safe_set_value_to_widget(self.name_input, value)
            
        if label == labels.ENABLED and value is not None:
            self.setEnabled(value)
            
        
            
        
            
    def values(self):
        return {label: self.value(label)\
                for label in self.value_widgets().keys()}
            
    def setValues(self, values):     
        for label, value in values.items():
            self.setValue(label, value)
            
        
    def set_callbacks(self):
        if self.enabled is not None:
            callback = lambda _, label=labels.ENABLED: self.value_changed(label)
            self.enabled.stateChanged.connect(callback)
        if self.name_input is not None:
            callback = lambda label=labels.NAME: self.value_changed(label)
            self.name_input.returnPressed.connect(callback)
            
   

    def setEnabled(self, enabled):
        widgets = [item for item in self.children()\
                   if isinstance(item, QWidget)]
        
        if self.list in widgets: widgets.remove(self.list)
        if self.enabled in widgets: widgets.remove(self.enabled)
        
        for widget in widgets:
            widget.setEnabled(enabled)
        
            

class EditSourcesNMView(ModelItemsWidget):
    LABEL = labels.SOURCES_NM
    explanation = ("To add a new source select Source NM from the toolbar and "
                   "click on the floorplan to add a source at that position."
                   "\n\n"
                   "When setting self shielding to 'Body', pyshield will "
                   "assume 10 cm of water as additional shielding (buildup "
                   "and attenuation). Radtracer will use a pre-simulated "
                   "spectrum after additional 15 cm of "
                   "shielding with water. Note that large differences in results "
                   "may occur between pyshield and radtracer when setting self "
                   "shielding to 'Body.'\n\n"
                   "Note that setting the self shielding to 'Body' may increase "
                   "the dose rates for pyshield for some isotopes. This is due "
                   "to the buildup in 10 cm of water. Using a user defined fixed "
                   "factor could provide a better results for pyshield.")
    
    
    def setValue(self, label, value):
        super().setValue(label, value)
        print(label, value)
                
    def create_widgets(self):
        
        super().create_widgets()
        self.position = PositionWidget(parent=self)
        
        self.isotope = IsotopeWidget(parent=self)
        
        self.duration = QDoubleSpinBox(self, decimals=3)
        self.duration.setRange(0, MAX_VALUE)
        self.duration_label = QLabel(labels.DURATION)
        
               
        self.activity = QDoubleSpinBox(self, decimals=2)
        self.activity.setRange(0, MAX_VALUE)
        self.activity_label = QLabel(labels.ACTIVITY)

        self.number_of_exams_label = QLabel(labels.NUMBER_OF_EXAMS, parent=self)
        self.number_of_exams_input = QSpinBox(self)
        self.number_of_exams_input.setRange(0, MAX_INT_VALUE)
        

        self.decay_correction = QCheckBox(labels.APPLY_DECAY_CORRECTION,
                                          parent=self)
        
        self.self_shielding = SelfShieldingWidget(parent=self)
        
        self.clearance_label = QLabel('Clearance Model', parent=self)
        self.clearance_list = QComboBox(self)
        
    def value_widgets(self):
       if self._value_widgets is None:
           self._value_widgets = super().value_widgets()
           self._value_widgets[labels.POSITION] = self.position
           self._value_widgets[labels.DURATION] = self.duration
           self._value_widgets[labels.ACTIVITY] = self.activity
           self._value_widgets[labels.ISOTOPE] = self.isotope
           self._value_widgets[labels.SELF_SHIELDING] = self.self_shielding
           self._value_widgets[labels.NUMBER_OF_EXAMS] = self.number_of_exams_input
           self._value_widgets[labels.APPLY_DECAY_CORRECTION] = self.decay_correction
           self._value_widgets[labels.CLEARANCE] = self.clearance_list
       return self._value_widgets
    
    
            

    def create_layout(self):
        
        self.add_list()
        self.add_name()

        row = self.layout.rowCount()
        
        self.layout.addWidget(self.position, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.isotope, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.decay_correction, row, 0, 1, 2)
        
        
        
        row += 1
        
        self.layout.addWidget(self.number_of_exams_label, row, 0)
        self.layout.addWidget(self.number_of_exams_input, row, 1)
        
        row += 1
        
        self.layout.addWidget(self.activity_label, row, 0)
        self.layout.addWidget(self.activity, row, 1)
        
        row += 1
        
        self.layout.addWidget(self.duration_label, row, 0)
        self.layout.addWidget(self.duration, row, 1)
        
        row += 1
        
        self.layout.addWidget(self.self_shielding, row, 0, 1, 2)
        
        
        row += 1

        self.layout.addWidget(self.clearance_label, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.clearance_list, row, 0, 1, 2)
        
        
           
        self.add_enabled()
           
    
    
    def set_callbacks(self):
        super().set_callbacks()
        
        
        label = labels.POSITION
        callback = lambda _, label=label: self.value_changed(label)        
        self.position.valueChanged.connect(callback)
        
        label = labels.ISOTOPE
        callback = lambda _, label=label: self.value_changed(label)        
        self.isotope.valueChanged.connect(callback)
        
        label = labels.APPLY_DECAY_CORRECTION
        callback = lambda _, label=label: self.value_changed(label)        
        self.decay_correction.stateChanged.connect(callback)
        
        label = labels.NUMBER_OF_EXAMS
        callback = lambda _, label=label: self.value_changed(label)
        self.number_of_exams_input.valueChanged.connect(callback)
        
        label = labels.ACTIVITY
        callback = lambda _, label=label: self.value_changed(label)
        self.activity.valueChanged.connect(callback)
        
        label = labels.DURATION
        callback = lambda _, label=label: self.value_changed(label)        
        self.duration.valueChanged.connect(callback)
        
        label = labels.CLEARANCE
        callback = lambda _, label=label: self.value_changed(label)        
        self.clearance_list.currentIndexChanged.connect(callback)
        
        label = labels.SELF_SHIELDING
        callback = lambda _, label=label: self.value_changed(label)        
        self.self_shielding.valueChanged.connect(callback)
        
    
         
class EditClearancesView(ModelItemsWidget):
    explanation = ("\nUp to two biological fraction can be defined with a"
                   " corresponding biological halflife. For each fraction "
                   "pyrateshield will calculate an effective halflife by "
                   "combining the physical halflife and biological halflife. "
                   "If (physical) decay is not checked in the Sources NM tab "
                   "physical decay will be ignored and only biological "
                   "decay will be applied.\n\n"
                   "If the fractions add up to less than 1, no biological"
                   "decay correction will be applied to the remaining fraction"
                   "\n\n"
                   "Optionally fractions can be split in time. The first "
                   "fraction will be integrated until the split time. The "
                   "second fraction and if applicable the remaining fraction "
                   "will be integrated from the split time. Integration will "
                   "always stop after source duration.")
    
    def create_widgets(self):
        super().create_widgets()
        self.add_list()
        self.add_name()
        
        self.decay_fraction1_checkbox = QCheckBox(labels.DECAY_FRACTION1)
        self.decay_fraction1 = QDoubleSpinBox(decimals=2)
        self.decay_fraction1.setRange(0, 1)
        self.decay_fraction1.setSingleStep(0.05)
        

        self.decay_fraction2_checkbox = QCheckBox(labels.DECAY_FRACTION2)
        self.decay_fraction2 = QDoubleSpinBox(decimals=2)
        self.decay_fraction2.setRange(0, 1)
        self.decay_fraction2.setSingleStep(0.05)
        
        # Prevent halflives to become zero
        self.half_life_label1 = QLabel(labels.HALF_LIFE)
        self.half_life_value1 = QDoubleSpinBoxInfinite(decimals=2)
        self.half_life_value1.setRange(0.01, MAX_VALUE)
        
        self.half_life_label2 = QLabel(labels.HALF_LIFE)
        self.half_life_value2 = QDoubleSpinBoxInfinite(decimals=2)
        self.half_life_value2.setRange(0.01, MAX_VALUE)
        
        self.split_time_checkbox = QCheckBox(labels.ENABLE_SPLIT_FRACTIONS)
        self.split_time_label = QLabel(labels.SPLIT_FRACTION_TIME)
        self.split_time_input = QDoubleSpinBox(decimals=1)
        self.split_time_input.setRange(0, MAX_VALUE)
        
        
        
        self.new_button = QPushButton('Add', self)
        self.delete_button = QPushButton("Delete")
        
    def value_widgets(self):
        if self._value_widgets is None:
            self._value_widgets = super().value_widgets()
            self._value_widgets[labels.APPLY_FRACTION1] = self.decay_fraction1_checkbox
            self._value_widgets[labels.APPLY_FRACTION2] = self.decay_fraction2_checkbox
            self._value_widgets[labels.DECAY_FRACTION1] = self.decay_fraction1
            self._value_widgets[labels.DECAY_FRACTION2] = self.decay_fraction2
            self._value_widgets[labels.HALFLIFE1] = self.half_life_value1
            self._value_widgets[labels.HALFLIFE2] = self.half_life_value2
            self._value_widgets[labels.ENABLE_SPLIT_FRACTIONS] = self.split_time_checkbox
            self._value_widgets[labels.SPLIT_FRACTION_TIME] = self.split_time_input
        return self._value_widgets
            
    def value_changed(self, label):
        super().value_changed(label)
        self.update_available_widgets()
    
    def setValues(self, values):        
        super().setValues(values)
        values = values or {}
        if labels.NAME in values.keys()\
            and values[labels.NAME] == labels.EMPTY_CLEARANCE:            
            self.setEnabled(False)
        else:                  
            self.setEnabled(True)            
            self.update_available_widgets()

    def update_available_widgets(self, _=None):
      
        enabled = self.name_input.isEnabled()
        if not enabled: return
        self.decay_fraction1_checkbox.setChecked(True)
        self.decay_fraction1_checkbox.setEnabled(False)
        
        self.decay_fraction1.setEnabled(True)
        self.half_life_value1.setEnabled(True)
        self.half_life_label1.setEnabled(True)
        
        
        enabled = self.decay_fraction2_checkbox.isChecked()
        
        self.decay_fraction2.setEnabled(enabled)
        self.half_life_value2.setEnabled(enabled)
        self.half_life_label2.setEnabled(enabled)
        
        
        enabled = self.split_time_checkbox.isChecked()
        self.split_time_input.setEnabled(enabled)
        self.split_time_label.setEnabled(enabled)
        
        if enabled:
            self.decay_fraction2_checkbox.setChecked(True)
            self.decay_fraction2_checkbox.setEnabled(False)
            self.decay_fraction2.setEnabled(False)
            self.half_life_value2.setEnabled(True)
        else:
            self.decay_fraction2_checkbox.setEnabled(True)

    def set_callbacks(self):
        super().set_callbacks()
        label = labels.HALFLIFE1
        callback = lambda _, label=label: self.value_changed(label)        
        self.half_life_value1.valueChanged.connect(callback)
        
        label = labels.HALFLIFE2
        callback = lambda _, label=label: self.value_changed(label)        
        self.half_life_value2.valueChanged.connect(callback)

        label = labels.SPLIT_FRACTION_TIME
        callback = lambda _, label=label: self.value_changed(label)        
        self.split_time_input.valueChanged.connect(callback)
        
        label = labels.DECAY_FRACTION1
        callback = lambda _, label=label: self.value_changed(label)        
        self.decay_fraction1.valueChanged.connect(callback)
        

        label = labels.DECAY_FRACTION2
        callback = lambda _, label=label: self.value_changed(label)        
        self.decay_fraction2.valueChanged.connect(callback)
        
        label = labels.APPLY_FRACTION1
        callback = lambda _, label=label: self.value_changed(label)        
        self.decay_fraction1_checkbox.stateChanged.connect(callback)
        
        label = labels.APPLY_FRACTION2
        callback = lambda _, label=label: self.value_changed(label)        
        self.decay_fraction2_checkbox.stateChanged.connect(callback)
        
        label = labels.ENABLE_SPLIT_FRACTIONS
        callback = lambda _, label=label: self.value_changed(label)        
        self.split_time_checkbox.stateChanged.connect(callback)
        
        self.list.currentIndexChanged.connect(self.update_available_widgets)
    
    def create_layout(self):
        super().create_layout()
        
        row = self.layout.rowCount() + 1
     
        self.layout.addWidget(self.decay_fraction1_checkbox, row, 0)
        self.layout.addWidget(self.decay_fraction1, row, 1)
        row += 1
        self.layout.addWidget(self.half_life_label1, row, 0)
        self.layout.addWidget(self.half_life_value1, row, 1)    
                
        row += 1
        
        self.layout.addWidget(self.decay_fraction2_checkbox, row, 0)
        self.layout.addWidget(self.decay_fraction2, row, 1)
        
        row += 1
        
        self.layout.addWidget(self.half_life_label2, row, 0)
        self.layout.addWidget(self.half_life_value2, row, 1)  
        
       
        row += 1
        
        self.layout.addWidget(self.split_time_checkbox, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.split_time_label, row, 0)
        self.layout.addWidget(self.split_time_input, row, 1)
   
        row += 1
        
        self.layout.addWidget(self.new_button, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.delete_button, row, 0, 1, 2)
    
    def setEnabled(self, enabled):
        super().setEnabled(enabled)
        self.new_button.setEnabled(True)
        

class EditSourcesXrayView(ModelItemsWidget):
 
    explanation = ("To add a new source select Source Xray from the toolbar and "
                   "click on the floorplan to add a source at that position.")
                   
    
    @property
    def kvp_labels(self):
        return [str(item.kvp) for item in CONSTANTS.xray]
    
    def create_widgets(self):
        super().create_widgets()
        self.add_list()
        self.add_name()
        
        self.position = PositionWidget()
        
        self.number_of_exams_input = QSpinBox()
        self.number_of_exams_input.setRange(0, MAX_INT_VALUE)
        self.number_of_exams_label = QLabel(labels.NUMBER_OF_EXAMS)
        
        self.kvp = QComboBox()
        self.kvp.addItems(self.kvp_labels) 
        self.kvp_label = QLabel(labels.KVP)

        self.dap = QDoubleSpinBox()
        self.dap.setRange(0, MAX_VALUE)
        self.dap_label = QLabel(labels.DAP)
        
    def value_widgets(self):
        if self._value_widgets is None:
            self._value_widgets = super().value_widgets()
            self._value_widgets[labels.POSITION] = self.position
            self._value_widgets[labels.NUMBER_OF_EXAMS] = self.number_of_exams_input
            self._value_widgets[labels.KVP] = self.kvp
            self._value_widgets[labels.DAP] = self.dap
        return self._value_widgets
        
    def set_callbacks(self):
        super().set_callbacks()
        label = labels.POSITION
        callback = lambda _, label=label: self.value_changed(label)        
        self.position.valueChanged.connect(callback)
        
        
        label = labels.NUMBER_OF_EXAMS
        callback = lambda _, label=label: self.value_changed(label)        
        self.number_of_exams_input.valueChanged.connect(callback)
        
        label = labels.KVP
        callback = lambda _, label=label: self.value_changed(label)        
        self.kvp.currentTextChanged.connect(callback)
        
        label = labels.DAP
        callback = lambda _, label=label: self.value_changed(label)        
        self.dap.valueChanged.connect(callback)

    def create_layout(self):
        
        row = self.layout.rowCount() + 1
        self.layout.addWidget(self.number_of_exams_label, row, 0)
        self.layout.addWidget(self.number_of_exams_input, row, 1)
        
        row += 1
        self.layout.addWidget(self.kvp_label, row, 0)
        self.layout.addWidget(self.kvp, row, 1)
        row += 1
        self.layout.addWidget(self.dap_label, row, 0)
        self.layout.addWidget(self.dap, row, 1)
        
        row += 1
        
        self.layout.addWidget(self.position, row, 0, 1, 2)
        
        self.add_enabled()
    

        



        
class EditSourcesCTView(ModelItemsWidget):
  
    explanation = ("To add a new source select Source CT from the toolbar and "
                   "click on the floorplan to add a source at that position.")
   
    
    @property
    def kvp_labels(self):
        return [str(item.kvp) for item in CONSTANTS.ct]
    
    def create_widgets(self):
        super().create_widgets()
        self.add_list()
        self.add_name()
        self.position = PositionWidget()
        
        self.number_of_exams_input = QSpinBox()
        self.number_of_exams_input.setRange(0, MAX_INT_VALUE)
        self.number_of_exams_label = QLabel(labels.NUMBER_OF_EXAMS)

        self.kvp = QComboBox()
        self.kvp.addItems(self.kvp_labels) 
        self.kvp_label = QLabel(labels.KVP)

        self.body_part = QComboBox()
        self.body_part.addItems(CONSTANTS.CT_body_part_options ) 
        self.body_part_label = QLabel(labels.CT_BODY_PART)

        self.dlp = QDoubleSpinBox()
        self.dlp.setRange(0, MAX_VALUE)
        self.dlp_label = QLabel(labels.DLP)
        
    def value_widgets(self):
        if self._value_widgets is None:
            self._value_widgets = super().value_widgets()
            self._value_widgets[labels.POSITION] = self.position
            self._value_widgets[labels.NUMBER_OF_EXAMS] = self.number_of_exams_input
            self._value_widgets[labels.KVP] = self.kvp
            self._value_widgets[labels.CT_BODY_PART] = self.body_part
            self._value_widgets[labels.DLP] = self.dlp
        return self._value_widgets

        
    def set_callbacks(self):
        super().set_callbacks()
        
        label = labels.POSITION
        callback = lambda _, label=label: self.value_changed(label)        
        self.position.valueChanged.connect(callback)
        
        
        label = labels.NUMBER_OF_EXAMS
        callback = lambda _, label=label: self.value_changed(label)                
        self.number_of_exams_input.valueChanged.connect(callback)
        
        label = labels.KVP
        callback = lambda _, label=label: self.value_changed(label)        
        self.kvp.currentTextChanged.connect(callback)
 
        
        label = labels.DLP
        callback = lambda _, label=label: self.value_changed(label)        
        self.dlp.valueChanged.connect(callback)
                
        label = labels.CT_BODY_PART
        callback = lambda _, label=label: self.value_changed(label)        
        self.body_part.currentTextChanged.connect(callback)
        
        
    def create_layout(self):
        row = self.layout.rowCount() + 1
        self.layout.addWidget(self.number_of_exams_label, row, 0)
        self.layout.addWidget(self.number_of_exams_input, row, 1)
        row += 1
        self.layout.addWidget(self.kvp_label, row, 0)
        self.layout.addWidget(self.kvp, row, 1)
        row += 1
        self.layout.addWidget(self.body_part_label, row, 0)
        self.layout.addWidget(self.body_part, row, 1)
        row += 1
        self.layout.addWidget(self.dlp_label, row, 0)
        self.layout.addWidget(self.dlp, row, 1)
        row += 1 
        self.layout.addWidget(self.position, row, 0, 1, 2)
        
        self.add_enabled()
    
  
    
class EditCriticalPointsView(ModelItemsWidget):
    LABEL = labels.CRITICAL_POINTS
    explanation = ("To add a new critcal point select Critical Point from "
                   "the toolbar and click on the floorplan to add a "
                   "critical point at that position.")
              
    
     

    def create_widgets(self):
        self.add_list()
        self.add_name()
        super().create_widgets()
        
        self.position = PositionWidget()
        self.occupancy_factor_label = QLabel("Occupancy Factor:")
        self.occupancy_factor_input = QDoubleSpinBox()
        self.occupancy_factor_input.setSingleStep(0.05)
        self.occupancy_factor_input.setRange(0, 1)
        self.occupancy_factor_input.setValue(1)
    
    def value_widgets(self):
        if self._value_widgets is None:
            self._value_widgets = super().value_widgets()
            self._value_widgets[labels.OCCUPANCY_FACTOR] = self.occupancy_factor_input
            self._value_widgets[labels.POSITION] = self.position
        return self._value_widgets

    def set_callbacks(self):
        super().set_callbacks()
        label = labels.OCCUPANCY_FACTOR
        callback = lambda _, label=label: self.value_changed(label)
    
        self.occupancy_factor_input.valueChanged.connect(callback)
        
        label = labels.POSITION
        callback = lambda _, label=label: self.value_changed(label)
    
        self.position.valueChanged.connect(callback)
        
  
        
    def create_layout(self):
        super().create_layout()

        row = self.layout.rowCount() + 1
        
        self.layout.addWidget(self.position, row, 0, 1, 2)

        row += 1
        
        self.layout.addWidget(self.occupancy_factor_label, row, 0)
        self.layout.addWidget(self.occupancy_factor_input, row, 1)
        
        self.add_enabled()
    
        
class EditShieldingsView(ModelItemsWidget):
    
    _color = 'r'
    _DEFAULT_THICKNESS = 1
    _DEFAULT_LINEWIDTH = 1
    
   
    def create_widgets(self):
        super().create_widgets()
        self.add_list()
        self.add_name()
        #icon = qta.icon('fa5s.circle', color='red')
        self.color_button = QPushButton("Select Color", self)
        #self.color_button.setIcon(icon)

        
        self.materials = MaterialsWidget()
        # materials = [material.name for material in CONSTANTS.materials]
        
        # self.material1_list.addItems(materials)
        # self.material2_list.addItems(materials)

       
        
        self.line_width_label = QLabel(labels.LINEWIDTH)
        self.line_width = QDoubleSpinBox()
        
        
        self.new_button = QPushButton('Add', self)
        self.delete_button = QPushButton("Delete")
        

        
    def value_widgets(self):
        if self._value_widgets is None:
            self._value_widgets = super().value_widgets()
            self._value_widgets[labels.MATERIALS] = self.materials
            self._value_widgets[labels.LINEWIDTH] = self.line_width
        return self._value_widgets
    
    def value(self, label):
        if label == labels.COLOR:
            return self._color
        else:
            return super().value(label)
    
    def setValues(self, values):
        super().setValues(values)
        values = values or {}
        if labels.NAME in values.keys()\
            and values[labels.NAME] == labels.EMPTY_SHIELDING:        
            self.setEnabled(False)
        else:              
            self.setEnabled(True)

        
    def values(self, label):
        values = super().values()
        values[labels.COLOR] = self._color
        
    def setValue(self, label, value):
        if label == labels.COLOR:
            self.setColor(value)
        else:
            super().setValue(label, value)
            

    
    def create_layout(self):
        
        row = self.layout.rowCount() + 1
        
        self.layout.addWidget(self.materials, row, 0, 1, 2)
        
        
        
        row += 1
        self.layout.addWidget(self.line_width_label, row, 0)
        self.layout.addWidget(self.line_width, row, 1)
        
        row += 1
        
        self.layout.addWidget(self.color_button, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.new_button, row, 0)
        self.layout.addWidget(self.delete_button, row, 1)
        
    def set_callbacks(self):
        super().set_callbacks()                
        
        label = labels.MATERIALS
        callback = lambda _, label=label: self.value_changed(label)        
        self.materials.valueChanged.connect(callback)
        
        
         
        label = labels.LINEWIDTH
        callback = lambda _, label=label: self.value_changed(label)  
        self.line_width.valueChanged.connect(callback)
        
        self.color_button.clicked.connect(self.select_color)
        
        
    def color(self):       
        return self._color
    
    def setColor(self, color):
        self._color = color        
        icon = qta.icon('fa5s.circle', color=color)
        
        self.color_button.setIcon(icon)
        
        self.value_changed(labels.COLOR)
    
    
    def select_color(self):
        color = QColorDialog().getColor()
        if color.isValid():
            self.setColor(color.name())
            
    def setEnabled(self, enabled):
        super().setEnabled(enabled)
        self.new_button.setEnabled(True)
     


        
       

class EditWallsView(ModelItemsWidget):
    explanation = ("To add a Wall select Wall from the toolbar. "
                   "Click and hold the left mouse button to draw a wall")
    
    start_x1, start_y1, start_x2, start_y2 = ['X1 [cm]', 'Y1 [cm]', 
                                              'X2 [cm]', 'Y2 [cm]']
    
    def create_widgets(self):
        super().create_widgets()
        
        self.shielding_label = QLabel("Shielding")
        self.shielding_list = QComboBox()
        
        self.vertices = PositionWidget()
                                
        self.scroll_widget = QScrollBar(QtCore.Qt.Horizontal)
        self.scroll_widget.setPageStep(1)
        
        self.vertex_label = QLabel("Vertex")
        self.vertex_list = QComboBox()
        
        self.index_label = QLabel()
    
    
        
    def value_widgets(self):
        if self._value_widgets is None:
            self._value_widgets = super().value_widgets()
            self._value_widgets[labels.SHIELDING] = self.shielding_list
            #self._value_widgets[labels.VERTICES] = self.vertices
        return self._value_widgets
        
    def set_callbacks(self):
        label = labels.SHIELDING
        callback = lambda _, label=label: self.value_changed(label)
        self.shielding_list.currentTextChanged.connect(callback)
        
        
        # label = labels.VERTICES
        # callback = lambda _, label=label: self.value_changed(label)
        # self.vertices.valueChanged.connect(callback)
                
        
    def setIndex(self, index=None):
        if index is None:
            return
        
        self.scroll_widget.setValue(index)
        self.index_label.setText(f'Wall index {index}')
        
    def create_layout(self): 
        row = 0
        
        self.layout.addWidget(self.scroll_widget, row , 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.index_label, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.shielding_label, row, 0)
        self.layout.addWidget(self.shielding_list, row, 1)
        
        row += 1
        
        self.layout.addWidget(self.vertex_label, row, 0)
        self.layout.addWidget(self.vertex_list, row, 1)
        
        row += 1 
        
        self.layout.addWidget(self.vertices, row, 0, 1, 2)

class EditMaterialsView(ModelItemsWidget):
    LABEL = labels.MATERIALS
    explanation =\
        ('Materials can be changed or added to a limited extend. '
         'Radtracer implements a limited set of materials. Pyshield uses '
         'attenuation and buildup tables for a limited set of '
         'materials. For some materials, like "Concrete-Barite", there is no '
         'buildup table available. For example the buildup table for "Concrete" is '
         'used for "Concrete-Barite" in pyshield. '
         '\n\n'
         'Defining or changing a material is mostly usefull to define a '
         'material that has a (slightly) different density. '
         'Both pyshield and radtracer can handle variations in density accurately.')
        
    
    def create_widgets(self):
        super().create_widgets()
        self.add_list()
        self.add_name()
        self.density_label = QLabel('Density [g/cm^3]')
        self.density_input = QDoubleSpinBox(decimals=3)
        self.attenuation_label = QLabel(labels.ATTENUATION_TABLE)
        self.attenuation_combo = QComboBox()
        self.attenuation_combo.addItems(CONSTANTS.base_materials)
        self.buildup_combo = QComboBox()
        self.buildup_combo.addItems(CONSTANTS.buildup_materials)
        self.buildup_label = QLabel(labels.BUILDUP_TABLE)
        self.radtracer_label = QLabel('Radtracer')
        self.pyshield_label = QLabel('Pyshield')
        self.radtracer_material_label = QLabel(labels.MATERIAL)
        self.radtracer_material_combo = QComboBox()
        self.radtracer_material_combo.addItems(CONSTANTS.base_materials)
        self.new_button = QPushButton('Add', self)
        self.delete_button = QPushButton("Delete")
        
        
        self.attenuation_combo.addItems(CONSTANTS.base_materials)
        self.buildup_combo.addItems(CONSTANTS.buildup_materials)
        
        
    def setValues(self, values):
        super().setValues(values)
        values = values or {}
        if labels.NAME in values.keys()\
            and (values[labels.NAME] == labels.EMPTY_MATERIAL\
                 or values[labels.NAME] in CONSTANTS.base_materials):        
            self.setEnabled(False)
        else:              
            self.setEnabled(True)    
        
    def value_widgets(self):
        if self._value_widgets is None:
            self._value_widgets = super().value_widgets()
            self._value_widgets[labels.DENSITY] = self.density_input
            self._value_widgets[labels.RADTRACER_MATERIAL] = self.radtracer_material_combo
            self._value_widgets[labels.ATTENUATION_TABLE] = self.attenuation_combo
            self._value_widgets[labels.BUILDUP_TABLE] = self.buildup_combo
        return self._value_widgets
            
    def set_callbacks(self):
        super().set_callbacks()
        
        label = labels.DENSITY
        callback = lambda _, label=label: self.value_changed(label)
        self.density_input.valueChanged.connect(callback)
        label = labels.RADTRACER_MATERIAL
        callback = lambda _, label=label: self.value_changed(label)
        self.radtracer_material_combo.currentIndexChanged.connect(callback)
        label = labels.ATTENUATION_TABLE
        callback = lambda _, label=label: self.value_changed(label)
        self.attenuation_combo.currentIndexChanged.connect(callback)
        label = labels.BUILDUP_TABLE
        callback = lambda _, label=label: self.value_changed(label)
        self.buildup_combo.currentIndexChanged.connect(callback)
        
        

    def create_layout(self):
        super().create_layout()
        
        row = self.layout.rowCount() + 1
        
        self.layout.addWidget(self.density_label, row, 0)
        self.layout.addWidget(self.density_input, row, 1)
        
        row += 1
        
        self.layout.addWidget(self.radtracer_label, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.radtracer_material_label, row, 0)
        self.layout.addWidget(self.radtracer_material_combo, row, 1)
        
        
        row += 1
        self.layout.addWidget(self.pyshield_label, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.attenuation_label, row, 0)
        self.layout.addWidget(self.attenuation_combo, row, 1)
        
        row += 1
        
        self.layout.addWidget(self.buildup_label, row, 0)
        self.layout.addWidget(self.buildup_combo, row, 1)
        
        row += 1
        
        self.layout.addWidget(self.new_button, row, 0)
        self.layout.addWidget(self.delete_button, row, 1)
    
    def setEnabled(self, enabled):
        super().setEnabled(enabled)
        self.new_button.setEnabled(True)




class EditPixelSizeView(ModelItemsWidget):  
   
    LABEL = labels.PIXEL_SIZE_CM
    
    explanation =\
("The pixel size can be set by hand or by a measurement on the floor plan " 
 "image. Measurement is done by drawing a line between two points for which "
 "the real world distance in cm is known.")

    def clear(self):
        super().clear()
        with BlockValueChangedSignal(self):
            self.vertices.clear()
            self.physical_distance.clear()
            self.pixel_size.clear()
            self.vertices.clear()
            self.pixel_distance.clear()
            
    def create_widgets(self):
        #self.explanation = QLabel(self.explanation.replace('\n', ' '))
        
        
        self.choose_fixed = QRadioButton("Set Fixed")
        
        self.choose_measured = QRadioButton("Measure")

        
        self.measure_button = QPushButton('Measure On Floorplan')
        
        
        
        self.physical_distance_label = QLabel("Real world distance [cm]")
        self.physical_distance = QDoubleSpinBox(decimals=2)
        self.physical_distance.setRange(-MAX_VALUE, MAX_VALUE)
        
        self.pixel_distance_label = QLabel("Distance [pixels]")
        self.pixel_distance = QLabel("Use Button To Measure")
        
        self.pixel_size_label = QLabel(labels.PIXEL_SIZE_CM)
        self.pixel_size = QDoubleSpinBox(decimals=2)
        self.pixel_size.setRange(-MAX_VALUE, MAX_VALUE)
        
        self.confirm_button = QPushButton("Confirm")
        
        self.choose_fixed.toggled.connect(self.radio_button)
        self.choose_measured.toggled.connect(self.radio_button)
                
        self.vertices = VerticesWidget(self, unit='pixels')
                                      
        
    def set_callbacks(self):
        label = labels.GEOMETRY
        cbk = lambda _, label=label: self.value_changed(label)
        self.choose_fixed.toggled.connect(cbk)
        self.choose_measured.toggled.connect(cbk)
        
        label = labels.REAL_WORLD_DISTANCE_CM
        cbk = lambda _, label=label: self.value_changed(label)
        self.physical_distance.valueChanged.connect(cbk)
        
        label = labels.PIXEL_SIZE_CM
        cbk = lambda _, label=label: self.value_changed(label)
        self.pixel_size.valueChanged.connect(cbk)
        
        label = labels.VERTICES_PIXELS
        cbk = lambda _, label=label: self.value_changed(label)
        self.vertices.valueChanged.connect(cbk)
        
        
    def value_widgets(self):
        if self.choose_fixed.isChecked():
            return {labels.PIXEL_SIZE_CM: self.pixel_size,
                    labels.GEOMETRY: self.choose_fixed}
        
        elif self.choose_measured.isChecked():
            return {labels.REAL_WORLD_DISTANCE_CM: self.physical_distance,
                    labels.VERTICES_PIXELS: self.vertices,
                    labels.GEOMETRY: self.choose_measured,
                    labels.PIXEL_SIZE_CM: self.pixel_size}
    
    def setValue(self, label, value):
        if label == labels.ORIGIN: return
        
        super().setValue(label, value)
        
        if label == labels.VERTICES_PIXELS:            
            vvp = value
            
            d= ((vvp[0][0]-vvp[1][0])**2 + (vvp[0][1] - vvp[1][1])**2)**0.5
            
            safe_set_value_to_widget(self.pixel_distance, round(d,1))
            self.set_pixel_size()
            
        elif label == labels.REAL_WORLD_DISTANCE_CM:
            self.set_pixel_size()
        
            
    def set_pixel_size(self):
        
        try:
            pd = float(safe_get_value_from_widget(self.pixel_distance))
        except ValueError: # self.pixel_distance in initiated as a string
            pd = 0
        
        rwd = safe_get_value_from_widget(self.physical_distance)
        
        if pd > 0 and rwd > 0:
            safe_set_value_to_widget(self.pixel_size, round(rwd/pd, 2))
            
    
    
        
        

    def radio_button(self):        
        if self.choose_measured.isChecked():
            self.set_choose_measured()
        elif self.choose_fixed.isChecked():
            self.set_choose_fixed()
        
    def set_choose_fixed(self):

        self.choose_measured.setChecked(False)
        self.choose_fixed.setChecked(True)
        
        self.measure_button.setEnabled(False)
     
        self.pixel_size_label.setEnabled(True)
        self.pixel_size.setEnabled(True)        
        self.vertices.setEnabled(False)
        
        self.physical_distance_label.setEnabled(False)
        self.physical_distance.setEnabled(False)
        
        self.pixel_distance_label.setEnabled(False)
        self.pixel_distance_label.setEnabled(False)
        
        self.vertices.setEnabled(False)
       
        
    def set_choose_measured(self):

        self.choose_measured.setChecked(True)
        self.choose_fixed.setChecked(False)
        self.measure_button.setEnabled(True)
        self.physical_distance.setEnabled(True)
        self.pixel_size_label.setEnabled(True)
        self.pixel_size.setEnabled(False)
        self.vertices.setEnabled(True)
        self.physical_distance_label.setEnabled(True)
        self.physical_distance.setEnabled(True)
        self.vertices.setEnabled(True)
        
        self.pixel_distance_label.setEnabled(True)
        self.pixel_distance_label.setEnabled(True)
        
        
    def create_layout(self):
        
        row = self.layout.rowCount() + 1
        
        #self.layout.addWidget(self.explanation, row, 0, 1, 2)
        
        #row += 1
        
        self.layout.addWidget(self.choose_fixed, row, 0, 1, 2)

        row += 1
        
        self.layout.addWidget(self.pixel_size_label, row, 0)
        self.layout.addWidget(self.pixel_size, row, 1)
        
        row += 1
        
        self.layout.addWidget(self.choose_measured, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.physical_distance_label, row, 0)
        self.layout.addWidget(self.physical_distance, row, 1)
        
        row += 1
        
        self.layout.addWidget(self.pixel_distance_label, row, 0)
        self.layout.addWidget(self.pixel_distance, row, 1)
        
        row += 1 
        
        self.layout.addWidget(self.vertices, row, 0, 1, 2)
        
        
        row += 1
        
        self.layout.addWidget(self.measure_button, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.confirm_button, row, 0, 1, 2)
        
        row += 1
        
    
        
        self.set_choose_measured()
       
        



       
if __name__ == "__main__":
    from pyrateshield import model_items
    x=Model.load_from_project_file('../../example_projects/SmallProject/project.zip')   
    sequence = x.sources_nm
   
    #sequence.deleteItem(sequence.items[0])
    sequence.items[0].name='test'
    
    x.sources_xray.addItem(model_items.SourceXray())
    x.sources_xray.addItem(model_items.SourceXray())
    app = QApplication([])
    window = QMainWindow()
    widget = EditClearancesView()
    window.setCentralWidget(widget)
    
    #contr = EditShieldingsController(model=x.walls, view=widget)
    #contr = EditShieldingsController(model=x.shieldings, view=widget)
    window.show()    
    app.exec_()


        
