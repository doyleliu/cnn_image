import os 
import logging 
import subprocess 

log = logging.getLogger("Core.Analysis.Processing") 
  
INTERPRETER = "/DB/rhome/dliu/project/nowamagic_venv/bin/python"
  
  
if not os.path.exists(INTERPRETER): 
  log.error("Cannot find INTERPRETER at path \"%s\"." % INTERPRETER) 
    
processor = "features_tmp.py"

for i in range(0,2):  
	pargs = [INTERPRETER, processor,"-database","thumbnails","-index", "features_final.h5","-number",str(i)] 
	subprocess.Popen(pargs)
