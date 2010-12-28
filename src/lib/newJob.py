import os
import sys

import drqueue.base.libdrqueue as drqueue

from lib.utils import newJob_widget_class
from lib.utils import newJob_base_class
from lib.utils import icons_path

class NewJob(newJob_widget_class, newJob_base_class):
    def __init__(self,parent=None):
        super(NewJob,self).__init__(parent)
        self.setupUi(self)
        self._job_=drqueue.job()
        
        
    