# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 15:25:31 2023

@author: r757021
"""
import numpy as np

from copy import copy
import math
from matplotlib.colors import LogNorm
from matplotlib.cm import get_cmap
from skimage.measure import find_contours

from PyQt5.QtWidgets import  (QGraphicsEllipseItem, QGraphicsPathItem,  
                              QGraphicsPolygonItem, QGraphicsTextItem,
                              QGraphicsRectItem, QGraphicsPixmapItem)
                              

from PyQt5.QtGui import (QPen, QPainterPath, QPolygonF, QBrush, QColor, 
                         QPixmap, QImage, QFont)
from PyQt5.QtCore import Qt, QPointF,  QRectF,  QSizeF, QObject, pyqtSignal, QLineF



from pyrateshield import labels
from pyrateshield.gui.legend import Legend

LINE_WIDTH = 'line_width'
LINE_COLOR = 'line_color'
FACE_COLOR = 'face_color'
SIZE       = 'size'
ZVALUE     = 'zvalue'
WIDTH      = 'width'
HEIGHT     = 'height'


RADIUS = 5
HIGHLIGHT_RADIUS = 10
SELECTED_RADIUS = 10

def numpy_array_to_qimage(numpy_array):
   
    if len(numpy_array.shape) == 3:
        height, width, channel = numpy_array.shape
    else:
        height, width = numpy_array.shape
        channel = 1
  
    # Create a QImage from the numpy array
    if channel == 3:
        qformat = QImage.Format_RGB888
    elif channel == 4:
        qformat= QImage.Format_RGBA8888
    elif channel == 1:
        qformat = QImage.Format_Grayscale8
        
    qimage = QImage(numpy_array.data, 
                    width, height, width * channel, qformat)
    return qimage


class DosemapPixmap(QGraphicsPixmapItem):
    showContextMenu = False
    _floorplan_size = None
    _dosemap = None
    ZVALUE = -1
    _legend = None
    
    def __init__(self, model=None, 
                       style=None):
                       
        
        super().__init__()
        if style is None:
            raise ValueError
        self.setZValue(self.ZVALUE)   
        self.style = style             
        self.set_callbacks()
        
       
        

        
    def setDosemap(self, dosemap):
        self._dosemap = dosemap
        self.updatePixmap()
        
    def dosemap(self):
        return self._dosemap
        
    def legend(self):
        if self._legend is None:
            self._legend = Legend(model=self.style)
        return self._legend
  
    def set_callbacks(self):        
        self.style.update_event.connect(self.style_update)
   
    def style_update(self, event_data):
        # label, src, old_value, new_value = event_data
 
        self._legend = None
        
        self.updatePixmap()
        
        
    def floorplanSize(self):
        return self.scene().floorplan().pixmap().size()
            
    def coloredDosemap(self):
        scale = LogNorm(self.style.vmin, self.style.vmax, clip=True)
        dosemap = np.flipud(self.dosemap())
        log_dosemap = scale(dosemap)
        log_dosemap = np.ma.getdata(log_dosemap)
        
        cmap = self.getCmap()
        color_dosemap = (cmap(log_dosemap) * 255)
        color_dosemap = color_dosemap.astype(np.uint8)
        return color_dosemap
            
    def updatePixmap(self):
        self.scene().removeContours()
        
        if self.dosemap() is None:
            pixmap = QPixmap()            
        else:
            dosemap_color = self.coloredDosemap()
            qdosemap = numpy_array_to_qimage(dosemap_color)
        
            pixmap = QPixmap.fromImage(qdosemap)
            pixmap = pixmap.scaled(self.floorplanSize())
            self.add_contours()
        
        self.setPixmap(pixmap)
            
    
    def getCmap(self):
        cmap = copy(get_cmap(self.style.cmap_name))        
        alphas = np.linspace(0, 1, cmap.N)
        cmap._init()
        cmap._lut[:len(alphas), -1] = alphas            
        cmap.set_under(alpha=0)
        return cmap

    def add_contours(self): 
        if self.scene() is None: return
        if self.dosemap() is None: return

        self.scene().removeContours()
        
        dosemap = np.flipud(self.dosemap())
        
        
        styles = self.style.contour_lines
        
        if not isinstance(styles, list) or len(styles) == 0:
            raise
        alpha = round(self.style.alpha * 255)
        alpha = min(alpha, 255)
        alpha = max(alpha, 0)
        for style in styles:
            level, line_color, line_style, line_width, enabled = style
            if not enabled: continue
            contour = GraphicsContourItem(dosemap,
                                          level=level,
                                          line_style=line_style,
                                          line_color=line_color,
                                          line_width=line_width,                                          
                                          floorplan_size=self.floorplanSize())
     
            self.scene().addItem(contour)

            
            


class FloorplanPixmap(QGraphicsPixmapItem):
    showContextMenu = True
    ZVALUE = -2
    def __init__(self, *args, model=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model
        self.setZValue(self.ZVALUE)
        self.set_callbacks()
        self.updatePixmap()
        
    def set_callbacks(self):
        self.model.update_event.connect(self.model_update)
    
    def model_update(self, event_data):
        label, src, old_value, new_value = event_data
        if label == labels.IMAGE:
            self.updatePixmap()
   
    def updatePixmap(self):
        if self.model is None: return
        qimage = numpy_array_to_qimage(self.model.image)
        self.setPixmap(QPixmap.fromImage(qimage))
    
     
        


class ZoomRect(QGraphicsPolygonItem):
    __pen = None
    def __init__(self, point):
        self.rect = QRectF(point, QSizeF(0,0))
        
        super().__init__(self.poly())
        self.setPen(self._pen())
        
    def poly(self):
        return QPolygonF([self.rect.topLeft(),
                          self.rect.topRight(),
                          self.rect.bottomRight(),
                          self.rect.bottomLeft()])
    
    def _pen(self):
        if self.__pen is None:
    
            self.__pen = QPen()            
            self.__pen.setColor(QColor(0,0,0))
            self.__pen.setWidth(0) # ensures width is always 1 pixel on screen
            self.__pen.setStyle(Qt.DotLine)
            
            
        return self.__pen
        
    def setPoint(self, point):        
        self.rect.setBottomRight(point)
        self.setPolygon(self.poly())
        


class GraphicsItem(QObject):
    showContextMenu         = False
    _highlighted            = False

    _style                  = {}
    _highlight_style        = {}
    _select_style           = {}
    _disabled_style         = {}
    
    _highlightable          = True
    _selectable             = True
    _movable                = True
    _send_position_change   = True
    _accept_hover           = True
    _ignore_transformations = True
    
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
      
        self.setFlag(self.ItemIsSelectable, self._selectable)
        self.setFlag(self.ItemIsMovable, self._movable)
        self.setFlag(self.ItemSendsScenePositionChanges, self._send_position_change)
        self.setAcceptHoverEvents(self._accept_hover)
        self.setFlag(self.ItemIgnoresTransformations, self._ignore_transformations)
        self.updateStyle()
        
    
       
    def zoomFactor(self):
        try:
            return self.scene().views()[0].zoomFactor()
        except:
            return 1
        
    def ctrlPressed(self):
        if self.scene() is not None:
            return self.scene().views()[0].ctrlPressed()
        else:
            return False
        
    def isHighlighted(self):
        return self._highlighted
    
    def setHighlighted(self, highlighted):
        if self._highlighted != highlighted and self._highlightable:
            self._highlighted = highlighted
            self.updateStyle()
            
    def hoverEnterEvent(self, event):
        if self._highlightable:
            event.accept()
            self.setHighlighted(True)
    
    def hoverLeaveEvent(self, event):
        if self._highlightable:
            self.setHighlighted(False)
                    
    def pointsToSceneUnits(self, points):
        if self.scene() is None:
            return points
        else:
            return self.scene().pointsToSceneUnits(points)
            
    def itemChange(self, change, value):
        
        if change == self.ItemSelectedHasChanged:    
            self.updateStyle()
        if change == self.ItemSceneHasChanged:
            self.updateStyle()
        return value
    
    def style_zvalue(self):
        return self.style().get(ZVALUE, 0)
    
    def size(self):
        size = self.pointsToSceneUnits(self.style().get(SIZE, 10))
        return size
    
    def width(self):
        size = self.pointsToSceneUnits(self.style().get(WIDTH, 10))
        return size
    
    def height(self):
        size = self.pointsToSceneUnits(self.style().get(HEIGHT, 10))
        return size
        
    
    def linewidth(self):
        width = self.pointsToSceneUnits(self.style().get(LINE_WIDTH, 0)) 
        return width 
    
    def linecolor(self):
        color = self.style().get(LINE_COLOR, [0, 0, 0])        
        color = QColor(*color)
        return color
    
    def facecolor(self):
        color = self.style().get(FACE_COLOR, [0, 0, 0])
        color = QColor(*color)
        return color
        
    def style(self):
        if not self.isEnabled():
            return self._disabled_style
        if self.isSelected():
            return self._select_style
        elif self.isHighlighted() and self._highlightable:
            return self._highlight_style
        else:
            return self._style
                                           
    def _pen(self):
        pen = QPen()

        pen.setColor(self.linecolor())
        pen.setWidthF(self.linewidth())
        return pen
           
    def _brush(self):
        return QBrush(self.facecolor())
        
    def updateStyle(self):
        self.setZValue(self.style_zvalue())
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.ctrl_pressed = True
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.ctrl_pressed = False
        super().keyReleaseEvent(event)
        
    def mousePressEvent(self, event):
        self.mouse_press_pos = self.mapToScene(event.pos())
        
    
    
        
        
                        
class GraphicsModelItem(GraphicsItem):
    POSITION_LABEL = labels.POSITION
    _block_updates_from_model  = False
    
    def __init__(self, model=None, **kwargs):                
        self.model = model
        self.set_callbacks()
        
        super().__init__(**kwargs)
        self.modelPositionToGraphics()
        self.setSelected(False)
        
        
    def hoverEnterEvent(self, event):
        super().hoverEnterEvent(event)
        
        if isinstance(self, Marker):
            self.setToolTip(self.parentItem().model.tooltip())
        else:
            self.setToolTip(self.model.tooltip())
            
    def set_callbacks(self):
      
        self.model.update_event.connect(self.modelUpdate)
        
    def itemChange(self, change, value):          
        if change == self.ItemPositionHasChanged:               
            self.graphicsPositionToModel()      
        return super().itemChange(change, value)                                       

    def graphicsPositionToModel(self):
        self._block_updates_from_model = True
        self.model.setPositionPixels(self.pos())
        self._block_updates_from_model = False
    
    def modelPositionToGraphics(self):
        self.setPos(self.model.positionPixels())

    def modelUpdate(self, event_data):
        src, label, old_value, value = event_data   
        if label == self.POSITION_LABEL:
            if not self._block_updates_from_model:
                self.modelPositionToGraphics()
        elif label == labels.ENABLED:
            self.setEnabled(value)
            self.updateStyle()
            
    def mousePressEvent(self, event):
        super().mousePressEvent(event)

        self.scene().sendToForeground(self)
     
            
class GraphicsPoint(QGraphicsEllipseItem, GraphicsModelItem):  
    showContextMenu         = True
    POSITION_LABEL = labels.POSITION
    mouse_press_pos = QPointF()
    __pen = None
    __brush = None
    
    _style = {SIZE: RADIUS,
              FACE_COLOR: [0, 255, 0, 128],
              LINE_COLOR: [0, 0, 0],
              LINE_WIDTH: 1,
              ZVALUE: 5}
    
    _highlight_style = {SIZE: HIGHLIGHT_RADIUS,
                  FACE_COLOR: [0, 255, 0, 128],
                  LINE_COLOR: [0, 0, 0],
                  LINE_WIDTH: 1,
                  ZVALUE: 10}
    
    _select_style = {SIZE: HIGHLIGHT_RADIUS,
                  FACE_COLOR: [0, 255, 0, 128],
                  LINE_COLOR: [0, 0, 0],
                  LINE_WIDTH: 1,
                  ZVALUE: 20}
    
    _disabled_style = {SIZE: RADIUS,
                       FACE_COLOR: [83, 83, 83],
                       LINE_COLOR: [0, 0, 0],
                       LINE_WIDTH:2,
                       ZVALUE: 5}
    
    
    
    def __init__(self, model=None, **kwargs):
        super().__init__(model=model, **kwargs)

    def drawRect(self):
        return QRectF(QPointF(-self.radius(), -self.radius()),
                      QSizeF(2*self.radius(), 2*self.radius()))
    
    def radius(self):
        return  self.size() / 2

    def updateStyle(self):
        super().updateStyle()
        self.setPen(self._pen())
        self.setBrush(self._brush())
        self.setRect(self.drawRect())
        
    def mousePressEvent(self, event):
        self.mouse_press_pos = self.pos()
        
    def itemChange(self, change, value):
        if change == self.ItemPositionChange and self.ctrlPressed():
            if self.scene() is not None and len(self.scene().selectedItems()) == 1:
                if self.mouse_press_pos is not None:
                    reference_pos = self.mouse_press_pos
                
                    dx = abs(reference_pos.x() - value.x())
                    dy = abs(reference_pos.y() - value.y())
                    
                    if dx >= dy:
                        value = QPointF(value.x(), reference_pos.y())
                    else:
                        value = QPointF(reference_pos.x(), value.y())
                
        return GraphicsModelItem.itemChange(self, change, value)  
    #     
    
    

class GraphicsSourceNM(GraphicsPoint):
    _style = {SIZE: RADIUS,
              FACE_COLOR: [139, 0, 0, 128],
              LINE_COLOR: [0, 0, 0],
              LINE_WIDTH: 2,
              ZVALUE: 5}
    
    _highlight_style = {SIZE: HIGHLIGHT_RADIUS,
                  FACE_COLOR: [139, 0, 0, 128],
                  LINE_COLOR: [0, 0, 0],
                  LINE_WIDTH: 2,
                  ZVALUE: 10}
    
    _select_style = {SIZE: SELECTED_RADIUS,
                  FACE_COLOR: [139, 0, 0, 128],
                  LINE_COLOR: [0, 0, 0],
                  LINE_WIDTH: 2,
                  ZVALUE: 20}
    

class GraphicsSourceCT(GraphicsPoint):
    _style = {SIZE: RADIUS,
              FACE_COLOR: [34, 139, 35, 128],
              LINE_COLOR: [0, 0, 0],
              LINE_WIDTH: 2,
              ZVALUE: 5}
    
    _highlight_style = {SIZE: HIGHLIGHT_RADIUS,
                  FACE_COLOR: [34, 139, 35, 128],
                  LINE_COLOR: [0, 0, 0],
                  LINE_WIDTH: 2,
                  ZVALUE: 10}
                  
    _select_style = {SIZE: SELECTED_RADIUS,
                     FACE_COLOR: [34, 139, 35, 128],
                     LINE_COLOR: [0, 0, 0],
                     LINE_WIDTH: 2,
                     ZVALUE: 20}
    

class GraphicsSourceXray(GraphicsPoint):
    _style = {SIZE: RADIUS,
              FACE_COLOR: [34, 34, 139, 128],
              LINE_COLOR: [0, 0, 0],
              LINE_WIDTH: 2,
              ZVALUE: 5}
    
    _highlight_style = {SIZE: HIGHLIGHT_RADIUS,
                        FACE_COLOR: [34, 34, 139, 128],
                        LINE_COLOR: [0, 0, 0],
                        LINE_WIDTH: 2,
                        ZVALUE: 10}
    
    _select_style = {SIZE: SELECTED_RADIUS,
                     FACE_COLOR: [34, 34, 139, 128],
                     LINE_COLOR: [0, 0, 0],
                      LINE_WIDTH: 2,
                      ZVALUE: 20}
    

    


class Cross(QGraphicsPolygonItem, GraphicsModelItem):
    showContextMenu         = True
    _style = {
           
              LINE_COLOR: [238, 75, 43, 128],
              LINE_WIDTH: 0.25 *RADIUS,
              WIDTH: RADIUS,
              HEIGHT: RADIUS,
              ZVALUE: 5}
              
    
    _highlight_style = {
                  
                  LINE_COLOR: [238, 75, 43, 128],
                  LINE_WIDTH: 0.25*HIGHLIGHT_RADIUS,
                  WIDTH: HIGHLIGHT_RADIUS,
                  HEIGHT: HIGHLIGHT_RADIUS,              
                  ZVALUE: 10}
                 
    
    _select_style = {
                  
                  LINE_COLOR: [238, 75, 43, 128],
                  LINE_WIDTH: 0.25*SELECTED_RADIUS,
                  WIDTH: SELECTED_RADIUS,
                  HEIGHT: SELECTED_RADIUS,
                  ZVALUE: 20}
    
    _disabled_style = {LINE_COLOR: [83, 83, 83],
                       LINE_WIDTH: 3,
                       WIDTH: 15,
                       HEIGHT: RADIUS,
                       ZVALUE: 5}
                  
    
    
    def __init__(self, model=None, **kwargs):

        super().__init__(model=model, **kwargs)
        self.modelPositionToGraphics()
        self.updateStyle()
       
    
    def points(self):
        return [[-1, -1],
                [ 1, 1],
                [0, 0],
                [-1, 1],
                [1, -1], 
                [0, 0]]
  
    
    
    def _polygon(self):
        w, h = self.width(), self.height()
        
        Xp = [QPointF(xi[0]*w*0.5, xi[1]*h*0.5) for xi in self.points()]
        
        return QPolygonF(Xp)
    
    def updateStyle(self):
        super().updateStyle()
        self.setPen(self._pen())
        self.setPolygon(self._polygon())
        
    def itemChange(self, change, value):
        if change == self.ItemPositionChange and self.ctrlPressed():
            if self.scene() is not None and len(self.scene().selectedItems()) == 1:
                if self.mouse_press_pos is not None:
                    reference_pos = self.mouse_press_pos
                
                    dx = abs(reference_pos.x() - value.x())
                    dy = abs(reference_pos.y() - value.y())
                    
                    if dx >= dy:
                        value = QPointF(value.x(), reference_pos.y())
                    else:
                        value = QPointF(reference_pos.x(), value.y())
                
        return GraphicsModelItem.itemChange(self, change, value) 
        

class Marker(QGraphicsRectItem, GraphicsItem):
    showContextMenu         = True
    _style = {WIDTH: RADIUS,
              HEIGHT: RADIUS,
              LINE_WIDTH: 2,
              ZVALUE: 3}
         
    _highlight_style = {WIDTH: HIGHLIGHT_RADIUS,
                        HEIGHT: HIGHLIGHT_RADIUS,
                        LINE_WIDTH: 2,
                        ZVALUE: 10}
    
    _select_style = {WIDTH: SELECTED_RADIUS,
                     HEIGHT: SELECTED_RADIUS,
                     LINE_WIDTH: 2,
                     ZVALUE: 20}
    
    def __init__(self, **kwargs):
        #self.line = line
        
        super().__init__(**kwargs)
        
    def style_zvalue(self):
        if any([marker.isSelected() for marker in self.otherMarkers()]):
            return self._select_style[ZVALUE]
        else:
            return super().style_zvalue()
            

    def _pen(self):
        return QPen(Qt.NoPen)
        
    def otherMarkers(self):
        return [marker for marker in self.parentItem().markers()\
                if marker is not self]
            
    def adjecentMarker(self):
        index = self.parentItem().markers().index(self)
        if index > 0:
            adjecent = self.parentItem().markers()[index-1]
        else:
            adjecent = self.parentItem().markers()[1]
        return adjecent
            
            
    def index(self):
        return self.parentItem().markers().index(self)
    
    def isHighlighted(self):
        return self._highlighted or any([marker._highlighted for marker in self.otherMarkers()])
               
    def _rect(self):
        return QRectF(-0.5*self.width(), -0.5*self.height(), 
                      self.width(), self.height())
    
    def facecolor(self):
        if self.parentItem() is None: return QColor()
        color = self.parentItem().linecolor()    
        color.setAlpha(128)
        return color
    
    def linecolor(self):
        if self.parentItem() is None: return QColor()
        return self.parentItem().linecolor()
    
    def itemChange(self, change, value):        
        if change == self.ItemSelectedHasChanged: 
            if not self.isSelected():
                self.setHighlighted(False)
            self.updateStyle()
        elif change == self.ItemPositionHasChanged:
            self.parentItem().graphicsPositionToModel()
            self.parentItem().modelPositionToGraphics()
        
        elif change == self.ItemPositionChange and self.ctrlPressed():
            if self.scene() is not None and len(self.scene().selectedItems()) == 1:

                reference_pos = self.adjecentMarker().pos()
                
            
                dx = abs(reference_pos.x() - value.x())
                dy = abs(reference_pos.y() - value.y())
                
                if dx >= dy:
                    value = QPointF(value.x(), reference_pos.y())
                else:
                    value = QPointF(reference_pos.x(), value.y())
                        
            return super().itemChange(change, value)  
            
       
        
    

        return super().itemChange(change, value)
    
    def updateStyle(self, update_others=True):    
        super().updateStyle()        
        self.setBrush(self._brush())
        self.setRect(self._rect())    
        self.setPen(self._pen())        
        if update_others:
            for marker in self.otherMarkers():
                marker.updateStyle(update_others=False)
                
   
class WallMarker(Marker):
    pass
        

   
class GraphicsLine(QGraphicsPathItem, GraphicsModelItem):
    POSITION_LABEL = labels.VERTICES
    markerClass = Marker
    _style = {LINE_WIDTH: 2,
              LINE_COLOR:  [0, 0, 139],
              ZVALUE: 0}
    
    # _highlight_style = {LINE_COLOR:  [0, 255, 0],                        
    #                     LINE_WIDTH: 0}
    
    
    # _select_style = {LINE_COLOR:  [0, 0, 139],                     
    #                  LINE_WIDTH: 0,
    #                  ZVALUE: 0}
    

    _markers = None
    _polygon = None
    
    _selectable = False
    _movable = False
    _highlightable = False
    _ignore_transformations = False
    
    def markerPolygon(self):
        return QPolygonF([marker.pos() for marker in self.markers()])
    
    def graphicsPositionToModel(self):          
            self._block_updates_from_model = True
            self.model.setPositionPixels(self.markerPolygon())
            self._block_updates_from_model = False
            
    def setSelected(self, selected):
        for marker in self.markers():
            marker.setSelected(selected)
            
    def isSelected(self):
        return all([marker.isSelected() for marker in self.markers()])
        
    def modelPositionToGraphics(self):
        poly = self.model.positionPixels()
        if self.model.isClosed():
            poly.append(poly[0])
        self.setPolygon(poly)
        self.updateMarkerPosition()
    
    def polygon(self):
        if self._polygon is None:
            self._polygon = QPolygonF()
        return self._polygon
    
    def setPolygon(self, polygon):
        self._polygon = polygon
        path = QPainterPath()
        path.addPolygon(polygon)
        self.setPath(path)
    
    def markers(self):
        if self._markers is None:
            self._markers = []
        return self._markers
    
    def updateMarkerPosition(self):
        all_selected = all([marker.isSelected() for marker in self.markers()])
        new_markers = len(self.model.vertices) - len(self.markers())
        markers = [self.markerClass(parent=self) for i in range(0, new_markers)]
        self.markers().extend(markers)
        
        if all_selected:
            for marker in markers:
                marker.setSelected(True)
               
        #delete_markers = len(self.markers()) - len(self.model.vertices)
        
        while len(self.markers()) > len(self.model.vertices):
            marker = self.markers().pop(0)
            self.scene().removeItem(marker)
            marker.setParentItem(None)
            del marker
            
        for point, marker in zip(self.polygon(), self.markers()):
            marker.setPos(point)
    
    def updateLineStyle(self):       
        self.setPen(self._pen())
    
    
    def modelUpdate(self, event_data):
        super().modelUpdate(event_data)
        src, label, old_value, value = event_data
        if label == labels.CLOSED:
           self.setSelected(False)
                
    def itemChange(self, change, value):
        if change == self.ItemSceneHasChanged:                        
            self.updateStyle()
        
        return super().itemChange(change, value)
            
    def updateStyle(self):
        super().updateStyle()
        #self.updateMarkers()
        self.setPen(self._pen())   
        for marker in self.markers():
            marker.updateStyle()
            
    def linewidth(self):
        width = self.pointsToSceneUnits(self.style().get(LINE_WIDTH, 0)) / self.zoomFactor()
        return width 
    
    def isPointOnEdge(self, point):
        def cross(v1, v2):
            return v1.x()*v2.y() - v1.y() * v2.x()
    
        polygon = self.polygon()    
        nvertices = len(polygon)
        if not self.model.isClosed():
            nvertices -= 1
            
        for i in range(nvertices):
            p1 = polygon[i]
            p2 = polygon[(i + 1) % len(polygon)]
            
            
            a = QPointF(p2 - p1)
            b = QPointF(point - p1)
            if a.manhattanLength() > 0:
                distance = abs(cross(a, b)) / a.manhattanLength()
  
                if distance <= self.linewidth():  # Adjust the threshold as needed
                    return True
        return False
    
    
    def mousePressEvent(self, event):
        if self.scene() is not None:
            self.scene().deselectAll()
        
        pos = self.mapToScene(event.pos())
        
        if self.isPointOnEdge(pos):        
            QGraphicsPathItem.mousePressEvent(self, event)
            GraphicsModelItem.mousePressEvent(self, event)

        else:

            QGraphicsPathItem.mousePressEvent(self, event)

    
        
class GraphicsWall(GraphicsLine):   
    markerClass = WallMarker

    
    def set_callbacks(self):
        super().set_callbacks()
        self.shieldings().styleChanged.connect(self.updateStyle)
        self.model.parent().shieldingChanged.connect(self.updateStyle)

    def _pen(self):
        pen = super()._pen()
        if self.model.get_shielding().name == labels.EMPTY_SHIELDING:
            pen.setStyle(Qt.DotLine)
        return pen
    
    def modelUpdate(self, event_data):
        super().modelUpdate(event_data)
        src, label, old_value, value = event_data     
        if label == labels.CLOSED:
            if not self._block_updates_from_model:
                self.modelPositionToGraphics()
        
        
    def linecolor(self):        
        color = self.model.get_shielding().color
        if isinstance(color, str):
            color = QColor(self.model.get_shielding().color)
        elif isinstance(color, (tuple, list)):
            color =  QColor(*self.model.get_shielding().color)
        return color
    
    def linewidth(self):
        shielding = self.model.get_shielding()
        width = self.pointsToSceneUnits(shielding.linewidth) / self.zoomFactor()
        
        return width
        
    def shieldings(self):             
        return self.model.parent().parent().shieldings
    
    
    
   
        
    
    
            
    
    
    
    
          
class PixelSizeMarker(Marker):
    
    _style = {SIZE: RADIUS,
              LINE_WIDTH: 2,
              ZVALUE: 3}
         
    _highlight_style = {SIZE: HIGHLIGHT_RADIUS,
                        LINE_WIDTH: 2,
                        ZVALUE: 10}
    
    _select_style = _style
    
    _highlightable = False
    
    def facecolor(self):
        color = self.parentItem().linecolor()    
        color.setAlpha(64)
        return color
    
    def _pen(self):
        pen = QPen()
        pen.setColor(self.parentItem().linecolor())
        pen.setWidth(0)
        pen.setStyle(Qt.DotLine)
        return pen
    
class RulerMarker(Marker):
    showContextMenu = False
    _style = {WIDTH: 0.3 * RADIUS,
              HEIGHT: RADIUS,
              LINE_WIDTH: 0,
              ZVALUE: 3}
         
    _highlight_style = {WIDTH: 0.3 * HIGHLIGHT_RADIUS,
                        HEIGHT: HIGHLIGHT_RADIUS,
                        LINE_WIDTH: 0,
                        ZVALUE: 10}
    
    _select_style = {WIDTH: 0.3 * RADIUS,
                     HEIGHT: HIGHLIGHT_RADIUS,
                     LINE_WIDTH: 0,
                     ZVALUE: 20}
    
    def facecolor(self):
        color = self.parentItem().linecolor()    
        color.setAlpha(255)
        return color
    
    def _pen(self):
        pen = QPen()
        pen.setColor(self.parentItem().linecolor())
        pen.setWidth(1)
        pen.setStyle(Qt.SolidLine)
        return pen
    
    
    def _rect(self):
         if self.parentItem() is None or self not in self.parentItem().markers():
             return QRectF(-0.5*self.width(), -0.5*self.height(), 
                           self.width(), self.height())
         
         index = self.parentItem().markers().index(self)
         lw = self.pointsToSceneUnits(self.parentItem()._style[LINE_WIDTH])
         
         
         if index == 1:
             return QRectF(-self.width()+0.5*lw, -0.5*self.height(), 
                           self.width(), self.height())
         if index == 0:
             return QRectF(-0.5*lw, -0.5*self.height(), 
                           self.width(), self.height())
    
    
# class PixelSizeLine(GraphicsLine):    
#     POSITION_LABEL = labels.VERTICES_PIXELS
#     markerClass = PixelSizeMarker

    
    
    
#     def graphicsPositionToModel(self):
#         vertices_pixels = [[marker.pos().x(), marker.pos().y()]\
#                            for marker in self.markers()]
        
#         self._block_updates_from_model = True
#         self.model.vertices_pixels = vertices_pixels
#         self._block_updates_from_model = False
        
#     def modelPositionToGraphics(self):       
#         p1 = QPointF(*self.model.vertices_pixels[0])
#         p2 = QPointF(*self.model.vertices_pixels[1])
#         self.setPolygon(QPolygonF((p1, p2)))
#         self.updateMarkerPosition()
        
        
        
class RulerLine(GraphicsLine):
    POSITION_LABEL = labels.VERTICES_PIXELS
    showContextMenu = False
    markerClass = RulerMarker
    TEXT_SIZE = 10
    def __init__(self, *args, show_text=True, **kwargs):
        self.show_text = show_text
        if self.show_text:
            self.text = QGraphicsTextItem("test")
       
        super().__init__(*args, **kwargs)
        if self.show_text:
            self.text.setParentItem(self)
            
            self.text.setFlag(self.ItemIgnoresTransformations, True)
        
    def _pen(self):
        pen = super()._pen()
        pen.setStyle(Qt.DashLine)
        return pen
    
    def font(self):
        font = QFont()
        
        size = self.pointsToSceneUnits(self.TEXT_SIZE)
        font.setPointSizeF(size)
        return font
    
    def modelPositionToGraphics(self):     
        p1 = QPointF(*self.model.vertices_pixels[0])
        p2 = QPointF(*self.model.vertices_pixels[1])
        self.setPolygon(QPolygonF((p1, p2)))
        self.updateMarkerPosition()
        
        self.markers()[0].setRotation(self.model.angle)
        self.markers()[1].setRotation(self.model.angle)
        if self.show_text:
            self.updateText()
            
    def graphicsPositionToModel(self):
         vertices_pixels = [[marker.pos().x(), marker.pos().y()]\
                            for marker in self.markers()]
         
         self._block_updates_from_model = True
         self.model.vertices_pixels = vertices_pixels
         self._block_updates_from_model = False
        
    def updateStyle(self):
        super().updateStyle()
        if self.show_text:
            self.updateText()
    
    def updateText(self):
        length = round(self.model.length_cm, 1)
        self.text.setPlainText(f'{length} cm')
        poly = self.polygon()
        if len(poly) == 0: return
        p1 = poly[0]
        p2 = poly[1]
        dy = p2.y() - p1.y()
        dx =  p2.x() - p1.x()
        line_angle = math.atan2(dy, dx)
        
        text_width = self.text.boundingRect().width()
        
        center = [(p2.x() + p1.x())/2, (p2.y() + p1.y())/2]
        
        #x2 + y2 = tw2
        
        #xi = center[0] + text_width/2 * math.sin(line_angle)
        #yi = center[1] + text_width/2 * math.cos(line_angle)
        
        xi = center[0] 
        yi = center[1]
        
        #self.text.setRotation(math.degrees(line_angle))
        self.text.setPos(QPointF(xi, yi))
        self.text.setFont(self.font())
        
        
    
    
class GraphicsContourItem(QGraphicsPathItem, GraphicsItem):
    _selectable = False
    _highlightable = False
    _movable = False
    _ignore_transformations = False
    
    def __init__(self, dosemap, level=1, line_style='solid', line_color='red',
                 line_width=0, floorplan_size=None):
        
        
        self.dosemap = dosemap
        self.level = level
        self.floorplan_size = floorplan_size
        self._line_style = line_style
        self._line_width = line_width        
        self._line_color = line_color
        super().__init__()
        self.setPath(self.path())
        self.updateStyle()
                      
    def updateStyle(self):
        self.setPen(self._pen())
        
    def linecolor(self):
        if isinstance(self._line_color, (list, tuple)):
            color = QColor(*self._line_color)
        else:
            color = QColor(self._line_color)                  
        return color
    
    def hoverEnterEvent(self, event):
        super().hoverEnterEvent(event)
        self.setToolTip(f'Dose level: {self.level} mSv')
            
    
        
    def linestyle(self):
        line_style = self._line_style
        if line_style == 'dashed':
            line_style = Qt.DashLine
        elif line_style == 'solid':
            line_style = Qt.SolidLine
        elif line_style == 'dashdot':
            line_style = Qt.DashDotLine
        elif line_style == 'dotted':
            line_style = Qt.DotLine
        return line_style
    
               
    def lineWidth(self):
        width = self.pointsToSceneUnits(self._line_width) / self.zoomFactor()
   
        return width

    def _pen(self):                    
        pen = QPen(self.linecolor(), self.lineWidth(), self.linestyle())
        return pen
    
    def path(self):
        path = QPainterPath()
        for polygon in self.polygons():            
            path.addPolygon(polygon)           
        return path
        
    def np_contours(self):
        return find_contours(self.dosemap, self.level)
    
    def polygons(self):
        polygons = []
        sx = self.floorplan_size.width()
        sy = self.floorplan_size.height()
        scale_x = sx / self.dosemap.shape[1]
        scale_y = sy / self.dosemap.shape[0]
        
        for np_contour in self.np_contours():
            np_contour += 0.5
            points = [QPointF(pi[1]*scale_x, pi[0]*scale_y) for pi in np_contour]
            polygon = QPolygonF(points)
            polygons += [polygon]
        return polygons
    
    