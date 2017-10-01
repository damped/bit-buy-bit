#!/usr/bin/env python3

'''Used to continuesly pull market data'''

import krakenex
import json
import pprint
import time
import csv

import q #debugger

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
        q(all_lines[-1])
        last_line = all_lines[-1][2]

        #q(last_line)
        last = int(last_line.replace('.',''))
        
        
        
        q(last)

        

        print("Last time in csv file: " + str(last))
        
except:
    print("Error opening tradesLog.csv")
    #raise

while 1:

    if last == None:
        
        
        
        print("No last time")
        try:
            r = k.query_public('Trades', {'pair': 'XXBTZUSD'})
        except:
            print("Connecton Error 1...")
            raise
         
        
    else:
        try:
            r = k.query_public('Trades', {'pair': 'XXBTZUSD', 'since': last})
        except:
            print("Connection Error 2...")
            raise

    last = r["result"]["last"]

    data = r["result"]["XXBTZUSD"]
    
    
    data[-1:].append(last)
    

    q(data[-1:])
    #q(last) 
    
    #q(type(data[2][2]))

    with open('tradesLog.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        #for line in data:
        #    #q(line)
        #    writer.writerow(line)
        writer.writerows(data)

        #writer.append


    time.sleep(6)










