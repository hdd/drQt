from pprint import pformat

import drqueue.base.libdrqueue as drqueue

def print_methods(inobject):
    for ink,inv in inobject.__dict__.iteritems():
        if not ink.startswith("_"):
            print ink,inv

jobs= drqueue.request_job_list(drqueue.CLIENT)
for job in jobs:
    id = job.id
    name = job.name
    vars=job.envvars
    print vars.name
    
    
#    print pformat(dir(job.envvars))
#    
#    print job.envvars.nvariables
    
#    vars=drqueue.envvars_dump_info(nvars)

#    var=drqueue.envvars_variable_find(vars,"USER")
#    if var:
#        print var.name , var.value