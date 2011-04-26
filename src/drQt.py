#!/usr/bin/env python

import sys
import os

os.environ["DEBUG"]="1"

try:
    # https://github.com/hdd/hlog
    import hlog as log
except:
    import logging as log



import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import PyQt4.QtWebKit as QtWebKit

try:
	import drqueue.base.libdrqueue as drqueue
except:
	raise "libdrqueue not found! please check drqueue python installation"

from lib.slaveTab import SlaveNodeTab
from lib.jobTab import JobTab
from lib.utils import Timer
from lib.utils import icons_path
from drQtNewJob import NewJob

import lib.ui.drQt_UI as drQtUI

class AboutDialog(QtGui.QDialog):
    def __init__(self,parent=None):
        super(AboutDialog,self).__init__(parent)
        layout=QtGui.QVBoxLayout()
        self.setLayout(layout)
        web_view=QtWebKit.QWebView()
        layout.addWidget(web_view)
        url=QtCore.QUrl("lib/ui/about.html")
        web_view.load(url)
        self.setFixedSize(600, 750)
        self.setWindowIcon(QtGui.QIcon(os.path.join(icons_path,"about.svg")))
        self.setWindowTitle("About")


class drQt(drQtUI.Ui_MainWindow,QtGui.QMainWindow):
    node_properties=["Id","Enabled","Running","Name","Os","CPUs","Load Avg","Pools"]
    job_properties=["Id","Name","Owner","Status","Process","Done","Priority","Pool"]
    
    def __init__(self,parent=None):
        super(drQt,self).__init__(parent=parent)
        
        try:
            self._get_all_jobs()
        except:
            raise "NO MASTER FOUND"
        
        self.setupUi(self)
        self._timer_=Timer(parent=self)
        self.timer_interrupt=0
        self.jobs_tab_list=[]
        self.nodes_tab_list=[]
        self._selected_job_row= None
        
        self.setup_main()
        self.PB_refresh.clicked.connect(self.refresh)
        self.CB_auto_refresh.stateChanged.connect(self.set_autorefresh)
        self.connect(self._timer_,QtCore.SIGNAL("time_elapsed"),self.refresh)
        
        self.SB_refresh_time.setMinimum(1)
        self.SB_refresh_time.setValue(2)

        self.setWindowFlags(QtCore.Qt.Window |
                            QtCore.Qt.WindowMinimizeButtonHint | 
                            QtCore.Qt.WindowCloseButtonHint | 
                            QtCore.Qt.WindowMaximizeButtonHint)   
             
        self.LB_header.setPixmap(QtGui.QPixmap(os.path.join(icons_path,"drQHeader.png")))   
        self.connect(self.TW_job,QtCore.SIGNAL("cellClicked(int,int)"),self._store_selected_job)
        self.connect(self.TW_job,QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self._create_context)
        
    def _raise_new_job(self):
        log.debug("start new job")
        newjobD=NewJob(self)
        newjobD.show()    
                    
    def _raise_about(self):
        aboutD= AboutDialog(self)
        aboutD.show()   
        
    def _store_selected_job(self,row,column):
        self._selected_job_row = row
            
    def setup_menu_bar(self):
        menu_bar = self.menuBar()
        job_bar = menu_bar.addMenu("&Job")
        new_job =QtGui.QAction("&New Job",self)
        self.connect(new_job, QtCore.SIGNAL('triggered()'), self._raise_new_job)
        job_bar.addAction(new_job)
        
        help_bar = menu_bar.addMenu("&Help")
        
        About =QtGui.QAction("&About",self)
        self.connect(About, QtCore.SIGNAL('triggered()'), self._raise_about)
        help_bar.addAction(About)

        
    def setup_main(self):
        self.setWindowTitle("DrQueue Manager")
        self.resize(1000,600)
        
        self.setup_menu_bar()
        self.set_main_icons()
        
        self.setup_jobs()
        self.init_jobs_tabs()
        
        self.setup_slaves()
        self.init_slaves_tabs()
        
    def setup_slaves(self):
        self.TW_node.clear()
        
        self.TW_node.setColumnCount(len(self.node_properties))
        self.TW_node.setHorizontalHeaderLabels(self.node_properties) 
        
        self.TW_node.verticalHeader().hide()
        self.TW_node.setAlternatingRowColors(True)
        self.TW_node.setSelectionBehavior(QtGui.QTableView.SelectRows)
        self.TW_node.setSelectionMode(QtGui.QTableView.SingleSelection) 
                               
    def setup_jobs(self):
        self.TW_job.clear()

        self.TW_job.setColumnCount(len(self.job_properties))
        self.TW_job.setHorizontalHeaderLabels(self.job_properties) 

        self.TW_job.verticalHeader().hide()
        self.TW_job.setAlternatingRowColors(True)
        self.TW_job.setSelectionBehavior(QtGui.QTableView.SelectRows)
        self.TW_job.setSelectionMode(QtGui.QTableView.SingleSelection)

    def refresh(self):
        self.setCursor(QtCore.Qt.WaitCursor);
        self.init_jobs_tabs()
        self.init_slaves_tabs()
        
        self.TW_job.repaint()
        self.TW_node.repaint()
        
        if self._selected_job_row != None:
            log.debug("restore row selection %s"%self._selected_job_row)
            self.TW_job.setCurrentCell(self._selected_job_row,0)
        
        self.setCursor(QtCore.Qt.ArrowCursor);
        
    def set_autorefresh(self,status):
        if status:
            log.debug("autorefresh:ON")
            refresh_time=self.SB_refresh_time.value()
            self._timer_.set_run_time(refresh_time)
            self._timer_.start()
        else:
            log.debug("autorefresh:OFF")
            self._timer_.terminate()

    def init_jobs_tabs(self):
        self.jobs_tab_list=[]
        log.debug("building job tabs...")
        self.TW_job.clearContents()
        jobs=self._get_all_jobs()
        num_jobs = len(jobs)
        self.TW_job.setRowCount(num_jobs)        

        for i in range(num_jobs):
            job_tab = JobTab(jobs[i],parent=self.TW_job)
            job_tab.add_to_table(self.TW_job, i)
            self.connect(job_tab, QtCore.SIGNAL('update'), self.refresh)
            self.jobs_tab_list.append(job_tab)
        
    def init_slaves_tabs(self):
        self.nodes_tab_list=[]
        log.debug("building nodes tabs...")
        nodes=self._get_all_slaves()
        num_nodes = len(nodes)
        self.TW_node.setRowCount(num_nodes)
        for i in range(num_nodes):
            log.debug("create slave Node Tab : %s"%type(nodes[i]))
            node_tab = SlaveNodeTab(nodes[i],parent=self.TW_node)
            node_tab.add_to_table(self.TW_node, i)
            self.connect(node_tab, QtCore.SIGNAL('update'), self.refresh)
            self.nodes_tab_list.append(node_tab)
            
    def set_main_icons(self):
        self.setWindowIcon(QtGui.QIcon(os.path.join(icons_path,"main.svg")))
        self.TW_main.setTabIcon(0,QtGui.QIcon(os.path.join(icons_path,"job.svg")))
        self.TW_main.setTabIcon(1,QtGui.QIcon(os.path.join(icons_path,"nodes.svg")))        
        
    def _get_all_jobs(self):
        job_list = drqueue.request_job_list(drqueue.CLIENT)
        return job_list
    
    def _get_all_slaves(self):
        computer_list = drqueue.request_computer_list(drqueue.CLIENT)
        return computer_list
    
    def _create_context(self,QPoint):
        """
        create the context menu
        """
        #print currentItem._tab_id
        newAct =QtGui.QAction("&New Job",self)
        newAct.setToolTip("createa new job")
        self.connect(newAct, QtCore.SIGNAL('triggered()'), self._new_job_show)  
        
        menu = QtGui.QMenu("Menu", self)
        menu.addAction(newAct)
        menu.exec_(QtGui.QCursor.pos())  
             
def main():
    app = QtGui.QApplication(sys.argv)
    dialog = drQt()   
    dialog.show()
    return app.exec_()

if __name__ == "__main__":
    main()
