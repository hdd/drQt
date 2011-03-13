from pprint import pformat

import drqueue.base.libdrqueue as drqueue


jobs= drqueue.request_job_list(drqueue.CLIENT)
for job in jobs:
    id = job.id
    name = job.name
    nvars=job.envvars.nvariables

    vars=job.envvars.variables
    print pformat(dir(vars))
    
#    
#    drqueue.envvars.dump_info(job.envvars)
#    for i in range(nvars):
#        print vars