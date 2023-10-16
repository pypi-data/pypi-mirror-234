import matplotlib.pyplot as plt
import qtawesome

from PyQt5.QtWidgets import (QPushButton, QLabel, QCheckBox, QColorDialog,
                             QComboBox, QSpinBox, QDoubleSpinBox, QApplication)
from PyQt5.QtGui import QIcon

from pyrateshield.gui.item_views import EditValueWidget



class View(EditValueWidget):
    def create_widgets(self):        
        self.grid_size = QSpinBox(self)
        self.grid_size.setRange(1, 9999)

        self.cmap_name = QComboBox(self)
        self.cmap_name.addItems(plt.colormaps())
        
        self.vmin = QDoubleSpinBox(self)
        self.vmin.setSingleStep(0.1)
        self.vmax = QDoubleSpinBox(self)
        self.vmax.setSingleStep(0.1)
        self.alpha = QDoubleSpinBox(self)
        self.alpha.setRange(0, 1)
        self.alpha.setSingleStep(0.1)
        self.alpha_gradient = QCheckBox(self)
        
        self.contour_line_widgets = []
        for i in range(5):
            clw = {
                "active": QCheckBox(self),
                "level": QDoubleSpinBox(self, decimals=3),
                "color_str": "",
                "color_btn": QPushButton(self),
                "dashing": QComboBox(self),
                "thickness": QDoubleSpinBox(self),
            }
            clw["color_btn"].setMinimumWidth(50)
            clw["color_btn"].clicked.connect(lambda state, x=i: self.linestyle_btn_callback(x))
            clw["dashing"].addItems(("solid", "dotted", "dashed", "dashdot"))
            
            self.contour_line_widgets.append(clw)
            
        self.legend = QCheckBox("Show legend")
        
        self.save_button = QPushButton('Apply')
        self.close_button = QPushButton('Close')
    
    def linestyle_btn_callback(self, index):
        color = QColorDialog(self).getColor()
        if color.isValid():
            self.set_linestyle_color(index, color.name())
            
    def set_linestyle_color(self, index, color):
        self.contour_line_widgets[index]["color_btn"].setStyleSheet('background-color: %s' % color)
        self.contour_line_widgets[index]["color_str"] = color
    
    def create_layout(self):            
        self.setWindowTitle('Dosemap style')
        icon = icon = qtawesome.icon('mdi.palette')
        self.setWindowIcon(QIcon(icon))
        
        row = 0
        
        label = QLabel('Dose map resolution')
        label.setStyleSheet('font-weight: bold')
        self.layout.addWidget(label, row, 0)
        
        row += 1
        
        self.layout.addWidget(QLabel('Matrix size:'), row, 0)
        self.layout.addWidget(self.grid_size, row, 1)
        
        row += 1
        
        text = "The dose map is calculated on an NxM grid, superimposed on "\
               "the current view of the project. This parameter is used to "\
               "specify the number of columns, which automatically fixes the "\
               "number of rows through the aspect ratio of the view. A higher "\
               "value (>200) results in a better looking dose map but may "\
               "cause longer computtion times, most notable for large projects."
        
        label = QLabel(text)
        label.setWordWrap(True)
        self.layout.addWidget(label, row, 0, 1, 4)        
        
        row += 1
        self.interpolate = QCheckBox('Interpolate dosemap to floorplan (slower)')
        self.layout.addWidget(self.interpolate, row, 0, 1, 4)
        
        row += 1
        self.multi_cpu = QCheckBox('Use multi cpu (disable when having issues!)')
        self.layout.addWidget(self.multi_cpu)
        
        row += 1
        self.layout.addWidget(QLabel(''), row, 0)
        
        row += 1
                
        label = QLabel('Heat map')
        label.setStyleSheet('font-weight: bold')
        self.layout.addWidget(label, row, 0)
        
        row += 1
        
        self.layout.addWidget(QLabel('Color map:'), row, 0)
        self.layout.addWidget(self.cmap_name, row, 1)
        
        row += 1
        
        self.layout.addWidget(QLabel('Vmin:'), row, 0)
        self.layout.addWidget(self.vmin, row, 1)
        
        row += 1
        
        self.layout.addWidget(QLabel('Vmax:'), row, 0)
        self.layout.addWidget(self.vmax, row, 1)
        
        row += 1
        
        self.layout.addWidget(QLabel('Alpha:'), row, 0)
        self.layout.addWidget(self.alpha, row, 1)
        
        row += 1
        
        self.layout.addWidget(QLabel('Alpha gradient:'), row, 0)
        self.layout.addWidget(self.alpha_gradient, row, 1)
                        
        row += 1
        self.layout.addWidget(QLabel(''), row, 0)
        
        row += 1
        label = QLabel('Contour lines')
        label.setStyleSheet('font-weight: bold')
        self.layout.addWidget(label, row, 0)
        
        row += 1
        self.layout.addWidget(QLabel('Level'), row, 0)
        self.layout.addWidget(QLabel('Style'), row, 1)
        self.layout.addWidget(QLabel('Color'), row, 2)
        self.layout.addWidget(QLabel('Thickness'), row, 3)
        self.layout.addWidget(QLabel('Show'), row, 4)
        
        for i, clw in enumerate(self.contour_line_widgets):
            row += 1
            
            self.layout.addWidget(clw["level"], row, 0)
            self.layout.addWidget(clw["dashing"], row, 1)
            self.layout.addWidget(clw["color_btn"], row, 2)
            self.layout.addWidget(clw["thickness"], row, 3)
            self.layout.addWidget(clw["active"], row, 4)
        
        row += 1
        
        self.layout.addWidget(self.legend)
        
        row += 1
        
        self.layout.addWidget(self.save_button, row, 0)
        self.layout.addWidget(self.close_button, row, 1)

        

