import os
import yaml
import qtawesome
import math

from functools import partial


from PyQt5.QtWidgets import QToolBar, QMainWindow, QApplication
from PyQt5.QtCore import Qt, pyqtSignal, QPointF
from PyQt5.QtGui import QIcon

from pyrateshield import labels, __pkg_root__
from pyrateshield.gui.graphics_items import ZoomRect,  Marker








class ToolbarController():
     item_to_move = None
     _zoomRect = None
     def __init__(self, view=None, model=None, parent=None):
         self.parent = parent
         self.view = view
         self.model = model
         self.graphics = self.parent.view.views[labels.CANVAS]
         
         
         self.set_callbacks()
    
     def set_callbacks(self):
         self.view.buttonClick.connect(self.toolbar_cbk)
         self.graphics.leftMouseClick.connect(self.leftClick)
         self.graphics.mouseMove.connect(self.mouseMove)
         self.graphics.mouseRelease.connect(self.mouseRelease)
        
        
     def leftClick(self, event, item):
         scene_pos = self.graphics.mapToScene(event.pos())
         pos_cm = self.model.floorplan.geometry.pixel_point_to_cm(scene_pos)
         self.click_pos = scene_pos
         if self.view.selected_tool() in (labels.SOURCES_NM,
                                          labels.SOURCES_CT,
                                          labels.SOURCES_XRAY,
                                          labels.CRITICAL_POINTS,
                                          labels.WALLS,
                                          labels.RULERS):
                                          
             
             
             self.new_model_item(pos_cm, self.view.selected_tool())
             
             
         elif self.view.selected_tool() == self.view.ZOOM:      
                  
            self.item_to_move = ZoomRect(scene_pos)
            self.graphics.scene().addItem(self.item_to_move)
            
         elif self.view.selected_tool() == Toolbar.SELECT:
            self.item_to_move = ZoomRect(scene_pos)
            self.graphics.scene().addItem(self.item_to_move)
            
    
     def mouseMove(self, event):
         scene_pos = self.graphics.mapToScene(event.pos())
         
         
         if self.item_to_move is not None:
             if isinstance(self.item_to_move, Marker):
                 if  event.modifiers() == Qt.ControlModifier:
                     pos_adjecent = self.item_to_move.adjecentMarker().pos()
                     dx = abs(pos_adjecent.x() - scene_pos.x())
                     dy = abs(pos_adjecent.y() - scene_pos.y())
                     if dx >= dy:
                         scene_pos.setY(pos_adjecent.y())
                     else:
                         scene_pos.setX(pos_adjecent.x())
                  
                 self.item_to_move.setPos(scene_pos)
                 
             elif isinstance(self.item_to_move, ZoomRect):                 
                 self.item_to_move.setPoint(scene_pos)
      
     
     def mouseRelease(self, event):      
        self.mouseMove(event)
        if self.view.selected_tool() == Toolbar.ZOOM:
            self.finishZoom()   
        elif self.view.selected_tool() == Toolbar.SELECT:
            self.finishSelect()
            
            
        self.item_to_move = None
        self.graphics.setCursor(Qt.ArrowCursor)
        
     def finishSelect(self):
         selection = self.item_to_move.rect
       
         for item in self.graphics.scene().itemsInRect(selection):
             item.setSelected(True)
         self.graphics.scene().removeItem(self.item_to_move)
         self.view.uncheck_all()          
         
            
     def finishZoom(self):      

        self.graphics.setZoomRect(self.item_to_move.rect)
        self.graphics.scene().removeItem(self.item_to_move)  
        
        self.view.uncheck_all()          
            
         
     def show_dosemap(self, engine):
        
         self.model.dosemap.engine = engine
         
         
         dosemap = self.parent.dosemapper.get_dosemap(self.model)
      
         
         if dosemap is None:
             print('No dosemap could be calculated. Possibly no sources defined or all sources are disabled!')
         else:             
             self.graphics.scene().dosemap().setDosemap(dosemap)
         self.parent.graphics().viewport().update()
         
            
     
         
             
     def delete(self):                
        items = self.graphics.scene().selectedGraphicsModelItems()
        self.model.delete_items([item.model for item in items])
         
        
     def toolbar_cbk(self, item):     
         if item == Toolbar.PYSHIELD:
             self.show_dosemap(labels.PYSHIELD)
         elif item == Toolbar.RADTRACER:
             self.show_dosemap(labels.RADTRACER)
         elif item == Toolbar.RESET:
             self.graphics.resetZoom()
         elif item == labels.FLOORPLAN:
              self.graphics.refresh()
         elif item == Toolbar.DELETE:
             self.delete()
         elif item == Toolbar.ALL:
            self.graphics.scene().selectAll()
         elif item == Toolbar.CLEAR:
            self.graphics.scene().deselectAll()
         elif item == Toolbar.UNDO:
            self.model.history.undo()
         elif item == Toolbar.REDO:
            self.model.history.redo()
         
             
             
     def refresh(self):
        self.graphics.refresh()
        
     # def mouse_pos_to_pixels(self, pos):
     #      return self.graphics.mapToScene(pos)
         
         
     # def mouse_pos_to_cm(self, pos):
     #     geometry = self.model.floorplan.geometry        
     #     #pos = self.mouse_pos_to_pixels(pos)
     #     pos_cm = geometry.pixels_to_cm([pos.x(), pos.y()])
     #     return pos_cm
    
     def new_model_item(self, pos_cm, item_label, interactive=True):
        # copy values of item that are currently in view to new model

        
        pos_pixels = self.model.floorplan.geometry.cm_to_pixel_point(pos_cm)
        sequence = self.model.get_attr_from_label(item_label)
        
        if item_label == labels.RULERS:
            item_model = sequence.item_class()
        else:
            current_item = self.parent.controllers[item_label].item_in_view()

            if current_item is None:            
                item_model = sequence.item_class()
            else:
                item_model = sequence.item_class.from_dict(current_item.to_dict()) 
            

        if item_label == labels.WALLS:     
            item_model.closed = False
            
            controller = self.parent.controllers[labels.SHIELDINGS]
            shielding = controller.item_in_view()
            if shielding is not None:
                item_model.shielding = shielding.name
            item_model.vertices = [pos_cm, pos_cm]
            
            
            
        elif item_label == labels.RULERS:
            item_model.vertices_pixels = [[pos_pixels.x(), pos_pixels.y()],
                                          [pos_pixels.x(), pos_pixels.y()]]
           
            

        else:            
            item_model.name = item_model.default_name
            item_model.position = pos_cm     
                   
       
            
        sequence.addItem(item_model)
        
        # Style item as selected        
        pixel_item = self.graphics.pixel_item_for_model_item(item_model)  
        pixel_item.updateStyle()
        
        self.graphics.scene().deselectAll()
        
        if item_label in (labels.WALLS, labels.RULERS):
            
            pixel_item.markers()[1].setSelected(False)
            pixel_item.markers()[0].setSelected(False)
        else:
            pixel_item.setSelected(False)
       
        
        if interactive:                      
            if item_label in (labels.WALLS, labels.RULERS):
                self.item_to_move = pixel_item.markers()[1]
               
            else:
                pass
        self.view.uncheck_all()
                # self.mouse._point_setter = pixel_item.setCenterPoint    

