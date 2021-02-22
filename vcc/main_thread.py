#!/usr/bin/env python
#############################################
#   Title: Relay Client Main Thread         #
# Project: VTGS Relay Control Daemon        #
# Version: 2.0                              #
#    Date: Dec 15, 2017                     #
#  Author: Zach Leffke, KJ4QLP              #
# Comment:                                  #
#   -Relay Control Client Main Thread       #
#   -Intended for use with systemd          #
#############################################

import threading
import time

from logger import *
#import numato
import service_thread

class Main_Thread(threading.Thread):
    def __init__ (self, cfg):
        threading.Thread.__init__(self, name = 'Main_Thread')
        self._stop      = threading.Event()
        self.cfg        = cfg
        self.startup_ts = cfg['startup_ts']
        self.log_path   = cfg['log_path']
        self.log_level  = cfg['log_level']
        self.cdh_id     = cfg['cdh_id']

        self.state  = 'BOOT' #BOOT
        self.msg_cnt = 0
        #setup logger
        self.main_log_fh = setup_logger(self.cdh_id, level= self.log_level, ts=self.startup_ts, log_path=self.log_path)
        self.logger = logging.getLogger(self.cdh_id) #main logger

    def run(self):
        print "{:s} Started...".format(self.name)
        self.logger.info('Launched {:s}'.format(self.name))
        try:
            while (not self._stop.isSet()):
                if self.state == 'BOOT':
                    self._handle_state_boot()
                elif self.state == 'ANTENNA':
                    self._handle_state_antenna()
                elif self.state == 'SAFE':
                    self._handle_state_safe()
                elif self.state == 'SCIENCE':
                    self._handle_state_science()
                elif self.state == 'FAULT':
                    self._handle_state_fault()
                time.sleep(0.01) #Needed to throttle CPU

        except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
            print "\nCaught CTRL-C, Killing Threads..."
            self.logger.warning('Caught CTRL-C, Terminating Threads...')
            #self.relay_thread.stop()
            #self.relay_thread.join() # wait for the thread to finish what it's doing
            self.service_thread.stop()
            self.service_thread.join() # wait for the thread to finish what it's doing
            self.logger.warning('Terminating {:s}...'.format(self.name))
            sys.exit()
        sys.exit()

    def _handle_state_boot(self):
        #Daemon activating for the first time
        #Activate all threads
        #State Change:  BOOT --> STANDBY
        #All Threads Started
        if self._init_threads():#if all threads activate succesfully
            self.set_state('SAFE', 'Successfully Launched Threads')
        else:
            self.set_state('FAULT', 'Failed to Launch Threads')

    def _handle_state_antenna(self):
        pass

    def _handle_state_safe(self):
        pass

    def _handle_state_science(self):
        pass

    def _handle_state_fault(self):
        pass

    def set_state(self, state, msg=None):
        self.state = state
        if (msg != None): self.logger.info(msg)
        self.logger.info('Changed STATE to: {:s}'.format(self.state))
        if self.state == 'BOOT':
            pass
        if self.state == 'ANTENNA':
            pass
        if self.state == 'SAFE':
            time.sleep(1)
        if self.state == 'SCIENCE':
            pass
        if self.state == 'FAULT':
            pass
            time.sleep(1)

    def _init_threads(self):
        try:
            #Initialize Relay Thread
            #self.logger.info('Setting up Relay_Thread')
            #self.relay_thread = numato.Ethernet_Relay(self.args)
            #self.relay_thread.daemon = True

            #Initialize Server Thread
            self.logger.info('Setting up Service_Thread')
            self.service_thread = service_thread.Service_Thread(self.cfg)
            self.service_thread.daemon = True

            #Launch threads
            #self.logger.info('Launching Relay_Thread')
            #self.relay_thread.start() #non-blocking

            self.logger.info('Launching Service_Thread')
            self.service_thread.start() #non-blocking

            time.sleep(2)
            return True
        except Exception as e:
            self.logger.warning('Error Launching Threads:')
            self.logger.warning(str(e))
            self.logger.warning('Setting STATE --> FAULT')
            self.state = 'FAULT'
            return False

    def stop(self):
        print '{:s} Terminating...'.format(self.name)
        self.logger.info('{:s} Terminating...'.format(self.name))
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()