class Controller:

    def __init__(self, model, parent=None):
        self.model = model        
        self.view = View()
        self.parent = parent
        
        self.view.grid_size.setValue(self.model.dosemap.grid_matrix_size)        
                
        value = self.view.cmap_name.findText(self.model.dosemap_style.cmap_name)
        self.view.cmap_name.setCurrentIndex(value)
        
        self.view.vmin.setValue(self.model.dosemap_style.vmin)
        self.view.vmax.setValue(self.model.dosemap_style.vmax)
        self.view.alpha.setValue(self.model.dosemap_style.alpha)
        self.view.alpha_gradient.setChecked(self.model.dosemap_style.alpha_gradient)
        self.view.interpolate.setChecked(self.model.dosemap_style.interpolate)
        self.view.multi_cpu.setChecked(self.model.dosemap_style.multi_cpu)
        
        for i, clw in enumerate(self.view.contour_line_widgets):
            if i < len(self.model.dosemap_style.contour_lines):
                cl = self.model.dosemap_style.contour_lines[i]
                level, color, dashing, thickness, active = cl
            else:
                level, color, dashing, thickness, active = (1.0, "black", "solid", 1.5, False)
                    
            clw["level"].setValue(level)
            self.view.set_linestyle_color(i, color)
            clw["dashing"].setCurrentIndex( clw["dashing"].findText(dashing) )
            clw["thickness"].setValue(thickness)
            clw["active"].setChecked(active)
        
        self.view.legend.setChecked(self.model.dosemap_style.show_legend)
        
        
        self.view.save_button.clicked.connect(self.apply)
        self.view.close_button.clicked.connect(self.view.close)
        
        
    
    def apply(self):
        cur_grid_size = self.model.dosemap.grid_matrix_size
        self.model.dosemap.grid_matrix_size = self.view.grid_size.value()
        self.model.dosemap_style.cmap_name = self.view.cmap_name.currentText()
        self.model.dosemap_style.vmin = self.view.vmin.value()
        self.model.dosemap_style.vmax = self.view.vmax.value()
        self.model.dosemap_style.alpha = self.view.alpha.value()
        self.model.dosemap_style.alpha_gradient = bool(self.view.alpha_gradient.checkState())
        self.model.dosemap_style.show_legend = self.view.legend.isChecked()
        self.model.dosemap_style.interpolate = self.view.interpolate.isChecked()
        self.model.dosemap_style.multi_cpu = self.view.multi_cpu.isChecked()
        contour_lines = []
        for i, clw in enumerate(self.view.contour_line_widgets):
            contour_lines.append([
                    clw["level"].value(),
                    clw["color_str"],
                    clw["dashing"].currentText(),
                    clw["thickness"].value(),
                    bool(clw["active"].checkState()),
                ])        
        self.model.dosemap_style.contour_lines = contour_lines
        self.parent.graphics().viewport().update()
        

if __name__ == "__main__":
    app = QApplication([])
    from pyrateshield.model import Model
    project = '../../example_projects/SmallProject/project.zip'

    model = Model.load_from_project_file(project)
    controller = Controller(model)
    window = controller.view
    window.show()    
    app.exec_()
    
    
    
    
