#!/usr/bin/env python
# coding=utf-8
#import queue
import threading 
import time 
from common import *

class worker(threading.Thread):
    def __init__(self, func, *args, **kvargs):
        threading.Thread.__init__(self)
        self.threadFunc = func
        self.args = args
        self.kvargs = kvargs
        self.status = threading.Event()
    
    def run(self):
        while True:
            if self.status.isSet():
                #logging.warning("Thread is Stopped.")
                break
            else:
                ret = self.threadFunc(*self.args, **self.kvargs)
                if ret == None:
                    logging.error("Thread run error.")
        #self.res = apply(self.func, self.args)
    
    def stop(self):
        self.status.set()

class threadPool:
    def __init__(self, workers_num, thread_worker):
        self.worker_num = workers_num
        self.workers = [] 
        self.thread_worker = thread_worker
        self.__createThread(worker) 
    
    def __createThread(self, worker):
        for i in range(self.worker_num):
            
            self.workers.append(worker(self.thread_worker.threadFunc, *self.thread_worker.args, **self.thread_worker.kvargs))

    def start(self):
        for i in range(self.worker_num):
            self.workers[i].start()
            #logging.info("start thread %d." % i)
            #print "start thread %d." % (i)
        logging.info("Start thread num:%d" % self.worker_num)
    def join(self):
        for i in range(self.worker_num):
            self.workers[i].join()
    
    def stop(self):
        for i in range(self.worker_num):
            self.workers[i].stop()
def test():
#    print "haffasdfas"
    time.sleep(1)
if __name__ == "__main__":
    test_worker = worker(test)
    thread_pool = threadPool(3, test_worker)
    thread_pool.start()

    time.sleep(1)
    thread_pool.stop()
