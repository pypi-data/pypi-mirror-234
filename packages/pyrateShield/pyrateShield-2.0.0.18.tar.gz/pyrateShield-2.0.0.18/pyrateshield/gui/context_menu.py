import pyperclip
import yaml
import numpy as np
import qtawesome as qta

from copy import deepcopy


from PyQt5.QtWidgets import QMenu, QAction
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import QPoint, QPointF
from pyrateshield import labels
from pyrateshield.gui.graphics_items import (FloorplanPixmap, 
                                             GraphicsModelItem, WallMarker, 
                                             GraphicsPoint, Cross)
from functools import partial

from pyrateshield.model_items import Wall
#from pyrateshield.gui.mpl_items_controller import PixelSizeLine

SNAP_RADIUS_CM = 100



class ContextMenuController():
   
    
    def __init__(self, model=None, view=None, parent=None):
        
        self.parent = parent
        self.view = view
        self.set_model(model)
        
        self.view.rightMouseClick.connect(self.right_click)
        

    def set_model(self, model):
        self.model = model
   
    def right_click(self, event, pixel_item):
        self.event = event
        pos = self.view.mapToScene(event.pos())
        
        if isinstance(pixel_item, FloorplanPixmap):
            self.show_canvas_context_menu(pos)
            event.accept()
    
        elif isinstance(pixel_item, (GraphicsModelItem, WallMarker))\
                        and pixel_item.showContextMenu:            
            self.show_pick_context_menu(pos, pixel_item)
            event.accept()
       
    @property
    def copied_items(self):
        # get plain text from clipboard
        text = pyperclip.paste()
        
        try: 
            items = yaml.safe_load(text)
        except:
            print('Invalid yaml on clipboard!')
            return None
        
        if not isinstance(items, dict):
            print('No data dictionary could be loaded from clipboard')
            return None
        
        for key in items.keys():
            if key not in [labels.WALLS, labels.SOURCES_CT, 
                           labels.SOURCES_NM, labels.SOURCES_XRAY,
                           labels.CRITICAL_POINTS, labels.RULERS]:
                print(f'Invalid key found in dictionary: {key}')
                return None
        copied_items = {}
        for key, dict_items in items.items():
            if not isinstance(dict_items, list):
                print(f'{key} does not contain a list!')
                return None
            copied_items[key] = []            
            item_class = self.model.item_class_for_label(key)
            for dict_item in dict_items:
                try:
                    item = item_class.from_dict(dict_item)
                except:
                    print('Could not convert to {item_class.__class__.__name__}:\n {yaml.dump(dict_item)}')
                    return None
                
                if key == labels.SOURCES_NM:
                    if item.clearance not in self.model.clearances.itemNames():
                        print(f'Clearance {item.clearance} not defined!')
                elif key == labels.WALLS:
                    if item.shielding not in self.model.shieldings.itemNames():
                        print(f'Shielding {item.shielding} not definied!')
                
                copied_items[key] += [item]
        return copied_items
            
                
      
        
    
    def show_canvas_context_menu(self, pos=None, _=None):
       
        
        context_menu = QMenu(self.view)
        pos_cm = self.model.floorplan.geometry.pixel_point_to_cm(pos)
        
        toolbar = self.parent.toolbar_controller
        for label in [labels.SOURCES_CT, labels.SOURCES_XRAY,
                      labels.SOURCES_NM, labels.CRITICAL_POINTS, labels.WALLS]:
            
            #pos_from_scene = self.view.mapFromScene(QPointF(*pos_cm))
      
            title = 'Add ' + label + ' item'
            action = context_menu.addAction(title)
        
            interactive = label == labels.WALLS
            
            
            callback = partial(toolbar.new_model_item, pos_cm, label, 
                               interactive=interactive)
            
            action.triggered.connect(callback)
            
        
        
        copied_items = self.copied_items
    
        if copied_items is not None:
            ncopied_items = sum([len(items) for key, items in copied_items.items()])                                 
        else:
            ncopied_items = 0
        
        action = context_menu.addAction('Paste item(s) (keep position)')
        callback = lambda: self.paste(pos_cm=None)
        action.triggered.connect(callback)
        action.setEnabled(ncopied_items > 0)
        
        action = context_menu.addAction('Paste item here')
        callback = lambda: self.paste(pos_cm=pos_cm)
        action.triggered.connect(callback)
        action.setEnabled(ncopied_items == 1 and labels.WALLS not in self.copied_items.keys())
        
        
        
        menu_position = QPoint(round(pos.x()), round(pos.y()))
        menu_position = self.view.mapFromScene(menu_position)
        menu_position = self.view.mapToGlobal(menu_position)       
        context_menu.exec_(menu_position)
            
    def add_item(self, label, position):
        self.mpl_controller.view.toolbar.button_checked(label, True)
        self.mpl_controller.add_model_item(label, position)                
  
                    
    def get_snap_action(self, marker):
        
        wall, index, _ = self.model.walls.closestVertexToPixelPoint(
            marker.pos(), exclude_wall=marker.parentItem().model)
        
        if wall is None: return
        
        closest_vertex = wall.vertices[index]

        disp_vv = str([round(vi) for vi in closest_vertex])
    
        shielding = self.model.shieldings.itemByName(wall.shielding)
        
        action = "Snap to: " + shielding.name + ' at ' + disp_vv
        snap_action = QAction(action)
    
    
        vertex_index = marker.parentItem().markers().index(marker)
        
        
        callback = partial(self.snap_wall, marker.parentItem(), 
                           vertex_index, closest_vertex)
                                   
        snap_action.triggered.connect(callback)
    
        icon = qta.icon('fa5s.circle', color=shielding.color)
        snap_action.setIcon(icon)

        # else:
        #     snap_action = QAction('Snap to: ')
        #     snap_action.setEnabled(False)
        return snap_action
    
    def selection_to_dict(self):
        return [item.to_dict() for item in self.graphics.scene().selectedItems()]
    
    def paste(self, pos_cm=None):
        if self.copied_items is None or len(self.copied_items) == 0:
            return
        
        self.parent.graphics().scene().deselectAll()
        
   
        for label, items in self.copied_items.items():
            sequence = self.model.get_attr_from_label(label) 
            
            for item in items:
                if pos_cm is not None:
                    item.position = pos_cm
                sequence.addItem(item)
                pixel_item = self.parent.graphics().pixel_item_for_model_item(item)
                pixel_item.setSelected(True)
        
        self.parent.graphics().scene().updateStyles()
        

            
        
    def centroid(self, items):
        points = []
        for item in items:
            if isinstance(item, Wall):
                points += [*item.vertices]
            else:
                points += [item.position]
            
        points = np.asarray(points)
        return np.mean(points, 0)
            
        
    
    def show_pick_context_menu(self, pos=None, pixel_item=None):
            pixel_item.setSelected(True)
        
        
            context_menu = QMenu(self.view)
      
                
            if isinstance(pixel_item, WallMarker):
                poly = pixel_item.parentItem()
                vertex_index = poly.markers().index(pixel_item)
                          
                wall = pixel_item.parentItem().model
                index = pixel_item.parentItem().markers().index(pixel_item)
                if not wall.isClosed() and (index == 0 or index == len(wall)-1):
                    text = "Add new marker"
                else:
                    text = "Insert new marker"
            
            
                wall_draw_action = context_menu.addAction(text)            
                callback = partial(self.continue_wall, poly, vertex_index)                        
                wall_draw_action.triggered.connect(callback)
                
                if poly.model.isClosable():
                    close_action = context_menu.addAction("Close polygon")
                    callback = pixel_item.parentItem().model.close
                    close_action.triggered.connect(callback)
                elif poly.model.isClosed():
                    open_action = context_menu.addAction("Open polygon")
                    callback = lambda: pixel_item.parentItem().model.open(vertex_index)
                    open_action.triggered.connect(callback)
                if len(poly.model) > 2:
                    delete_action = context_menu.addAction('Delete marker')
                    callback = lambda: pixel_item.parentItem().model.deleteVertex(vertex_index)
                    delete_action.triggered.connect(callback)
        
                snap_action = self.get_snap_action(marker=pixel_item)
                                                
                if snap_action is not None:                             
                    context_menu.addAction(snap_action)
                    
                    
            if pixel_item.isEnabled():
                cut_action = context_menu.addAction("Cut selection")
                cut_action.triggered.connect(self.cut_selected_items)
                     
                copy_action = context_menu.addAction("Copy selection") 
                copy_action.triggered.connect(self.copy_selected_items)
             
                delete_action = context_menu.addAction("Delete selection")
                delete_action.triggered.connect(self.delete_selected_items)
            
            if isinstance(pixel_item, (GraphicsPoint, Cross)):
                enabled_action = context_menu.addAction("Enabled")
                enabled_action.setCheckable(True)            
                enabled_action.setChecked(pixel_item.model.enabled)            
                enabled_action.triggered.connect(pixel_item.model.enable)
                
                
                
                
                label = pixel_item.model.label
                sequence = self.model.get_attr_from_label(label)
                
                enabled = [item.enabled for item in sequence]
                
                if not all(enabled):
                    enable_all_action = context_menu.addAction(f"Enable all {label}")
                    enable_all_action.triggered.connect(lambda: self.enable_all(label))
                
                if any(enabled):
                    disable_all_action = context_menu.addAction(f"Disable all {label}")
                    disable_all_action.triggered.connect(lambda: self.disable_all(label))
             
                
            context_menu.exec_(QCursor.pos())
            
    def enable_all(self, label):
        sequence = self.model.get_attr_from_label(label)
        for item in sequence:
            item.enabled = True
            
    def disable_all(self, label):
        sequence = self.model.get_attr_from_label(label)
        for item in sequence:
            item.enabled = False
                 
    def delete(self, pixel_item):
        self.model.delete_item(pixel_item.model)
        

    def continue_wall(self, pixel_item, vertex_index):
       
        vertex = pixel_item.model.positionPixels()[vertex_index]

        if vertex_index == len(pixel_item.model) - 1:
            vertex_index += 1   
    
        pixel_item.model.insertVertexPixelPoint(vertex_index, vertex)
     
       
        marker = pixel_item.markers()[vertex_index]
        self.parent.toolbar_controller.item_to_move = marker
        
        
    def snap_wall(self, wall, vertex_index, closest_vertex):     
        wall.model.setVertex(vertex_index, closest_vertex)
       
    def copy_selected_items(self):
        selected = self.parent.graphics().scene().selectedGraphicsModelItems()
        
        selected_model_items = [item.model for item in selected]
        
        selected_model_items = self.model.sort_model_items(selected_model_items)
        
        # use deepcopy to prevent anchors and aliases in yaml
        to_yaml = {label: [deepcopy(item.to_dict()) for item in seq]\
                             for label, seq in selected_model_items.items()}
        
        # remove empty walls or sources
        to_yaml = {k: v for k, v in to_yaml.items() if len(v) > 0}
        
            
        self.copy_yaml = yaml.dump(to_yaml, default_flow_style=None)
        
        pyperclip.copy(self.copy_yaml)
        
    
  
    def delete_selected_items(self):        
        selected = self.parent.graphics().scene().selectedGraphicsModelItems()
        self.model.delete_items([item.model for item in selected])
       
        
    def cut_selected_items(self):

        self.copy_selected_items()
        self.delete_selected_items()
        
  