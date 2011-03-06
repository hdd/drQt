import sys
import os

import logging

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore

import drqueue.base.libdrqueue as drqueue

from utils import icons_path
from utils import tooltips_path

logging.basicConfig()
log = logging.getLogger("slave_tab")
log.setLevel(logging.DEBUG)

class SlaveNodeTab(QtGui.QWidget):
    
    def __init__(self,drq_node_object=None,parent=None):
        super(SlaveNodeTab,self).__init__(parent=parent)
        self._drq_node_object=drq_node_object
                 
        self.columns=[] 
               
        self.icons=[]       

  
        self.icons.append(QtGui.QPixmap(os.path.join(icons_path,"stop.png")))
        self.icons.append(QtGui.QPixmap(os.path.join(icons_path,"ok.png")))       
        #node_properties=["Id","Enabled","Running","Name","Os","CPUs","Load Avg","Pools"]
        
        self._tab_id=QtGui.QLabel()
        self._tab_id.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter) 
        self.columns.append(self._tab_id)
        
        self._tab_enabled=QtGui.QLabel()
        self._tab_enabled.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)                
        self.columns.append(self._tab_enabled)
        
        self._tab_running=QtGui.QLabel()
        self._tab_running.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)  
        self.columns.append(self._tab_running)
               
        self._tab_name=QtGui.QLabel()
        self._tab_name.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.columns.append(self._tab_name)
        
        self._tab_os=QtGui.QLabel()
        self._tab_os.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.columns.append(self._tab_os)

        self._tab_cpus=QtGui.QLabel()
        self._tab_cpus.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.columns.append(self._tab_cpus)
        
        self._tab_loadavg=QtGui.QLabel()
        self._tab_loadavg.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.columns.append(self._tab_loadavg)
        
        self._tab_pools=QtGui.QComboBox()
        #self._tab_pools.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.columns.append(self._tab_pools)
        
        self._set_values()
        self._set_context()
        self._set_tooltip()
        
    def _set_values(self):
        self._tab_id.setText("%d"%self._drq_node_object.hwinfo.id)
        self._tab_name.setText("%s"%self._drq_node_object.hwinfo.name)
        self._tab_enabled.setPixmap( self.icons[self._drq_node_object.limits.enabled].scaled(25,25))
        
        self._tab_loadavg.setText("%d:%d:%d"%(self._drq_node_object.status.get_loadavg(0),
                                              self._drq_node_object.status.get_loadavg(1),
                                              self._drq_node_object.status.get_loadavg(2)))
        
        self._tab_os.setText("%s"%drqueue.osstring(self._drq_node_object.hwinfo.os))
        self._tab_cpus.setText("%d"%self._drq_node_object.hwinfo.ncpus)
        self._tab_pools.addItem("%s"%self._drq_node_object.limits.pool)
                
    def _set_context(self):
        for column in self.columns:
            column.setContextMenuPolicy(QtCore.Qt.CustomContextMenu) 
            self.connect(column, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self._create_context)            

    def _set_tooltip(self):
        html_tooltip=open(os.path.join(tooltips_path,"node_info.html"),"r")
        tooltipData ={}
        tooltipData["id"]=self._drq_node_object.hwinfo.id
        tooltipData["arch"]=drqueue.archstring(self._drq_node_object.hwinfo.arch)
        tooltipData["memory"]=self._drq_node_object.hwinfo.memory
        tooltipData["name"]=self._drq_node_object.hwinfo.name
        tooltipData["ncpus"]=self._drq_node_object.hwinfo.ncpus
        tooltipData["nnbits"]=drqueue.bitsstring(self._drq_node_object.hwinfo.nnbits)
        tooltipData["os"]=drqueue.osstring(self._drq_node_object.hwinfo.os)
        tooltipData["procspeed"]=self._drq_node_object.hwinfo.procspeed
        tooltipData["proctype"]=drqueue.proctypestring(self._drq_node_object.hwinfo.proctype)
        tooltipData["speedindex"]=self._drq_node_object.hwinfo.speedindex
        
        formattedTolltip=str(html_tooltip.read()).format(**tooltipData)
        
        for column in self.columns:
            column.setToolTip(formattedTolltip)
            
    def _create_context(self,QPoint):

        enableAct = QtGui.QAction("&Enable",self)        
        self.connect(enableAct, QtCore.SIGNAL('triggered()'), self._enable_slave) 
        
        disableAct = QtGui.QAction("&Disable",self)   
        self.connect(disableAct, QtCore.SIGNAL('triggered()'), self._disable_slave) 
        
        menu = QtGui.QMenu("Menu", self) 
        menu.addAction(enableAct)
        menu.addAction(disableAct)
        menu.exec_(QtGui.QCursor.pos())           

    def _enable_slave(self):
        self._drq_node_object.request_enable(drqueue.CLIENT)
        self._emit_uptdate()

    def _disable_slave(self):
        self._drq_node_object.request_disable(drqueue.CLIENT)
        self._emit_uptdate()

    def _emit_uptdate(self):
        log.debug("emit update")
        self.emit(QtCore.SIGNAL("update"))  
                        
    def add_to_table(self,table,index):
            table.setCellWidget(index,0,self._tab_id)
            table.setCellWidget(index,1,self._tab_enabled)
            table.setCellWidget(index,2,self._tab_running)
            table.setCellWidget(index,3,self._tab_name) 
            table.setCellWidget(index,4,self._tab_os) 
            table.setCellWidget(index,5,self._tab_cpus) 
            table.setCellWidget(index,6,self._tab_loadavg) 
            table.setCellWidget(index,7,self._tab_pools) 