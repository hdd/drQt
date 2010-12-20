import sys
import os

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import PyQt4.uic as uic

import drQueueCore as core

properties={
    "id": 0,
    "name":"test",
    "owner":"user",
    "status":1,
    "process":294232,
    "left":"10%",
    "done":0,
    "pri":0,
    "pool":0
    }

ui_path=os.path.join(os.path.dirname(__file__),"ui","drQueueUi.ui")
widget_class, base_class = uic.loadUiType(ui_path)

class drQ(widget_class, base_class):
	def __init__(self,*args,**kwargs):
		super(drQ,self).__init__(*args,**kwargs)
		self.jobs=[]
		self.setup_main()

	@QtCore.pyqtSignature("on_exitButton_clicked()")
	def on_exitButton_clicked(self):
		self.close()
		
	@QtCore.pyqtSignature("on_Refresh_clicked()")
	def on_Refresh_clicked(self):
		pass

	def setup_main(self):
		self.setupUi(self)
	
		self.setWindowTitle("DrQueue Manager")
		self.set_main_icons()
		self.setup_about()
		self.setup_jobs()
		
	def setup_jobs(self):
		#add a couple of jobs
		self.TW_job.clear()

		self.TW_job.setColumnCount(len(properties.keys()))
		self.TW_job.setHorizontalHeaderLabels(properties.keys()) 

		#	set the dialog as a standard window
		self.setWindowFlags(QtCore.Qt.Window |
						    QtCore.Qt.WindowMinimizeButtonHint | 
						    QtCore.Qt.WindowCloseButtonHint | 
						    QtCore.Qt.WindowMaximizeButtonHint)
				
		for i in range(100):
			job = self.add_job()
			job.update(properties)
					
	def add_job(self):
		num_jobs = len(self.jobs)
		self.TW_job.setRowCount(num_jobs+1)
		job_tab = core.JobDataTab("test_%s"%num_jobs)
		job_tab.add(self.TW_job, num_jobs)
		self.jobs.append(job_tab)
		return job_tab
		
	def setup_about(self):
		url=QtCore.QUrl("about.html")
		self.WV_about.load(url)
		
	def set_main_icons(self):
		self.setWindowIcon(QtGui.QIcon("icons/main.svg"))
		self.TW_main.setTabIcon(0,QtGui.QIcon("icons/job.svg"))
		self.TW_main.setTabIcon(1,QtGui.QIcon("icons/nodes.svg"))		
		self.TW_main.setTabIcon(2,QtGui.QIcon("icons/about.svg"))		
		
def main():
	app = QtGui.QApplication(sys.argv)
	dialog = drQ()
	print "dialog",dialog
	
	dialog.show()
	return app.exec_()

if __name__ == "__main__":
	main()
