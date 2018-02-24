#!/usr/bin/python3

from bitex import Bitstamp
import time

b = Bitstamp()

last = None
while True:
    try:
        response = b.ticker('btcusd')
    except:
        print("Ticker Error")

    if last == response.formatted[8]:
        time.sleep(1)
        pass

    else:
        print(response.formatted[0], response.formatted[8])
        time.sleep(3)
        last = response.formatted[8]

