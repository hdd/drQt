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
        
        try:
            drqueue.request_job_list(drqueue.CLIENT)
        except:
            raise "NO MASTER FOUND"
        
        
        self.setupUi(self)
        self._timer_=core.Timer(parent=self)
        self.timer_interrupt=0
        self.jobs_tab_list=[]
        self.nodes_tab_list=[]
        self.setup_main()
        self.PB_refresh.clicked.connect(self.refresh)
        self.CB_auto_refresh.stateChanged.connect(self.autorefresh)
        
        #    catch the "done" signal from the thread and update the table
        self.connect(self._timer_,QtCore.SIGNAL("done"),self.refresh)
        self.SB_refresh_time.setMinimum(1)
        self.SB_refresh_time.setValue(3)
        #    set the dialog as a standard window
        self.setWindowFlags(QtCore.Qt.Window |
                            QtCore.Qt.WindowMinimizeButtonHint | 
                            QtCore.Qt.WindowCloseButtonHint | 
                            QtCore.Qt.WindowMaximizeButtonHint)        
        
    def setup_main(self):
        self.setWindowTitle("DrQueue Manager")
        self.set_main_icons()
        self.setup_about()
        self.setup_jobs()
        self.init_jobs_tabs()
        
        self.setup_nodes()
        self.init_nodes_tabs()
        
    def setup_nodes(self):
        self.TW_node.clear()
        node_properties=["Id","Enabled","Running","Name","Os","CPUs","Load Avg","Pools"]
        self.TW_node.setColumnCount(len(node_properties))
        self.TW_node.setHorizontalHeaderLabels(node_properties) 
        
        self.TW_node.verticalHeader().hide()
        self.TW_node.setAlternatingRowColors(True)
        self.TW_node.setSelectionBehavior(QtGui.QTableView.SelectRows)
        self.TW_node.setSelectionMode(QtGui.QTableView.SingleSelection) 
                       
    def setup_jobs(self):
        #add a couple of jobs
        self.TW_job.clear()
        job_properties=["Id","Name","Owner","Status","Process","Left","Done","Priority","Pool"]

        self.TW_job.setColumnCount(len(job_properties))
        self.TW_job.setHorizontalHeaderLabels(job_properties) 

        self.TW_job.verticalHeader().hide()
        self.TW_job.setAlternatingRowColors(True)
        self.TW_job.setSelectionBehavior(QtGui.QTableView.SelectRows)
        self.TW_job.setSelectionMode(QtGui.QTableView.SingleSelection)  
        self.TW_job.setContextMenuPolicy(QtCore.Qt.CustomContextMenu) 
        
        self.connect(self.TW_job, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.create_job_context)
        
    def refresh(self):
        self.setCursor(QtCore.Qt.WaitCursor);
        self.init_jobs_tabs()
        self.init_nodes_tabs()
        self.TW_job.repaint()
        self.TW_node.repaint()
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
        self.jobs_tab_list=[]
        print "building job tabs..."
        self.TW_job.clearContents()
        jobs=self._get_all_jobs()
        num_jobs = len(jobs)
        self.TW_job.setRowCount(num_jobs)        

        for i in range(num_jobs):
            job_tab = core.JobDataTab(jobs[i],parent=self.TW_job)
            job_tab.add(self.TW_job, i)
            self.jobs_tab_list.append(job_tab)
        
    def init_nodes_tabs(self):
        self.nodes_tab_list=[]
        print "building nodes tabs..."
        nodes=self._get_all_nodes()
        num_nodes = len(nodes)
        self.TW_node.setRowCount(num_nodes)
        for i in range(num_nodes):
            node_tab = core.NodeDataTab(nodes[i],parent=self.TW_node)
            node_tab.add(self.TW_node, i)
            self.nodes_tab_list.append(node_tab)
                      
    def setup_about(self):
        url=QtCore.QUrl("about.html")
        self.WV_about.load(url)
        
    def set_main_icons(self):
        self.setWindowIcon(QtGui.QIcon("icons/main.svg"))
        self.TW_main.setTabIcon(0,QtGui.QIcon("icons/job.svg"))
        self.TW_main.setTabIcon(1,QtGui.QIcon("icons/nodes.svg"))        
        self.TW_main.setTabIcon(2,QtGui.QIcon("icons/about.svg"))        


    def create_job_context(self,QPoint):
        detailsAct = QtGui.QAction("&Details",self)
        detailsAct.setToolTip("get details on the job")
        #self.connect(detailsAct, QtCore.SIGNAL('triggered()'), self.on_details)

        newAct =QtGui.QAction("&New Job",self)
        newAct.setToolTip("createa new job")
        #self.connect(newAct, QtCore.SIGNAL('triggered()'), self.on_new)
                
        copyAct = QtGui.QAction("&Copy Job",self)
        copyAct.setToolTip("copy the job")
        #self.connect(copyAct, QtCore.SIGNAL('triggered()'), self.on_copy)    
        
        rerunAct = QtGui.QAction("&Re Run",self)
        rerunAct.setToolTip("Re run the job")
        #self.connect(copyAct, QtCore.SIGNAL('triggered()'), self.on_rerun)        

        stopAct = QtGui.QAction("&Stop",self)
        stopAct.setToolTip("stop the running job")
        #self.connect(stopAct, QtCore.SIGNAL('triggered()'), self.on_stop)        
                
        hstopAct = QtGui.QAction("&Hard Stop",self)
        hstopAct.setToolTip("hard stop the running job")
        #self.connect(hstopAct, QtCore.SIGNAL('triggered()'), self.on_hstop)                        

        continueAct = QtGui.QAction("&Continue",self)
        continueAct.setToolTip("Continue the stop job")
        #self.connect(continueAct, QtCore.SIGNAL('triggered()'), self.on_continue)    
        
        deleteAct = QtGui.QAction("D&elete",self)
        deleteAct.setToolTip("delete the job")
        #self.connect(deleteAct, QtCore.SIGNAL('triggered()'), self.on_delete)    
        
        # Create a menu
        menu = QtGui.QMenu("Menu", self) 
        menu.addAction(detailsAct) 
        menu.addSeparator()
        menu.addAction(newAct)
        menu.addAction(copyAct) 
        menu.addSeparator()
        menu.addAction(rerunAct)
        menu.addAction(stopAct) 
        menu.addAction(hstopAct)
        menu.addAction(continueAct) 
        menu.addAction("Delete")
        
        # Show the context menu in the mouse position 
        menu.exec_(QtGui.QCursor.pos()) 
        
    def _get_all_jobs(self):
        job_list = drqueue.request_job_list(drqueue.CLIENT)
        return job_list
    
    def _get_all_nodes(self):
        computer_list = drqueue.request_computer_list (drqueue.CLIENT)
        return computer_list
        
def main():
    app = QtGui.QApplication(sys.argv)
    dialog = drQ()    
    dialog.show()
    return app.exec_()

if __name__ == "__main__":
    main()