class Toolbar(QToolBar):
    buttonClick = pyqtSignal(str)
    # only display the buttons we need
    # EVENT_TOOLBUTTON_CLICK = 'event_toolbutton_click'
    _toolbutton_style = Qt.ToolButtonTextUnderIcon
    
    # explicit naming to easily catch events

    NEW = 'New'
    IMAGE = 'Image'
    
    SEPERATOR = 'Seperator'
    RESET = 'Reset'
    
    ZOOM = 'Zoom'
    SELECT = 'Select'
    ALL = 'All'
    CLEAR = 'Clear'
    
    UNDO = 'Undo'
    REDO = 'Redo'
    
    
    DELETE = 'Del'
    SNAPSHOT = 'Snap'
    LOAD = 'Load'
    SAVE = 'Save'
    SAVE_AS = 'Save As'
    CALCULATOR = 'Calc'
    
    DOSEMAP_STYLE = 'Style'    
    ISOTOPES = 'Isotopes'
    FLOORPLAN = 'Floorplan'
    CRITICAL_POINT = 'Point'
    SOURCE_NM = 'NM'
    SOURCE_CT = 'CT'
    SOURCE_XRAY = 'Xray'
    RULER = 'Ruler'
    WALL = 'Wall'
    PYSHIELD = 'pyShield'
    RADTRACER = 'Radtracer'
    
    # Use shorter names to display in GUI when clicked return the name 
    # used throughout pyrateshield
    tool_name_map = {DOSEMAP_STYLE: labels.DOSEMAP_STYLE,
                     ISOTOPES: labels.ISOTOPES,
                     FLOORPLAN: labels.FLOORPLAN,
                     CRITICAL_POINT: labels.CRITICAL_POINTS,
                     SOURCE_NM:  labels.SOURCES_NM,
                     SOURCE_CT: labels.SOURCES_CT,
                     WALL: labels.WALLS,
                     PYSHIELD: labels.PYSHIELD,
                     RADTRACER: labels.RADTRACER,
                     SOURCE_XRAY: labels.SOURCES_XRAY,
                     RULER: labels.RULERS}

    def __init__(self):
        QToolBar.__init__(self)
      
        
        self.setToolButtonStyle(self._toolbutton_style)
        #self.setStyleSheet("border-bottom: 0px; border-top: 0px;")
        self.populate_toolbar()
        
    def get_layout(self):
        try:
            folder = os.path.split(__file__)[0]
        except:
            folder = os.getcwd()
            
        file = os.path.join(folder, 'toolbar.yml')
        return yaml.safe_load(open(file))
        
    def enable_tool(self, label, enable):
        self._actions[label].setEnabled(enable)
    
    
    def populate_toolbar(self):
        layout = self.get_layout()
        self._actions = {}
        self._checkable_tools = []
        for item in layout:
            if item[labels.LABEL] == self.SEPERATOR:
                self.addSeparator()
            else:
                icon = self.icon(item[labels.ICON])
                action = self.addAction(icon, item[labels.LABEL])
                action.setToolTip(item[labels.TOOILTIP])                
                action.setCheckable(item[labels.CHECKABLE])
                if item[labels.CHECKABLE]:
                    self._checkable_tools += [item[labels.LABEL]]
                    cbk = partial(self.checkable_tool_clicked, action)
                    action.triggered.connect(cbk)
                else:
                    cbk = partial(self.emit, item[labels.LABEL])
                    action.triggered.connect(cbk)
                self._actions[item[labels.LABEL]] = action
    
        
    def checkable_tool_clicked(self, clicked_action):
       
        for action in self._actions.values():
            if action is clicked_action:
                continue
            action.setChecked(False)
            
        
                
    def icon(self, name):
        if name == 'icon':
           
            icon = QIcon(os.path.join(__pkg_root__, 'gui', 'icon.png'))
        else:
            icon = qtawesome.icon(name)
        return icon
    
    def emit(self, tool_name):

        if tool_name in self._checkable_tools:
            self.uncheck_all(except_tool=tool_name)
        else:
            self.uncheck_all()
        
        tool_name = self.tool_name_map.get(tool_name, tool_name)
            
        self.buttonClick.emit(tool_name)
        
   
    def selected_tool(self):
        for tool_name in self._checkable_tools:
            widget = self.widgetForAction(self._actions[tool_name]) 
            if widget.isChecked():
                return self.tool_name_map.get(tool_name, tool_name)
        

    def uncheck_all(self, except_tool=None):        
        for tool_name in self._checkable_tools: 
      
            if tool_name == except_tool:
                continue
            
            action = self._actions[tool_name]
            if action.isChecked():
                action.setChecked(False)

    
    

if __name__ == '__main__':
    app = QApplication([])
    
    
    project = '../example_projects/SmallProject/project.zip'

    
    window = QMainWindow()
    toolbar = Toolbar()
    
    window.addToolBar(toolbar)
    toolbar.actions()[-11].setChecked(True)
    toolbar.actions()[-11].setChecked(False)

    

    
    window.show()
    app.exec_()
    