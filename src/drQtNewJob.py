#!/usr/bin/env python

import os
import sys

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import PyQt4.QtWebKit as QtWebKit

from lib.utils import KojsConfigParser

try:
    import drqueue.base.libdrqueue as drqueue
except:
    raise "libdrqueue not found! please check drqueue python installation"

from lib.utils import newJob_widget_class
from lib.utils import newJob_base_class
from lib.utils import icons_path

local_path=os.path.dirname(__file__)

class EngineWidget(QtGui.QWidget):
    def __init__(self,engine_name,parent=None):
        super(EngineWidget,self).__init__(parent=parent)
        self._engine_name=engine_name
        self._layout=QtGui.QVBoxLayout()
        self._widget_list={}
        self.setLayout(self._layout)

    def _chk_readonly(self,value):
        '''
        check if the entry is editable
        '''
        return not value.startswith("${")
    
    def get_widget(self,widget_name):
        if self._widget_list.has_key(widget_name):
            return self._widget_list[widget_name]
        else:
            print "%s not found in widget list"%widget_name
            return None
    
    def init_from_dict(self,engine_dict):
        render_box = QtGui.QGroupBox()
        render_box.setTitle(self._engine_name)
        box_layout=QtGui.QVBoxLayout()
        
        self._layout.addWidget(render_box)
        
        description=engine_dict["description"]
        dsc_widget = QtGui.QTextEdit()
        dsc_widget.setText(description)
        dsc_widget.setMaximumSize(1000, 50)
        dsc_widget.setEnabled(False)
        box_layout.addWidget(dsc_widget)
        self._layout.addLayout(box_layout)
        
        for k,v in engine_dict.iteritems():
            if isinstance(v,dict):
                '''
                ok we probably found an option
                '''
                self._options_group=QtGui.QGroupBox()
                
                self._options_group.setTitle(k.capitalize())  
                layout = QtGui.QVBoxLayout()
                layout.addWidget(self._options_group)
                box_layout.addLayout(layout)
                
                for kl, vl in v.iteritems():
                    widget=EntryWidget("%s"%kl,"%s"%vl)
                    if self._chk_readonly(str(vl)):
                        widget.setEnabled(False)
                    else:
                        widget.set_value("")
                        
                    layout.addWidget(widget)
                    self._widget_list[kl]=widget
            else:
                if k !="description":
                    widget=EntryWidget("%s"%k,"%s"%v)
                    if self._chk_readonly(str(v)):
                        widget.setEnabled(False)
                    else:
                        widget.set_value("")
                    box_layout.addWidget(widget)
                    self._widget_list[k]=widget
        return 

class EntryWidget(QtGui.QWidget):
    def __init__(self,name, value,parent=None):
        super(EntryWidget,self).__init__(parent=parent)
        self._layout= QtGui.QGridLayout()
        self._layout.setMargin(0)
        self._layout.setSpacing(0)
        self._layout.setColumnMinimumWidth(0,200)
        self._layout.setColumnMinimumWidth(1,100)
        self._label = QtGui.QLabel()
        self._label.setText("%s"%name)
        self._value = QtGui.QLineEdit()
        self._value.setText("%s"%value)
        self._layout.addWidget(self._label,0,0)
        self._layout.addWidget(self._value,0,1)
        self.setLayout(self._layout)
        
    def set_value(self,value):
        self._value.setText("%s"%value)

class NewJob(newJob_widget_class, newJob_base_class):
    def __init__(self,parent=None):
        super(NewJob,self).__init__(parent)
        self._widgets={}
        self._options_group=None
        self.setupUi(self)
        self.setWindowTitle("Create New Job")
        self.LB_header.setPixmap(QtGui.QPixmap(os.path.join(icons_path,"drQHeader.png"))) 
        #self.setFixedSize(600, 500)
        self.setWindowIcon(QtGui.QIcon(os.path.join(icons_path,"main.svg")))
        self._job_=drqueue.job()
        self._kojs=KojsConfigParser(os.path.join(local_path,"kojs.json"))
        self.fill_job_types()
        self.connect(self.CB_job_type, QtCore.SIGNAL("highlighted(QString)"), self.enable_engine)         
        self.enable_engine("Custom")
        
    def draw_engine(self,engine_name):
        engine_dict=self._kojs.get_engine(engine_name)    
        engine_widget= EngineWidget(engine_name)
        engine_widget.init_from_dict(engine_dict)
        engine_widget.hide()
        self._widgets[engine_name]=engine_widget
        
        #print engine_widget
        self.LY_information.addWidget(engine_widget)
        
    def enable_engine(self,engine_name):
        for k,v in self._widgets.iteritems():
            v.hide()
            
        widget=self._widgets[str(engine_name)]
        widget.show()
        
    def fill_job_types(self):
        engines=self._kojs.get_engines()
        for k in engines:
            self.CB_job_type.addItem(k)
            self.draw_engine(k)
        
def main():
    app = QtGui.QApplication(sys.argv)
    dialog=NewJob()  
    dialog.show()
    return app.exec_()

if __name__ == "__main__":
    main()

        
    