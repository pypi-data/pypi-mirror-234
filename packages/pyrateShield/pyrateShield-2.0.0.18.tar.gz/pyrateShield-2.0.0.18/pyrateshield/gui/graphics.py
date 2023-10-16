from functools import partial

from PyQt5.QtWidgets import  (QApplication, QGraphicsView,  
                              QMainWindow, QGraphicsScene)

from PyQt5.QtGui import QPainter, QTransform
from PyQt5.QtCore import Qt, pyqtSignal, QRectF, QPointF
from pyrateshield.gui.legend import Legend
from pyrateshield.model import Model


from pyrateshield import labels
from pyrateshield.model_items import (Wall, SourceNM, SourceCT, 
                                      SourceXray, CriticalPoint, Ruler)
from pyrateshield.gui.graphics_items import (GraphicsModelItem,                                              
                                             GraphicsSourceNM, 
                                             GraphicsSourceCT, 
                                             GraphicsSourceXray, 
                                             DosemapPixmap,                                             
                                             GraphicsWall, 
                                             GraphicsContourItem,
                                             FloorplanPixmap,
                                             Marker,
                                             Cross,
                                             RulerLine,
                                             GraphicsItem)


        


class GraphicsScene(QGraphicsScene):
    _pixel_size_line = None
    _floorplan = None
    _dosemap = None
    

        
    def _select_all(self, select=True):
       self.blockSignals(True)
       for item in self.graphicsModelItems() + self.markers():
           item.setSelected(select)
       self.blockSignals(False)
       self.selectionChanged.emit()
    
    def removeItem(self, item):
        if item is None or item not in self.items():
            return
        super().removeItem(item)
       
    def addItem(self, item):        
        if isinstance(item, FloorplanPixmap):
            self.removeFloorplan()
        elif isinstance(item, DosemapPixmap):
            self.removeDosemap()
        super().addItem(item)
        
    def silentSelectItem(self, item, deselect_others=True):
        self.blockSignals(True)
        for selected in self.selectedItems():
            if item is not selected:
                selected.setSelected(False)
                
        if item not in self.selectedItems():
             item.setSelected(True)
        self.blockSignals(False)
        #self.selectionChanged.emit()
                
    def sendToForeground(self, item):
        if isinstance(item , Marker):
            item = item.parentItem()
        
        for gitem in self.graphicsModelItems():
            if gitem is item:
                gitem.setZValue(100)
            else:               
                gitem.setZValue(item.style_zvalue())
        
       
                
    
    
    def deselectAll(self):     
        self._select_all(False)
   
    def selectAll(self):
        self._select_all(True)
        
    def floorplan(self):
        items = [item for item in self.items()\
                 if isinstance(item, FloorplanPixmap)]
        if len(items) == 1:
            return items[0]
        if len(items) == 0:
            return None
    
    def dosemap(self):
        items = [item for item in self.items()\
                 if isinstance(item, DosemapPixmap)]
        return None if len(items) == 0 else items[0]
        
    def legend(self):
        items = [item for item in self.items()\
                 if isinstance(item, Legend)]
        return None if len(items) == 0 else items[0]
        
    
    def removeFloorplan(self):
        self.removeItem(self.floorplan())
        
    def removeDosemap(self):
        self.removeItem(self.dosemap())
                
    def removeContours(self):
        for item in self.contourItems():
            self.removeItem(item)
                
    def contourItems(self):
        return [item for item in self.items()\
                if isinstance(item, GraphicsContourItem)]    
            
    def graphicsModelItems(self):
        return [item for item in self.items()\
                if isinstance(item, GraphicsModelItem)]
            
    def walls(self):
        return [item for item in self.items()\
                if isinstance(item, GraphicsWall)]
            
    def markers(self):
        return [item for item in self.items()\
                if isinstance(item, Marker)]
            
    def rulers(self):
        return [item for item in self.items()\
                if isinstance(item, RulerLine)]
                
    def setVisibleGraphicsModelItems(self, visible):
        for item in self.graphicsModelItems():            
                item.setVisible(visible)
    
    def itemsInRect(self, rect):
        return [item for item in self.graphicsModelItems() + self.markers()\
                if self.itemInRect(rect, item)]
            
    def itemInRect(self, rect, item):
        pos = item.pos()
        
        return pos.x() >= rect.left() and pos.x() <= rect.right()\
                and pos.y() <= rect.bottom() and pos.y() >= rect.top()
                
    def selectedGraphicsModelItems(self):   
        selected=set()
        for item in self.selectedItems():
            if isinstance(item, Marker):
                item = item.parentItem()
            if isinstance(item, GraphicsModelItem):
                selected.add(item)
        return list(selected)
                
                
    def updateStyles(self):
        for item in self.graphicsModelItems() + self.contourItems():
            item.updateStyle()
            
            
    def sceneUnitsToPoints(self, scene_units):
        dpi = QApplication.desktop().physicalDpiX()
        
        scale_factor = self.width() / self.sceneRect().width()
            
        pixels = scene_units * scale_factor
        
        points = pixels * 72 / dpi
        return points
    
    def pointsToSceneUnits(self, points):
        dpi = QApplication.desktop().physicalDpiX()
        
        # Convert points to pixels
        pixels = points * dpi / 72.0
    
       
        scale_factor = self.width() / self.sceneRect().width()
        
        
    
        # Convert pixels to scene units
        scene_units = pixels / scale_factor
        return scene_units
    
    

