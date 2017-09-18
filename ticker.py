#!/usr/bin/env python3

'''Used to continuesly pull market data'''

import krakenex
import json
import pprint
import time
import csv

k = krakenex.API()
#k.load_key('kraken.key')

pp = pprint.PrettyPrinter(indent=4)

#pp.pprint(k.query_private('TradeBalance'))

last = None

try:
    with open('tradesLog.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        
        print("CSV FILE")
        
        #row_count = sum(1 for row in reader)
        all_lines = list(reader)
        last_line = all_lines[-1]

        last = last_line["result"]["last"]
        print("Last: " + last)
        
except:
    print("Error opening tradesLog.csv")
    raise


while 1:

    if last == None:
        
        
        
        print("No last time")
        try:
            r = k.query_public('Trades', {'pair': 'XXBTZUSD'})
        except:
            print("Connecton Error...")
            raise
         
        
    else:
        try:
            r = k.query_public('Trades', {'pair': 'XXBTZUSD', 'since': last})
        except:
            print("Connection Error...")
            raise

    last = r["result"]["last"]

    data = r["result"]["XXBTZUSD"]

    pp.pprint(data)

    with open('tradesLog.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        for line in data:
            writer.writerow(line)


    time.sleep(6)










