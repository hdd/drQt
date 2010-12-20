import sys
import os

#from PyQt4.QtGui import *
from PyQt4 import QtCore
from PyQt4 import QtGui

class JobDataTab(QtCore.QObject):
    def __init__(self,job_name=None):
        super(JobDataTab,self).__init__()
                
        self.icons=[]
        self.columns=[]        
        
        self.current_path = os.path.dirname(__file__)
        
        self.icons.append(QtGui.QPixmap(os.path.join(self.current_path,"icons","NO.png")))    
        self.icons.append(QtGui.QPixmap(os.path.join(self.current_path,"icons","OK.png")))
        self.icons.append(QtGui.QPixmap(os.path.join(self.current_path,"icons","NONE.png")))       
                        
        self.properties={
            "id": QtGui.QLabel(),
            "name":QtGui.QLabel(),
            "owner":QtGui.QLabel(),
            "status":QtGui.QLabel(),
            "process":QtGui.QLabel(),
            "left":QtGui.QLabel(),
            "done":QtGui.QLabel(),
            "pri":QtGui.QLabel(),
            "pool":QtGui.QLabel(),
            }
   
        self.properties["name"].setText("%s"%job_name),
        self.properties["status"].setPixmap(self.icons[0])
        
        self._register_properties()
        
    def _register_properties(self):
        for k,v in self.properties.iteritems():
        	#register get_set for entries
        	pass
        
    def add(self,table,index):
        for job_name , widget in self.properties.iteritems():
            widget.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            job_row = table.setCellWidget(index,len(self.columns),widget)
            self.columns.append(job_row)
            
    def update(self,value_dict):
        for k,v in value_dict.iteritems():
            self.properties[k].setText(str(v))
            if k == "status":
            	self.properties[k].setPixmap(self.icons[v])


        
        
        