#!/usr/bin/env python
#############################################
#   Title: Relay Client Service Thread      #
# Project: VTGS Relay Control Daemon        #
# Version: 2.0                              #
#    Date: Dec 15, 2017                     #
#  Author: Zach Leffke, KJ4QLP              #
# Comment:                                  #
#   -Relay Control Client Service Thread    #
#                                           #
#############################################

import threading
import time
import pika
import logging
import sys

from Queue import Queue

class Service_Thread(threading.Thread):
    def __init__ (self, cfg):
        threading.Thread.__init__(self, name = 'Service_Thread')
        self._stop  = threading.Event()
        self.cfg    = cfg
        self.cdh_id = cfg['cdh_id']
        self.ip     = cfg['ip']
        self.port   = cfg['port']

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.ip, self.port))

        self.rx_q   = Queue() #MEssages received from COSMOS, TC
        self.tx_q   = Queue() #Messages sent to COSMOS, TM

        self.connected = False

        self.logger = logging.getLogger(self.cdh_id)
        print "Initializing {}".format(self.name)
        self.logger.info("Initializing {}".format(self.name))


    def run(self):
        print "{:s} Started...".format(self.name)
        self.logger.info('Launched {:s}'.format(self.name))
        sock.listen(1)
        while 1:
            time.sleep(1)

        self.logger.warning('{:s} Terminated'.format(self.name))
        sys.exit()

    def get_connection_state(self):
        return self.connected

    def stop(self):
        print '{:s} Terminating...'.format(self.name)
        self.logger.info('{:s} Terminating...'.format(self.name))
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()
