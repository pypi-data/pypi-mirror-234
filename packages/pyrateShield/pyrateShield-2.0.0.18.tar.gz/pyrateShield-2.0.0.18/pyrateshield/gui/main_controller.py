from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QObject, QEvent

from pyrateshield.model import Model
from pyrateshield.dosemapper import Dosemapper
from pyrateshield.model_items import Wall, ModelItem, Ruler

from pyrateshield.gui import io, calculator, dosemap_style, isotopes
from pyrateshield.gui.main_view import MainView, TOOLBOX_LAYOUT
from pyrateshield.gui.graphics_items import  GraphicsModelItem, WallMarker
from pyrateshield.gui.toolbar import ToolbarController
from pyrateshield.gui.context_menu import ContextMenuController
from pyrateshield.gui.critical_point_controller import CriticalPointReportController
from pyrateshield.gui.toolbar import Toolbar
from pyrateshield.gui.item_controllers import (EditModelItemsController, 
                                               EditSourcesNMController,                                               
                                               EditWallsController, 
                                               EditClearancesController, 
                                               EditShieldingsController,
                                               EditPixelSizeController,
                                               EditMaterialsController)
                                               
                                                                                              
from pyrateshield import labels


class MainController():
    _mpl_controller = None
    _critical_points_controller = None
    _calculator = None
    _dosemap_style = None
    _old_status2_msg = None
    model = None
    
    
    def __init__(self, dosemapper=None, model=None, view=None):
        
        if dosemapper is None:
            dosemapper = Dosemapper(multi_cpu=False)
        
        if model is None:
            model = self.get_empty_model()
    
        if view is None:
            view = MainView()
        
        self.last_selected_item = None
        
        self.dosemapper = dosemapper
        self.view = view
        self.model=model
        
        self.controllers = self.create_controllers()

        self.connect_model()
        
        self.set_view_callbacks()

        self.controllers[labels.SHIELDINGS].view.setEnabled(True)
        
        self.graphics().scene().updateStyles()
        
        self.graphics().mouseMove.connect(self.updateMousePosition)
        
        self.model.history.reset()
        
        self.dosemapper.progress.connect(self.set_progress)
        self.dosemapper.calculation_time.connect(self.calculation_time)
        self.dosemapper.interpolate.connect(self.interpolate_msg)
        
    def set_progress(self, value):
        value = int(round(value*100))
        value = max(0, value)
        value = min(value, 100)
        self.view.progress.setValue(value)
        self.view.progress.update()
        
    def interpolate_msg(self, interpolating):
        if self._old_status2_msg is None:
            self._old_status2_msg = self.view.status_label2.text()
        if interpolating == -1:
            self.view.status_label2.setText('Interpolating.....')
        else:
            time = round(interpolating, 1)
            if time == 0:
                time = '< 0.1'
            new_msg = self._old_status2_msg
            new_msg += f' | Interpolation time: {time} s'
            self.view.status_label2.setText(new_msg)
            self._old_status2_msg = None
        
    def calculation_time(self, time):
        time = round(time, 1)
        if time == 0:
            time = '< 0.1'
        self.view.status_label2.setText(f'Calculation time: {time} s')
        
    def updateMousePosition(self, event):
        pos = self.graphics().mapToScene(event.pos())
        psize = self.model.get_pixel_size_cm()
        
        x = round(pos.x() * psize, 1)
        y = round(pos.y() * psize, 1)
        
        text = f'Mouse position [cm]: {x}, {y}'
        
        self.view.status_text = text
        

    def graphics(self):
        return self.view.views[labels.CANVAS]
        
    def disconnect_model(self):
        for key, controller in self.controllers.items():           
            controller.disconnect_model()
            
    def set_model(self, model):     
        self.view.clear()              
        self.disconnect_model()
        self.model = model
        self.connect_model()
        
    def connect_model(self):           
        self.graphics().setModel(self.model)
        self.toolbar_controller.model = self.model
        for key, controller in self.controllers.items():
            model = self.model.get_attr_from_label(key)
            controller.set_model(model)
   
        
        self.context_menu_controller.set_model(self.model)
        self.crit_point_controller.set_model(self.model)
        item = None
        if len(self.model.sources_nm) > 0:
            item = self.model.sources_nm[0]
        elif len(self.model.sources_ct) > 0:
            item = self.model.sources_ct[0]
        elif len(self.model.sources_xray) > 0:
            item = self.model.sources_xray[0]
        elif len(self.model.critical_points) > 0:
            item = self.model.critical_points[0]
        elif len(self.model.walls) > 0:
            item = self.model.walls[0]
        if item is not None:
            self.select_item(item)
            
        
    def itemChanged(self, *args, **kwargs):
        pass
   

    def set_view_callbacks(self):
        for label, tab in self.view.toolbox_tabs.items():            
            if len(TOOLBOX_LAYOUT[label]) > 1:                
                tab.currentChanged.connect(self.tab_selected)
                
        self.view.toolbox.currentChanged.connect(self.toolbox_selected)
       
       
        self.view.toolbar.buttonClick.connect(self.toolbar_callback)
        
        #self.graphics().scene().selectionChanged.connect(self.graphics_selection_changed)
        
        self.graphics().leftMouseClick.connect(self.select_by_mouse)
        
        
    def select_by_mouse(self, _, item):
        self.select_item(item)

    def select_item(self, item):   
        # if isinstance(item, Marker):
        #     item = item.parentItem()
            
        if isinstance(item, GraphicsModelItem):
            item = item.model

        if isinstance(item, Wall):
            self.view.set_focus(labels.WALLS)                            
            self.controllers[labels.WALLS].item_to_view(item)
            
        elif isinstance(item, WallMarker):
            controller = self.controllers[labels.WALLS]
            wall = item.parentItem().model
            
            if wall is not controller.item_in_view():
                controller.item_to_view(wall)
            
        
            index = item.parentItem().markers().index(item)
            
            controller.set_vertex_index(index)
            
            
            item.scene().silentSelectItem(item)
            
            
            self.view.set_focus(labels.WALLS)             
            
        elif isinstance(item, ModelItem) and not isinstance(item, Ruler):        
            self.view.set_focus(item.label)
            self.controllers[item.label].item_to_view(item)            
        

      
    @property
    def controller_types(self):
        return {
                labels.SOURCES_CT:        EditModelItemsController,
                labels.SOURCES_XRAY:      EditModelItemsController,
                labels.SOURCES_NM:        EditSourcesNMController,
                labels.CLEARANCE:         EditClearancesController,
                labels.WALLS:             EditWallsController,
                labels.SHIELDINGS:        EditShieldingsController,
                labels.CRITICAL_POINTS:   EditModelItemsController,
                labels.PIXEL_SIZE_CM:     EditPixelSizeController,
                labels.MATERIALS:         EditMaterialsController}       

        
    def create_controllers(self):
        # FIX!: dosemapper=self.dosemapper,
        
        view = self.view.views[labels.CANVAS]
        
    
        
        self.toolbar_controller = ToolbarController(view=self.view.toolbar,
                                                    model=self.model,
                                                    parent=self)
                                                  
        
        self.context_menu_controller = ContextMenuController( 
            model=self.model, view=self.graphics(), parent=self)
        
        view = self.view.views[labels.CRITICAL_POINT_REPORT_VIEW]
        self.crit_point_controller = CriticalPointReportController(
            view=view, model=self.model, 
            controller=self, dosemapper=self.dosemapper)
        
    
        controllers = {}
        for key in self.controller_types.keys():
                    # labels.CRITICAL_POINTS, labels.PIXEL_SIZE_CM, 
                    #  labels.MATERIALS):
           
            contr_type = self.controller_types[key]
            view = self.view.views[key]
            model = self.model.get_attr_from_label(key)
            controllers[key] = contr_type(model = model, 
                                          view = view,
                                          parent = self)
            
        
                                         
        return controllers

            
    def toolbox_selected(self, _=None):
        self.tab_selected()
        
        
    def tab_selected(self, index=None):        
        label = self.view.get_active_tool_panel_name()
        self.view.focusSet.emit(label)
        
    def toolbar_callback(self, toolname):
        if toolname == Toolbar.SAVE_AS:
            self.save_as()
        elif toolname == Toolbar.LOAD:
            self.load()
        elif toolname == Toolbar.SAVE:
            self.save()
        elif toolname == Toolbar.IMAGE:
            self.load_image()
        elif toolname == Toolbar.NEW:
            self.new()
        elif toolname == Toolbar.CALCULATOR:
            self.show_calculator()
        elif toolname == labels.DOSEMAP_STYLE:
            self.show_dosemap_style()
        elif toolname == Toolbar.SNAPSHOT:
            self.snapshot()
        elif toolname == Toolbar.ISOTOPES:
            self.show_isotopes()
           
    def snapshot(self):
        file = io.ask_new_image_file('Save snapshot to disk')
        if file is not None:
          
            
            viewport = self.view.views[labels.CANVAS].viewport()
            pixmap = QtGui.QPixmap(viewport.size())
            painter = QtGui.QPainter(pixmap)
            viewport.render(painter)
            painter.end()
            
            pixmap.save(file)
            
            
    def load_image(self):
       image = io.safe_load_image()
       if image is not None:
           
           # Load floorplan and reset pixel size (geometry)
           self.model.floorplan.image = image                                                    
           self.view.set_focus(labels.PIXEL_SIZE_CM)
           
    def new(self):        
        confirm = io.confirm_new_project()
        if confirm:
            self.set_model(self.get_empty_model())
        self.view.set_focus(labels.SOURCES_NM)
        
            
    def save(self):
        io.safe_write_model(model=self.model, 
                                        filename=self.model.filename)
            
    def save_as(self):
        io.safe_write_model(model=self.model)
               
    def load(self):
        model = io.safe_load_model(self.model.filename)        
        if model is not None:
            self.set_model(model)
               
    def show_calculator(self):
        self._calculator = calculator.Controller()
        self._calculator.view.show()
    
    def show_dosemap_style(self):
        self._dosemap_style = dosemap_style.Controller(self.model,
                                                       parent=self)
        self._dosemap_style.view.show() 
        
    def show_isotopes(self):
        self._isotopes = isotopes.Controller()
        self._isotopes.view.show()
        self._isotopes.view.resize(500, 300)
        
        
    def get_empty_model(self):
        model = Model()
        model.floorplan.geometry.origin = labels.TOP_LEFT
        return model

def main(model=None, controller=None, dm=None):
        app = QApplication([])
        
        controller = MainController(model=model, dosemapper=dm)
        window = controller.view
        window.show()    
        app.exec_()
      
if __name__ == "__main__":  
    project = '../../example_projects/SmallProject/project.zip'
    project = '../../example_projects/LargeProject/project.zip'
    #project = '/Users/marcel/Downloads/T1 NG_20230828_Self-shielding pt 20cm water_All Sources On_v12.zip'
    #model = Model.load_from_project_file(project)
    #file = 'C:/Users/r757021/Desktop/test.zip'
    model = Model.load_from_project_file(project)
    #model = Model()
    
    app = QApplication([])
    dosemapper = Dosemapper(multi_cpu=True)
    #controller = MainController(model=Model(), dosemapper=None)
    controller = MainController(model=model, dosemapper=dosemapper)

    window = controller.view
    window.show()    
    
    # global_event_filter = GlobalEventFilter(model=controller.model)
    # app.installEventFilter(global_event_filter)
    
    # model = Model.load_from_project_file(project)
    app.exec_()
    
    
