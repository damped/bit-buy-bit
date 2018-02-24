#!/usr/bin/python3

from bitex.api.WSS import BitstampWSS
import time
import logging
import json

log = logging.getLogger('bitstamp.api.WSS')
log.setLevel(logging.ERROR)



wss = BitstampWSS(include_only=["live_trades"])
wss.start()
#time.sleep(20)

print("Data" + "=" * 10)
#while not wss.data_q.empty():

while True:

    r = wss.data_q.get()
    if r[0] == "live_trades" and r[1] == "BTCUSD":
        data = json.loads(r[2])
        print(data["price"], data["timestamp"])


wss.stop()
