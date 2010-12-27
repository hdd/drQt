import sys
import os

import logging

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore

import drqueue.base.libdrqueue as drqueue

from utils import icons_path
from utils import tooltips_path
from lib.nodeViewer import NodeViewer

logging.basicConfig()
log = logging.getLogger("job_tab")
log.setLevel(logging.DEBUG)

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
     
           
    def _node_view_show(self):
        log.debug("starting node view")
        NW_widget=NodeViewer(self)
        NW_widget.add_node(self._drq_job_object)
        NW_widget.show()
        
    
    def _set_values(self):        
        """
        set tab values using the drq job object 
        """
        self._tab_id.setText("%s"%self._drq_job_object.id)        
        self._tab_name.setText("%s"%self._drq_job_object.name)
        self._tab_owner.setText("%s"%self._drq_job_object.owner)
        self._tab_status.setPixmap( self.icons[self._drq_job_object.status].scaled(25,25))
        self._tab_procs.setText("%d"%self._drq_job_object.nprocs)
        self._tab_est_time.setText("%d"%self._drq_job_object.fdone)
        self._tab_priority.setText("%d"%self._drq_job_object.priority)
        self._tab_pool.setText("%s"%self._drq_job_object.limits.pool)
            
    def _set_context(self):
        """
        bind the context menu to all the columns
        """
        for column in self.columns:
            column.setContextMenuPolicy(QtCore.Qt.CustomContextMenu) 
            self.connect(column, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self._create_context)
                        
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
        for column in self.columns:
            column.setToolTip(formattedTolltip)
            
    def _create_context(self,QPoint):
        """
        create the context menu
        """
        #print currentItem._tab_id
        #newAct =QtGui.QAction("&New Job",self)
        #newAct.setToolTip("createa new job")
        #self.connect(newAct, QtCore.SIGNAL('triggered()'), self._new_job_show)  
                
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
        
        deleteAct = QtGui.QAction("&Delete",self)
        deleteAct.setToolTip("delete the job")


        nodedAct = QtGui.QAction("Node &View",self)
        nodedAct.setToolTip("view job dependencies")    
        self.connect(nodedAct, QtCore.SIGNAL('triggered()'), self._node_view_show)  
        
        # Create a menu
        menu = QtGui.QMenu("Menu", self)
        #menu.addAction(newAct)
        menu.addAction(copyAct) 
        menu.addSeparator()
        menu.addAction(rerunAct)
        menu.addAction(stopAct) 
        menu.addAction(hstopAct)
        menu.addAction(deleteAct)
        menu.addSeparator()
        menu.addAction(nodedAct) 
        # Show the context menu in the mouse position 
        menu.exec_(QtGui.QCursor.pos())         
                
                
    def delete_job(self):
        self._drq_job_object.delete()
                
    def add_to_table(self,table,index):
        """
        bind the job row data to the job table
        """
        table.setCellWidget(index,0,self._tab_id)
        table.setCellWidget(index,1,self._tab_name)
        table.setCellWidget(index,2,self._tab_owner)
        table.setCellWidget(index,3,self._tab_status) 
        table.setCellWidget(index,4,self._tab_procs) 
        table.setCellWidget(index,5,self._tab_est_time) 
        
        table.setCellWidget(index,7,self._tab_priority) 
        table.setCellWidget(index,8,self._tab_pool) 
        