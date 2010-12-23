import sys
import os

import time
    
from PyQt4 import QtCore
from PyQt4 import QtGui

#class Timer(threading.Thread):
class Timer(QtCore.QThread):
    def __init__(self,parent=None):
        super(Timer,self).__init__(parent=parent)
        self.mutex = QtCore.QMutex()
        self.condition = QtCore.QWaitCondition()
        self.runTime = 5
        self.action=None
        self._running=True
        
    def set_run_time(self,time=5):
        self.runTime = time
        
    def run(self):
        print "thread starting..." 
        while True:
            counter = self.runTime
            for sec in range(self.runTime):
                print "..tic..."
                time.sleep(1.0)
                counter -= 1
                
            self.emit(QtCore.SIGNAL("done"))

class JobDataTab(QtCore.QObject):
    
    def __init__(self,drq_job_object=None):
        super(JobDataTab,self).__init__()
        self._drq_job_object=drq_job_object
                
        self.icons=[]
        self.columns=[]        
        
        self.current_path = os.path.dirname(__file__)
        
        ##job_properties=["id","name","owner","status","process","left","done","pri","pool"]
        
        print drq_job_object.__dict__
        
        self.icons.append(QtGui.QPixmap(os.path.join(self.current_path,"icons","NONE.png")))  
        self.icons.append(QtGui.QPixmap(os.path.join(self.current_path,"icons","NONE.png")))  
        self.icons.append(QtGui.QPixmap(os.path.join(self.current_path,"icons","OK.png")))
        self.icons.append(QtGui.QPixmap(os.path.join(self.current_path,"icons","OK.png")))
        
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
        
        
        
        self._tab_id.setText("%s"%drq_job_object.id)        
        self._tab_name.setText("%s"%drq_job_object.name)
        self._tab_owner.setText("%s"%drq_job_object.owner)
        self._tab_status.setPixmap( self.icons[drq_job_object.status])
        self._tab_procs.setText("%d"%drq_job_object.nprocs)
        self._tab_priority.setText("%d"%drq_job_object.priority)
        
        
        
    def add(self,table,index):
            table.setCellWidget(index,0,self._tab_id)
            table.setCellWidget(index,1,self._tab_name)
            table.setCellWidget(index,2,self._tab_owner)
            table.setCellWidget(index,3,self._tab_status) 
            table.setCellWidget(index,4,self._tab_procs) 
            table.setCellWidget(index,7,self._tab_priority) 