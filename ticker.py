#!/usr/bin/env python3

'''Used to continuesly pull market data'''

import krakenex #api libary
import time     #for polling the data every few seconds
import datetime #used to convert from unix time
import csv      #csv file read and write


k = krakenex.API()  #instatiate api
#k.load_key('kraken.key')





last = None     #if there is nothing in the csv file start from here


try:
    with open('tradesLog.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        
        print("RESUMING CSV FILE\n")
        
        all_lines = list(reader)        #go through all lines in the reader object and put them in a list
        last_line = all_lines[-1][6]    #get the timestamp from the last line

        last = int(last_line)
        
        
        print('-' * 50 )

        print("Last time in csv file: " + str(last))
        print(datetime.datetime.fromtimestamp(last/10**9).strftime('[%Y-%m-%d]  %A %B %e, %l:%M %p'))
        
        print('-' * 50 + "\n")

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
    

    with open('tradesLog.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        for line in data:
            print(line)
            line.append(last)
            writer.writerow(line)
        
        
        #writer.writerows(data)



    time.sleep(8)










