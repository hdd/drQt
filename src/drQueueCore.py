#import sys
#from PyQt4.QtGui import *
from PyQt4 import QtCore
from PyQt4 import QtGui

class JobDataUI(QtCore.QObject):
    def __init__(self):
        super(JobDataUI,self).__init__()

        self.properties={
            "tab_id": 0,
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
        for prop , value in self.properties.iteritems():
            table.setCellWidget(index,i,self.input_status)
            i+=1


        
        
        