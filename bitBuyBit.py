#!/usr/bin/env python3

import time
import argparse
import datetime
import threading
import queue

#Data Logger and csv loading
import csv
import ast  # literal_eval() to convert strings to correct datatypes

#API
from bitex.api.WSS import BitstampWSS
import logging
import json

import q # debuger


# Defaults
filename = "csv.log"
#fieldnames = ['amount', 'buy_order_id', 'sell_order_id', 'amount_str', 'price_str', 'timestamp', 'price', 'type', 'id']
fieldnames = ['amount', 'buy_order_id', 'sell_order_id', 'timestamp', 'price', 'type', 'id']
longAvgWindow = 60

def main(filename):
    try:

        dataLogger_q = queue.Queue()
        analysis_q = queue.Queue()
        trading_q = queue.Queue()


        # Startup

        
        resume(filename, [analysis_q])  

        # Start Threads
        # ---- API ----


        apiActive = threading.Event()
        apiActive.set()
        t_api = threading.Thread(name='API Thread',
                target=api, args=(apiActive, [dataLogger_q, analysis_q]))

        t_api.start()
        

        # ---- Data Logger (For csv file) ----
        dataLoggerActive = threading.Event()
        dataLoggerActive.set()
        t_dataLogger = threading.Thread(name='Data Logger Thread',
                target=dataLogger, args=(dataLoggerActive, dataLogger_q, filename))

        t_dataLogger.start()


        # ---- Analysis ----
        analysisActive = threading.Event()
        analysisActive.set()
        t_analysis = threading.Thread(name='Analysis Thread',
                target=analysis, args=(analysisActive, analysis_q, trading_q, longAvgWindow))

        t_analysis.start()

        while True:
            time.sleep(1)
        # ---- Trade ----

    except KeyboardInterrupt:
        print("\r" + " " * 10)  # Remove ^C
        print("Keyboard interrupt")
        apiActive.clear()
        dataLoggerActive.clear()
        analysisActive.clear()
        t_api.join(0.1)
        t_dataLogger.join(0.1)
        t_analysis.join(0.1)
        




def resume(filename, outputQueues): 
    try:    # Try to open file
        with open(filename, 'r') as csvfile:
            print("Resumeing from file: " + filename)
            reader = csv.DictReader(csvfile, delimiter=' ', quotechar='|')
            
            all_lines = list(reader)                                # Each line is a dictonary
            lastTime = int(all_lines[-1]["timestamp"])              # Get the -1th (aka last) line
            
            print('-' * 50)
            print("Last time in csv file: " + str(lastTime))
            print(datetime.datetime.fromtimestamp(lastTime).strftime('[%Y-%m-%d] %A %B %e, %l:%M %p'))
            print('-' * 50)

            for line in all_lines:
                line = dict(line)                                   # Convert orderd dict to dict

                line["amount"] = float(line["amount"])              # Convert strings to correct types
                line["buy_order_id"] = int(line["buy_order_id"])
                line["sell_order_id"] = int(line["sell_order_id"])
                line["timestamp"] = int(line["timestamp"])
                line["price"] = float(line["price"])
                line["type"] = int(line["type"])
                line["id"] = int(line["id"])


                for qu in outputQueues:                             # Output to all queues supplied
                    qu.put(line, block = True)                      # Block untill operation is compleat
    
    except FileNotFoundError:   # Make a new file with fieldname header
        print("File " + str(filename) + " does not exist. Creating...")

        with open(filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writeheader()

    except:
        print("Error opening " + filename)
        raise





def api(apiActive, outputQueues):
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
                #print(data["price"], data["timestamp"])
                #dataLogger_q.put(data, block=True)

                del data["amount_str"]  # Remove unnesasary string representations
                del data["price_str"]

                data["timestamp"] = int(data["timestamp"])  # Make timestamp and int

                for q in outputQueues:
                    q.put(data, block=True)

            #wss.data_q.task_done()
            
    wss.stop()





def dataLogger(dataLoggerActive, dataLogger_q, filename):
    while dataLoggerActive.isSet():
        try:
            r = dataLogger_q.get(block=False)
        except queue.Empty:
            time.sleep(0.01)
            pass
        else:

            with open(filename, 'a', newline='') as csvfile:
                
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(r)


            dataLogger_q.task_done()





def analysis(analysisActive, analysis_q, trading_q, longAvgWindow):

    dataset = []    # Holds the currently relevent data for long and shortterm averaging
    fresh = False   # Flag to indicate dat fresh data to process
    oldestTime = 0  # Oldest time in dataset to trigger rescan

    while analysisActive.isSet():


        try:
            r = analysis_q.get(block=False)
        except queue.Empty:
            # When we dont have any new data to process purge dataset and caclulat new average
            if fresh or oldestTime <= int(time.time()) - longAvgWindow:
                    fresh = False

                    for line in dataset:
                        if line["timestamp"] <= int(time.time()) - longAvgWindow:
                            dataset.remove(line)

                    if dataset: # if the list is not empty save the oldest timestamp
                        oldestTime = dataset[0]["timestamp"]
                        print("=" * 10)
                        sumof = 0.0
                        count = 0
                        for line in dataset:
                            print(line["price"])
                            sumof += line["price"]
                            count += 1
                        print("Avg: " + str(sumof/count))
                    


            
            time.sleep(0.01)
            pass
        else:

            if r["timestamp"] >= int(time.time()) - longAvgWindow:     # only add to averinging if its not too old
                dataset.append(r)
                fresh = True



            analysis_q.task_done()





def parseOptions():
    parser = argparse.ArgumentParser(description="Bit Buy Bit - Making you less poor, hopefully.")
    parser.add_argument('-f', '--file', dest='filename', default=filename, 
            help=("File name to log to (default: " + filename + ")"))

    return parser.parse_args()




if __name__ == '__main__':

    args = parseOptions()
    filename = args.filename
    main(filename)


