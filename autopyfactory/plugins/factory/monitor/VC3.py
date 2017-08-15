#!/bin/env python

'''VC3 Montoring plugin
 Copied over wholesale from autopyfactory-tools
 Provides methods for job, queue, and factory monitoring calls 
 Enters information into the configured infoservice. 

Info to publish: By Request, then broken down by factoryname (i.e. hostname?)

# Raw info for each allocation, by factory.
Request.statusraw =
       { "factoryid" :  {  "<allocation>" : { 'unsub' : 0,
                                              'idle' : 10,
                                              'running' : 5,
                                              'removed' : 0,
                                              'completed' : 0,
                                              'held' : 0,
                                              'error': 0
                                         },
                "<allocation2>" : { 'unsub' : 0,
                                              'idle' : 10,
                                              'running' : 5,
                                              'removed' : 0,
                                              'completed' : 0,
                                              'held' : 0,
                                              'error': 0
                             },
                },
         "factoryid2" : {  "<allocation3>" : { 'unsub' : 0,
                                              'idle' : 10,
                                              'running' : 5,
                                              'removed' : 0,
                                              'completed' : 0,
                                              'held' : 0,
                                              'error': 0
                                         },
                "<allocation4>" : {  'unsub' : 0,
                                              'idle' : 10,
                                              'running' : 5,
                                              'removed' : 0,
                                              'completed' : 0,
                                              'held' : 0,
                                              'error': 0
                             },
                },
        }

# Aggregate numbers for this entire request.
# This is what Master lifecycle task would look at to determine overall
# (virtual) cluster state.
Request.status = { 'unsub' : 0,
                   'idle' : 10,
                   'running' : 5,
                   'removed' : 0,
                   'completed' : 0,
                   'held' : 0,
                   'error': 0
                  }








'''

import argparse   
import copy
import subprocess
import time

import htcondor

from vc3client.client import VC3ClientAPI
from vc3infoservice.infoclient import  InfoMissingPairingException, InfoConnectionFailure

from autopyfactory.interfaces import MonitorInterface
from autopyfactory.interfaces import _thread

class _vc3(_thread, MonitorInterface):
    
    def __init__(self, factory, config, section):
        _thread.__init__(self)

        self.log = logging.getLogger("autopyfactory.monitor")
        self.log.debug("VC3 monitor initialized.")

        self.factory = factory
        self.apfqueuesmanager = self.factory.apfqueuesmanager
        self.apfqueues = self.apfqueuesmanager.queues

        self.factory.threadsregistry.add("plugin", self)
        self._thread_loop_interval = 30 # FIXME !!


    def _run(self):
        newinfo = self._update()


    def _update(self):
       
        # info = {  "<queue1>" : { 'unsub' : 0,
        #                          'idle' : 10,
        #                          'running' : 5,
        #                          'removed' : 0,
        #                          'completed' : 0,
        #                          'held' : 0,
        #                          'error': 0},
        #           "<queue2>" : { 'unsub' : 0,
        #                          'idle' : 10,
        #                          'running' : 5,
        #                          'removed' : 0,
        #                          'completed' : 0,
        #                          'held' : 0,
        #                          'error': 0},
        #        }

        self.log.debug('starting')

        info = {}
         
        for apfqueue in self.apfqueues:
            apfqname = apfqueue.apfqname
            self.log.info('calling getInfo() for queue %s' %apfqname)
            qinfo = apfque.batchstatus_plugin.getInfo(apfqname)
            info['apfqname']['running'] = qinfo.running
            info['apfqname']['idle'] = qinfo.pending
                
        self.log.info('returning with info object %s' %info)
        return info


    def registerFactory(self, apfqueue):
        """
        Initial startup hello message from new factory...
        
        """
        self.log.debug("registerFactory( apfqueue = %s) called." % apfqueue)
        return None
    
    
    def sendMessage(self, text):
        """
        Send message to monitor, if it supports this function. 
        """
        self.log.debug("sendMessage( text=%s) called." % text)
    
    
    def updateJobs(self, jobinfolist ):
        """
        Update information about job/jobs. 
        Should support either single job object or list of job objects.  
         
        """
        self.log.debug("updateJobs(jobinfolist=%s) called." % jobinfolist )
        return None
   
    def registerJobs(self, apfqueue, jobinfolist ):
        """
        Update information about job/jobs. 
        Should support either single job object or list of job objects.  
         
        """
        self.log.debug("registerJobs(apfqueue=%s, jobinfolist=%s) called." % ( apfqueue, jobinfolist))
        return None   
    
    def updateLabel(self, label, msg):
        """
        Update label. 
        Should support either single job object or list of job objects.  
         
        """
        self.log.debug("updateLabel(label=%s, msg=%s) called." % (label, msg))
        return None       
        


class VC3(object):
      
    # for now, we deal with it as a true Singleton
    instance = None

    def __new__(cls, *k, **kw):
        if not VC3.instance:
            VC3.instance = _vc3(*k, **kw)
        return VC3.instance
        
