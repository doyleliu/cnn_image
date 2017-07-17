import os 
import logging 
import subprocess 
from threading import Thread 
from Queue import Queue 

num_threads=3 
q=Queue() 

def workprocess(i,queue):
  while True: 
    nums = queue.get()
    log = logging.getLogger("Core.Analysis.Processing") 
    INTERPRETER = "/DB/rhome/dliu/project/nowamagic_venv/bin/python"
    if not os.path.exists(INTERPRETER): 
      log.error("Cannot find INTERPRETER at path \"%s\"." % INTERPRETER) 
    processor = "features_tmp.py"
    pargs = [INTERPRETER, processor,"-database","thumbnails","-index", "features_final.h5","-number",str(nums)] 
    subprocess.Popen(pargs)
    queue.task_done()


for i in range(num_threads): 
  t=Thread(target=workprocess, args=(i,q)) 
  t.setDaemon(True) 
  t.start() 
for i in range(0,2):
  q.put(i)

q.join();print 'Done'
