import sys
import os

import logging

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore

import drqueue.base.libdrqueue as drqueue

from utils import icons_path
from utils import tooltips_path


class JobNode(QtGui.QGraphicsItem ):
    xsize=60
    ysize=30
    def __init__(self):
        super(JobNode,self).__init__()
        self.setFlag(QtGui.QGraphicsItem.ItemIsFocusable)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setPos(0,0)
        self.setScale(2)
        self.rect=QtCore.QRectF(self.xsize,self.ysize,self.xsize,self.ysize)
        #self._name = drq_job_object.name
        
    def boundingRect(self):
        return QtCore.QRectF(self.xsize,self.ysize,self.xsize,self.ysize)

    def paint(self, painter, option, widget):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 1));
        painter.setBrush(QtGui.QBrush(QtCore.Qt.yellow, QtCore.Qt.SolidPattern));        
        painter.drawRect(self.rect)
        painter.setFont(QtGui.QFont("arial",4,5))
        painter.drawText(self.rect,"#jobId\nJobName",QtGui.QTextOption(QtCore.Qt.AlignLeft))  
        
class NodeViewer(QtGui.QWidget):
    def __init__(self):
        super(NodeViewer,self).__init__()
        view = QtGui.QGraphicsView()
        scene = QtGui.QGraphicsScene()
        layout = QtGui.QVBoxLayout()
        layout.addWidget(view)
        self.setLayout(layout)
        #job_node = JobNode()
        #scene.addItem(job_node)
        #view.setScene(scene)