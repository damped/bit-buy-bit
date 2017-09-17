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

while 1:

    if last == None:
        print("No last time")
        try:
            r = k.query_public('Trades', {'pair': 'XXBTZUSD'})
        except:
            print("Connecton Error...")
            pass
        
        try:
            with open('tradesLog.csv', 'r') as csvfile:
                reader = csv.reader(csvfile, delimiter=' ', quoatechar='|')
                for row in reader:
                    print(row)
        except:
            print("Error opening tradesLog.csv")

    else:
        try:
            r = k.query_public('Trades', {'pair': 'XXBTZUSD', 'since': last})
        except:
            print("Connection Error...")
            pass

        last = r["result"]["last"]

        data = r["result"]["XXBTZUSD"]

        pp.pprint(data)

        with open('tradesLog.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

            for line in data:
                writer.writerow(line)


        time.sleep(6)










