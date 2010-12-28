import sys
import os

import logging

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore

import drqueue.base.libdrqueue as drqueue

from utils import icons_path
from utils import tooltips_path


class ConnectionItem(QtGui.QGraphicsItem ):
    def __init__(self,source_node =None, dest_node=None):
        super(ConnectionItem,self).__init__()
        self.start_point=QtCore.QPointF(source_node.pos())
        self.dest_point=QtCore.QPointF(dest_node.pos())
        
    def paint(self, painter, option, widget):
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 1))
        line = QtCore.QLineF(self.start_point, self.dest_point)
        painter.drawLine(line);
    
class JobNode(QtGui.QGraphicsItem ):
    xsize=60
    ysize=30
    def __init__(self,drq_job_object):
        super(JobNode,self).__init__()
        self.setFlag(QtGui.QGraphicsItem.ItemIsFocusable)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setPos(0,0)
        self.setScale(2)
        self.rect=QtCore.QRectF(self.xsize,self.ysize,self.xsize,self.ysize)
        self._drq_job_object = drq_job_object
        self._set_tooltip()
        
    def boundingRect(self):
        return QtCore.QRectF(self.xsize,self.ysize,self.xsize,self.ysize)

    def paint(self, painter, option, widget):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 1))
        painter.setBrush(QtGui.QBrush(QtCore.Qt.green, QtCore.Qt.SolidPattern))   
        painter.drawRect(self.rect)
        painter.setFont(QtGui.QFont("arial",4,3))
                
        node_text="Job:#%d\nName: %s"%(self._drq_job_object.id,self._drq_job_object.name)

        painter.drawText(self.rect,node_text,QtGui.QTextOption(QtCore.Qt.AlignVCenter|QtCore.Qt.AlignHCenter))  
 
    def _set_tooltip(self):
        """
        build up the tooltip using the drq job object
        bind the tooltip to all the columns
        """
        html_tooltip=open(os.path.join(tooltips_path,"job_info.html"),"r")
        tooltipData ={}
        tooltipData["cmd"]=self._drq_job_object.cmd
        tooltipData["envvars"]=self._drq_job_object.envvars
        tooltipData["dependid"]=self._drq_job_object.dependid
        
        formattedTolltip=str(html_tooltip.read()).format(**tooltipData)
        self.setToolTip(formattedTolltip)
                    
        
class NodeViewer(QtGui.QDialog):
    def __init__(self,parent=None):
        super(NodeViewer,self).__init__(parent)
        self.view = QtGui.QGraphicsView()
        self.scene = QtGui.QGraphicsScene()
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)
        self.view.setScene(self.scene)
        self.setWindowTitle("job node view")
        self.setWindowIcon(QtGui.QIcon(os.path.join(icons_path,"nodes.svg")))
        self.setMinimumSize(600,400)
        
    def add_node(self,drq_job_object):
        job_node = JobNode(drq_job_object)
        self.scene.addItem(job_node)
        