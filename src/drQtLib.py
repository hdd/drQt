import sys
import os

import time
import logging

logging.basicConfig()
log = logging.getLogger("drQtLib")
log.setLevel(logging.DEBUG)

from PyQt4 import QtCore
from PyQt4 import QtGui

current_path = os.path.dirname(__file__)
tooltips_path= os.path.join(current_path,"ui","tooltips")
icons_path = os.path.join(current_path,"ui","icons")


class Timer(QtCore.QThread):
    def __init__(self,parent=None):
        super(Timer,self).__init__(parent=parent)
        self.runTime = 5
        self.action=None
        self._running=True
        
    def set_run_time(self,time=5):
        self.runTime = time
        
    def run(self): 
        while True:
            counter = self.runTime
            for sec in range(self.runTime):
                time.sleep(1.0)
                counter -= 1
            self.emit(QtCore.SIGNAL("time_elapsed"))        


                 
class JobTab(QtGui.QWidget):
    
    def __init__(self,drq_job_object=None,parent=None):
        super(JobTab,self).__init__(parent=parent)
        self._drq_job_object = drq_job_object
                
        self.columns=[]        
        self.icons=[]      
         
        self.icons.append(QtGui.QPixmap(os.path.join(icons_path,"running.png")))  
        self.icons.append(QtGui.QPixmap(os.path.join(icons_path,"running.png")))  
        self.icons.append(QtGui.QPixmap(os.path.join(icons_path,"stop.png")))
        self.icons.append(QtGui.QPixmap(os.path.join(icons_path,"ok.png")))
        
        self._tab_id=QtGui.QLabel()
        self._tab_id.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.columns.append(self._tab_id)
        
        self._tab_name=QtGui.QLabel()
        self._tab_name.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.columns.append(self._tab_name)
        
        self._tab_owner=QtGui.QLabel()
        self._tab_owner.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.columns.append(self._tab_owner)
        
        self._tab_status=QtGui.QLabel()
        self._tab_status.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.columns.append(self._tab_status)
        
        self._tab_procs=QtGui.QLabel()
        self._tab_procs.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.columns.append(self._tab_procs)
        
        self._tab_priority=QtGui.QLabel()
        self._tab_priority.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.columns.append(self._tab_priority)

        self._tab_pool=QtGui.QLabel()
        self._tab_pool.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.columns.append(self._tab_pool)
        
        self._tab_est_time=QtGui.QLabel()
        self._tab_est_time.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.columns.append(self._tab_est_time)
        
        self._set_values()
        self._set_context()
        self._set_tooltip()
    
    def _set_values(self):        
        self._tab_id.setText("%s"%self._drq_job_object.id)        
        self._tab_name.setText("%s"%self._drq_job_object.name)
        self._tab_owner.setText("%s"%self._drq_job_object.owner)
        self._tab_status.setPixmap( self.icons[self._drq_job_object.status].scaled(25,25))
        self._tab_procs.setText("%d"%self._drq_job_object.nprocs)
        self._tab_est_time.setText("%d"%self._drq_job_object.fdone)
        self._tab_priority.setText("%d"%self._drq_job_object.priority)
        self._tab_pool.setText("%s"%self._drq_job_object.limits.pool)
            
    def _set_context(self):
        for column in self.columns:
            column.setContextMenuPolicy(QtCore.Qt.CustomContextMenu) 
            self.connect(column, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self._create_context)
                        
    def _set_tooltip(self):
        html_tooltip=open(os.path.join(tooltips_path,"job_info.html"),"r")
        tooltipData ={}
        tooltipData["cmd"]=self._drq_job_object.cmd
        tooltipData["envvars"]=self._drq_job_object.envvars
        tooltipData["dependid"]=self._drq_job_object.dependid
        
        formattedTolltip=str(html_tooltip.read()).format(**tooltipData)
        for column in self.columns:
            column.setToolTip(formattedTolltip)
            
    def _create_context(self,QPoint):
        #print currentItem._tab_id
        newAct =QtGui.QAction("&New Job",self)
        newAct.setToolTip("createa new job")
                
        copyAct = QtGui.QAction("&Copy Job",self)
        copyAct.setToolTip("copy the job")
        
        rerunAct = QtGui.QAction("&Re Run",self)
        rerunAct.setToolTip("Re run the job")

        stopAct = QtGui.QAction("&Stop",self)
        stopAct.setToolTip("stop the running job")
                
        hstopAct = QtGui.QAction("&Hard Stop",self)
        hstopAct.setToolTip("hard stop the running job")

        continueAct = QtGui.QAction("&Continue",self)
        continueAct.setToolTip("Continue the stop job")
        
        deleteAct = QtGui.QAction("D&elete",self)
        deleteAct.setToolTip("delete the job")
        
        # Create a menu
        menu = QtGui.QMenu("Menu", self)
        menu.addAction(newAct)
        menu.addAction(copyAct) 
        menu.addSeparator()
        menu.addAction(rerunAct)
        menu.addAction(stopAct) 
        menu.addAction(hstopAct)
        menu.addAction(continueAct) 
        menu.addAction("Delete")
        
        # Show the context menu in the mouse position 
        menu.exec_(QtGui.QCursor.pos())   
        
    def _emit_details(self):
        self.emit(QtCore.SIGNAL("job_details(QVariant)"), QtCore.QVariant(self._drq_job_object))       
                
    def add_to_table(self,table,index):
            table.setCellWidget(index,0,self._tab_id)
            table.setCellWidget(index,1,self._tab_name)
            table.setCellWidget(index,2,self._tab_owner)
            table.setCellWidget(index,3,self._tab_status) 
            table.setCellWidget(index,4,self._tab_procs) 
            table.setCellWidget(index,5,self._tab_est_time) 
            
            table.setCellWidget(index,7,self._tab_priority) 
            table.setCellWidget(index,8,self._tab_pool) 
            

