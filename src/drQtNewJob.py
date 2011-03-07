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
    
class EntryWidget(QtGui.QWidget):
    def __init__(self,name, value,parent=None):
        super(EntryWidget,self).__init__(parent=parent
                                         )
        self._layout= QtGui.QGridLayout()
        self._layout.setMargin(0)
        self._layout.setSpacing(0)
        self._layout.setColumnMinimumWidth(0,200)
        self._layout.setAlignment(self,QtCore.Qt.AlignTop|QtCore.Qt.AlignHCenter)
        
        self._label = QtGui.QLabel()
        self._label.setText("%s"%name)
        
        self._value = QtGui.QLineEdit()
        self._value.setText("%s"%value)
        
        self._layout.addWidget(self._label,0,0)
        self._layout.addWidget(self._value,0,1)
        
        self.setLayout(self._layout)
        self.connect(self._value,QtCore.SIGNAL("textEdited(QString)"),self._emit_value_updated)
        

    def set_value(self,value):
        self._value.setText("%s"%value)
        self._emit_value_updated(value)
        
    def _emit_value_updated(self,value):
        self.emit(QtCore.SIGNAL("updated(QString)"),value)  
        
    def get_value(self):
        if self._value.text()!="":
            return str(self._value.text())
        return None

    def get_name(self):
        return str(self._label.text())
    
class EngineWidget(QtGui.QWidget):
    def __init__(self,engine_name,parent=None):
        super(EngineWidget,self).__init__(parent=parent)
        self._engine_name=engine_name
        self._layout=QtGui.QVBoxLayout()
        self._layout.setAlignment(self,QtCore.Qt.AlignTop|QtCore.Qt.AlignHCenter)

        self._attribute_widget_list={}
        self._options_widget_list={}
        
        
        self._info_line=QtGui.QTextEdit()
        self._info_line.setMaximumSize(1000, 75)
        self._info_line.setEnabled(True)
        
        self.info_box=QtGui.QGroupBox()
        self.info_box.setTitle("Command Preview")
        layout_info_box = QtGui.QVBoxLayout()
        layout_info_box.addWidget(self._info_line)
        self.info_box.setLayout(layout_info_box)                           
        self.setLayout(self._layout)

    def _emit_updated(self,value):
        self.emit(QtCore.SIGNAL("updated(QString)"),value)

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
    
    def set_info_line(self,value):
        self._info_line.setText(str(value))
    
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
        
        self._attributes_group=QtGui.QGroupBox()
        layout_attribute = QtGui.QVBoxLayout()
        layout_attribute.addWidget(self._attributes_group)
        box_layout.addLayout(layout_attribute)
        box_layout.setAlignment(self,QtCore.Qt.AlignTop|QtCore.Qt.AlignHCenter)
        self._attributes_group.setTitle("Attributes")
        
        self._options_group=QtGui.QGroupBox()
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._options_group)
        layout.setAlignment(self,QtCore.Qt.AlignTop|QtCore.Qt.AlignHCenter)
        box_layout.addLayout(layout)
        self._layout.addWidget(self.info_box)
                
        for k,v in engine_dict.iteritems():
            if isinstance(v,dict):
                '''
                ok we probably found an option
                '''
                self._options_group.setTitle(k.capitalize())
                
                for kl, vl in v.iteritems():
                    widget=EntryWidget("%s"%kl,"%s"%vl)
                    if self._chk_readonly(str(vl)):
                        widget.setEnabled(False)
                    else:
                        widget.set_value("")
                        
                    self.connect(widget,QtCore.SIGNAL("updated(QString)"),self._emit_updated)    
                    layout.addWidget(widget)
                    self._options_widget_list[kl]=widget
            else:
                if k !="description":
                    widget=EntryWidget("%s"%k,"%s"%v)
                    if self._chk_readonly(str(v)):
                        widget.setEnabled(False)
                    else:
                        widget.set_value("")
                                                
                    self.connect(widget,QtCore.SIGNAL("updated(QString)"),self._emit_updated)
                    layout_attribute.addWidget(widget)
                    self._attribute_widget_list[k]=widget
                    


                                
    def get_attributes_widgets(self):
        return self._attribute_widget_list
    
    def get_options_widgets(self):
        return self._options_widget_list
        
    def get_composed_flags(self):
        string_return = []
        for k,v in self._options_widget_list.iteritems():
            if v.get_value():
                string_return.append("-%s %s"%(k,v.get_value()))
            
        string_return = " ".join(string_return)
        return string_return
    
    def get_composed_cmd(self):
        complete_cmd=[]

        pre_cmd_val=self._attribute_widget_list["pre_cmd"].get_value()
        if pre_cmd_val:
            complete_cmd.append(pre_cmd_val)
                
        cmd_val=self._attribute_widget_list["cmd"].get_value()
        if cmd_val:
            cmd_options="%s %s"%(cmd_val,self.get_composed_flags())
            complete_cmd.append(cmd_options)
        
        post_cmd_val=self._attribute_widget_list["post_cmd"].get_value()
        if post_cmd_val:
            complete_cmd.append(post_cmd_val)       
            
        return ";".join(complete_cmd) 


class NewJob(newJob_widget_class, newJob_base_class):
    def __init__(self,parent=None):
        super(NewJob,self).__init__(parent)
        self._widgets={}
        self._current_active_widget=None
        self._options_group=None
        self.setupUi(self)
        self.setWindowTitle("Create New Job")
        self.LB_header.setPixmap(QtGui.QPixmap(os.path.join(icons_path,"drQHeader.png"))) 
        self.LY_information.setAlignment(self,QtCore.Qt.AlignTop|QtCore.Qt.AlignHCenter)
        self.setWindowIcon(QtGui.QIcon(os.path.join(icons_path,"main.svg")))
        self._job_=drqueue.job()
        self._kojs=KojsConfigParser(os.path.join(local_path,"kojs.json"))
        self.fill_job_types()
        
        self.connect(self.CB_job_type, QtCore.SIGNAL("highlighted(QString)"), self.enable_engine)
        self.connect(self.PB_submit, QtCore.SIGNAL("clicked()"), self.process)

    def process(self,*args):
        '''
        return the complete command
        '''
        current_cmd=self._current_active_widget.get_composed_cmd()
        self._current_active_widget.set_info_line(current_cmd)
        
    def draw_engine(self,engine_name):
        engine_dict=self._kojs.get_engine(engine_name)    
        engine_widget= EngineWidget(engine_name)
        engine_widget.init_from_dict(engine_dict)
        engine_widget.hide()
        
        self.connect(engine_widget,QtCore.SIGNAL("updated(QString)"),self.process) 

        self._widgets[engine_name]=engine_widget
        self.LY_information.addWidget(engine_widget)
        
        
    def enable_engine(self,engine_name):
        for k,v in self._widgets.iteritems():
            v.hide()
            
        if not engine_name in self._widgets.keys():
            return 
        
        widget=self._widgets[str(engine_name)]
        widget.show()
        self._current_active_widget=widget
        self.process()
        
    def fill_job_types(self):
        engines=self._kojs.get_engines()
        self.CB_job_type.addItem(" --- select and engine ---")
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

        
    