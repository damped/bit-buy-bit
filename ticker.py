#!/usr/bin/env python3

'''Used to continuesly pull market data'''

import krakenex
import pprint

k = krakenex.API()
k.load_key('kraken.key')

pp = pprint.PrettyPrinter(indent=4)

pp.pprint(k.query_private('TradeBalance'))
