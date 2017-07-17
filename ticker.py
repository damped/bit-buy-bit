#!/usr/bin/env python3

'''Used to continuesly pull market data'''

import krakenex
import json
import pprint
import time

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
	else:
		try:
			r = k.query_public('Trades', {'pair': 'XXBTZUSD', 'since': 'last'})
		except:
			print("Connection Error...")
			pass

	last = r["result"]["last"]	

	pp.pprint((last, r["result"]["XXBTZUSD"]))

	time.sleep(6)
