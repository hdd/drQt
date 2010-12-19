#import sys
#from PyQt4.QtGui import *
from PyQt4 import QtCore
from PyQt4 import QtGui

class JobDataTab(QtCore.QObject):
    def __init__(self):
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
            "pool":QtGui.QLineEdit()
            }
        
    def add(self,table,index):
        i=0
        print "adding"
        for prop , value in self.properties.iteritems():
            widget = table.setCellWidget(index,i,value)
            self.columns.append(widget)
            i+=1
            
    def update(self,value_dict):
    	for k,v in value_dict.iteritems():
    	 self.properties[k].setText(str(v))


        
        
        