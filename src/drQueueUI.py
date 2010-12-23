import sys
import os

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import PyQt4.uic as uic

import drQueueCore as core
import drqueue.base.libdrqueue as drqueue

ui_path=os.path.join(os.path.dirname(__file__),"ui","drQueueUi.ui")
widget_class, base_class = uic.loadUiType(ui_path)



class drQ(widget_class, base_class):
    def __init__(self,*args,**kwargs):
        super(drQ,self).__init__(*args,**kwargs)
        self.setupUi(self)
        self._timer_=core.Timer()
        self.timer_interrupt=0
        self.tab_list=[]
        
        self.setup_main()
        self.PB_refresh.clicked.connect(self.refresh)
        self.CB_auto_refresh.stateChanged.connect(self.autorefresh)
        
        self.connect(self._timer_,QtCore.SIGNAL("done"),self.refresh)
        self.SB_refresh_time.setMinimum(1)
        
    def setup_main(self):
        self.setWindowTitle("DrQueue Manager")
        self.set_main_icons()
        self.setup_about()
        self.setup_jobs()
        self.init_jobs_tabs()
        
    def setup_jobs(self):
        #add a couple of jobs
        self.TW_job.clear()
        job_properties=["id","name","owner","status","process","left","done","priority","pool"]

        self.TW_job.setColumnCount(len(job_properties))
        self.TW_job.setHorizontalHeaderLabels(job_properties) 

        #    set the dialog as a standard window
        self.setWindowFlags(QtCore.Qt.Window |
                            QtCore.Qt.WindowMinimizeButtonHint | 
                            QtCore.Qt.WindowCloseButtonHint | 
                            QtCore.Qt.WindowMaximizeButtonHint)
        
        self.TW_job.verticalHeader().hide()
        self.TW_job.setAlternatingRowColors(True)
        self.TW_job.setSelectionBehavior(QtGui.QTableView.SelectRows)
        self.TW_job.setSelectionMode(QtGui.QTableView.SingleSelection)
        
    def refresh(self):
        self.setCursor(QtCore.Qt.WaitCursor);
        self.init_jobs_tabs()
        self.setCursor(QtCore.Qt.ArrowCursor);
        
    def autorefresh(self,status):
        if status:
            print "autorefresh:ON"
            refresh_time=self.SB_refresh_time.value()
            self._timer_.set_run_time(refresh_time)
            self._timer_.start()
        else:
            print "autorefresh:OFF"
            self._timer_.terminate()

    def init_jobs_tabs(self):
        self.tab_list=[]
        print "building tabs..."
        self.TW_job.clearContents()
        jobs=self._get_all_jobs()
        num_jobs = len(jobs)
        self.TW_job.setRowCount(num_jobs)        

        for i in range(num_jobs):
            job_tab = core.JobDataTab(jobs[i])
            job_tab.add(self.TW_job, i)
            self.tab_list.append(job_tab)
        
    def setup_about(self):
        url=QtCore.QUrl("about.html")
        self.WV_about.load(url)
        
    def set_main_icons(self):
        self.setWindowIcon(QtGui.QIcon("icons/main.svg"))
        self.TW_main.setTabIcon(0,QtGui.QIcon("icons/job.svg"))
        self.TW_main.setTabIcon(1,QtGui.QIcon("icons/nodes.svg"))        
        self.TW_main.setTabIcon(2,QtGui.QIcon("icons/about.svg"))        

    def _get_all_jobs(self):
        job_list = drqueue.request_job_list(drqueue.CLIENT)
        return job_list
    
    def _get_all_slaves(self):
        computer_list = drqueue.request_computer_list (drqueue.CLIENT)
        print "Computers connected to the master:"
        for computer in computer_list:
            print "ID: %3i  Name: %s | Enabled: %s"%(computer.hwinfo.id,computer.hwinfo.name.ljust(20),(lambda x: x and "Yes" or "No")(computer.limits.enabled)) 

def main():
    app = QtGui.QApplication(sys.argv)
    dialog = drQ()    
    dialog.show()
    return app.exec_()

if __name__ == "__main__":
    main()
