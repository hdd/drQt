import sys
import os

import time
    
from PyQt4 import QtCore
from PyQt4 import QtGui

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
            self.emit(QtCore.SIGNAL("done"))



class NodeDataTab(QtGui.QWidget):
    def __init__(self,drq_node_object=None,parent=None):
        super(NodeDataTab,self).__init__(parent=parent)
        self.drq_node_object=drq_node_object
                 
        self.columns=[] 
               
        self.current_path = os.path.dirname(__file__)
        self.icons=[]       
        
        self.oss=["windows","macOs","linux"]
  
        self.icons.append(QtGui.QPixmap(os.path.join(self.current_path,"icons","stop.png")))
        self.icons.append(QtGui.QPixmap(os.path.join(self.current_path,"icons","ok.png")))       
        #node_properties=["Id","Enabled","Running","Name","Os","CPUs","Load Avg","Pools"]
        
        self._tab_id=QtGui.QLabel()
        self._tab_id.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter) 
        
        self._tab_enabled=QtGui.QLabel()
        self._tab_enabled.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)                

        self._tab_running=QtGui.QLabel()
        self._tab_running.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)  
               
        self._tab_name=QtGui.QLabel()
        self._tab_name.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        
        self._tab_os=QtGui.QLabel()
        self._tab_os.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)

        self._tab_cpus=QtGui.QLabel()
        self._tab_cpus.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        
        self._tab_loadavg=QtGui.QLabel()
        self._tab_loadavg.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        
        self._tab_pools=QtGui.QLabel()
        self._tab_pools.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        
        self._tab_id.setText("%d"%drq_node_object.hwinfo.id)
        self._tab_name.setText("%s"%drq_node_object.hwinfo.name)
        self._tab_enabled.setPixmap( self.icons[drq_node_object.limits.enabled].scaled(25,25))
        
        self._tab_os.setText("%s"%self.oss[drq_node_object.hwinfo.os])
        self._tab_cpus.setText("%d"%drq_node_object.hwinfo.ncpus)
        #self._tab_pools.setText("%s"%drq_node_object.limits.pool)
        
    def add(self,table,index):
            table.setCellWidget(index,0,self._tab_id)
            table.setCellWidget(index,1,self._tab_enabled)
            table.setCellWidget(index,2,self._tab_running)
            table.setCellWidget(index,3,self._tab_name) 
            table.setCellWidget(index,4,self._tab_os) 
            table.setCellWidget(index,5,self._tab_cpus) 
            table.setCellWidget(index,6,self._tab_loadavg) 
            table.setCellWidget(index,7,self._tab_pools)         
                        
class JobDataTab(QtGui.QWidget):
    
    def __init__(self,drq_job_object=None,parent=None):
        super(JobDataTab,self).__init__(parent=parent)
        self._drq_job_object=drq_job_object
                
        self.columns=[]        
        
        self.current_path = os.path.dirname(__file__)
        self.icons=[]       
        self.icons.append(QtGui.QPixmap(os.path.join(self.current_path,"icons","running.png")))  
        self.icons.append(QtGui.QPixmap(os.path.join(self.current_path,"icons","running.png")))  
        self.icons.append(QtGui.QPixmap(os.path.join(self.current_path,"icons","stop.png")))
        self.icons.append(QtGui.QPixmap(os.path.join(self.current_path,"icons","ok.png")))
        
        self._tab_id=QtGui.QLabel()
        self._tab_id.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        
        self._tab_name=QtGui.QLabel()
        self._tab_name.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        
        self._tab_owner=QtGui.QLabel()
        self._tab_owner.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        
        self._tab_status=QtGui.QLabel()
        self._tab_status.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)

        self._tab_procs=QtGui.QLabel()
        self._tab_procs.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        
        self._tab_priority=QtGui.QLabel()
        self._tab_priority.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)

        self._tab_pool=QtGui.QLabel()
        self._tab_pool.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        
        self._tab_est_time=QtGui.QLabel()
        self._tab_est_time.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        
        """
            set values from drQ job instance
        """
        
        self._tab_id.setText("%s"%drq_job_object.id)        
        self._tab_name.setText("%s"%drq_job_object.name)
        self._tab_owner.setText("%s"%drq_job_object.owner)
        self._tab_status.setPixmap( self.icons[drq_job_object.status].scaled(25,25))
        self._tab_procs.setText("%d"%drq_job_object.nprocs)
        
        self._tab_est_time.setText("%d"%drq_job_object.fdone)
        
        self._tab_priority.setText("%d"%drq_job_object.priority)
        self._tab_pool.setText("%s"%drq_job_object.limits.pool)
        
        self._tab_id.setToolTip("hey")
        
    def add(self,table,index):
            table.setCellWidget(index,0,self._tab_id)
            table.setCellWidget(index,1,self._tab_name)
            table.setCellWidget(index,2,self._tab_owner)
            table.setCellWidget(index,3,self._tab_status) 
            table.setCellWidget(index,4,self._tab_procs) 
            table.setCellWidget(index,5,self._tab_est_time) 
            
            table.setCellWidget(index,7,self._tab_priority) 
            table.setCellWidget(index,8,self._tab_pool) 