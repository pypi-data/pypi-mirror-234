# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 11:54:13 2023

@author: r757021
"""


from PyQt5.QtWidgets import (QApplication, QGraphicsScene,  
                             QGraphicsRectItem, QGraphicsTextItem, 
                             QGraphicsLineItem)
                             
from PyQt5.QtGui import QPen, QColor, QBrush, QFont
from PyQt5.QtCore import Qt


class Legend(QGraphicsScene):
    
    FONT_SIZE       = 10
    

    def __init__(self, model=None):
        self.model = model
       
        super().__init__()

        self.drawItems()
    
    def dpiX(self):
        return QApplication.desktop().physicalDpiX()
    
    def dpiY(self):
        return QApplication.desktop().physicalDpiY()
    
    def spacingX(self):
        return 0.1 * self.dpiX()
    
    def spacingY(self):
        return 0.1 * self.dpiY()
    
    def marginX(self):
        return 0.1 * self.dpiX()
    
    def marginY(self):
        return 0.1 * self.dpiY()
    
    def lineLength(self):
        return 0.5 * self.dpiX()

    def left(self):
        return 0.2 * self.dpiX()
    
    def top(self):
        return 0.2 * self.dpiY()
            
    def font(self):
        font = QFont()
        font.setPointSizeF(self.FONT_SIZE)
        return font

    def drawItems(self):
        self.clear()
        self.drawLines()
        self.addItem(self._rect())
        self.setSceneRect(self.itemsBoundingRect())

    def _rect(self):
        bounds = self.itemsBoundingRect()
      
        rect = QGraphicsRectItem(bounds.x() - self.marginX(),
                                 bounds.y() - self.marginY(),
                                 bounds.width() + 2 * self.marginX(),
                                 bounds.height() + 2 * self.marginY())
                                        
        rect.setZValue(30)
        brush = QBrush()
        brush.setColor(QColor(255, 255, 255, 200))
        brush.setStyle(Qt.SolidPattern)
        rect.setBrush(brush)
        return rect
    
    def _linePen(self, style, color, width):
        style = self.model.get_qt_linestyle(style)
        color = self.model.get_qt_color(color)
        
        pen = QPen()
        pen.setColor(color)
        pen.setStyle(style)
        pen.setWidthF(width*self.dpiX()/72)
        return pen

    
    def entry(self, msv, color, style, linewidth, row):                               
        ll      = self.lineLength()
        sx, sy  = self.spacingX(), self.spacingY()
        
        text = QGraphicsTextItem(str(msv) + ' mSv')
        text.setFont(self.font())
        th = text.boundingRect().height()
        
        text.setPos(ll + sx, row * th + (row-1) * sy)
        
        ly = text.pos().y() + 0.5 * th  
        line = QGraphicsLineItem(0, ly, ll, ly)
        line.setPen(self._linePen(style, color, linewidth))
     
        text.setZValue(31)
        line.setZValue(31)
        
        return line, text
        
    
    def drawLines(self):    
        lines = [line for line in self.model.contour_lines\
                 if line[4]]
        for i, line in enumerate(lines):
            msv, color, style, linewidth, enabled = line
            if not enabled: continue
            line, text = self.entry(msv, color, style, linewidth, i)
        
            self.addItem(text)
            self.addItem(line)
            
    
    
