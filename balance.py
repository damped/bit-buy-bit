#!/usr/bin/env python3

import krakenex


k = krakenex.API()
k.load_key('kraken.key')

balance = k.query_private('Balance')

print(balance)
