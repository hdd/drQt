import sys
import os
import time
import PyQt4.uic as uic

import PyQt4.QtCore as QtCore

current_path = os.path.dirname(__file__)

tooltips_path= os.path.join(current_path,"ui","tooltips")
icons_path = os.path.join(current_path,"ui","icons")

main_ui_path=os.path.join(current_path,"ui","drQt.ui")
main_widget_class, main_base_class = uic.loadUiType(main_ui_path)  

newJob_ui_path=os.path.join(current_path,"ui","newJob.ui")
newJob_widget_class, newJob_base_class = uic.loadUiType(newJob_ui_path)  

class Timer(QtCore.QThread):
    """
    generic threaded timer
    emit a "time_elapsed" signal to notify the elapsed time  
    """
    def __init__(self,parent=None):
        super(Timer,self).__init__(parent=parent)
        self.runTime = 5
        self.action=None
        self._running=True
        
    def set_run_time(self,time=5):
        """
        set the time between the signal emissions
        """
        self.runTime = time
        
    def run(self): 
        """
        here is where the count down happen
        """
        while True:
            counter = self.runTime
            for sec in range(self.runTime):
                time.sleep(1.0)
                counter -= 1
            self.emit(QtCore.SIGNAL("time_elapsed"))   
            
