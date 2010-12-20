#import sys
#from PyQt4.QtGui import *
from PyQt4 import QtCore
from PyQt4 import QtGui

class JobDataTab(QtCore.QObject):
    def __init__(self,job_name=None):
        super(JobDataTab,self).__init__()
        
        self.columns=[]
        
        self.properties={
            "id": QtGui.QLineEdit(),
            "name":QtGui.QLineEdit(),
            "owner":QtGui.QLineEdit(),
            "status":QtGui.QLineEdit(),
            "process":QtGui.QLineEdit(),
            "left":QtGui.QLineEdit(),
            "done":QtGui.QLineEdit(),
            "pri":QtGui.QLineEdit(),
            "pool":QtGui.QLineEdit(),
            }
   
        self.properties["name"].setText("%s"%job_name),
        
    def add(self,table,index):
        i=0
        for job_entry_name , widget in self.properties.iteritems():
            print "adding"   
            job_row = table.setCellWidget(index,i,widget)
            self.columns.append(job_row)
            i+=1
            
    def update(self,value_dict):
        for k,v in value_dict.iteritems():
            self.properties[k].setText(str(v))


        
        
        