import sys
from PyQt4.QtGui import *
from PyQt4.uic import loadUiType
from PyQt4.QtCore import *


(form, formbase) = loadUiType('ui/drQueueUi.ui')

class drQ(form,QDialog):
	def __init__(self,*args):
		QDialog.__init__(self,*args)
		self.setup()
		
	@pyqtSignature("on_exitButton_clicked()")
	def on_exitButton_clicked(self):
		self.close()
		
	@pyqtSignature("on_Refresh_clicked()")
	def on_Refresh_clicked(self):
		pass

	def setup(self):
		self.setupUi(self)
		self.setWindowTitle("DrQueue Manager")
		self.setIcons()
		self.setAbout()		
		#	set the dialog as a standard window
		self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint | Qt.WindowMaximizeButtonHint)
	
	def setAbout(self):
		url=QUrl("about.html")
		self.AboutBrw.load(url)
		
	def setIcons(self):
		self.setWindowIcon(QIcon("icons/main.svg"))
		self.tabWidget.setTabIcon(0,QIcon("icons/job.svg"))
		self.tabWidget.setTabIcon(1,QIcon("icons/nodes.svg"))		
		self.tabWidget.setTabIcon(2,QIcon("icons/about.svg"))		
		
def main():
	app = QApplication(sys.argv)
	dialog = drQ()
	dialog.show()
	return app.exec_()

if __name__ == "__main__":
	sys.exit(main())
