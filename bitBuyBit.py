#!/usr/bin/env python3

import time
import argparse
import datetime
import threading
import queue

#Data Logger
import csv

#API
from bitex.api.WSS import BitstampWSS
import logging
import json


# Defaults
filename = "csv.log"


def main(filename):
    try:
        # Startup
        ####resume(filename)
        # Start Threads
        # > API
        apiActive = threading.Event()
        apiActive.set()
        t_api = threading.Thread(name='API Thread',
                target=api, args=(apiActive,))

        t_api.start()
        

        dataLoggerActive = threading.Event()
        dataLoggerActive.set()
        t_dataLogger = threading.Thread(name='Data Logger Thread',
                target=dataLogger, args=(dataLoggerActive,))

        t_dataLogger.start()

        while True:
            time.sleep(1)
        # > > Data Logger (For csv file)
        # > > Analysis
        # > > > Trade

    except KeyboardInterrupt:
        print("\r" + " " * 10)  # Remove ^C
        print("Keyboard interrupt")
        apiActive.clear()
        t_api.join(0.1)
        dataLoggerActive.clear()
        t_dataLogger.join(0.1)
        
        
        
        #main_thread = threading.currentThread()
        #for t in threading.enumerate():
        #    print(t)
        #    if t is not main_thread:
        #        t.join(timeout=0.2)


def resume(filename):
    print("Resumeing from file: " + filename)
    
    try:
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile,delimiter=' ', quotechar='|')
            
            all_lines = list(reader)
            lastTime = int(all_lines[-1][6])

            print('-' * 50)

            print("Last time in csv file: " + str(lastTime))
            print(datetime.datetime.fromtimestamp(lastTime/10**9).strftime('[%Y-%m-%d] %A %B %e, %l:%M %p'))

            print('-' * 50)

    except:
        #print("Error opening " + filename)
        raise

def api(apiActive):
    log = logging.getLogger('bitstamp.api.WSS')
    log.setLevel(logging.ERROR)

    wss = BitstampWSS(include_only=["live_trades"])
    wss.start()
    while apiActive.isSet():
        try:
            r = wss.data_q.get(block=False)
        except queue.Empty:
            time.sleep(0.01)
            pass

        else:

            if r[0] == "live_trades" and r[1] == "BTCUSD":
                data = json.loads(r[2])
                print(data["price"], data["timestamp"])
            wss.data_q.task_done()
            
    wss.stop()

def dataLogger(dataLoggerActive):
    print("dataLogger")
    time.sleep(10)
    pass


def parseOptions():
    parser = argparse.ArgumentParser(description="Bit Buy Bit - Making you less poor, hopefully.")
    parser.add_argument('-f', '--file', dest='filename', default=filename, 
            help=("File name to log to (default: " + filename + ")"))

    return parser.parse_args()

if __name__ == '__main__':

    args = parseOptions()
    filename = args.filename
    main(filename)


