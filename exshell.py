import os 
import logging 
import subprocess 

log = logging.getLogger("Core.Analysis.Processing") 
  
INTERPRETER = "/usr/bin/python"
  
  
if not os.path.exists(INTERPRETER): 
  log.error("Cannot find INTERPRETER at path \"%s\"." % INTERPRETER) 
    
processor = "features_tmp.py"
  
pargs = [INTERPRETER, processor] 
pargs.extend(["-database thumbnails -index featureCNN.h5 -number 0"]) 
subprocess.Popen(pargs)