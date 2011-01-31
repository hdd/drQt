import os
import sys

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import PyQt4.QtWebKit as QtWebKit

import drqueue.base.libdrqueue as drqueue

from lib.utils import newJob_widget_class
from lib.utils import newJob_base_class
from lib.utils import icons_path

def get_methods(pyoject):
    methods=[]
    for m in dir(pyoject):
        if m.find("_") == -1:
            methods.append(str(m))
    return methods

def get_kojs():
    kojs=drqueue.koj_info()
    return get_methods(kojs)

class NewJob(newJob_widget_class, newJob_base_class):
    def __init__(self,parent=None):
        super(NewJob,self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Create New Job")
        self.setFixedSize(600, 500)
        self._job_=drqueue.job()
        self._kojs=get_kojs()
        
        self.fill_job_types()
        
    def fill_job_types(self):    
        for k in self._kojs:
            self.CB_job_type.addItem(k)
        
def main():
    app = QtGui.QApplication(sys.argv)
    dialog=NewJob()  
    dialog.show()
    return app.exec_()

if __name__ == "__main__":
    main()

        
    