class NodeTab(QtGui.QWidget):
    def __init__(self,drq_node_object=None,parent=None):
        super(NodeTab,self).__init__(parent=parent)
        self._drq_node_object=drq_node_object
                 
        self.columns=[] 
               
        self.icons=[]       
        
        self.oss=["Irix","OsX","Linux","Windows"]
  
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
        
        self._tab_pools=QtGui.QLabel()
        self._tab_pools.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.columns.append(self._tab_pools)
        
        self._set_values()
        self._set_context()
        self._set_tooltip()
        
    def _set_values(self):
        self._tab_id.setText("%d"%self._drq_node_object.hwinfo.id)
        self._tab_name.setText("%s"%self._drq_node_object.hwinfo.name)
        self._tab_enabled.setPixmap( self.icons[self._drq_node_object.limits.enabled].scaled(25,25))
        
        self._tab_os.setText("%s"%self.oss[self._drq_node_object.hwinfo.os])
        self._tab_cpus.setText("%d"%self._drq_node_object.hwinfo.ncpus)
                
    def _set_context(self):
        for column in self.columns:
            column.setContextMenuPolicy(QtCore.Qt.CustomContextMenu) 
            self.connect(column, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self._create_context)            

    def _set_tooltip(self):
        html_tooltip=open(os.path.join(tooltips_path,"node_info.html"),"r")
        tooltipData ={}
        tooltipData["id"]=self._drq_node_object.hwinfo.id
        tooltipData["arch"]=self._drq_node_object.hwinfo.arch
        tooltipData["memory"]=self._drq_node_object.hwinfo.memory
        tooltipData["name"]=self._drq_node_object.hwinfo.name
        tooltipData["ncpus"]=self._drq_node_object.hwinfo.ncpus
        tooltipData["nnbits"]=self._drq_node_object.hwinfo.nnbits
        tooltipData["os"]=self.oss[self._drq_node_object.hwinfo.os]
        tooltipData["procspeed"]=self._drq_node_object.hwinfo.procspeed
        tooltipData["proctype"]=self._drq_node_object.hwinfo.proctype
        tooltipData["speedindex"]=self._drq_node_object.hwinfo.speedindex
        
        formattedTolltip=str(html_tooltip.read()).format(**tooltipData)
        
        for column in self.columns:
            column.setToolTip(formattedTolltip)
            
    def _create_context(self,QPoint):
        detailsAct = QtGui.QAction("&Details",self)
        detailsAct.setToolTip("get details on the job")
        #self.connect(detailsAct, SIGNAL('triggered()'), self.on_details)
        # Create a menu
        menu = QtGui.QMenu("Menu", self) 
        menu.addAction(detailsAct) 
        menu.addSeparator()
        menu.addAction("Enable")
        menu.addAction("Disable") 
        # Show the context menu in the mouse position 
        menu.exec_(QtGui.QCursor.pos())           

    def _emit_details(self):
        self.emit(QtCore.SIGNAL("job_details(QVariant)"), QtCore.QVariant(self.drq_node_object))   
                        
    def add_to_table(self,table,index):
            table.setCellWidget(index,0,self._tab_id)
            table.setCellWidget(index,1,self._tab_enabled)
            table.setCellWidget(index,2,self._tab_running)
            table.setCellWidget(index,3,self._tab_name) 
            table.setCellWidget(index,4,self._tab_os) 
            table.setCellWidget(index,5,self._tab_cpus) 
            table.setCellWidget(index,6,self._tab_loadavg) 
            table.setCellWidget(index,7,self._tab_pools)         