class Graphics(QGraphicsView):
    mouse_press_point = None
    _dosemap = None
    _zoomRect = None
    _ctrl_pressed = False


    leftMouseClick      = pyqtSignal(object, object)
    rightMouseClick     = pyqtSignal(object, object)
    mouseMove           = pyqtSignal(object)
    mouseRelease        = pyqtSignal(object)
    askTooltip          = pyqtSignal(object)
    
    

    pixel_item_class_map = {SourceNM:       GraphicsSourceNM,
                            SourceXray:     GraphicsSourceXray,
                            SourceCT:       GraphicsSourceCT,
                            CriticalPoint:  Cross,
                            Wall:           GraphicsWall,
                            Ruler:          RulerLine}
    
        
    def __init__(self, model=None, scene=None, parent_controller=None):
        if model is None:
            model = Model()
        
        if scene is None:
            scene = GraphicsScene()
                    
        super().__init__(scene)
        
        

        self.setRenderHints(QPainter.HighQualityAntialiasing)
        self.setModel(model)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.scene().selectionChanged.connect(self.selection_changed)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        
        self.last_clicked_item = None
    
    def ctrlPressed(self):
        return self._ctrl_pressed
    
    def selection_changed(self):
       
        self.model.history.clean()
        
    def visibleRect(self):
        return self.mapToScene(self.viewport().rect()).boundingRect()
    
    def selectedModelItems(self):
        items = self.scene().selectedItems()
        
        points = [item.model for item in items\
                  if not isinstance(item, Marker)]
            
        lines = []
        for item in items:
            if isinstance(item, Marker):
                if item.parent_line not in lines:
                    lines += [item.parent_line.model]
                        
        return self.model.sort_model_items(points + lines)
    
    def wheelEvent(self, event):
        if event.modifiers() != Qt.ControlModifier: return
        zoom_in_factor = 1.05
        zoom_out_factor = 0.95
        zoom_steps = 10

        angle = event.angleDelta().y() / 8
        steps = angle / 15

        if steps > 0:
            for _ in range(zoom_steps):
                zoom_factor = self.zoomFactor() * zoom_in_factor
        else:
            for _ in range(zoom_steps):
                zoom_factor = self.zoomFactor() * zoom_out_factor
        
        zoom_factor = max(0.1, min(zoom_factor, 50.0))
        
        self.setTransform(QTransform().scale(zoom_factor, zoom_factor))

        if steps < 0 and  self.visibleRect().contains(self.sceneRect()):
            self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)
        
        self.zoomChanged()
    
    def mouseMoveEvent(self, event):
        self.mouseMove.emit(event)
        super().mouseMoveEvent(event)
        
    def mouseReleaseEvent(self, event):    
        self.mouseRelease.emit(event)

        super().mouseReleaseEvent(event)
        self.model.history.clean()
        self.mouse_press_point = None
    
    def mousePressPoint(self):
        if self.mouse_press_point is not None:
            return self.mouse_press_point
        else:
            return QPointF()
    
    def selectionToModel(self):        
        for item in self.scene().selectedGraphicsModelItems():  
               item.graphicsPositionToModel()
        
    def mousePressEvent(self, event):
        self.mouse_press_point = self.mapToScene(event.pos())
        self.last_clicked_item
        
        item = self.itemAt(event.pos())
        
        for scene_item in self.scene().graphicsModelItems():
            if scene_item is item or item is None:
                continue
            
            if item.zValue() == 100:

                item.updateStyle()
            
            if item.zValue() > 50:
                raise 
                
        if event.button() == 1:  # Left mouse button
            self.leftMouseClick.emit(event, item)
                           
        elif event.button() == 2:  # Right mouse button
            self.rightMouseClick.emit(event, item)
        
        super().mousePressEvent(event)
        
        
    def setModel(self, model):                  
        self.model = model
        

        for sequence in (self.model.sources_nm,
                         self.model.sources_ct,
                         self.model.sources_xray,
                         self.model.critical_points,
                         self.model.walls,
                         self.model.rulers):
            
            cbk = partial(self.model_item_about_to_be_removed, sequence)
            sequence.rowsAboutToBeRemoved.connect(cbk)
            
            cbk = partial(self.model_item_inserted, sequence)
            sequence.rowsInserted.connect(cbk)
        
        cbk = self.refresh
        self.model.floorplan.update_event.connect(self.refresh)
        
        self.refresh()
    
   
    
    def refresh(self, _=None):
        self.model.dosemap.result = None        
        self.scene().clear()
        
        floorplan = FloorplanPixmap(model=self.model.floorplan)
        self.scene().addItem(floorplan)
        
        dosemap = DosemapPixmap(style=self.model.dosemap_style)                               
        self.scene().addItem(dosemap)
        
        self.create_pixel_items()
        self.scene().updateStyles()
        self.resetZoom()
        
        
    def model_item_inserted(self, sequence, index):
        model_item = sequence.itemAtIndex(index)
       
        self.create_pixel_item(model_item, select=True)

    def model_item_about_to_be_removed(self, sequence, index):

        model_item = sequence.itemAtIndex(index)
        
        pixel_item = self.pixel_item_for_model_item(model_item)
        
        if pixel_item is self.last_clicked_item:
            self.last_clicked_item = None
       
        if pixel_item is not None:            
            self.scene().removeItem(pixel_item)        
            del pixel_item
            
        
    def floorplan_update(self, event_data):
        pass
           

    
    def pixel_item_for_model_item(self, model_item):
        if isinstance(model_item, GraphicsModelItem):
            return model_item
        
        for pixel_item in self.scene().graphicsModelItems():                                       
            if pixel_item.model is model_item:
                return pixel_item


    def create_pixel_items(self):
        for model_item in [*self.model.sources_nm,
                           *self.model.sources_ct,
                           *self.model.sources_xray,
                           *self.model.walls,
                           *self.model.critical_points,
                           *self.model.rulers]:
            self.create_pixel_item(model_item, select=False)
            
        
    def create_pixel_item(self, model_item, select=True):
      
        pixel_item_class  = self.pixel_item_class_map[model_item.__class__]
      
        
        pixel_item = pixel_item_class(model=model_item)
      
        self.scene().addItem(pixel_item)
        
        return pixel_item

    

    def zoomFactor(self):
        return self.transform().m11()
   
    def zoomChanged(self):
        for wall in self.scene().walls():
            wall.updateLineStyle()
        for contour in self.scene().contourItems():
            contour.updateStyle()
        for line in self.scene().rulers():
            line.updateStyle()
 
    
    def setZoomRect(self, rect):       
        self.fitInView(rect, Qt.KeepAspectRatio)
        self.zoomChanged()
        
    def resetZoom(self):
        self.setZoomRect(QRectF(self.scene().floorplan().pixmap().rect()))

    def resizeEvent(self, *args):
        super().resizeEvent(*args)
        if self.scene().floorplan() is not None:
            rect = QRectF(self.scene().floorplan().pixmap().rect())
            if self.visibleRect().contains(rect):
                self.resetZoom()
  
    def legend(self):
        if self.scene().contourItems() and self.model.dosemap_style.show_legend:
            return self.scene().dosemap().legend()
        else:
            return None
  
    def paintEvent(self, event):
        # Call the base class paintEvent to ensure proper drawing
        super().paintEvent(event)
        if self.legend() is not None:
            self.paintLegend()
            
    def paintLegend(self):
        p = QPainter(self.viewport())
        p.setRenderHints(self.renderHints())
        legend = self.legend()
        rect = QRectF(legend.left(), legend.top(),
                      legend.sceneRect().width(),
                      legend.sceneRect().height())
        
        legend.render(p, rect)
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Z and event.modifiers() == Qt.ControlModifier:
            self._ctrl_pressed = False
            self.model.history.undo()
        elif event.key() == Qt.Key_Y and event.modifiers() == Qt.ControlModifier:
            self._ctrl_pressed = False
            self.model.history.redo()
        elif event.key() == Qt.Key_Left:
            self.moveSelectedItems(-1, 0)
        elif event.key() == Qt.Key_Right:
            self.moveSelectedItems(1, 0)
        elif event.key() == Qt.Key_Up:
            self.moveSelectedItems(0, -1)
        elif event.key() == Qt.Key_Down:
            self.moveSelectedItems(0, 1)
        elif event.key() == Qt.Key_Control:
            self._ctrl_pressed = True
            
        super().keyPressEvent(event)
        
    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self._ctrl_pressed = False
        super().keyReleaseEvent(event)

    def moveSelectedItems(self, dx, dy):
        MOVE_PIXELS = 10
        dx *= MOVE_PIXELS
        dy *= MOVE_PIXELS
        
        for item in self.scene().selectedGraphicsModelItems():
            item.model.move_pixels(dx, dy)
        
        
        
        

if __name__ == '__main__':
    
    app = QApplication([])
    
    
    project = '../../example_projects/SmallProject/project.zip'
    project = '../../example_projects/SmallProject/project.zip'
    model = Model.load_from_project_file(project)
    window = QMainWindow()
    
    view = Graphics(model=model)

    
   
    window.setCentralWidget(view)
    
    # view.legend.setBottomRight()
   
    
   
    

    
    window.show()
    
    
  

    app.exec_()
