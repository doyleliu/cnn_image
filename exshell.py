import os 
import logging 
import subprocess 
from threading import Thread 
from Queue import Queue 



def workprocess(nums):
  log = logging.getLogger("Core.Analysis.Processing") 
  INTERPRETER = "/DB/rhome/dliu/project/nowamagic_venv/bin/python"
  if not os.path.exists(INTERPRETER): 
    log.error("Cannot find INTERPRETER at path \"%s\"." % INTERPRETER) 
  processor = "features_tmp.py"
  pargs = [INTERPRETER, processor,"-database","thumbnails","-index", "features_final.h5","-number",str(nums)] 
  p = subprocess.Popen(pargs)
  p.wait()
  return
  
for i in range(199,596):
  workprocess(i)
  print "The %d process"%(i)

print "Done!"
